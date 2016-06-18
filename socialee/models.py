import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from allauth.account.models import EmailAddress


class UserEntry(User):
    class Meta(User.Meta):
        proxy = True
        verbose_name = "manuelle User Erfassung"
        verbose_name_plural = "manuelle User Erfassungen"

    def __str__(self):
        return "User ({})".format(self.username)


class Origin(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Origin: {}'.format(self.title)


def upload_location(instance, filename):
    location = str(instance.user.username)
    return "%s/%s" % (location, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=5, null=True, blank=True)
    newsletter = models.BooleanField(default=False)
    liked_projects = models.ForeignKey('Project',
                                       blank=True,
                                       null=True,
                                       on_delete=models.SET_NULL,
                                       related_name='likes')

    def is_email_verified(self):
        return (self.user.is_authenticated and
                EmailAddress.objects.filter(email=self.user.email,
                                            verified=True).exists())

    origin = models.ForeignKey(Origin, blank=True, null=True)

    def user_first_name(self):
        return self.user.first_name if self.user else None
    user_first_name.short_description = _("First name")

    def user_last_name(self):
        return self.user.last_name if self.user else None
    user_last_name.short_description = _("Last name")

    def user_email(self):
        return self.user.email if self.user else None
    user_email.short_description = _("E-Mail")

    def __str__(self):
        return 'Profile ({})'.format(self.user)


class Zettel(models.Model):
    class Meta:
        verbose_name_plural = _('Zettel')

    profile = models.ForeignKey(Profile)
    image = models.ImageField(upload_to='zettel/%Y-%m/', blank=True)
    number = models.CharField(blank=True, null=True, max_length=50,
                              default="2015_000_0000",
                              verbose_name=_("Number on the zettel"))

    origin = models.ForeignKey(Origin, blank=True, null=True)

    def __str__(self):
        return 'Zettel from {}'.format(self.profile)


class InputOutput(models.Model):
    UNKNOWN = ''
    KNOWLEDGE = 'knowledge'
    SKILL = 'skill'
    PROBLEM = 'problem'
    RESOURCE = 'resource'
    SOLUTION = 'solution'
    TYPES = (
        (UNKNOWN, 'sonstige'),
        (KNOWLEDGE, 'Wissen'),
        (SKILL, 'Fähigkeit'),
        (PROBLEM, 'Problem'),
        (RESOURCE, 'Resource'),
        (SOLUTION, 'Lösung'),
    )

    class Meta:
        abstract = True

    profile = models.ForeignKey(Profile, null=True)
    zettel = models.ForeignKey(Zettel, null=True)
    type = models.CharField(max_length=25,
                            choices=list(TYPES),
                            default=UNKNOWN)

    def itemclass(self):
        return self.__class__()


class Input(InputOutput):
    title = models.CharField(verbose_name="Was ist der Input?",
                             max_length=200)

    def __str__(self):
        return 'Input "{}" from profile {} and zettel {}'.format(
          self.title, self.profile, self.zettel)


class Output(InputOutput):
    title = models.CharField(verbose_name="Was ist der Output?",
                             max_length=200)

    def __str__(self):
        return 'Output "{}" from profile {} and zettel {}'.format(
          self.title, self.profile, self.zettel)


class Project(models.Model):
    title = models.CharField(max_length=60)
    tagline = models.CharField(max_length=140, null= True)
    description = models.TextField(max_length=5000, null=True)
    slug = models.SlugField()
    profiles = models.ManyToManyField(Profile)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    inputs = models.ManyToManyField(Input)
    outputs = models.ManyToManyField(Output)
    liked_users = models.ForeignKey(Profile,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='likes')

    def __str__(self):
        return 'Project "{}"'.format(self.title)

    def itemclass(self):
        return self.__class__()

    def get_absolute_url(self):
        return reverse('project_detailview', kwargs = {"slug": self.slug})


def pre_save_project(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug

pre_save.connect(pre_save_project, sender = Project)

class Invite(models.Model):
    full_name = models.CharField(max_length=120, blank=True, null=True, verbose_name='Name')
    email = models.EmailField()
    message = models.TextField(max_length=1200, blank=True, null=True, verbose_name='Nachricht')
    timestamp = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False, verbose_name='erledigt?')

    class Meta:
        verbose_name = 'Bitte ladet mich ein!'
        verbose_name_plural = 'Bitte ladet mich ein!'


    def was_submitted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=24) <= self.timestamp <= now
    was_submitted_recently.admin_order_field = 'timestamp'
    was_submitted_recently.boolean = True
    was_submitted_recently.short_description = 'Neu?'

    def __str__(self):
        return self.full_name












