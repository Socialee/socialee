from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

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


class Profile(models.Model):
    user = models.OneToOneField(UserEntry, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    # TODO: dh> "PhoneField" (Validierung etc)
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
    profiles = models.ManyToManyField(Profile)
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