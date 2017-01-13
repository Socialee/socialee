# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_object_id', models.CharField(db_index=True, max_length=255)),
                ('verb', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('target_object_id', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('action_object_object_id', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('public', models.BooleanField(db_index=True, default=True)),
                ('data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('action_object_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_object', to='contenttypes.ContentType')),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='contenttypes.ContentType')),
                ('target_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_object_id', models.CharField(db_index=True, max_length=255)),
                ('object_id', models.CharField(db_index=True, max_length=255)),
                ('actor_only', models.BooleanField(default=True, verbose_name='Only follow actions where the object is the target.')),
                ('started', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('user_content_type', 'user_object_id', 'content_type', 'object_id')]),
        ),
    ]
