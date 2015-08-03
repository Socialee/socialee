from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress

import hashlib


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
        return 'Profile ({})'.format(self.user)

# TODO 2 Hier sollte das facebook Profilbild geladen werden, wird verwendet in navbar.html // ist das cool so? 
    # def profile_image_url(self):
    #     fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
     
    #     if len(fb_uid):
    #         return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
     
    #     return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())
# END TODO 2

class InputOutput(models.Model):
    class Meta:
        abstract = True

    profile = models.ForeignKey(Profile, null=True)
    zettel = models.ForeignKey('Zettel', null=True)


class Input(models.Model):
    title = models.CharField(verbose_name="What's the offer?", max_length=5000)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return 'Input "{}"'.format(self.title)


class Output(models.Model):
    title = models.CharField(verbose_name="What's the request?", max_length=5000)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return 'Output "{}" from profile {}'.format(self.title, self.profile)


class Project(models.Model):
    title = models.TextField(max_length=5000)
    inputs = models.ManyToManyField(Input)
    outputs = models.ManyToManyField(Output)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return 'Project "{}" from profile {}'.format(self.title, self.profile)

class Dream(models.Model):
    title = models.TextField(max_length=5000)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return '{}'.format(self.title)


class Wish(models.Model):
    title = models.TextField(max_length=5000)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return 'Wish "{}" from profile {}'.format(self.title, self.profile)


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