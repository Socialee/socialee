# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-25 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0008_auto_20160825_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='output',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='project',
            name='inputs',
        ),
        migrations.RemoveField(
            model_name='project',
            name='outputs',
        ),
        migrations.AddField(
            model_name='commonground',
            name='inputs',
            field=models.ManyToManyField(blank=True, to='socialee.Input'),
        ),
        migrations.AddField(
            model_name='commonground',
            name='outputs',
            field=models.ManyToManyField(blank=True, to='socialee.Output'),
        ),
        migrations.AddField(
            model_name='input',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.CommonGround'),
        ),
        migrations.AddField(
            model_name='output',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.CommonGround'),
        ),
    ]
