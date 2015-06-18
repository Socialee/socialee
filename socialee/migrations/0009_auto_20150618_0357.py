# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0008_auto_20150605_2300'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProfileErfassung',
        ),
        migrations.AddField(
            model_name='profile',
            name='origin',
            field=models.ForeignKey(null=True, blank=True, to='socialee.Origin'),
        ),
    ]
