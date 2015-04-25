from django.contrib.auth.models import User
from django.db import models

# TODO: BaseModel: created/updated


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, unique=True)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    # TODO: PhoneField
    phone = models.CharField(max_length=50, blank=True)
    newsletter = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile ({})'.format(self.email)

# class Zettel:
#     image = models.ImageField(upload_to='zettels/images/input/', null=True)
#     inputs = models.ManyToManyField(Input)
#     outputs = models.ManyToManyField(Output)


class InputOutput(models.Model):
    class Meta:
        abstract= True

    profile = models.ForeignKey(Profile)


class Input(InputOutput):
    title = models.CharField(verbose_name="What's the offer?",
                             max_length=200)

    def __str__(self):
        return 'Input "{}" from {}'.format(self.title, self.profile)


class Output(InputOutput):
    title = models.CharField(verbose_name="What's the request?",
                             max_length=200)

    def __str__(self):
        return 'Output "{}" from {}'.format(self.title, self.profile)


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    inputs = models.ManyToManyField(Input)
    outputs = models.ManyToManyField(Output)
    # desc
    # img
    # featured
