# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-08 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0029_auto_20161008_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
    ]