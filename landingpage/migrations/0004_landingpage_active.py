# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-19 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landingpage', '0003_auto_20160919_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpage',
            name='active',
            field=models.BooleanField(default=False, verbose_name='veröffentlicht?'),
        ),
    ]
