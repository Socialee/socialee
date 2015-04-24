# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.digiinput'
        db.alter_column(u'nutzer_user', 'digiinput_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nutzer.Digiinput'], unique=True, null=True))

    def backwards(self, orm):

        # Changing field 'User.digiinput'
        db.alter_column(u'nutzer_user', 'digiinput_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nutzer.Digiinput'], unique=True, null=True))

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
            'digiinput': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['nutzer.Digiinput']", 'unique': 'True', 'null': 'True'}),
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