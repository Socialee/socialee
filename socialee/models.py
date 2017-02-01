import datetime
import PIL
from PIL import Image
import os.path
import urllib.request
from urllib.parse import urlparse
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
from django.core.files.images import ImageFile

# from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from allauth.account.models import EmailAddress

from embed_video.fields import EmbedVideoField

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase, TagBase


def upload_location(instance, filename):
    slug = str(instance.slug)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%HUhr%M")
    return "%s/%s/%s/%s" % (str("instances"), slug, date, filename)

def upload_location_user_pic(instance, filename):
    slug = str(instance.user.username)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%HUhr%M")
    return "%s/%s/%s/%s" % (str("users"), slug, date, filename)


class LocationTaggedItem(TaggedItemBase):
    content_object = models.ForeignKey('CommonGround')

class CommonGround(models.Model):
    """
    Stores all the common fields for :model:`Profile` and :model:`Project`.
    """
    slug = models.SlugField( db_index=True )
    created_by = models.ForeignKey(User, null=True, related_name='instances')
    tagline = models.CharField(max_length=140, null= True, blank=True, verbose_name="Tagline")
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Kurzbeschreibung')
    conversation = models.OneToOneField('Conversation', blank=True, null=True, related_name='instance')
    tags = TaggableManager( blank=True, verbose_name='Tags' )
    location = TaggableManager(verbose_name='Location', through=LocationTaggedItem, related_name='in_locations', blank=True)
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)

    current = models.BooleanField(default=False)
    #follower = models.ManyToManyField(User, related_name='follows')
    #inst_follower = models.ManyToManyField('CommonGround', related_name='inst_follows')
    #liked_messages = models.ManyToManyField('Message', related_name='message_likes')

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

    def get_absolute_url(self):
        if hasattr(self, 'profile'):
            return self.profile.get_absolute_url()
        elif hasattr(self, 'project'):
            return self.project.get_absolute_url()
        else:
            return self.slug

    def get_profile_or_project(self):
        if hasattr(self, 'profile'):
            return self.profile
        elif hasattr(self, 'project'):
            return self.project
        else:
            return self

    def __str__(self):
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
    by_instance = models.ForeignKey(CommonGround, null=True)
    by_user = models.ForeignKey(User, null=True, blank=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    reply_to = models.ForeignKey('Message', null=True, blank=True, related_name='replys') # message Replys
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
        ordering = ['-date']


class Project(CommonGround):
    title = models.CharField(max_length=60, verbose_name='Titel')
    managers = models.ManyToManyField(User, related_name='managed_projects', blank=True)
    video = EmbedVideoField(blank=True, null=True, verbose_name='Video-URL')
    longdescription = models.TextField(max_length=2500, null=True, blank=True, verbose_name="Worum geht es in diesem Projekt?")
    history = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Wie ist dieses Projekt enstanden?')


    def use_pic(self, idea):
        name = os.path.basename(idea.picture.name)
        if urlparse(settings.MEDIA_URL).scheme != "":
            idea_path = os.path.join(settings.MEDIA_URL, idea.picture.name).replace(" ", "%20")
            result, headers = urllib.request.urlretrieve(idea_path)
            image_file = ImageFile(open(result, 'rb'))
            self.picture.save(name, image_file, save=True)
        else:
            idea_path = os.path.join(settings.MEDIA_ROOT, idea.picture.name)
            image_file = ImageFile(open(idea_path, 'rb'))
            self.picture.save(name, image_file, save=True)
    
    
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
    phone = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=5, null=True, blank=True)
    newsletter = models.BooleanField(default=False)

    def is_email_verified(self):
        return (self.created_by.is_authenticated and
                EmailAddress.objects.filter(email=self.created_by.email,
                                            verified=True).exists())

    def user_first_name(self):
        return self.created_by.first_name if self.created_by else None
    user_first_name.short_description = _("Vorname")

    def user_last_name(self):
        return self.created_by.last_name if self.created_by else None
    user_last_name.short_description = _("Nachname")

    def user_full_name(self):
        return self.created_by.first_name + ' ' + self.created_by.last_name if self.created_by else None
    user_full_name.short_description = _("Name")

    def user_email(self):
        return self.created_by.email if self.created_by else None
    user_email.short_description = _("E-Mail")

    def long_name(self):
        if self.created_by.first_name and self.created_by.last_name:
            return self.created_by.first_name + " " + self.created_by.last_name
        elif self.created_by.first_name or self.created_by.last_name:
            return self.created_by.first_name + self.created_by.last_name
        else:
            return self.created_by.username

    def short_name(self):
        if self.created_by.first_name:
            return self.created_by.first_name
        else:
            return self.created_by.username

    def __str__(self):
        return 'Profil von {}'.format(self.created_by)

    def get_absolute_url(self):
        return reverse('profile_view', kwargs = {"slug": self.slug})


    #saving picture in small size
    #TODO make this a bit nicer
    def save(self, **kwargs):

        super(Profile, self).save(kwargs)

        if not self.picture:
            return            


        image = Image.open(self.picture)
        (width, height) = image.size
    
        #resize to 210x210
        if ( width < height):
            factor =  210.0 / height 
        else:
            factor =  210.0 / width

        size = ( int(width * factor), int(height * factor))
        image = image.resize(size, Image.ANTIALIAS)
        w,h = image.size
        small = h
        if w<h:
            small = w
        image = image.crop((0, 0, small, small))
        image.save(self.picture.path)

def pre_save_profile(sender, instance, *args, **kwargs):
    # right now there is only one profile per user
    instance.slug = instance.created_by.username

pre_save.connect(pre_save_profile, sender = Profile)


# def post_save_message(sender, instance, created, **kwargs):
#     # created
#     if created:
#         recipient = instance.conversation.instance.created_by
#         creator = instance.by_user
#         if instance.by_instance:
#             creator = instance.by_instance

#         notify.send(creator, recipient=recipient, action_object=instance, target=instance.conversation.instance, verb='Neuer Komentar', description=instance.message)

# post_save.connect(post_save_message, sender=Message)


User.current_instance = property(lambda u: u.instances.get(current=True))













