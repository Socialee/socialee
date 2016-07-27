# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 14:23
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import socialee.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', 'sonstige'), ('knowledge', 'Wissen'), ('skill', 'Fähigkeit'), ('problem', 'Problem'), ('resource', 'Resource'), ('solution', 'Lösung')], default='', max_length=25)),
                ('title', models.CharField(max_length=200, verbose_name='Was ist der Input?')),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Name')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(blank=True, max_length=1200, null=True, verbose_name='Nachricht')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('done', models.BooleanField(default=False, verbose_name='erledigt?')),
            ],
            options={
                'verbose_name': 'Bitte ladet mich ein!',
                'verbose_name_plural': 'Bitte ladet mich ein!',
            },
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', 'sonstige'), ('knowledge', 'Wissen'), ('skill', 'Fähigkeit'), ('problem', 'Problem'), ('resource', 'Resource'), ('solution', 'Lösung')], default='', max_length=25)),
                ('title', models.CharField(max_length=200, verbose_name='Was ist der Output?')),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default='slug')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=socialee.models.upload_location)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('plz', models.CharField(blank=True, max_length=5, null=True)),
                ('newsletter', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('tagline', models.CharField(max_length=140, null=True)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('header_img', models.ImageField(blank=True, null=True, upload_to=socialee.models.upload_location)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', 'sonstige'), ('knowledge', 'Wissen'), ('skill', 'Fähigkeit'), ('problem', 'Problem'), ('resource', 'Resource'), ('solution', 'Lösung')], default='', max_length=25)),
                ('title', models.CharField(max_length=200, verbose_name='Tag-Beschreibung')),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserEntry',
            fields=[
            ],
            options={
                'verbose_name': 'manuelle User Erfassung',
                'abstract': False,
                'verbose_name_plural': 'manuelle User Erfassungen',
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='inputs',
            field=models.ManyToManyField(blank=True, to='socialee.Input'),
        ),
        migrations.AddField(
            model_name='project',
            name='managers',
            field=models.ManyToManyField(blank=True, related_name='Project_Managers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='outputs',
            field=models.ManyToManyField(blank=True, to='socialee.Output'),
        ),
        migrations.AddField(
            model_name='project',
            name='profiles',
            field=models.ManyToManyField(related_name='Socialeebhaber', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_projects',
            field=models.ManyToManyField(related_name='likes', to='socialee.Project'),
        ),
        migrations.AddField(
            model_name='profile',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.Origin'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='output',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.Profile'),
        ),
        migrations.AddField(
            model_name='input',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.Profile'),
        ),
    ]
