# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-19 13:54
from __future__ import unicode_literals

from django.db import migrations, models
import landingpage.models


class Migration(migrations.Migration):

    dependencies = [
        ('landingpage', '0002_auto_20160919_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='symbol',
            field=models.FileField(upload_to=landingpage.models.upload_location),
        ),
    ]
