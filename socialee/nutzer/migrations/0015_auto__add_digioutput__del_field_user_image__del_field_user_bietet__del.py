# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Digioutput'
        db.create_table(u'nutzer_digioutput', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='output', unique=True, null=True, to=orm['nutzer.User'])),
            ('bietet', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'nutzer', ['Digioutput'])

        # Deleting field 'User.image'
        db.delete_column(u'nutzer_user', 'image')

        # Deleting field 'User.bietet'
        db.delete_column(u'nutzer_user', 'bietet')

        # Deleting field 'User.braucht'
        db.delete_column(u'nutzer_user', 'braucht')


    def backwards(self, orm):
        # Deleting model 'Digioutput'
        db.delete_table(u'nutzer_digioutput')

        # Adding field 'User.image'
        db.add_column(u'nutzer_user', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'User.bietet'
        db.add_column(u'nutzer_user', 'bietet',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'User.braucht'
        db.add_column(u'nutzer_user', 'braucht',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'nutzer.digiinput': {
            'Meta': {'object_name': 'Digiinput'},
            'bietet': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'input'", 'unique': 'True', 'null': 'True', 'to': u"orm['nutzer.User']"})
        },
        u'nutzer.digioutput': {
            'Meta': {'object_name': 'Digioutput'},
            'bietet': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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