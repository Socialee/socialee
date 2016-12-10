# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-10 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0034_auto_20161027_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonground',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Kurzbeschreibung'),
        ),
        migrations.AlterField(
            model_name='commonground',
            name='tagline',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='Tagline'),
        ),
        migrations.AlterField(
            model_name='project',
            name='history',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Wie ist dieses Projekt enstanden?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='longdescription',
            field=models.TextField(blank=True, max_length=2500, null=True, verbose_name='Worum geht es in diesem Projekt?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=60, verbose_name='Titel'),
        ),
    ]
