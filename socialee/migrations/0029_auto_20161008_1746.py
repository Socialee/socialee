# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-08 15:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0028_auto_20161008_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonground',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instances', to=settings.AUTH_USER_MODEL),
        ),
    ]
