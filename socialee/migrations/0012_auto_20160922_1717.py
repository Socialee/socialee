# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-22 15:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialee', '0011_auto_20160922_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commonground',
            name='profiles',
        ),
        migrations.RemoveField(
            model_name='commonground',
            name='projects',
        ),
        migrations.AddField(
            model_name='commonground',
            name='liked_messages',
            field=models.ManyToManyField(related_name='message_likes', to='socialee.Message'),
        ),
        migrations.AddField(
            model_name='commonground',
            name='liked_profiles',
            field=models.ManyToManyField(related_name='profile_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commonground',
            name='liked_projects',
            field=models.ManyToManyField(related_name='project_likes', to='socialee.Project'),
        ),
    ]
