# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-04 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0020_auto_20161003_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
    ]
