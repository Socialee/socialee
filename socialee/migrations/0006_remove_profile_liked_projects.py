# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-24 16:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0005_auto_20160824_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='liked_projects',
        ),
    ]
