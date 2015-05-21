# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0004_auto_20150511_2225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='nickname',
        ),
        migrations.AddField(
            model_name='profile',
            name='plz',
            field=models.CharField(max_length=5, null=True, default='10969', blank=True),
        ),
        migrations.AlterField(
            model_name='zettel',
            name='number',
            field=models.CharField(max_length=50, null=True, verbose_name='Number on the zettel', blank=True),
        ),
    ]
