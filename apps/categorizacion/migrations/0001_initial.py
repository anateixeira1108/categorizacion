# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TipoMedida'
        db.create_table(u'categorizacion_tipomedida', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoMedida'])

        # Adding model 'TipoRespuesta'
        db.create_table(u'categorizacion_tiporespuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('input_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoRespuesta'])

        # Adding model 'Direccion'
        db.create_table(u'categorizacion_direccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['Direccion'])

        # Adding model 'Categoria'
        db.create_table(u'categorizacion_categoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('valor', self.gf('django.db.models.fields.IntegerField')()),
            ('tipo_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ClasificacionPadrePst'])),
        ))
        db.send_create_signal(u'categorizacion', ['Categoria'])

        # Adding model 'ClasificacionPadrePst'
        db.create_table(u'categorizacion_clasificacionpadrepst', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['ClasificacionPadrePst'])

        # Adding model 'TipoMotivo'
        db.create_table(u'categorizacion_tipomotivo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoMotivo'])

        # Adding model 'ParametroConfiguracion'
        db.create_table(u'categorizacion_parametroconfiguracion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clave', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('valor', self.gf('django.db.models.fields.TextField')(max_length=2048)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'categorizacion', ['ParametroConfiguracion'])

        # Adding model 'PlantillaDocumento'
        db.create_table(u'categorizacion_plantilladocumento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('formato', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['PlantillaDocumento'])

        # Adding model 'TipoAsignacion'
        db.create_table(u'categorizacion_tipoasignacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoAsignacion'])

        # Adding model 'TipoComentario'
        db.create_table(u'categorizacion_tipocomentario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoComentario'])

        # Adding model 'TipoDocumentoIdentidad'
        db.create_table(u'categorizacion_tipodocumentoidentidad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoDocumentoIdentidad'])

        # Adding model 'TipoRequisitoPago'
        db.create_table(u'categorizacion_tiporequisitopago', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoRequisitoPago'])

        # Adding model 'TipoRol'
        db.create_table(u'categorizacion_tiporol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'categorizacion', ['TipoRol'])

        # Adding model 'TipoSolicitud'
        db.create_table(u'categorizacion_tiposolicitud', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoSolicitud'])

        # Adding model 'TipoSubseccion'
        db.create_table(u'categorizacion_tiposubseccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoSubseccion'])

        # Adding model 'Solicitud'
        db.create_table(u'categorizacion_solicitud', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pst_genera_solicitudes_de_categorizacion', to=orm['registro.Pst'])),
            ('estatus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Estatus'])),
            ('fecha_apertura', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Sucursales'], null=True)),
            ('fecha_modificacion_estado', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('fecha_clausura', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'funcionario', null=True, to=orm['categorizacion.Funcionario'])),
            ('funcionario_extra', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'funcionario_extra', null=True, to=orm['categorizacion.Funcionario'])),
            ('pst_categoria_doc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.PstCategoriaDocumentoCompuesto'], null=True, blank=True)),
            ('permitir_prorroga', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tabulador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Tabulador'])),
        ))
        db.send_create_signal(u'categorizacion', ['Solicitud'])

        # Adding model 'HistoricoCategorizacion'
        db.create_table(u'categorizacion_historicocategorizacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.TipoPst'])),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Solicitud'])),
            ('motivo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoMotivo'])),
            ('rif', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('correo_electronico', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('cedula', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rtn', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('fecha_ingreso_historico', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_inicio_solicitud', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'categorizacion', ['HistoricoCategorizacion'])

        # Adding model 'AreaNoCompletada'
        db.create_table(u'categorizacion_areanocompletada', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('historico_categorizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.HistoricoCategorizacion'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['AreaNoCompletada'])

        # Adding model 'Asignacion'
        db.create_table(u'categorizacion_asignacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Funcionario'])),
            ('tipo_asignacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoAsignacion'])),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Solicitud'], null=True)),
            ('solicitud_libro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.SolicitudLibro'], null=True)),
            ('fecha_asignacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('asignacion_habilitada', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'categorizacion', ['Asignacion'])

        # Adding model 'AspectoFundamental'
        db.create_table(u'categorizacion_aspectofundamental', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('respuesta_tabulador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.RespuestaTabulador'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['AspectoFundamental'])

        # Adding model 'AspectoFundamentalConfig'
        db.create_table(u'categorizacion_aspectofundamentalconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tabulador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Tabulador'])),
        ))
        db.send_create_signal(u'categorizacion', ['AspectoFundamentalConfig'])

        # Adding model 'TipoDocumentoCompuesto'
        db.create_table(u'categorizacion_tipodocumentocompuesto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['TipoDocumentoCompuesto'])

        # Adding model 'Documento'
        db.create_table(u'categorizacion_documento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plantilla_documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.PlantillaDocumento'])),
            ('fecha_emision', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_aprobacion', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('tipo_documento_compuesto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoDocumentoCompuesto'], null=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ruta_documento', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['Documento'])

        # Adding model 'Estatus'
        db.create_table(u'categorizacion_estatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoSolicitud'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'categorizacion', ['Estatus'])

        # Adding model 'Folio'
        db.create_table(u'categorizacion_folio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lsr_fisico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.LsrFisico'])),
            ('file_path', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=255, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=255)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('fecha_carga', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['Folio'])

        # Adding model 'Funcionario'
        db.create_table(u'categorizacion_funcionario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('direccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Direccion'])),
            ('tiporol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoRol'])),
            ('cedula', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('habilitado', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'categorizacion', ['Funcionario'])

        # Adding unique constraint on 'Funcionario', fields ['user', 'direccion']
        db.create_unique(u'categorizacion_funcionario', ['user_id', 'direccion_id'])

        # Adding model 'Entrada'
        db.create_table(u'categorizacion_entrada', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_comentario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoComentario'])),
            ('turista', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Turista'])),
            ('lsr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.LsrDigital'])),
            ('severidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Severidad'], null=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Estatus'])),
            ('comentario', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fecha_entrada', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name=u'related_forced_name_again', null=True, blank=True, to=orm['categorizacion.Encuesta'])),
            ('es_anonimo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'categorizacion', ['Entrada'])

        # Adding model 'SeccionEncuesta'
        db.create_table(u'categorizacion_seccionencuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['SeccionEncuesta'])

        # Adding model 'Encuesta'
        db.create_table(u'categorizacion_encuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('tipo_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.TipoPst'])),
        ))
        db.send_create_signal(u'categorizacion', ['Encuesta'])

        # Adding model 'ElementoEncuestaSeccionEncuesta'
        db.create_table(u'categorizacion_elementoencuestaseccionencuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('elemento_encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ElementoEncuesta'])),
            ('seccion_encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.SeccionEncuesta'])),
            ('encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Encuesta'])),
        ))
        db.send_create_signal(u'categorizacion', ['ElementoEncuestaSeccionEncuesta'])

        # Adding model 'ElementoEncuesta'
        db.create_table(u'categorizacion_elementoencuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['ElementoEncuesta'])

        # Adding model 'RespuestaEncuesta'
        db.create_table(u'categorizacion_respuestaencuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Entrada'])),
            ('valoracion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Valoracion'])),
            ('observacion', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('elemento_encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ElementoEncuesta'])),
        ))
        db.send_create_signal(u'categorizacion', ['RespuestaEncuesta'])

        # Adding model 'Valoracion'
        db.create_table(u'categorizacion_valoracion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('puntaje', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['Valoracion'])

        # Adding model 'ValoracionConfig'
        db.create_table(u'categorizacion_valoracionconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('elemento_encuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ElementoEncuesta'])),
            ('valoracion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Valoracion'])),
        ))
        db.send_create_signal(u'categorizacion', ['ValoracionConfig'])

        # Adding model 'Severidad'
        db.create_table(u'categorizacion_severidad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abreviacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('valor', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal(u'categorizacion', ['Severidad'])

        # Adding model 'LsrDigital'
        db.create_table(u'categorizacion_lsrdigital', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Sucursales'], null=True)),
        ))
        db.send_create_signal(u'categorizacion', ['LsrDigital'])

        # Adding model 'LsrFisico'
        db.create_table(u'categorizacion_lsrfisico', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Sucursales'])),
            ('solicitud_libro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.SolicitudLibro'])),
            ('identificador', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'categorizacion', ['LsrFisico'])

        # Adding model 'Notificacion'
        db.create_table(u'categorizacion_notificacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emisor', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'notificacion_tiene_emisor', to=orm['cuentas.MinturUser'])),
            ('receptor', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'notificacion_tiene_receptor', to=orm['cuentas.MinturUser'])),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Solicitud'])),
            ('asunto', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('observacion', self.gf('django.db.models.fields.TextField')(default=u'No se han registrado observaciones', blank=True)),
            ('fecha_emision', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('estatus_actual', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'estatus_actual', to=orm['categorizacion.Estatus'])),
        ))
        db.send_create_signal(u'categorizacion', ['Notificacion'])

        # Adding model 'NotificacionBackup'
        db.create_table(u'categorizacion_notificacionbackup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emisor', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'notificacion_backup_emisor', to=orm['cuentas.MinturUser'])),
            ('receptor', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'notificacion_backup_receptor', to=orm['cuentas.MinturUser'])),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Solicitud'])),
            ('asunto', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('observacion', self.gf('django.db.models.fields.TextField')(default=u'No se han registrado observaciones', blank=True)),
            ('fecha_emision', self.gf('django.db.models.fields.DateTimeField')()),
            ('estatus_actual', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'estatus_backup_actual', to=orm['categorizacion.Estatus'])),
        ))
        db.send_create_signal(u'categorizacion', ['NotificacionBackup'])

        # Adding model 'NotificacionDocumentoCompuesto'
        db.create_table(u'categorizacion_notificaciondocumentocompuesto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notificacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Notificacion'], null=True, blank=True)),
            ('documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Documento'])),
            ('notificacion_backup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.NotificacionBackup'], null=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['NotificacionDocumentoCompuesto'])

        # Adding model 'ObservacionGeneral'
        db.create_table(u'categorizacion_observaciongeneral', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Funcionario'])),
            ('observacion', self.gf('django.db.models.fields.TextField')()),
            ('aspecto_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.AspectoFundamentalConfig'], null=True)),
        ))
        db.send_create_signal(u'categorizacion', ['ObservacionGeneral'])

        # Adding model 'PadreTipo'
        db.create_table(u'categorizacion_padretipo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.TipoPst'])),
            ('clasificacion_padre_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ClasificacionPadrePst'])),
        ))
        db.send_create_signal(u'categorizacion', ['PadreTipo'])

        # Adding model 'PstCategoriaDocumentoCompuesto'
        db.create_table(u'categorizacion_pstcategoriadocumentocompuesto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Categoria'])),
            ('documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Documento'], unique=True)),
            ('fecha_categorizacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('calificacion', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'categorizacion', ['PstCategoriaDocumentoCompuesto'])

        # Adding model 'RequisitoDigital'
        db.create_table(u'categorizacion_requisitodigital', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Solicitud'])),
            ('file_path', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=255, null=True, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, blank=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_carga', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['RequisitoDigital'])

        # Adding model 'RequisitosPago'
        db.create_table(u'categorizacion_requisitospago', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.SolicitudLibro'])),
            ('tipo_requisito_pago', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoRequisitoPago'])),
            ('file_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_carga', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['RequisitosPago'])

        # Adding model 'RespuestaLsr'
        db.create_table(u'categorizacion_respuestalsr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('comentario', self.gf('django.db.models.fields.TextField')()),
            ('entrada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Entrada'])),
        ))
        db.send_create_signal(u'categorizacion', ['RespuestaLsr'])

        # Adding model 'RespuestaTabulador'
        db.create_table(u'categorizacion_respuestatabulador', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('tabulador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Tabulador'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('solicitud', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Solicitud'])),
        ))
        db.send_create_signal(u'categorizacion', ['RespuestaTabulador'])

        # Adding model 'SolicitudLibro'
        db.create_table(u'categorizacion_solicitudlibro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estatus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Estatus'])),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pst_genera_solicitudes_de_libros', to=orm['registro.Pst'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Sucursales'])),
            ('oficina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.OficinaRegional'])),
            ('fecha_realizacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'funcionarioLSR', null=True, to=orm['categorizacion.Funcionario'])),
            ('numero_comprobante', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('archivo_comprobante', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=255, null=True)),
        ))
        db.send_create_signal(u'categorizacion', ['SolicitudLibro'])

        # Adding model 'SeccionConfig'
        db.create_table(u'categorizacion_seccionconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('aspecto_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.AspectoFundamentalConfig'])),
            ('seccion_padre_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.SeccionConfig'], null=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['SeccionConfig'])

        # Adding model 'Subseccion'
        db.create_table(u'categorizacion_subseccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('observacion', self.gf('django.db.models.fields.TextField')(default=u'No se han registrado observaciones')),
            ('tipo_subseccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoSubseccion'])),
            ('subseccion_config', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'subseccion_config_id', to=orm['categorizacion.SubseccionConfig'])),
            ('respuesta_tabulador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.RespuestaTabulador'])),
        ))
        db.send_create_signal(u'categorizacion', ['Subseccion'])

        # Adding model 'SubseccionConfig'
        db.create_table(u'categorizacion_subseccionconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('seccion_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.SeccionConfig'])),
            ('tipo_subseccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoSubseccion'])),
            ('respuesta_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.RespuestaConfig'])),
            ('subseccion_config_padre', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'subseccion_config_tiene_subseccion_padre_config_id', null=True, to=orm['categorizacion.SubseccionConfig'])),
        ))
        db.send_create_signal(u'categorizacion', ['SubseccionConfig'])

        # Adding model 'SubseccionArchivoRequisito'
        db.create_table(u'categorizacion_subseccionarchivorequisito', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subseccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Subseccion'])),
            ('requisito_digital', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.RequisitoDigital'])),
        ))
        db.send_create_signal(u'categorizacion', ['SubseccionArchivoRequisito'])

        # Adding model 'Tabulador'
        db.create_table(u'categorizacion_tabulador', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ClasificacionPadrePst'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_column=u'fecha_creacion', blank=True)),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('version_actual', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'categorizacion', ['Tabulador'])

        # Adding model 'Turista'
        db.create_table(u'categorizacion_turista', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('correo_electronico', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('ciudad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Ciudad'], null=True, blank=True)),
            ('telefono_contacto', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero_documento_identidad', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('tipo_documento_identidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoDocumentoIdentidad'], null=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['Turista'])

        # Adding model 'OficinaRegional'
        db.create_table(u'categorizacion_oficinaregional', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Municipio'])),
            ('direccion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'categorizacion', ['OficinaRegional'])

        # Adding model 'RespuestaConfig'
        db.create_table(u'categorizacion_respuestaconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tipo_respuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoRespuesta'])),
            ('tipo_medida', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.TipoMedida'], null=True, blank=True)),
        ))
        db.send_create_signal(u'categorizacion', ['RespuestaConfig'])

        # Adding model 'RespuestaValorRespuesta'
        db.create_table(u'categorizacion_respuestavalorrespuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pregunta_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.RespuestaConfig'])),
            ('respuesta_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ValorRespuestaConfig'])),
        ))
        db.send_create_signal(u'categorizacion', ['RespuestaValorRespuesta'])

        # Adding model 'ValorRespuestaConfig'
        db.create_table(u'categorizacion_valorrespuestaconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('puntaje', self.gf('django.db.models.fields.FloatField')()),
            ('limite_inferior', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('limite_superior', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('respuesta_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.RespuestaConfig'])),
        ))
        db.send_create_signal(u'categorizacion', ['ValorRespuestaConfig'])

        # Adding model 'ValorRespuesta'
        db.create_table(u'categorizacion_valorrespuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True, blank=True)),
            ('subseccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.Subseccion'])),
            ('valor_respuesta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categorizacion.ValorRespuestaConfig'])),
        ))
        db.send_create_signal(u'categorizacion', ['ValorRespuesta'])


    def backwards(self, orm):
        # Removing unique constraint on 'Funcionario', fields ['user', 'direccion']
        db.delete_unique(u'categorizacion_funcionario', ['user_id', 'direccion_id'])

        # Deleting model 'TipoMedida'
        db.delete_table(u'categorizacion_tipomedida')

        # Deleting model 'TipoRespuesta'
        db.delete_table(u'categorizacion_tiporespuesta')

        # Deleting model 'Direccion'
        db.delete_table(u'categorizacion_direccion')

        # Deleting model 'Categoria'
        db.delete_table(u'categorizacion_categoria')

        # Deleting model 'ClasificacionPadrePst'
        db.delete_table(u'categorizacion_clasificacionpadrepst')

        # Deleting model 'TipoMotivo'
        db.delete_table(u'categorizacion_tipomotivo')

        # Deleting model 'ParametroConfiguracion'
        db.delete_table(u'categorizacion_parametroconfiguracion')

        # Deleting model 'PlantillaDocumento'
        db.delete_table(u'categorizacion_plantilladocumento')

        # Deleting model 'TipoAsignacion'
        db.delete_table(u'categorizacion_tipoasignacion')

        # Deleting model 'TipoComentario'
        db.delete_table(u'categorizacion_tipocomentario')

        # Deleting model 'TipoDocumentoIdentidad'
        db.delete_table(u'categorizacion_tipodocumentoidentidad')

        # Deleting model 'TipoRequisitoPago'
        db.delete_table(u'categorizacion_tiporequisitopago')

        # Deleting model 'TipoRol'
        db.delete_table(u'categorizacion_tiporol')

        # Deleting model 'TipoSolicitud'
        db.delete_table(u'categorizacion_tiposolicitud')

        # Deleting model 'TipoSubseccion'
        db.delete_table(u'categorizacion_tiposubseccion')

        # Deleting model 'Solicitud'
        db.delete_table(u'categorizacion_solicitud')

        # Deleting model 'HistoricoCategorizacion'
        db.delete_table(u'categorizacion_historicocategorizacion')

        # Deleting model 'AreaNoCompletada'
        db.delete_table(u'categorizacion_areanocompletada')

        # Deleting model 'Asignacion'
        db.delete_table(u'categorizacion_asignacion')

        # Deleting model 'AspectoFundamental'
        db.delete_table(u'categorizacion_aspectofundamental')

        # Deleting model 'AspectoFundamentalConfig'
        db.delete_table(u'categorizacion_aspectofundamentalconfig')

        # Deleting model 'TipoDocumentoCompuesto'
        db.delete_table(u'categorizacion_tipodocumentocompuesto')

        # Deleting model 'Documento'
        db.delete_table(u'categorizacion_documento')

        # Deleting model 'Estatus'
        db.delete_table(u'categorizacion_estatus')

        # Deleting model 'Folio'
        db.delete_table(u'categorizacion_folio')

        # Deleting model 'Funcionario'
        db.delete_table(u'categorizacion_funcionario')

        # Deleting model 'Entrada'
        db.delete_table(u'categorizacion_entrada')

        # Deleting model 'SeccionEncuesta'
        db.delete_table(u'categorizacion_seccionencuesta')

        # Deleting model 'Encuesta'
        db.delete_table(u'categorizacion_encuesta')

        # Deleting model 'ElementoEncuestaSeccionEncuesta'
        db.delete_table(u'categorizacion_elementoencuestaseccionencuesta')

        # Deleting model 'ElementoEncuesta'
        db.delete_table(u'categorizacion_elementoencuesta')

        # Deleting model 'RespuestaEncuesta'
        db.delete_table(u'categorizacion_respuestaencuesta')

        # Deleting model 'Valoracion'
        db.delete_table(u'categorizacion_valoracion')

        # Deleting model 'ValoracionConfig'
        db.delete_table(u'categorizacion_valoracionconfig')

        # Deleting model 'Severidad'
        db.delete_table(u'categorizacion_severidad')

        # Deleting model 'LsrDigital'
        db.delete_table(u'categorizacion_lsrdigital')

        # Deleting model 'LsrFisico'
        db.delete_table(u'categorizacion_lsrfisico')

        # Deleting model 'Notificacion'
        db.delete_table(u'categorizacion_notificacion')

        # Deleting model 'NotificacionBackup'
        db.delete_table(u'categorizacion_notificacionbackup')

        # Deleting model 'NotificacionDocumentoCompuesto'
        db.delete_table(u'categorizacion_notificaciondocumentocompuesto')

        # Deleting model 'ObservacionGeneral'
        db.delete_table(u'categorizacion_observaciongeneral')

        # Deleting model 'PadreTipo'
        db.delete_table(u'categorizacion_padretipo')

        # Deleting model 'PstCategoriaDocumentoCompuesto'
        db.delete_table(u'categorizacion_pstcategoriadocumentocompuesto')

        # Deleting model 'RequisitoDigital'
        db.delete_table(u'categorizacion_requisitodigital')

        # Deleting model 'RequisitosPago'
        db.delete_table(u'categorizacion_requisitospago')

        # Deleting model 'RespuestaLsr'
        db.delete_table(u'categorizacion_respuestalsr')

        # Deleting model 'RespuestaTabulador'
        db.delete_table(u'categorizacion_respuestatabulador')

        # Deleting model 'SolicitudLibro'
        db.delete_table(u'categorizacion_solicitudlibro')

        # Deleting model 'SeccionConfig'
        db.delete_table(u'categorizacion_seccionconfig')

        # Deleting model 'Subseccion'
        db.delete_table(u'categorizacion_subseccion')

        # Deleting model 'SubseccionConfig'
        db.delete_table(u'categorizacion_subseccionconfig')

        # Deleting model 'SubseccionArchivoRequisito'
        db.delete_table(u'categorizacion_subseccionarchivorequisito')

        # Deleting model 'Tabulador'
        db.delete_table(u'categorizacion_tabulador')

        # Deleting model 'Turista'
        db.delete_table(u'categorizacion_turista')

        # Deleting model 'OficinaRegional'
        db.delete_table(u'categorizacion_oficinaregional')

        # Deleting model 'RespuestaConfig'
        db.delete_table(u'categorizacion_respuestaconfig')

        # Deleting model 'RespuestaValorRespuesta'
        db.delete_table(u'categorizacion_respuestavalorrespuesta')

        # Deleting model 'ValorRespuestaConfig'
        db.delete_table(u'categorizacion_valorrespuestaconfig')

        # Deleting model 'ValorRespuesta'
        db.delete_table(u'categorizacion_valorrespuesta')


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
        u'categorizacion.areanocompletada': {
            'Meta': {'object_name': 'AreaNoCompletada'},
            'historico_categorizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.HistoricoCategorizacion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.asignacion': {
            'Meta': {'object_name': 'Asignacion'},
            'asignacion_habilitada': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha_asignacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']", 'null': 'True'}),
            'solicitud_libro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']", 'null': 'True'}),
            'tipo_asignacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoAsignacion']"})
        },
        u'categorizacion.aspectofundamental': {
            'Meta': {'object_name': 'AspectoFundamental'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'respuesta_tabulador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaTabulador']"})
        },
        u'categorizacion.aspectofundamentalconfig': {
            'Meta': {'object_name': 'AspectoFundamentalConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tabulador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"})
        },
        u'categorizacion.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'clasificacion_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ClasificacionPadrePst']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'valor': ('django.db.models.fields.IntegerField', [], {})
        },
        u'categorizacion.clasificacionpadrepst': {
            'Meta': {'object_name': 'ClasificacionPadrePst'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fecha_aprobacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'plantilla_documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.PlantillaDocumento']"}),
            'ruta_documento': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tipo_documento_compuesto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoDocumentoCompuesto']", 'null': 'True'})
        },
        u'categorizacion.elementoencuesta': {
            'Meta': {'object_name': 'ElementoEncuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.elementoencuestaseccionencuesta': {
            'Meta': {'object_name': 'ElementoEncuestaSeccionEncuesta'},
            'elemento_encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ElementoEncuesta']"}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Encuesta']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seccion_encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SeccionEncuesta']"})
        },
        u'categorizacion.encuesta': {
            'Meta': {'object_name': 'Encuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.TipoPst']"})
        },
        u'categorizacion.entrada': {
            'Meta': {'object_name': 'Entrada'},
            'comentario': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'related_forced_name_again'", 'null': 'True', 'blank': 'True', 'to': u"orm['categorizacion.Encuesta']"}),
            'es_anonimo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estatus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'fecha_entrada': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lsr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.LsrDigital']"}),
            'severidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Severidad']", 'null': 'True', 'blank': 'True'}),
            'tipo_comentario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoComentario']"}),
            'turista': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Turista']"})
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
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_path': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lsr_fisico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.LsrFisico']"}),
            'numero': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255'})
        },
        u'categorizacion.funcionario': {
            'Meta': {'unique_together': "((u'user', u'direccion'),)", 'object_name': 'Funcionario'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'direccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Direccion']"}),
            'habilitado': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tiporol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoRol']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'categorizacion.historicocategorizacion': {
            'Meta': {'object_name': 'HistoricoCategorizacion'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cedula': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'fecha_ingreso_historico': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_inicio_solicitud': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoMotivo']"}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rtn': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.TipoPst']"})
        },
        u'categorizacion.lsrdigital': {
            'Meta': {'object_name': 'LsrDigital'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True'})
        },
        u'categorizacion.lsrfisico': {
            'Meta': {'object_name': 'LsrFisico'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificador': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'solicitud_libro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']"}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']"})
        },
        u'categorizacion.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'asunto': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emisor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'notificacion_tiene_emisor'", 'to': u"orm['cuentas.MinturUser']"}),
            'estatus_actual': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'estatus_actual'", 'to': u"orm['categorizacion.Estatus']"}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'", 'blank': 'True'}),
            'receptor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'notificacion_tiene_receptor'", 'to': u"orm['cuentas.MinturUser']"}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"})
        },
        u'categorizacion.notificacionbackup': {
            'Meta': {'object_name': 'NotificacionBackup'},
            'asunto': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emisor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'notificacion_backup_emisor'", 'to': u"orm['cuentas.MinturUser']"}),
            'estatus_actual': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'estatus_backup_actual'", 'to': u"orm['categorizacion.Estatus']"}),
            'fecha_emision': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'", 'blank': 'True'}),
            'receptor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'notificacion_backup_receptor'", 'to': u"orm['cuentas.MinturUser']"}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"})
        },
        u'categorizacion.notificaciondocumentocompuesto': {
            'Meta': {'object_name': 'NotificacionDocumentoCompuesto'},
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Documento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notificacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Notificacion']", 'null': 'True', 'blank': 'True'}),
            'notificacion_backup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.NotificacionBackup']", 'null': 'True', 'blank': 'True'})
        },
        u'categorizacion.observaciongeneral': {
            'Meta': {'object_name': 'ObservacionGeneral'},
            'aspecto_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.AspectoFundamentalConfig']", 'null': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {})
        },
        u'categorizacion.oficinaregional': {
            'Meta': {'object_name': 'OficinaRegional'},
            'direccion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'categorizacion.padretipo': {
            'Meta': {'object_name': 'PadreTipo'},
            'clasificacion_padre_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ClasificacionPadrePst']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.TipoPst']"})
        },
        u'categorizacion.parametroconfiguracion': {
            'Meta': {'object_name': 'ParametroConfiguracion'},
            'clave': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valor': ('django.db.models.fields.TextField', [], {'max_length': '2048'})
        },
        u'categorizacion.plantilladocumento': {
            'Meta': {'object_name': 'PlantillaDocumento'},
            'formato': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'categorizacion.pstcategoriadocumentocompuesto': {
            'Meta': {'object_name': 'PstCategoriaDocumentoCompuesto'},
            'calificacion': ('django.db.models.fields.IntegerField', [], {}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Categoria']"}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Documento']", 'unique': 'True'}),
            'fecha_categorizacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'categorizacion.requisitodigital': {
            'Meta': {'object_name': 'RequisitoDigital'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_path': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"})
        },
        u'categorizacion.requisitospago': {
            'Meta': {'object_name': 'RequisitosPago'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fecha_carga': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SolicitudLibro']"}),
            'tipo_requisito_pago': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoRequisitoPago']"})
        },
        u'categorizacion.respuestaconfig': {
            'Meta': {'object_name': 'RespuestaConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_medida': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoMedida']", 'null': 'True', 'blank': 'True'}),
            'tipo_respuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoRespuesta']"})
        },
        u'categorizacion.respuestaencuesta': {
            'Meta': {'object_name': 'RespuestaEncuesta'},
            'elemento_encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ElementoEncuesta']"}),
            'entrada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Entrada']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'valoracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Valoracion']"})
        },
        u'categorizacion.respuestalsr': {
            'Meta': {'object_name': 'RespuestaLsr'},
            'comentario': ('django.db.models.fields.TextField', [], {}),
            'emisor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'entrada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Entrada']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'categorizacion.respuestatabulador': {
            'Meta': {'object_name': 'RespuestaTabulador'},
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Solicitud']"}),
            'tabulador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"})
        },
        u'categorizacion.respuestavalorrespuesta': {
            'Meta': {'object_name': 'RespuestaValorRespuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pregunta_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"}),
            'respuesta_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ValorRespuestaConfig']"})
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
            'estatus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'fecha_apertura': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_clausura': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_modificacion_estado': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'funcionario'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            'funcionario_extra': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'funcionario_extra'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permitir_prorroga': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pst_genera_solicitudes_de_categorizacion'", 'to': u"orm['registro.Pst']"}),
            'pst_categoria_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.PstCategoriaDocumentoCompuesto']", 'null': 'True', 'blank': 'True'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']", 'null': 'True'}),
            'tabulador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Tabulador']"})
        },
        u'categorizacion.solicitudlibro': {
            'Meta': {'object_name': 'SolicitudLibro'},
            'archivo_comprobante': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '255', 'null': 'True'}),
            'estatus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Estatus']"}),
            'fecha_realizacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'funcionarioLSR'", 'null': 'True', 'to': u"orm['categorizacion.Funcionario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_comprobante': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'oficina': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.OficinaRegional']"}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pst_genera_solicitudes_de_libros'", 'to': u"orm['registro.Pst']"}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Sucursales']"})
        },
        u'categorizacion.subseccion': {
            'Meta': {'object_name': 'Subseccion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'observacion': ('django.db.models.fields.TextField', [], {'default': "u'No se han registrado observaciones'"}),
            'respuesta_tabulador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaTabulador']"}),
            'subseccion_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'subseccion_config_id'", 'to': u"orm['categorizacion.SubseccionConfig']"}),
            'tipo_subseccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoSubseccion']"})
        },
        u'categorizacion.subseccionarchivorequisito': {
            'Meta': {'object_name': 'SubseccionArchivoRequisito'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requisito_digital': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RequisitoDigital']"}),
            'subseccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Subseccion']"})
        },
        u'categorizacion.subseccionconfig': {
            'Meta': {'object_name': 'SubseccionConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'respuesta_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"}),
            'seccion_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.SeccionConfig']"}),
            'subseccion_config_padre': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'subseccion_config_tiene_subseccion_padre_config_id'", 'null': 'True', 'to': u"orm['categorizacion.SubseccionConfig']"}),
            'tipo_subseccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.TipoSubseccion']"})
        },
        u'categorizacion.tabulador': {
            'Meta': {'object_name': 'Tabulador'},
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "u'fecha_creacion'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo_pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ClasificacionPadrePst']"}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'version_actual': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'categorizacion.tipoasignacion': {
            'Meta': {'object_name': 'TipoAsignacion'},
            'abreviacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'categorizacion.tipomedida': {
            'Meta': {'object_name': 'TipoMedida'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'categorizacion.tipomotivo': {
            'Meta': {'object_name': 'TipoMotivo'},
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
            'puntaje': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'})
        },
        u'categorizacion.valoracionconfig': {
            'Meta': {'object_name': 'ValoracionConfig'},
            'elemento_encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ElementoEncuesta']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valoracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Valoracion']"})
        },
        u'categorizacion.valorrespuesta': {
            'Meta': {'object_name': 'ValorRespuesta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subseccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.Subseccion']"}),
            'valor': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'valor_respuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.ValorRespuestaConfig']"})
        },
        u'categorizacion.valorrespuestaconfig': {
            'Meta': {'object_name': 'ValorRespuestaConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limite_inferior': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'limite_superior': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'puntaje': ('django.db.models.fields.FloatField', [], {}),
            'respuesta_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categorizacion.RespuestaConfig']"})
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