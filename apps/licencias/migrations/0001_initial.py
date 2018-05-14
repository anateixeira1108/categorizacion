# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArchivoRecaudo'
        db.create_table(u'licencias_archivorecaudo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ruta', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_carga', self.gf('django.db.models.fields.DateTimeField')()),
            ('recaudoid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.Recaudo'], db_column=u'recaudoid')),
            ('solicitud_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudLicencia'], db_column=u'solicitud_licenciaid')),
            ('certificado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'licencias', ['ArchivoRecaudo'])

        # Adding model 'ArchivoRespuesta'
        db.create_table(u'licencias_archivorespuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ruta', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'licencias', ['ArchivoRespuesta'])

        # Adding model 'EstatusSolicitud'
        db.create_table(u'licencias_estatussolicitud', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('clase', self.gf('django.db.models.fields.CharField')(default=u'label-warning', max_length=255)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'licencias', ['EstatusSolicitud'])

        # Adding model 'ValorPosible'
        db.create_table(u'licencias_valorposible', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'licencias', ['ValorPosible'])

        # Adding model 'TipoRespuesta'
        db.create_table(u'licencias_tiporespuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'licencias', ['TipoRespuesta'])

        # Adding model 'Pregunta'
        db.create_table(u'licencias_pregunta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tipo_respuestaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.TipoRespuesta'], db_column=u'tipo_respuestaid')),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'licencias', ['Pregunta'])

        # Adding M2M table for field valoresPosibles on 'Pregunta'
        m2m_table_name = db.shorten_name(u'licencias_pregunta_valoresPosibles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pregunta', models.ForeignKey(orm[u'licencias.pregunta'], null=False)),
            ('valorposible', models.ForeignKey(orm[u'licencias.valorposible'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pregunta_id', 'valorposible_id'])

        # Adding model 'Formulario'
        db.create_table(u'licencias_formulario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'licencias', ['Formulario'])

        # Adding M2M table for field preguntas on 'Formulario'
        m2m_table_name = db.shorten_name(u'licencias_formulario_preguntas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formulario', models.ForeignKey(orm[u'licencias.formulario'], null=False)),
            ('pregunta', models.ForeignKey(orm[u'licencias.pregunta'], null=False))
        ))
        db.create_unique(m2m_table_name, ['formulario_id', 'pregunta_id'])

        # Adding model 'HistoricoSolicitudesLicencias'
        db.create_table(u'licencias_historicosolicitudeslicencias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solicitud_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudLicencia'], db_column=u'solicitud_licenciaid')),
            ('usuariomodificar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')()),
            ('estatus_solicitudid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.EstatusSolicitud'], db_column=u'estatus_solicitudid')),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'licencias', ['HistoricoSolicitudesLicencias'])

        # Adding model 'Inspeccion'
        db.create_table(u'licencias_inspeccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')()),
            ('fecha_inspeccion', self.gf('django.db.models.fields.DateTimeField')()),
            ('solicitud_inspeccionid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudInspeccion'], db_column=u'solicitud_inspeccionid')),
            ('estado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tipo_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.TipoLicencia'], db_column=u'tipo_licenciaid')),
        ))
        db.send_create_signal(u'licencias', ['Inspeccion'])

        # Adding M2M table for field inspectores on 'Inspeccion'
        m2m_table_name = db.shorten_name(u'licencias_inspeccion_inspectores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('inspeccion', models.ForeignKey(orm[u'licencias.inspeccion'], null=False)),
            ('minturuser', models.ForeignKey(orm[u'cuentas.minturuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['inspeccion_id', 'minturuser_id'])

        # Adding model 'Notificacion'
        db.create_table(u'licencias_notificacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asunto', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fecha_emision', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('solicitud_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudLicencia'], db_column=u'solicitud_licenciaid')),
            ('estatus_solicitudid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.EstatusSolicitud'], db_column=u'estatus_solicitudid')),
            ('emisor', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'emisor', to=orm['cuentas.MinturUser'])),
            ('receptor', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'receptor', to=orm['cuentas.MinturUser'])),
            ('indicador', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'licencias', ['Notificacion'])

        # Adding model 'Recaudo'
        db.create_table(u'licencias_recaudo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('requerido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sucursal', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'licencias', ['Recaudo'])

        # Adding model 'Respuesta'
        db.create_table(u'licencias_respuesta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solicitud_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudLicencia'], null=True, db_column=u'solicitud_licenciaid', blank=True)),
            ('inspeccionid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.Inspeccion'], null=True, db_column=u'inspeccionid', blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('auth_userid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
        ))
        db.send_create_signal(u'licencias', ['Respuesta'])

        # Adding model 'RespuestaDefinida'
        db.create_table(u'licencias_respuestadefinida', (
            (u'respuesta_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['licencias.Respuesta'], unique=True, primary_key=True)),
            ('respuesta_descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'licencias', ['RespuestaDefinida'])

        # Adding model 'RespuestaIndefinida'
        db.create_table(u'licencias_respuestaindefinida', (
            (u'respuesta_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['licencias.Respuesta'], unique=True, primary_key=True)),
            ('archivo_respuestaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.ArchivoRespuesta'], db_column=u'archivo_respuestaid')),
            ('respuesta', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'licencias', ['RespuestaIndefinida'])

        # Adding model 'SolicitudInspeccion'
        db.create_table(u'licencias_solicitudinspeccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solicitud_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.SolicitudLicencia'], db_column=u'solicitud_licenciaid')),
            ('estado', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('auth_userid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('tipo_usuario', self.gf('django.db.models.fields.BooleanField')()),
            ('fecha_solicitud', self.gf('django.db.models.fields.DateTimeField')()),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'licencias', ['SolicitudInspeccion'])

        # Adding model 'SolicitudLicencia'
        db.create_table(u'licencias_solicitudlicencia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateTimeField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tipo_licenciaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.TipoLicencia'], db_column=u'tipo_licenciaid')),
            ('estatus_solicitudid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.EstatusSolicitud'], db_column=u'estatus_solicitudid')),
            ('tipo_solicitudid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.TipoSolicitud'], db_column=u'tipo_solicitudid')),
            ('edicion', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('usuario_pst_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'Upst', to=orm['cuentas.MinturUser'])),
            ('analista_asignado', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'analista', null=True, to=orm['cuentas.MinturUser'])),
            ('result_inspeccion', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'licencias', ['SolicitudLicencia'])

        # Adding model 'TipoLicencia'
        db.create_table(u'licencias_tipolicencia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('padre', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'tipo_padre_id', null=True, to=orm['licencias.TipoLicencia'])),
            ('formulario_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.Formulario'], db_column=u'formulario_id')),
        ))
        db.send_create_signal(u'licencias', ['TipoLicencia'])

        # Adding M2M table for field recaudos on 'TipoLicencia'
        m2m_table_name = db.shorten_name(u'licencias_tipolicencia_recaudos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tipolicencia', models.ForeignKey(orm[u'licencias.tipolicencia'], null=False)),
            ('recaudo', models.ForeignKey(orm[u'licencias.recaudo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tipolicencia_id', 'recaudo_id'])

        # Adding model 'TipoSolicitud'
        db.create_table(u'licencias_tiposolicitud', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'licencias', ['TipoSolicitud'])

        # Adding model 'ValoresRdefinida'
        db.create_table(u'licencias_valoresrdefinida', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor_posibleid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.ValorPosible'], db_column=u'valor_posibleid')),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('respuesta_definida', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.RespuestaDefinida'], db_column=u'respuesta_definidarespuesta')),
            ('archivo_respuestaid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licencias.ArchivoRespuesta'], db_column=u'archivo_respuestaid')),
        ))
        db.send_create_signal(u'licencias', ['ValoresRdefinida'])


    def backwards(self, orm):
        # Deleting model 'ArchivoRecaudo'
        db.delete_table(u'licencias_archivorecaudo')

        # Deleting model 'ArchivoRespuesta'
        db.delete_table(u'licencias_archivorespuesta')

        # Deleting model 'EstatusSolicitud'
        db.delete_table(u'licencias_estatussolicitud')

        # Deleting model 'ValorPosible'
        db.delete_table(u'licencias_valorposible')

        # Deleting model 'TipoRespuesta'
        db.delete_table(u'licencias_tiporespuesta')

        # Deleting model 'Pregunta'
        db.delete_table(u'licencias_pregunta')

        # Removing M2M table for field valoresPosibles on 'Pregunta'
        db.delete_table(db.shorten_name(u'licencias_pregunta_valoresPosibles'))

        # Deleting model 'Formulario'
        db.delete_table(u'licencias_formulario')

        # Removing M2M table for field preguntas on 'Formulario'
        db.delete_table(db.shorten_name(u'licencias_formulario_preguntas'))

        # Deleting model 'HistoricoSolicitudesLicencias'
        db.delete_table(u'licencias_historicosolicitudeslicencias')

        # Deleting model 'Inspeccion'
        db.delete_table(u'licencias_inspeccion')

        # Removing M2M table for field inspectores on 'Inspeccion'
        db.delete_table(db.shorten_name(u'licencias_inspeccion_inspectores'))

        # Deleting model 'Notificacion'
        db.delete_table(u'licencias_notificacion')

        # Deleting model 'Recaudo'
        db.delete_table(u'licencias_recaudo')

        # Deleting model 'Respuesta'
        db.delete_table(u'licencias_respuesta')

        # Deleting model 'RespuestaDefinida'
        db.delete_table(u'licencias_respuestadefinida')

        # Deleting model 'RespuestaIndefinida'
        db.delete_table(u'licencias_respuestaindefinida')

        # Deleting model 'SolicitudInspeccion'
        db.delete_table(u'licencias_solicitudinspeccion')

        # Deleting model 'SolicitudLicencia'
        db.delete_table(u'licencias_solicitudlicencia')

        # Deleting model 'TipoLicencia'
        db.delete_table(u'licencias_tipolicencia')

        # Removing M2M table for field recaudos on 'TipoLicencia'
        db.delete_table(db.shorten_name(u'licencias_tipolicencia_recaudos'))

        # Deleting model 'TipoSolicitud'
        db.delete_table(u'licencias_tiposolicitud')

        # Deleting model 'ValoresRdefinida'
        db.delete_table(u'licencias_valoresrdefinida')


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
            'respuesta': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'respuesta_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['licencias.Respuesta']", 'unique': 'True', 'primary_key': 'True'})
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