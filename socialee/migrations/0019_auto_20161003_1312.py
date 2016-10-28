# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-03 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0018_auto_20160930_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonground',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='commonground',
            name='tagline',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='Kurzbeschreibung oder Motto'),
        ),
        migrations.AlterField(
            model_name='input',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='input',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='benötigen & nehmen'),
        ),
        migrations.AlterField(
            model_name='input',
            name='type',
            field=models.CharField(blank=True, choices=[('...', 'sonstige'), ('knowledge', 'Wissen und Fähigkeit'), ('problem', 'Problem'), ('resource', 'Resource'), ('solution', 'Lösung')], default='...', max_length=25, null=True, verbose_name='Typ'),
        ),
        migrations.AlterField(
            model_name='output',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='output',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='bieten & geben'),
        ),
        migrations.AlterField(
            model_name='output',
            name='type',
            field=models.CharField(blank=True, choices=[('...', 'sonstige'), ('knowledge', 'Wissen und Fähigkeit'), ('problem', 'Problem'), ('resource', 'Resource'), ('solution', 'Lösung')], default='...', max_length=25, null=True, verbose_name='Typ'),
        ),
    ]