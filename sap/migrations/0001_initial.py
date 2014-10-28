# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Assunto'
        db.create_table(u'sap_assunto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'sap', ['Assunto'])

        # Adding model 'Inspetoria'
        db.create_table(u'sap_inspetoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'sap', ['Inspetoria'])

        # Adding model 'Situacao'
        db.create_table(u'sap_situacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'sap', ['Situacao'])

        # Adding model 'Procedimento'
        db.create_table(u'sap_procedimento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome_parte', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, unique=True, null=True, blank=True)),
            ('telefone_fixo', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('telefone_celular', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('tipo_documento', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('tipo_documento_conteudo', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('assunto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sap.Assunto'])),
            ('situacao', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sap.Situacao'])),
            ('auditor_responsavel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_auditor_responsavel', to=orm['auth.User'])),
            ('observacoes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('inspetoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sap.Inspetoria'])),
            ('criado_por', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_criado_por', null=True, to=orm['auth.User'])),
            ('modificado_por', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_modificado_por', null=True, to=orm['auth.User'])),
            ('criado_em', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modificado_em', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sap', ['Procedimento'])

        # Adding model 'Exigencia'
        db.create_table(u'sap_exigencia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('procedimento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sap.Procedimento'])),
            ('conteudo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('atendida', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'sap', ['Exigencia'])

        # Adding model 'Usuario_Inspetoria'
        db.create_table(u'sap_usuario_inspetoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('inspetoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sap.Inspetoria'])),
        ))
        db.send_create_signal(u'sap', ['Usuario_Inspetoria'])

        # Adding model 'GrupoTrabalho'
        db.create_table(u'sap_grupotrabalho', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('assunto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sap.Assunto'])),
        ))
        db.send_create_signal(u'sap', ['GrupoTrabalho'])

        # Adding model 'GrupoTrabalhoAuditor'
        db.create_table(u'sap_grupotrabalhoauditor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grupo_trabalho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sap.GrupoTrabalho'])),
            ('auditor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'sap', ['GrupoTrabalhoAuditor'])


    def backwards(self, orm):
        # Deleting model 'Assunto'
        db.delete_table(u'sap_assunto')

        # Deleting model 'Inspetoria'
        db.delete_table(u'sap_inspetoria')

        # Deleting model 'Situacao'
        db.delete_table(u'sap_situacao')

        # Deleting model 'Procedimento'
        db.delete_table(u'sap_procedimento')

        # Deleting model 'Exigencia'
        db.delete_table(u'sap_exigencia')

        # Deleting model 'Usuario_Inspetoria'
        db.delete_table(u'sap_usuario_inspetoria')

        # Deleting model 'GrupoTrabalho'
        db.delete_table(u'sap_grupotrabalho')

        # Deleting model 'GrupoTrabalhoAuditor'
        db.delete_table(u'sap_grupotrabalhoauditor')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sap.assunto': {
            'Meta': {'object_name': 'Assunto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'sap.exigencia': {
            'Meta': {'object_name': 'Exigencia'},
            'atendida': ('django.db.models.fields.BooleanField', [], {}),
            'conteudo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedimento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sap.Procedimento']"})
        },
        u'sap.grupotrabalho': {
            'Meta': {'object_name': 'GrupoTrabalho'},
            'assunto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sap.Assunto']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'sap.grupotrabalhoauditor': {
            'Meta': {'object_name': 'GrupoTrabalhoAuditor'},
            'auditor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'grupo_trabalho': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sap.GrupoTrabalho']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sap.inspetoria': {
            'Meta': {'object_name': 'Inspetoria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'sap.procedimento': {
            'Meta': {'object_name': 'Procedimento'},
            'assunto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sap.Assunto']"}),
            'auditor_responsavel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_auditor_responsavel'", 'to': u"orm['auth.User']"}),
            'criado_em': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'criado_por': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_criado_por'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspetoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sap.Inspetoria']"}),
            'modificado_em': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'modificado_por': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_modificado_por'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'nome_parte': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'observacoes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'situacao': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sap.Situacao']"}),
            'telefone_celular': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'telefone_fixo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tipo_documento': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'tipo_documento_conteudo': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        u'sap.situacao': {
            'Meta': {'object_name': 'Situacao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'sap.usuario_inspetoria': {
            'Meta': {'object_name': 'Usuario_Inspetoria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspetoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sap.Inspetoria']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sap']