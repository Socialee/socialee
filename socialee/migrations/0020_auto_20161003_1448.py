# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-03 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0019_auto_20161003_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='type',
            field=models.CharField(blank=True, choices=[('...', 'sonstige'), ('knowledge', 'Wissen und Fähigkeit'), ('problem', 'Problem'), ('resource', 'Ressource')], default='...', max_length=25, null=True, verbose_name='Typ'),
        ),
        migrations.AlterField(
            model_name='output',
            name='type',
            field=models.CharField(blank=True, choices=[('...', 'sonstige'), ('knowledge', 'Wissen und Fähigkeit'), ('problem', 'Problem'), ('resource', 'Ressource')], default='...', max_length=25, null=True, verbose_name='Typ'),
        ),
    ]