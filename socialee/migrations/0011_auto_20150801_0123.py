# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0010_remove_profile_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.TextField(verbose_name='Was ist Dein Traum?', max_length=5000)),
                ('profiles', models.ManyToManyField(to='socialee.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.TextField(max_length=5000)),
                ('profiles', models.ManyToManyField(to='socialee.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='profiles',
            field=models.ManyToManyField(to='socialee.Profile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.TextField(unique=True, max_length=100),
        ),
    ]
