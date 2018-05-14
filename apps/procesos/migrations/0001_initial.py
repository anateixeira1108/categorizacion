# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Proceso'
        db.create_table(u'procesos_proceso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_desactivacion', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'procesos', ['Proceso'])

        # Adding model 'Flujo'
        db.create_table(u'procesos_flujo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proceso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.Proceso'])),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('inicio', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'procesos', ['Flujo'])

        # Adding model 'FlujoSecuencia'
        db.create_table(u'procesos_flujosecuencia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actual', self.gf('django.db.models.fields.IntegerField')()),
            ('siguiente', self.gf('django.db.models.fields.IntegerField')()),
            ('proceso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.Proceso'])),
        ))
        db.send_create_signal(u'procesos', ['FlujoSecuencia'])

        # Adding model 'ProcesoPst'
        db.create_table(u'procesos_procesopst', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('proceso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.Proceso'])),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.Flujo'])),
            ('nombre_estado', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_fin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'procesos', ['ProcesoPst'])

        # Adding model 'HistorialSecuencia'
        db.create_table(u'procesos_historialsecuencia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('proceso_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.ProcesoPst'])),
            ('proceso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.Proceso'])),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['procesos.Flujo'])),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('fecha_registro', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'procesos', ['HistorialSecuencia'])


    def backwards(self, orm):
        # Deleting model 'Proceso'
        db.delete_table(u'procesos_proceso')

        # Deleting model 'Flujo'
        db.delete_table(u'procesos_flujo')

        # Deleting model 'FlujoSecuencia'
        db.delete_table(u'procesos_flujosecuencia')

        # Deleting model 'ProcesoPst'
        db.delete_table(u'procesos_procesopst')

        # Deleting model 'HistorialSecuencia'
        db.delete_table(u'procesos_historialsecuencia')


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
        u'procesos.flujo': {
            'Meta': {'object_name': 'Flujo'},
            'fin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'proceso': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.Proceso']"})
        },
        u'procesos.flujosecuencia': {
            'Meta': {'object_name': 'FlujoSecuencia'},
            'actual': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proceso': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.Proceso']"}),
            'siguiente': ('django.db.models.fields.IntegerField', [], {})
        },
        u'procesos.historialsecuencia': {
            'Meta': {'object_name': 'HistorialSecuencia'},
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.Flujo']"}),
            'fecha_registro': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'proceso': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.Proceso']"}),
            'proceso_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.ProcesoPst']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'procesos.proceso': {
            'Meta': {'object_name': 'Proceso'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_desactivacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'procesos.procesopst': {
            'Meta': {'object_name': 'ProcesoPst'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.Flujo']"}),
            'fecha_fin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_estado': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'proceso': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['procesos.Proceso']"}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'registro.pst': {
            'Meta': {'object_name': 'Pst'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'archivo_cedula': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_pasaporte': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_rif': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_servicio': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cedula': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'creado_el': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'denominacion_comercial': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'emprendedor': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'estado_contribuyente': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'estatus': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio_actividad_comercial': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modificado_el': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'numero_contribuyente': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'razon_social': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'rtn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'telefono_celular': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_fijo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tiene_firma_personal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tipo_figura': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'tipo_juridica': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.TipoPst']", 'null': 'True', 'blank': 'True'}),
            'ultima_fiscalizacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ultima_verificacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'registro.tipopst': {
            'Meta': {'object_name': 'TipoPst'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tipo_persona': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['procesos']