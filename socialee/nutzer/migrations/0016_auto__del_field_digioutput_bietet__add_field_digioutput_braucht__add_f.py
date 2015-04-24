# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Digioutput.bietet'
        db.delete_column(u'nutzer_digioutput', 'bietet')

        # Adding field 'Digioutput.braucht'
        db.add_column(u'nutzer_digioutput', 'braucht',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Digioutput.image'
        db.add_column(u'nutzer_digioutput', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Digiinput.image'
        db.add_column(u'nutzer_digiinput', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Digioutput.bietet'
        db.add_column(u'nutzer_digioutput', 'bietet',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Digioutput.braucht'
        db.delete_column(u'nutzer_digioutput', 'braucht')

        # Deleting field 'Digioutput.image'
        db.delete_column(u'nutzer_digioutput', 'image')

        # Deleting field 'Digiinput.image'
        db.delete_column(u'nutzer_digiinput', 'image')


    models = {
        u'nutzer.digiinput': {
            'Meta': {'object_name': 'Digiinput'},
            'bietet': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'input'", 'unique': 'True', 'null': 'True', 'to': u"orm['nutzer.User']"})
        },
        u'nutzer.digioutput': {
            'Meta': {'object_name': 'Digioutput'},
            'braucht': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'output'", 'unique': 'True', 'null': 'True', 'to': u"orm['nutzer.User']"})
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