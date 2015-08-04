# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0014_auto_20150803_0102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='profiles',
        ),
        migrations.RemoveField(
            model_name='output',
            name='profiles',
        ),
        migrations.AddField(
            model_name='input',
            name='profile',
            field=models.ForeignKey(to='socialee.Profile', null=True),
        ),
        migrations.AddField(
            model_name='input',
            name='zettel',
            field=models.ForeignKey(to='socialee.Zettel', null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='profile',
            field=models.ForeignKey(to='socialee.Profile', null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='zettel',
            field=models.ForeignKey(to='socialee.Zettel', null=True),
        ),
        migrations.AlterField(
            model_name='input',
            name='title',
            field=models.CharField(verbose_name="What's the offer?", max_length=200),
        ),
        migrations.AlterField(
            model_name='output',
            name='title',
            field=models.CharField(verbose_name="What's the request?", max_length=200),
        ),
    ]
