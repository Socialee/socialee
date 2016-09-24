# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-24 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers

def generate_id(apps, schema_editor):
    CommonGround = apps.get_model('socialee', 'CommonGround')
    i=0
    for common in CommonGround.objects.all().iterator():
        common.id = i
        i+=1

        common.save()


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0014_auto_20160922_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonground',
            name='id',
            field=models.AutoField(auto_created=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.RunPython(
            generate_id,
        ),
        migrations.AlterField(
            model_name='commonground',
            name='slug',
            field=models.SlugField(),
        ),
	migrations.AlterField(
            model_name='commonground',
            name='id',
            field=models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commonground',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
