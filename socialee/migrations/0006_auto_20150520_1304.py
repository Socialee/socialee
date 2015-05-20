# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0005_auto_20150520_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zettel',
            name='number',
            field=models.CharField(default='2015_000_0000', null=True, verbose_name='Number on the zettel', max_length=50, blank=True),
        ),
    ]
