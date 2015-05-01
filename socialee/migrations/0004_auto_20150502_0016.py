# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0003_zettel_nrdclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zettel',
            name='nrdclass',
        ),
        migrations.AddField(
            model_name='zettel',
            name='number',
            field=models.IntegerField(verbose_name='Number on the zettel', blank=True, null=True),
        ),
    ]
