# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Quote'
        db.create_table(u'qdbapp_quote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'qdbapp', ['Quote'])


    def backwards(self, orm):
        # Deleting model 'Quote'
        db.delete_table(u'qdbapp_quote')


    models = {
        u'qdbapp.quote': {
            'Meta': {'object_name': 'Quote'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['qdbapp']