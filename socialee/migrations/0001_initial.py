# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name="What's the offer?")),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name="What's the request?")),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('username', models.CharField(blank=True, null=True, max_length=50, unique=True)),
                ('firstname', models.CharField(blank=True, max_length=100)),
                ('lastname', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('newsletter', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('inputs', models.ManyToManyField(to='socialee.Input')),
                ('outputs', models.ManyToManyField(to='socialee.Output')),
            ],
        ),
        migrations.CreateModel(
            name='Zettel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('image', models.ImageField(blank=True, upload_to='zettel/%Y-%m/')),
                ('inputs', models.ManyToManyField(to='socialee.Input')),
                ('outputs', models.ManyToManyField(to='socialee.Output')),
                ('profile', models.ForeignKey(to='socialee.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='output',
            name='profile',
            field=models.ForeignKey(to='socialee.Profile'),
        ),
        migrations.AddField(
            model_name='input',
            name='profile',
            field=models.ForeignKey(to='socialee.Profile'),
        ),
    ]
