# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-24 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0015_auto_20160924_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericslugtaggeditem',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='genericslugtaggeditem',
            name='tag',
        ),
        migrations.DeleteModel(
            name='GenericSlugTaggedItem',
        ),
    ]