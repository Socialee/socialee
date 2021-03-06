# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-06 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import socialee.models


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0023_auto_20161005_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='project',
            name='header_img',
        ),
        migrations.AddField(
            model_name='commonground',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=socialee.models.upload_location),
        ),
        migrations.AlterField(
            model_name='message',
            name='by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.CommonGround'),
        ),
    ]
