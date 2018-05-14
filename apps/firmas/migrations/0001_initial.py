# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Firma'
        db.create_table(u'firmas_firma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('ministro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('fecha_providencia', self.gf('django.db.models.fields.DateField')()),
            ('numero_providencia', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('numero_gaceta', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('fecha_gaceta', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'firmas', ['Firma'])

        # Adding model 'FirmaDelegada'
        db.create_table(u'firmas_firmadelegada', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firma', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firmas.Firma'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuracion.Area'])),
            ('fecha_providencia', self.gf('django.db.models.fields.DateField')()),
            ('numero_providencia', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('numero_gaceta', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('fecha_gaceta', self.gf('django.db.models.fields.DateField')()),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_desactivacion', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'firmas', ['FirmaDelegada'])


    def backwards(self, orm):
        # Deleting model 'Firma'
        db.delete_table(u'firmas_firma')

        # Deleting model 'FirmaDelegada'
        db.delete_table(u'firmas_firmadelegada')


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
        u'configuracion.area': {
            'Meta': {'object_name': 'Area'},
            'acronimo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cuentas.minturuser': {
            'Meta': {'object_name': 'MinturUser'},
            'account_activation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cedula': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'correo_electronico2': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'reset_password_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reset_password_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rif': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'role': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'firmas.firma': {
            'Meta': {'object_name': 'Firma'},
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'fecha_gaceta': ('django.db.models.fields.DateField', [], {}),
            'fecha_providencia': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ministro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numero_gaceta': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'numero_providencia': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'firmas.firmadelegada': {
            'Meta': {'object_name': 'FirmaDelegada'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['configuracion.Area']"}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_desactivacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_gaceta': ('django.db.models.fields.DateField', [], {}),
            'fecha_providencia': ('django.db.models.fields.DateField', [], {}),
            'firma': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['firmas.Firma']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_gaceta': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'numero_providencia': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['firmas']