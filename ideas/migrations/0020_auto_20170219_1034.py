# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0019_idea_authoruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='subm_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Datum'),
        ),
    ]
