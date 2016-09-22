# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-22 14:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialee', '0009_auto_20160825_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, max_length=5000, null=True)),
                ('by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='socialee.Conversation')),
                ('reply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replys', to='socialee.Message')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='tagline',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='commonground',
            name='conversation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='socialee.Conversation'),
        ),
    ]
