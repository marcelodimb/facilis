# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Procedimento'
        db.create_table(u'sap_procedimento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interessado', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, unique=True, null=True, blank=True)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('observacoes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('criado_em', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modificado_em', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sap', ['Procedimento'])


    def backwards(self, orm):
        # Deleting model 'Procedimento'
        db.delete_table(u'sap_procedimento')


    models = {
        u'sap.procedimento': {
            'Meta': {'object_name': 'Procedimento'},
            'criado_em': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interessado': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'modificado_em': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'observacoes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sap']