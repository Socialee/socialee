import datetime
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
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

class GenericSlugTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.SlugField(verbose_name=_('Object id'), db_index=True)

class CommonGround(models.Model):
    """
    Stores all the common fields for :model:`Profile` and :model:`Project`.
    """
    slug = models.SlugField(primary_key=True)
    inputs = models.ManyToManyField('Input', blank=True)
    outputs = models.ManyToManyField('Output', blank=True)
    tagline = models.CharField(max_length=140, null= True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    conversation = models.OneToOneField('Conversation', blank=True, null=True)
    liked_profiles = models.ManyToManyField(User, related_name='profile_likes') # follower/beobachter
    liked_projects = models.ManyToManyField('Project', related_name='project_likes')
    liked_messages = models.ManyToManyField('Message', related_name='message_likes')
    tags = TaggableManager(through=GenericSlugTaggedItem)


def upload_location(instance, filename):
    location = str(instance.user.username)
    return "%s/%s" % (location, filename)

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

    owner = models.ForeignKey(CommonGround, null=True)
    type = models.CharField(max_length=25,
                            choices=list(TYPES),
                            default=UNKNOWN)

    def itemclass(self):
        return self.__class__()


class Input(InputOutput):
    title = models.CharField(verbose_name="Was ist der Input?",
                             max_length=200)
    description = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return 'Input "{}" from profile {}'.format(
          self.title, self.profile)


class Output(InputOutput):
    title = models.CharField(verbose_name="Was ist der Output?",
                             max_length=200)
    description = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return 'Output "{}" from profile {}'.format(
          self.title, self.profile)

class Conversation(models.Model):
    slug = models.SlugField(primary_key=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages') # message Replys
    by_user = models.ForeignKey(User, null=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    reply_to = models.ForeignKey('Message', related_name='replys') # message Replys


class Project(CommonGround):
    title = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, null=True)
    header_img = models.ImageField(upload_to=upload_location, null=True, blank=True)    
    
    
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


class Profile(CommonGround):
    user = models.OneToOneField(User, blank=True, null=True)
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=5, null=True, blank=True)
    newsletter = models.BooleanField(default=False)

    def is_email_verified(self):
        return (self.user.is_authenticated and
                EmailAddress.objects.filter(email=self.user.email,
                                            verified=True).exists())

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













