# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


def forwards_func(apps, schema_editor):
    """
    Migrate Profile to User(Erfassung).
    """
    Profile = apps.get_model("socialee", "Profile")
    User = apps.get_model("socialee", "UserEntry")
    db_alias = schema_editor.connection.alias
    for Profile in Profile.objects.using(db_alias).all():
        User.objects.create(username=Profile.email,
                            email=Profile.email,
                            first_name=Profile.firstname,
                            last_name=Profile.lastname)


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
        ),

        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='lastname',
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, to='socialee.UserEntry'),
        ),
    ]
