# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TipoSubseccion.tipopadre'
        db.alter_column(u'categorizacion_tiposubseccion', 'tipopadre_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoSubseccion'], null=True))

    def backwards(self, orm):

        # Changing field 'TipoSubseccion.tipopadre'
        db.alter_column(u'categorizacion_tiposubseccion', 'tipopadre_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Estatus'], null=True))

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
        u'categorizacion.asignacion': {
            'Meta': {'object_name': 'Asignacion'},
            'asignacion_habilitada': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha_asignacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solicitud': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Solicitud']", 'null': 'True'}),
            'solicitud_libro': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']", 'null': 'True'}),
            'tipo_asignacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoAsignacion']"})
        },
        u'categorizacion.aspectofundamental': {
            'Meta': {'object_name': 'AspectoFundamental'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'respuesta_tabulador': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.RespuestaTabulador']"})
        },
        u'categorizacion.aspectofundamentalconfig': {
            'Meta': {'object_name': 'AspectoFundamentalConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'peso_porcentual': ('django.db.models.fields.FloatField', [], {}),
            'tabulador': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"}),
            'tipo_aspecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoAspectoFundamental']"})
        },
        u'categorizacion.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']"}),
            'tope_porcentual': ('django.db.models.fields.FloatField', [], {'default': '15.0'}),
            'valor': ('django.db.models.fields.IntegerField', [], {})
        },
        u'categorizacion.consignacion': {
            'Meta': {'object_name': 'Consignacion'},
            'estatus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'funcionarioconsignacion'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'solicitud_libro': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']"}),
            'sucursal': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.direccion': {
            'Meta': {'object_name': 'Direccion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.documento': {
            'Meta': {'object_name': 'Documento'},
            'eliminado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fecha_aprobacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'firmado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'plantilla_documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.PlantillaDocumento']", 'null': 'True'}),
            'ruta_documento': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tipo_documento_compuesto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoDocumentoCompuesto']", 'null': 'True'})
        },
        u'categorizacion.elementoencuesta': {
            'Meta': {'object_name': 'ElementoEncuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tipo_valoracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoValoracion']"})
        },
        u'categorizacion.elementoencuestaseccionencuesta': {
            'Meta': {'object_name': 'ElementoEncuestaSeccionEncuesta'},
            'elemento_encuesta': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.ElementoEncuesta']"}),
            'encuesta': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Encuesta']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seccion_encuesta': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SeccionEncuesta']"})
        },
        u'categorizacion.encuesta': {
            'Meta': {'object_name': 'Encuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']"})
        },
        u'categorizacion.entrada': {
            'Meta': {'object_name': 'Entrada'},
            'comentario': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'es_anonimo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estatus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'fecha_entrada': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lsr': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.LsrDigital']"}),
            'severidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Severidad']", 'null': 'True', 'blank': 'True'}),
            'tipo_comentario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoComentario']"}),
            'turista': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Turista']"})
        },
        u'categorizacion.especificacionlegal': {
            'Meta': {'object_name': 'EspecificacionLegal'},
            'contenido': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'documento_asociado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoDocumentoCompuesto']"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificador_legal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'tipo_especificacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoEspecificacion']"}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']"})
        },
        u'categorizacion.estatus': {
            'Meta': {'object_name': 'Estatus'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tipo_solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoSolicitud']"})
        },
        u'categorizacion.folio': {
            'Meta': {'object_name': 'Folio'},
            'consignacion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Consignacion']", 'null': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_notificacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file_path': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lsr_fisico': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.LsrFisico']"}),
            'numero': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255'})
        },
        u'categorizacion.funcionario': {
            'Meta': {'unique_together': "((u'user', u'direccion'),)", 'object_name': 'Funcionario'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'direccion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Direccion']"}),
            'habilitado': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tiporol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoRol']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']", 'unique': 'True'})
        },
        u'categorizacion.incidencia': {
            'Meta': {'object_name': 'Incidencia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incidencia_condicional': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.IncidenciaCondicional']"}),
            'tabulador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"})
        },
        u'categorizacion.incidenciacondicional': {
            'Meta': {'object_name': 'IncidenciaCondicional'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porcentaje_inferior': ('django.db.models.fields.FloatField', [], {}),
            'porcentaje_superior': ('django.db.models.fields.FloatField', [], {}),
            'valor_incidencia': ('django.db.models.fields.FloatField', [], {})
        },
        u'categorizacion.indicador': {
            'Meta': {'object_name': 'Indicador'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suministrado': ('django.db.models.fields.BooleanField', [], {})
        },
        u'categorizacion.lsrdigital': {
            'Meta': {'object_name': 'LsrDigital'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'sucursal': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.lsrfisico': {
            'Meta': {'object_name': 'LsrFisico'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificador': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'solicitud_libro': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']"}),
            'sucursal': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'asunto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'emisor': ('mintur.fields.BigForeignKey', [], {'related_name': "u'notificacion_tiene_emisor'", 'to': u"orm['cuentas.MinturUser']"}),
            'estatus_actual': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'estatus_actual'", 'to': u"orm['categorizacion.Estatus']"}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'", 'blank': 'True'}),
            'receptor': ('mintur.fields.BigForeignKey', [], {'related_name': "u'notificacion_tiene_receptor'", 'to': u"orm['cuentas.MinturUser']"}),
            'solicitud': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Solicitud']", 'null': 'True'}),
            'solicitud_libro': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']", 'null': 'True'})
        },
        u'categorizacion.notificacionbackup': {
            'Meta': {'object_name': 'NotificacionBackup'},
            'asunto': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'emisor': ('mintur.fields.BigForeignKey', [], {'related_name': "u'notificacion_backup_emisor'", 'to': u"orm['cuentas.MinturUser']"}),
            'estatus_actual': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'estatus_backup_actual'", 'to': u"orm['categorizacion.Estatus']"}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'", 'blank': 'True'}),
            'receptor': ('mintur.fields.BigForeignKey', [], {'related_name': "u'notificacion_backup_receptor'", 'to': u"orm['cuentas.MinturUser']"}),
            'solicitud': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"})
        },
        u'categorizacion.notificaciondocumentocompuesto': {
            'Meta': {'object_name': 'NotificacionDocumentoCompuesto'},
            'documento': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Documento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notificacion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Notificacion']", 'null': 'True', 'blank': 'True'}),
            'notificacion_backup': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.NotificacionBackup']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.observaciongeneral': {
            'Meta': {'object_name': 'ObservacionGeneral'},
            'funcionario': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'"}),
            'subseccion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Subseccion']"})
        },
        u'categorizacion.oficinaregional': {
            'Meta': {'object_name': 'OficinaRegional'},
            'direccion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('mintur.fields.BigForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.opcionesrepeticion': {
            'Meta': {'object_name': 'OpcionesRepeticion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'respuesta_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"}),
            'seccion_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SeccionConfig']"})
        },
        u'categorizacion.operadorformula': {
            'Meta': {'object_name': 'OperadorFormula'},
            'aridad': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'representacion': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'categorizacion.parametroconfiguracion': {
            'Meta': {'object_name': 'ParametroConfiguracion'},
            'clave': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valor': ('django.db.models.fields.TextField', [], {'max_length': '2048'})
        },
        u'categorizacion.placa': {
            'Meta': {'object_name': 'Placa'},
            'documento': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Documento']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licencia_asignada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.LicenciaAsignada']"}),
            'pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'categorizacion.plantilladocumento': {
            'Meta': {'object_name': 'PlantillaDocumento'},
            'formato': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'categorizacion.pstcategoriadocumentocompuesto': {
            'Meta': {'object_name': 'PstCategoriaDocumentoCompuesto'},
            'calificacion': ('django.db.models.fields.IntegerField', [], {}),
            'calificacion_definitiva': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Categoria']"}),
            'documento': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Documento']", 'unique': 'True', 'null': 'True'}),
            'fecha_categorizacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'categorizacion.relevancia': {
            'Meta': {'object_name': 'Relevancia'},
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Categoria']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operador_logico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.OperadorFormula']", 'null': 'True', 'blank': 'True'}),
            'repeticion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subseccion_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SubseccionConfig']"})
        },
        u'categorizacion.repeticion': {
            'Meta': {'object_name': 'Repeticion'},
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Categoria']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeticion_esperada': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'subseccion_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SubseccionConfig']"})
        },
        u'categorizacion.requisitodigital': {
            'Meta': {'object_name': 'RequisitoDigital'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_path': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'solicitud': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"})
        },
        u'categorizacion.requisitospago': {
            'Meta': {'object_name': 'RequisitosPago'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'solicitud': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']"}),
            'tipo_requisito_pago': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoRequisitoPago']"})
        },
        u'categorizacion.respuestaconfig': {
            'Meta': {'object_name': 'RespuestaConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_medida': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.TipoMedida']", 'null': 'True', 'blank': 'True'}),
            'tipo_respuesta': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.TipoRespuesta']"})
        },
        u'categorizacion.respuestaencuesta': {
            'Meta': {'object_name': 'RespuestaEncuesta'},
            'elemento_encuesta': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.ElementoEncuesta']"}),
            'entrada': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Entrada']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'seccion_encuesta': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SeccionEncuesta']"}),
            'valoracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Valoracion']"})
        },
        u'categorizacion.respuestalsr': {
            'Meta': {'object_name': 'RespuestaLsr'},
            'comentario': ('django.db.models.fields.TextField', [], {}),
            'emisor': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'entrada': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Entrada']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'categorizacion.respuestatabulador': {
            'Meta': {'object_name': 'RespuestaTabulador'},
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pst': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']", 'unique': 'True'}),
            'tabulador': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"})
        },
        u'categorizacion.respuestavalorrespuesta': {
            'Meta': {'object_name': 'RespuestaValorRespuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pregunta_config': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"}),
            'respuesta_config': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.ValorRespuestaConfig']"}),
            'valor_minino_aceptacion': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'categorizacion.seccionconfig': {
            'Meta': {'object_name': 'SeccionConfig'},
            'aspecto_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.AspectoFundamentalConfig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seccion_padre_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SeccionConfig']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.seccionencuesta': {
            'Meta': {'object_name': 'SeccionEncuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.severidad': {
            'Meta': {'object_name': 'Severidad'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'valor': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        u'categorizacion.solicitud': {
            'Meta': {'object_name': 'Solicitud'},
            'dias_prorroga': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255', 'null': 'True'}),
            'estatus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'fecha_apertura': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_clausura': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_modificacion_estado': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'funcionario'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            'funcionario_extra': ('mintur.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "u'funcionario_extra'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permitir_prorroga': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pst': ('mintur.fields.BigForeignKey', [], {'related_name': "u'pst_genera_solicitudes_de_categorizacion'", 'to': u"orm['registro.Pst']"}),
            'pst_categoria_doc': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.PstCategoriaDocumentoCompuesto']", 'null': 'True', 'blank': 'True'}),
            'renovar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'}),
            'tabulador': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"})
        },
        u'categorizacion.solicitudlibro': {
            'Meta': {'object_name': 'SolicitudLibro'},
            'archivo_comprobante': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True'}),
            'estatus': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'fecha_culminacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_realizacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'funcionariolsr'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_comprobante': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'oficina': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.OficinaRegional']"}),
            'pst': ('mintur.fields.BigForeignKey', [], {'related_name': "u'pst_genera_solicitudes_de_libros'", 'to': u"orm['registro.Pst']"}),
            'sucursal': ('mintur.fields.BigForeignKey', [], {'default': 'None', 'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.subseccion': {
            'Meta': {'object_name': 'Subseccion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'"}),
            'respuesta_tabulador': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.RespuestaTabulador']"}),
            'subseccion_config': ('mintur.fields.BigForeignKey', [], {'related_name': "u'subseccion_config_id'", 'to': u"orm['categorizacion.SubseccionConfig']"}),
            'tipo_subseccion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.TipoSubseccion']"})
        },
        u'categorizacion.subseccionarchivorequisito': {
            'Meta': {'object_name': 'SubseccionArchivoRequisito'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requisito_digital': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.RequisitoDigital']"}),
            'subseccion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Subseccion']"})
        },
        u'categorizacion.subseccionconfig': {
            'Meta': {'object_name': 'SubseccionConfig'},
            'condicion_posneg': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'respuesta_config': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"}),
            'seccion_config': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.SeccionConfig']"}),
            'subs_imagen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subseccion_config_padre': ('mintur.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "u'subseccion_config_tiene_subseccion_padre_config_id'", 'null': 'True', 'to': u"orm['categorizacion.SubseccionConfig']"}),
            'tipo_subseccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoSubseccion']"})
        },
        u'categorizacion.tabulador': {
            'Meta': {'object_name': 'Tabulador'},
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "u'fecha_creacion'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']"}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'version_actual': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'categorizacion.tipoasignacion': {
            'Meta': {'object_name': 'TipoAsignacion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.tipoaspectofundamental': {
            'Meta': {'object_name': 'TipoAspectoFundamental'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.tipocomentario': {
            'Meta': {'object_name': 'TipoComentario'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.tipodocumentocompuesto': {
            'Meta': {'object_name': 'TipoDocumentoCompuesto'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.tipodocumentoidentidad': {
            'Meta': {'object_name': 'TipoDocumentoIdentidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.tipoespecificacion': {
            'Meta': {'object_name': 'TipoEspecificacion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.tipomedida': {
            'Meta': {'object_name': 'TipoMedida'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.tiporequisitopago': {
            'Meta': {'object_name': 'TipoRequisitoPago'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.tiporespuesta': {
            'Meta': {'object_name': 'TipoRespuesta'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': "u'10'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.tiporol': {
            'Meta': {'object_name': 'TipoRol'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.tiposolicitud': {
            'Meta': {'object_name': 'TipoSolicitud'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.tiposubseccion': {
            'Meta': {'object_name': 'TipoSubseccion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipopadre': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['categorizacion.TipoSubseccion']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.tipovaloracion': {
            'Meta': {'object_name': 'TipoValoracion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.turista': {
            'Meta': {'object_name': 'Turista'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Ciudad']", 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'numero_documento_identidad': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'telefono_contacto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tipo_documento_identidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoDocumentoIdentidad']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.valoracion': {
            'Meta': {'object_name': 'Valoracion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'puntaje': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tipo_valoracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoValoracion']"})
        },
        u'categorizacion.valorcategoria': {
            'Meta': {'object_name': 'ValorCategoria'},
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Categoria']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Indicador']"}),
            'operador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.OperadorFormula']", 'null': 'True', 'blank': 'True'}),
            'valor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valor_comparacion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.valorindicador': {
            'Meta': {'object_name': 'ValorIndicador'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Indicador']"}),
            'operador_derecho': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'operador_derecho'", 'null': 'True', 'to': u"orm['categorizacion.OperadorFormula']"}),
            'operador_izquierdo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'operador_izquierdo'", 'null': 'True', 'to': u"orm['categorizacion.OperadorFormula']"}),
            'orden': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'respuesta_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"})
        },
        u'categorizacion.valorrespuesta': {
            'Meta': {'object_name': 'ValorRespuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subseccion': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Subseccion']"}),
            'valor': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'valor_respuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ValorRespuestaConfig']"})
        },
        u'categorizacion.valorrespuestaconfig': {
            'Meta': {'object_name': 'ValorRespuestaConfig'},
            'categoria': ('mintur.fields.BigForeignKey', [], {'to': u"orm['categorizacion.Categoria']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limite_inferior': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'limite_superior': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'licencias.licenciaasignada': {
            'Meta': {'object_name': 'LicenciaAsignada'},
            'estatus': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_renovacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_vencimiento': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_licencia': ('django.db.models.fields.IntegerField', [], {}),
            'solicitud_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.SolicitudLicencia']", 'db_column': "u'solicitud_licenciaid'"}),
            'sucursal': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'}),
            'tipo_licenciaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoLicencia']", 'db_column': "u'tipo_licenciaid'"}),
            'usuario_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'licencias.pregunta': {
            'Meta': {'object_name': 'Pregunta'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_respuestaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licencias.TipoRespuesta']", 'db_column': "u'tipo_respuestaid'"}),
            'valoresPosibles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['licencias.ValorPosible']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'licencias.recaudo': {
            'Meta': {'object_name': 'Recaudo'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'requerido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sucursal': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'sucursal': ('mintur.fields.BigForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True', 'blank': 'True'}),
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
            'recaudos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['licencias.Recaudo']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
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
        u'licencias.valorposible': {
            'Meta': {'object_name': 'ValorPosible'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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
            'rtn': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        u'registro.sucursales': {
            'Meta': {'object_name': 'Sucursales'},
            'avenida_calle': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'codigo_postal': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'edificio': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Estado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'oficina_apartamento': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Parroquia']"}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
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
        u'venezuela.ciudad': {
            'Meta': {'object_name': 'Ciudad'},
            'capital': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Estado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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

    complete_apps = ['categorizacion']