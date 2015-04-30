# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0002_auto_20150429_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='zettel',
            name='nrdclass',
            field=models.CharField(max_length=3, blank=True),
        ),
    ]
