# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-11 12:24
from __future__ import unicode_literals

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0036_auto_20161211_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
