# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0013_auto_20150803_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='title',
            field=models.CharField(verbose_name="What's the offer?", max_length=5000),
        ),
        migrations.AlterField(
            model_name='output',
            name='title',
            field=models.CharField(verbose_name="What's the request?", max_length=5000),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.TextField(max_length=5000),
        ),
    ]
