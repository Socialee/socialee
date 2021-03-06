# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 07:50
from __future__ import unicode_literals

from django.db import migrations, models

def migrate_authoruser(apps, schema_editor):
    Idea = apps.get_model("ideas", "Idea")
    User = apps.get_model("auth", "User")
    for idea in Idea.objects.all():
        if idea.author and User.objects.filter(email=idea.author).exists():
            user = User.objects.get(email=idea.author)
            idea.authorUser = user
            idea.save()

def migrate_authoruser_back(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0020_auto_20170219_1034'),
    ]

    operations = [
        migrations.RunPython(migrate_authoruser,migrate_authoruser_back),
    ]
