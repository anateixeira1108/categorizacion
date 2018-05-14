# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TipoActa'
        db.create_table(u'actas_tipoacta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('codigo_documento', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
        ))
        db.send_create_signal(u'actas', ['TipoActa'])

        # Adding model 'ActaDocumentos'
        db.create_table(u'actas_actadocumentos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actas.TipoActa'])),
            ('providencia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actas.ActaDocumentos'], null=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pst_actas_v_f', null=True, to=orm['registro.Pst'])),
            ('verificacion', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['verificacion.Verificacion'], null=True, blank=True)),
            ('fiscalizacion', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['fiscalizacion.Fiscalizacion'], null=True, blank=True)),
            ('fecha_generacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_notificacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('hallazgos_materia', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('hallazgos_condicion', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('hallazgos_criterio', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('hallazgos_efecto', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('hallazgos_evidencia', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'actas', ['ActaDocumentos'])

        # Adding model 'ActaReparoAtributos'
        db.create_table(u'actas_actareparoatributos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('periodo', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('ingresos_brutos', self.gf('django.db.models.fields.FloatField')()),
            ('calculo_segun_fiscalizacion', self.gf('django.db.models.fields.FloatField')()),
            ('monto_pagado_segun_declaracion', self.gf('django.db.models.fields.FloatField')()),
            ('diferencia_por_pagar', self.gf('django.db.models.fields.FloatField')()),
            ('acta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actas.ActaDocumentos'])),
        ))
        db.send_create_signal(u'actas', ['ActaReparoAtributos'])

        # Adding model 'Requisito'
        db.create_table(u'actas_requisito', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('requisito', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'actas', ['Requisito'])

        # Adding model 'ActaRequisito'
        db.create_table(u'actas_actarequisito', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('acta', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actas_v_f', to=orm['actas.ActaDocumentos'])),
            ('requisito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actas.Requisito'])),
            ('entrego', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'actas', ['ActaRequisito'])

        # Adding model 'ActaLogCambiarStatus'
        db.create_table(u'actas_actalogcambiarstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('acta', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actas_log_c_s', to=orm['actas.ActaDocumentos'])),
            ('estatus', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha_generacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_notificacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('justificacion_cambio_de_estatus', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
        ))
        db.send_create_signal(u'actas', ['ActaLogCambiarStatus'])


    def backwards(self, orm):
        # Deleting model 'TipoActa'
        db.delete_table(u'actas_tipoacta')

        # Deleting model 'ActaDocumentos'
        db.delete_table(u'actas_actadocumentos')

        # Deleting model 'ActaReparoAtributos'
        db.delete_table(u'actas_actareparoatributos')

        # Deleting model 'Requisito'
        db.delete_table(u'actas_requisito')

        # Deleting model 'ActaRequisito'
        db.delete_table(u'actas_actarequisito')

        # Deleting model 'ActaLogCambiarStatus'
        db.delete_table(u'actas_actalogcambiarstatus')


    models = {
        u'actas.actadocumentos': {
            'Meta': {'object_name': 'ActaDocumentos'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'estatus': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_generacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_notificacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fiscalizacion': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['fiscalizacion.Fiscalizacion']", 'null': 'True', 'blank': 'True'}),
            'hallazgos_condicion': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hallazgos_criterio': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hallazgos_efecto': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hallazgos_evidencia': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hallazgos_materia': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'providencia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actas.ActaDocumentos']", 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pst_actas_v_f'", 'null': 'True', 'to': u"orm['registro.Pst']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actas.TipoActa']"}),
            'verificacion': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['verificacion.Verificacion']", 'null': 'True', 'blank': 'True'})
        },
        u'actas.actalogcambiarstatus': {
            'Meta': {'object_name': 'ActaLogCambiarStatus'},
            'acta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actas_log_c_s'", 'to': u"orm['actas.ActaDocumentos']"}),
            'estatus': ('django.db.models.fields.IntegerField', [], {}),
            'fecha_generacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_notificacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'justificacion_cambio_de_estatus': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'actas.actareparoatributos': {
            'Meta': {'object_name': 'ActaReparoAtributos'},
            'acta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actas.ActaDocumentos']"}),
            'calculo_segun_fiscalizacion': ('django.db.models.fields.FloatField', [], {}),
            'diferencia_por_pagar': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingresos_brutos': ('django.db.models.fields.FloatField', [], {}),
            'monto_pagado_segun_declaracion': ('django.db.models.fields.FloatField', [], {}),
            'periodo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'actas.actarequisito': {
            'Meta': {'object_name': 'ActaRequisito'},
            'acta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actas_v_f'", 'to': u"orm['actas.ActaDocumentos']"}),
            'entrego': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requisito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actas.Requisito']"})
        },
        u'actas.requisito': {
            'Meta': {'object_name': 'Requisito'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requisito': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'actas.tipoacta': {
            'Meta': {'object_name': 'TipoActa'},
            'codigo_documento': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
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
        u'fiscalizacion.fiscalizacion': {
            'Meta': {'object_name': 'Fiscalizacion'},
            'creado_el': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desde': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'estatus': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'hasta': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        },
        u'verificacion.verificacion': {
            'Meta': {'object_name': 'Verificacion'},
            'conclusiones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creado_el': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desde': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'estatus': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'hasta': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tipo_verificacion': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['actas']