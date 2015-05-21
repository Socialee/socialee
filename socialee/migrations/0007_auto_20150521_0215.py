# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialee', '0006_auto_20150520_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('plz', models.CharField(default='10969', max_length=5, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100, blank=True, null=True)),
                ('date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileErfassung',
            fields=[
            ],
            options={
                'verbose_name': 'Profil-Erfassung',
                'verbose_name_plural': 'Profil-Erfassungen',
                'proxy': True,
            },
            bases=('socialee.profile',),
        ),
        migrations.RemoveField(
            model_name='zettel',
            name='inputs',
        ),
        migrations.RemoveField(
            model_name='zettel',
            name='outputs',
        ),
        migrations.AddField(
            model_name='input',
            name='zettel',
            field=models.ForeignKey(to='socialee.Zettel', null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='zettel',
            field=models.ForeignKey(to='socialee.Zettel', null=True),
        ),
        migrations.AlterField(
            model_name='input',
            name='profile',
            field=models.ForeignKey(to='socialee.Profile', null=True),
        ),
        migrations.AlterField(
            model_name='output',
            name='profile',
            field=models.ForeignKey(to='socialee.Profile', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zettel',
            name='origin',
            field=models.ForeignKey(to='socialee.Origin', blank=True, null=True),
        ),
    ]
