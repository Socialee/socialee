# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-25 12:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ideas', '0003_idea_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='hands',
            field=models.ManyToManyField(related_name='gives_hand_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='money',
            field=models.ManyToManyField(related_name='gives_money_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
