# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-08 15:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialee', '0026_auto_20161008_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonground',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
