from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# TODO: BaseModel: created/updated
# TODO: mj>  user-Passwort / Postleitzahl / Geburtsdatum /

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    # TODO: dh> "PhoneField" (Validierung etc)
    phone = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=5, null=True, blank=True, default='10969')
    # mj> geburtsdatum = models.DateField(auto_now=False, auto_now_add=False,
    #                                     blank=True, null=True)
    newsletter = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile ({})'.format(self.email)


class ProfileErfassung(Profile):
    class Meta:
        proxy = True
        verbose_name = "Profil-Erfassung"
        verbose_name_plural = "Profil-Erfassungen"


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


class Origin(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Origin: {}'.format(self.title)


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
