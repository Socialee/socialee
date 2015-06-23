# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


def forwards_func(apps, schema_editor):
    """
    Migrate Profile to User(Entry).
    """
    Profile = apps.get_model("socialee", "Profile")
    User = apps.get_model("socialee", "UserEntry")
    db_alias = schema_editor.connection.alias
    for Profile in Profile.objects.using(db_alias).all():
        # Use part before "@", if username is longer than 30 (maxlength of
        # Django's User.username; https://code.djangoproject.com/ticket/20846).
        username = Profile.email
        if len(username) > 30:
            username = username.split("@", 1)[0]
        user = User.objects.create(username=username,
                                   email=Profile.email,
                                   first_name=Profile.firstname,
                                   last_name=Profile.lastname)
        Profile.user = user
        Profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('socialee', '0007_auto_20150521_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEntry',
            fields=[
            ],
            options={
                'verbose_name': 'User-Erfassung',
                'verbose_name_plural': 'User-Erfassungen',
                'proxy': True,
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),

        migrations.RunPython(
            forwards_func,
            reverse_code=migrations.RunPython.noop
        ),
    ]
