# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0015_auto_20150803_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='input',
            name='zettel',
        ),
        migrations.RemoveField(
            model_name='output',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='output',
            name='zettel',
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
            model_name='input',
            name='profiles',
            field=models.ManyToManyField(to='socialee.Profile'),
        ),
        migrations.AddField(
            model_name='output',
            name='profiles',
            field=models.ManyToManyField(to='socialee.Profile'),
        ),
        migrations.AlterField(
            model_name='input',
            name='title',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='output',
            name='title',
            field=models.TextField(max_length=5000),
        ),
    ]
