from datetime import datetime
import PIL
from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from allauth.account.signals import email_confirmed
from django.dispatch import receiver

# from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from allauth.account.models import EmailAddress

from taggit.managers import TaggableManager


def upload_location(instance, filename):
    location = str(instance.id)
    return "%s/%s" % (location, filename)

class CommonGround(models.Model):
    """
    Stores all the common fields for :model:`Profile` and :model:`Project`.
    """
    slug = models.SlugField( db_index=True )
    tagline = models.CharField(max_length=140, null= True, blank=True, verbose_name="Kurzbeschreibung oder Motto")
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Beschreibung")
    conversation = models.OneToOneField('Conversation', blank=True, null=True)
    liked_profiles = models.ManyToManyField(User, related_name='profile_likes') # follower/beobachter
    liked_projects = models.ManyToManyField('Project', related_name='project_likes')
    liked_messages = models.ManyToManyField('Message', related_name='message_likes')
    tags = TaggableManager( blank=True )
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)

    def long_name(self):
        if hasattr(self, 'profile'):
            return self.profile.long_name()
        elif hasattr(self, 'project'):
            return self.project.long_name()
        else:
            return self.slug

    def short_name(self):
        if hasattr(self, 'profile'):
            return self.profile.short_name()
        elif hasattr(self, 'project'):
            return self.project.short_name()
        else:
            return self.slug

class InputOutput(models.Model):
    UNKNOWN = '...'
    SKILL = 'knowledge'
    PROBLEM = 'problem'
    RESOURCE = 'resource'
    TYPES = (
        (UNKNOWN, 'sonstige'),
        (SKILL, 'Wissen und Fähigkeit'),
        (PROBLEM, 'Problem'),
        (RESOURCE, 'Ressource'),
    )

    class Meta:
        abstract = True

    owner = models.ForeignKey(CommonGround, null=True, related_name="%(app_label)s_%(class)s")
    type = models.CharField(max_length=25,
                            choices=list(TYPES),
                            default=UNKNOWN, 
                            blank=True, null=True,
                            verbose_name="Typ")

    def itemclass(self):
        return self.__class__()


class Input(InputOutput):
    title = models.CharField(verbose_name="benötigen & nehmen",
                             max_length=200, blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Beschreibung")

    def __str__(self):
        return self.title


class Output(InputOutput):
    title = models.CharField(verbose_name="bieten & geben",
                             max_length=200, blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Beschreibung")

    def __str__(self):
        return self.title

class Conversation(models.Model):
    slug = models.SlugField(null=True, blank=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', null=True, blank=True) # message Replys
    by_user = models.ForeignKey(CommonGround, null=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    reply_to = models.ForeignKey('Message', null=True, blank=True, related_name='replys') # message Replys
    date = models.DateTimeField(auto_now=False, auto_now_add=True)


class Project(CommonGround):
    title = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, null=True)
    managers = models.ManyToManyField(User, related_name='Project_Managers', blank=True)
    video = models.FileField(upload_to=upload_location, null=True, blank=True) 
    longdescription = models.TextField(max_length=2500, null=True, blank=True)
    history = models.TextField(max_length=1000, null=True, blank=True)
    
    
    def __str__(self):
        return 'Project "{}"'.format(self.title)

    def itemclass(self):
        return self.__class__()

    def get_absolute_url(self):
        return reverse('project_view', kwargs = {"slug": self.slug})

    def long_name(self):
       return self.title

    def short_name(self):
       return self.title


def pre_save_project(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug

pre_save.connect(pre_save_project, sender = Project)


class Profile(CommonGround):
    user = models.OneToOneField(User, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=5, null=True, blank=True)
    newsletter = models.BooleanField(default=False)

    def is_email_verified(self):
        return (self.user.is_authenticated and
                EmailAddress.objects.filter(email=self.user.email,
                                            verified=True).exists())

    def user_first_name(self):
        return self.user.first_name if self.user else None
    user_first_name.short_description = _("Vorname")

    def user_last_name(self):
        return self.user.last_name if self.user else None
    user_last_name.short_description = _("Nachname")

    def user_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name if self.user else None
    user_full_name.short_description = _("Name")

    def user_email(self):
        return self.user.email if self.user else None
    user_email.short_description = _("E-Mail")

    def long_name(self):
        if self.user.first_name and self.user.last_name:
            return self.user.first_name + " " + self.user.last_name
        elif self.user.first_name or self.user.last_name:
            return self.user.first_name + self.user.last_name
        else:
            return self.user.username

    def short_name(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username

    def __str__(self):
        return 'Profil von {}'.format(self.user)


    #saving picture in small size
    #TODO make this a bit nicer
    def save(self, **kwargs):

        super(Profile, self).save(kwargs)

        if not self.picture:
            return            


        image = Image.open(self.picture)
        (width, height) = image.size
    
        if ( width < height):
            factor =  200 / height 
        else:
            factor =  200 / width

        size = ( int(width * factor), int(height * factor))
        image = image.resize(size, Image.ANTIALIAS)
        w,h = image.size
        small = h
        if w<h:
            small = w
        image = image.crop((0, 0, small, small))
        image.save(self.picture.path)



User.profile = property(lambda u: Profile.objects.get_or_create(user=u, slug=u.username)[0])













