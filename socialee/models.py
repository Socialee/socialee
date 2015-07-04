from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from allauth.socialaccount.models import SocialAccount
import hashlib

# TODO: BaseModel: created/updated
# TODO: mj>  user-Passwort / Postleitzahl / Geburtsdatum /

class UserEntry(User):
    class Meta(User.Meta):
        proxy = True
        verbose_name = "User-Erfassung"
        verbose_name_plural = "User-Erfassungen"

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
    plz = models.CharField(max_length=5, null=True, blank=True, default='10969')
    # mj> geburtsdatum = models.DateField(auto_now=False, auto_now_add=False,
    #                                     blank=True, null=True)
    newsletter = models.BooleanField(default=False)

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


class InputOutput(models.Model):
    class Meta:
        abstract = True

    profile = models.ForeignKey(Profile, null=True)
    zettel = models.ForeignKey('Zettel', null=True)


class Input(InputOutput):
    title = models.CharField(verbose_name="What's the offer?",
                             max_length=200)

    def __str__(self):
        return 'Input "{}" from profile {} and zettel {}'.format(self.title,
                                                                 self.profile,
                                                                 self.zettel)


class Output(InputOutput):
    title = models.CharField(verbose_name="What's the request?",
                             max_length=200)

    def __str__(self):
        return 'Output "{}" from profile {} and zettel {}'.format(self.title,
                                                                  self.profile,
                                                                  self.zettel)


class Location(models.Model):
    plz = models.CharField(max_length=5, null=True, blank=True, default='10969')


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


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    inputs = models.ManyToManyField(Input)
    outputs = models.ManyToManyField(Output)
    # desc
    # img
    # featured


def profile_image_url(self):
    fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
 
    if len(fb_uid):
        return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
 
    return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())
