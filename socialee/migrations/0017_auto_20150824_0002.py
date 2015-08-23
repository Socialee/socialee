# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0016_auto_20150803_2131'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
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
            field=models.ForeignKey(null=True, to='socialee.Profile'),
        ),
        migrations.AddField(
            model_name='input',
            name='zettel',
            field=models.ForeignKey(null=True, to='socialee.Zettel'),
        ),
        migrations.AddField(
            model_name='output',
            name='profile',
            field=models.ForeignKey(null=True, to='socialee.Profile'),
        ),
        migrations.AddField(
            model_name='output',
            name='zettel',
            field=models.ForeignKey(null=True, to='socialee.Zettel'),
        ),
        migrations.AddField(
            model_name='project',
            name='inputs',
            field=models.ManyToManyField(to='socialee.Input'),
        ),
        migrations.AddField(
            model_name='project',
            name='outputs',
            field=models.ManyToManyField(to='socialee.Output'),
        ),
        migrations.AlterField(
            model_name='input',
            name='title',
            field=models.CharField(max_length=200, verbose_name="What's the offer?"),
        ),
        migrations.AlterField(
            model_name='output',
            name='title',
            field=models.CharField(max_length=200, verbose_name="What's the request?"),
        ),
    ]
