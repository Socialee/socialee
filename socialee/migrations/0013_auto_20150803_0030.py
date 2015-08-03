# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0012_auto_20150803_0021'),
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
    ]
