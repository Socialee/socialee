# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-12 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0044_auto_20170105_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonground',
            name='conversation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instance', to='socialee.Conversation'),
        ),
    ]
