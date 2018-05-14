# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RespuestaIndefinida.padre'
        db.add_column(u'licencias_respuestaindefinida', 'padre',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.RespuestaIndefinida'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'RespuestaIndefinida.significado'
        db.add_column(u'licencias_respuestaindefinida', 'significado',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RespuestaIndefinida.padre'
        db.delete_column(u'licencias_respuestaindefinida', 'padre_id')

        # Deleting field 'RespuestaIndefinida.significado'
        db.delete_column(u'licencias_respuestaindefinida', 'significado')


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
        }
    }

    complete_apps = ['licencias']