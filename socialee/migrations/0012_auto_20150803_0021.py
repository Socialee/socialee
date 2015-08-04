# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0011_auto_20150801_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='title',
            field=models.TextField(max_length=5000),
        ),
    ]
