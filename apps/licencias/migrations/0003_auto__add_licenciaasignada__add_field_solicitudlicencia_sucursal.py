# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LicenciaAsignada'
        db.create_table(u'licencias_licenciaasignada', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('numero_licencia', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha_emision', self.gf('django.db.models.fields.DateTimeField')()),
            ('fecha_vencimiento', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('fecha_renovacion', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tipo_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.TipoLicencia'], db_column=u'tipo_licenciaid')),
            ('solicitud_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudLicencia'], db_column=u'solicitud_licenciaid')),
            ('usuario_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Sucursales'], null=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'licencias', ['LicenciaAsignada'])

        # Adding field 'SolicitudLicencia.sucursal'
        db.add_column(u'licencias_solicitudlicencia', 'sucursal',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Sucursales'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'LicenciaAsignada'
        db.delete_table(u'licencias_licenciaasignada')

        # Deleting field 'SolicitudLicencia.sucursal'
        db.delete_column(u'licencias_solicitudlicencia', 'sucursal_id')


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
        u'licencias.archivorecaudo': {
            'Meta': {'object_name': 'ArchivoRecaudo'},
            'certificado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recaudoid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.Recaudo']", 'db_column': "u'recaudoid'"}),
            'ruta': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'db_column': "u'solicitud_licenciaid'"})
        },
        u'licencias.archivorespuesta': {
            'Meta': {'object_name': 'ArchivoRespuesta'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ruta': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'licencias.estatussolicitud': {
            'Meta': {'object_name': 'EstatusSolicitud'},
            'clase': ('django.db.models.fields.CharField', [], {'default': "u'label-warning'", 'max_length': '255'}),
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'licencias.formulario': {
            'Meta': {'object_name': 'Formulario'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'preguntas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['licencias.Pregunta']", 'symmetrical': 'False'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'licencias.historicosolicitudeslicencias': {
            'Meta': {'object_name': 'HistoricoSolicitudesLicencias'},
            'estatus_solicitudid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.EstatusSolicitud']", 'db_column': "u'estatus_solicitudid'"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'db_column': "u'solicitud_licenciaid'"}),
            'usuariomodificar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'licencias.inspeccion': {
            'Meta': {'object_name': 'Inspeccion'},
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_inspeccion': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspectores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'inspectores'", 'symmetrical': 'False', 'to': u"orm['cuentas.MinturUser']"}),
            'solicitud_inspeccionid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudInspeccion']", 'db_column': "u'solicitud_inspeccionid'"}),
            'tipo_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']", 'db_column': "u'tipo_licenciaid'"})
        },
        u'licencias.licenciaasignada': {
            'Meta': {'object_name': 'LicenciaAsignada'},
            'estatus': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_renovacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_vencimiento': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_licencia': ('django.db.models.fields.IntegerField', [], {}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'db_column': "u'solicitud_licenciaid'"}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'}),
            'tipo_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']", 'db_column': "u'tipo_licenciaid'"}),
            'usuario_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'licencias.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'asunto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'emisor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'emisor'", 'to': u"orm['cuentas.MinturUser']"}),
            'estatus_solicitudid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.EstatusSolicitud']", 'db_column': "u'estatus_solicitudid'"}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'receptor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'receptor'", 'to': u"orm['cuentas.MinturUser']"}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'db_column': "u'solicitud_licenciaid'"})
        },
        u'licencias.pregunta': {
            'Meta': {'object_name': 'Pregunta'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_respuestaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoRespuesta']", 'db_column': "u'tipo_respuestaid'"}),
            'valoresPosibles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['licencias.ValorPosible']", 'symmetrical': 'False'})
        },
        u'licencias.recaudo': {
            'Meta': {'object_name': 'Recaudo'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'requerido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sucursal': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'licencias.respuesta': {
            'Meta': {'object_name': 'Respuesta'},
            'auth_userid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspeccionid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.Inspeccion']", 'null': 'True', 'db_column': "u'inspeccionid'", 'blank': 'True'}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'null': 'True', 'db_column': "u'solicitud_licenciaid'", 'blank': 'True'})
        },
        u'licencias.respuestadefinida': {
            'Meta': {'object_name': 'RespuestaDefinida', '_ormbases': [u'licencias.Respuesta']},
            'respuesta_descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'respuesta_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['licencias.Respuesta']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'licencias.respuestaindefinida': {
            'Meta': {'object_name': 'RespuestaIndefinida', '_ormbases': [u'licencias.Respuesta']},
            'archivo_respuestaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.ArchivoRespuesta']", 'db_column': "u'archivo_respuestaid'"}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.RespuestaIndefinida']", 'null': 'True', 'blank': 'True'}),
            'respuesta': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'respuesta_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['licencias.Respuesta']", 'unique': 'True', 'primary_key': 'True'}),
            'significado': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'licencias.solicitudinspeccion': {
            'Meta': {'object_name': 'SolicitudInspeccion'},
            'auth_userid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            'estado': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'fecha_solicitud': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'db_column': "u'solicitud_licenciaid'"}),
            'tipo_usuario': ('django.db.models.fields.BooleanField', [], {})
        },
        u'licencias.solicitudlicencia': {
            'Meta': {'object_name': 'SolicitudLicencia'},
            'analista_asignado': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'analista'", 'null': 'True', 'to': u"orm['cuentas.MinturUser']"}),
            'edicion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estatus_solicitudid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.EstatusSolicitud']", 'db_column': "u'estatus_solicitudid'"}),
            'fecha_fin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_inspeccion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'}),
            'tipo_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']", 'db_column': "u'tipo_licenciaid'"}),
            'tipo_solicitudid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoSolicitud']", 'db_column': "u'tipo_solicitudid'"}),
            'usuario_pst_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Upst'", 'to': u"orm['cuentas.MinturUser']"})
        },
        u'licencias.tipolicencia': {
            'Meta': {'object_name': 'TipoLicencia'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'formulario_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.Formulario']", 'db_column': "u'formulario_id'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'tipo_padre_id'", 'null': 'True', 'to': u"orm['licencias.TipoLicencia']"}),
            'recaudos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['licencias.Recaudo']", 'symmetrical': 'False'})
        },
        u'licencias.tiporespuesta': {
            'Meta': {'object_name': 'TipoRespuesta'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'licencias.tiposolicitud': {
            'Meta': {'object_name': 'TipoSolicitud'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'licencias.valoresrdefinida': {
            'Meta': {'object_name': 'ValoresRdefinida'},
            'archivo_respuestaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.ArchivoRespuesta']", 'db_column': "u'archivo_respuestaid'"}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'respuesta_definida': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.RespuestaDefinida']", 'db_column': "u'respuesta_definidarespuesta'"}),
            'valor_posibleid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.ValorPosible']", 'db_column': "u'valor_posibleid'"})
        },
        u'licencias.valorposible': {
            'Meta': {'object_name': 'ValorPosible'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'registro.categoriazonainteresturistico': {
            'Meta': {'object_name': 'CategoriaZonaInteresTuristico'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'registro.pst': {
            'Meta': {'object_name': 'Pst'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'archivo_cedula': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_pasaporte': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_rif': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_servicio': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cantidad_declaraciones_extemporaneas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cantidad_declaraciones_omitidas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cedula': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'creado_el': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'denominacion_comercial': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'emprendedor': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'esta_solvente': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estado_contribuyente': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'estatus': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'estatus_certificacion_riftur': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'estatus_certificacion_rtn': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('mintur.fields.BigAutoField', [], {'primary_key': 'True'}),
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
            'tipo_figura': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'tipo_juridica': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'tipo_pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.TipoPst']", 'null': 'True', 'blank': 'True'}),
            'ultima_fiscalizacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ultima_verificacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('mintur.fields.BigForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            'zona_interes_turistica': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.ZonasInteresTuristico']", 'null': 'True', 'blank': 'True'})
        },
        u'registro.sucursales': {
            'Meta': {'object_name': 'Sucursales'},
            'avenida_calle': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'codigo_postal': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'edificio': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'estado': ('mintur.fields.BigForeignKey', [], {'to': u"orm['venezuela.Estado']"}),
            'id': ('mintur.fields.BigAutoField', [], {'primary_key': 'True'}),
            'municipio': ('mintur.fields.BigForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'oficina_apartamento': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parroquia': ('mintur.fields.BigForeignKey', [], {'to': u"orm['venezuela.Parroquia']"}),
            'pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'punto_referencia': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'urbanizacion': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'registro.tipopst': {
            'Meta': {'object_name': 'TipoPst'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_persona': ('django.db.models.fields.IntegerField', [], {})
        },
        u'registro.zonasinteresturistico': {
            'Meta': {'object_name': 'ZonasInteresTuristico'},
            'categoria': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.CategoriaZonaInteresTuristico']"}),
            'decreto': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'gaceta_oficial': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'ordenamiento_legal': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'superficie': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'ubicacion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'venezuela.estado': {
            'Meta': {'object_name': 'Estado'},
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3166_2': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'venezuela.municipio': {
            'Meta': {'object_name': 'Municipio'},
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Estado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'venezuela.parroquia': {
            'Meta': {'object_name': 'Parroquia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'parroquia': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['licencias']