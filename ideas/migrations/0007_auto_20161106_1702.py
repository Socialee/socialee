# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-06 16:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0006_remove_idea_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='hands',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='money',
        ),
    ]