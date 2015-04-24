# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field digiinput on 'User'
        db.delete_table(db.shorten_name(u'nutzer_user_digiinput'))

        # Removing M2M table for field user on 'Digiinput'
        db.delete_table(db.shorten_name(u'nutzer_digiinput_user'))


    def backwards(self, orm):
        # Adding M2M table for field digiinput on 'User'
        m2m_table_name = db.shorten_name(u'nutzer_user_digiinput')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'nutzer.user'], null=False)),
            ('digiinput', models.ForeignKey(orm[u'nutzer.digiinput'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'digiinput_id'])

        # Adding M2M table for field user on 'Digiinput'
        m2m_table_name = db.shorten_name(u'nutzer_digiinput_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digiinput', models.ForeignKey(orm[u'nutzer.digiinput'], null=False)),
            ('user', models.ForeignKey(orm[u'nutzer.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['digiinput_id', 'user_id'])


    models = {
        u'nutzer.digiinput': {
            'Meta': {'object_name': 'Digiinput'},
            'bietet': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'nutzer.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "'nickname'", 'max_length': '120'})
        }
    }

    complete_apps = ['nutzer']