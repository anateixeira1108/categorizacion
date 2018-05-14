# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cache'
        db.create_table(u'registro_cache', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tabla', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('relacion_id', self.gf('django.db.models.fields.IntegerField')()),
            ('datos_json', self.gf('django.db.models.fields.TextField')()),
            ('fecha_modificacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Cache'])

        # Adding model 'TipoPst'
        db.create_table(u'registro_tipopst', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tipo_persona', self.gf('django.db.models.fields.IntegerField')()),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['TipoPst'])

        # Adding model 'Pst'
        db.create_table(u'registro_pst', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.TipoPst'], null=True, blank=True)),
            ('tipo_figura', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('tipo_juridica', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('cedula', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('rif', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('razon_social', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('denominacion_comercial', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('estado_contribuyente', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('creado_el', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modificado_el', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('pagina_web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('telefono_fijo', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('telefono_celular', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('correo_electronico', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('emprendedor', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tiene_firma_personal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ultima_verificacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ultima_fiscalizacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('inicio_actividad_comercial', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('rtn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('numero_contribuyente', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('archivo_cedula', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_rif', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_pasaporte', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_servicio', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Pst'])

        # Adding model 'Direccion'
        db.create_table(u'registro_direccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Estado'])),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Municipio'])),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Parroquia'])),
            ('urbanizacion', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('avenida_calle', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('edificio', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('oficina_apartamento', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('codigo_postal', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('punto_referencia', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Direccion'])

        # Adding model 'RepresentanteContacto'
        db.create_table(u'registro_representantecontacto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cedula', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('rif', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('cargo_empresa', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('telefono_fijo', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('telefono_celular', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('correo_electronico', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pagina_web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('archivo_cedula', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_rif', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['RepresentanteContacto'])

        # Adding model 'Accionista'
        db.create_table(u'registro_accionista', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cedula', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('rif', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('fecha_incorporacion', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('numero_acciones', self.gf('django.db.models.fields.IntegerField')()),
            ('director', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archivo_cedula', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_rif', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Accionista'])

        # Adding model 'DatoEspecifico'
        db.create_table(u'registro_datoespecifico', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('guia_especializado', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('egresado_instituto', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('nombre_curso', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('presta_servicio', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('primeros_auxilios', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('ciudad_primeros_auxilios', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('anios_experiencia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('titulo_universitario', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('grado_licencia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('certificado_medico', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('fecha_primeros_auxilios', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_vencimiento_licencia', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_vencimiento_certificado', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_curso', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('archivo_certificado', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_licencia', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_curriculum', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_certificado_guia_especializado', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_constancia_curso_primeros_auxilios', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['DatoEspecifico'])

        # Adding model 'Idioma'
        db.create_table(u'registro_idioma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'registro', ['Idioma'])

        # Adding model 'IdiomasPst'
        db.create_table(u'registro_idiomaspst', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idioma', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Idioma'])),
            ('dato_especifico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.DatoEspecifico'])),
            ('lee', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('habla', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('escribe', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'registro', ['IdiomasPst'])

        # Adding model 'Acta'
        db.create_table(u'registro_acta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('circuito_circunscripcion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Circunscripcion'])),
            ('registro_mercantil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.RegistroMercantil'])),
            ('tomo', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('numero_tomo', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('fecha_registro', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('fecha_ultima_asamblea', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('duracion', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('capital_suscrito', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('capital_pagado', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('objetivo_modificacion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tipo_acta', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('motivo_modificacion', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('archivo_acta_constitutiva', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Acta'])

        # Adding model 'Sunacoop'
        db.create_table(u'registro_sunacoop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('numero', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('archivo_comprobante', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Sunacoop'])

        # Adding model 'Circunscripcion'
        db.create_table(u'registro_circunscripcion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'registro', ['Circunscripcion'])

        # Adding model 'RegistroMercantil'
        db.create_table(u'registro_registromercantil', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'registro', ['RegistroMercantil'])

        # Adding model 'CertificacionesPST'
        db.create_table(u'registro_certificacionespst', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('fecha_certificacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('conclusiones_analisis', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('observaciones_analisis', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['CertificacionesPST'])

        # Adding model 'CertificacionRIFTUR'
        db.create_table(u'registro_certificacionriftur', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('fecha_certificacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('numero_comprobante', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('numero_contribuyente', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
        ))
        db.send_create_signal(u'registro', ['CertificacionRIFTUR'])

        # Adding model 'CertificacionRTN'
        db.create_table(u'registro_certificacionrtn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('fecha_certificacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('numero_comprobante', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rtn', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
        ))
        db.send_create_signal(u'registro', ['CertificacionRTN'])

        # Adding model 'Sucursales'
        db.create_table(u'registro_sucursales', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Estado'])),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Municipio'])),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Parroquia'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('urbanizacion', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('avenida_calle', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('edificio', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('oficina_apartamento', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('codigo_postal', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('punto_referencia', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Sucursales'])

        # Adding model 'RegistroPaso'
        db.create_table(u'registro_registropaso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('es_opcional', self.gf('django.db.models.fields.BooleanField')()),
            ('paso', self.gf('django.db.models.fields.IntegerField')()),
            ('proceso', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
        ))
        db.send_create_signal(u'registro', ['RegistroPaso'])

        # Adding model 'SolicitudCambioPerfil'
        db.create_table(u'registro_solicitudcambioperfil', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('fecha_generacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_verificacion', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'registro', ['SolicitudCambioPerfil'])

        # Adding model 'ActividadComercial'
        db.create_table(u'registro_actividadcomercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actividad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.TipoPst'])),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actividad', to=orm['registro.Pst'])),
            ('tipo_actividad', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('licencia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['ActividadComercial'])


    def backwards(self, orm):
        # Deleting model 'Cache'
        db.delete_table(u'registro_cache')

        # Deleting model 'TipoPst'
        db.delete_table(u'registro_tipopst')

        # Deleting model 'Pst'
        db.delete_table(u'registro_pst')

        # Deleting model 'Direccion'
        db.delete_table(u'registro_direccion')

        # Deleting model 'RepresentanteContacto'
        db.delete_table(u'registro_representantecontacto')

        # Deleting model 'Accionista'
        db.delete_table(u'registro_accionista')

        # Deleting model 'DatoEspecifico'
        db.delete_table(u'registro_datoespecifico')

        # Deleting model 'Idioma'
        db.delete_table(u'registro_idioma')

        # Deleting model 'IdiomasPst'
        db.delete_table(u'registro_idiomaspst')

        # Deleting model 'Acta'
        db.delete_table(u'registro_acta')

        # Deleting model 'Sunacoop'
        db.delete_table(u'registro_sunacoop')

        # Deleting model 'Circunscripcion'
        db.delete_table(u'registro_circunscripcion')

        # Deleting model 'RegistroMercantil'
        db.delete_table(u'registro_registromercantil')

        # Deleting model 'CertificacionesPST'
        db.delete_table(u'registro_certificacionespst')

        # Deleting model 'CertificacionRIFTUR'
        db.delete_table(u'registro_certificacionriftur')

        # Deleting model 'CertificacionRTN'
        db.delete_table(u'registro_certificacionrtn')

        # Deleting model 'Sucursales'
        db.delete_table(u'registro_sucursales')

        # Deleting model 'RegistroPaso'
        db.delete_table(u'registro_registropaso')

        # Deleting model 'SolicitudCambioPerfil'
        db.delete_table(u'registro_solicitudcambioperfil')

        # Deleting model 'ActividadComercial'
        db.delete_table(u'registro_actividadcomercial')


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
        u'registro.accionista': {
            'Meta': {'object_name': 'Accionista'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'archivo_cedula': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_rif': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cedula': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'director': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_incorporacion': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numero_acciones': ('django.db.models.fields.IntegerField', [], {}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'registro.acta': {
            'Meta': {'object_name': 'Acta'},
            'archivo_acta_constitutiva': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'capital_pagado': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'capital_suscrito': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'circuito_circunscripcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Circunscripcion']"}),
            'duracion': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fecha_registro': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'fecha_ultima_asamblea': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivo_modificacion': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'numero_tomo': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'objetivo_modificacion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'registro_mercantil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.RegistroMercantil']"}),
            'tipo_acta': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'tomo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'registro.actividadcomercial': {
            'Meta': {'object_name': 'ActividadComercial'},
            'actividad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.TipoPst']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licencia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actividad'", 'to': u"orm['registro.Pst']"}),
            'tipo_actividad': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'registro.cache': {
            'Meta': {'object_name': 'Cache'},
            'datos_json': ('django.db.models.fields.TextField', [], {}),
            'fecha_modificacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relacion_id': ('django.db.models.fields.IntegerField', [], {}),
            'tabla': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registro.certificacionespst': {
            'Meta': {'object_name': 'CertificacionesPST'},
            'conclusiones_analisis': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fecha_certificacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'observaciones_analisis': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'registro.certificacionriftur': {
            'Meta': {'object_name': 'CertificacionRIFTUR'},
            'fecha_certificacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_comprobante': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numero_contribuyente': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'registro.certificacionrtn': {
            'Meta': {'object_name': 'CertificacionRTN'},
            'fecha_certificacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_comprobante': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'rtn': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'registro.circunscripcion': {
            'Meta': {'object_name': 'Circunscripcion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'registro.datoespecifico': {
            'Meta': {'object_name': 'DatoEspecifico'},
            'anios_experiencia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'archivo_certificado': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_certificado_guia_especializado': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_constancia_curso_primeros_auxilios': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_curriculum': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_licencia': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'certificado_medico': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'ciudad_primeros_auxilios': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'egresado_instituto': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fecha_curso': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_primeros_auxilios': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_vencimiento_certificado': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_vencimiento_licencia': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'grado_licencia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'guia_especializado': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idiomas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['registro.Idioma']", 'null': 'True', 'through': u"orm['registro.IdiomasPst']", 'blank': 'True'}),
            'nombre_curso': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'presta_servicio': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'primeros_auxilios': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'titulo_universitario': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        u'registro.direccion': {
            'Meta': {'object_name': 'Direccion'},
            'avenida_calle': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'codigo_postal': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'edificio': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Estado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'oficina_apartamento': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Parroquia']"}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'punto_referencia': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'urbanizacion': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'registro.idioma': {
            'Meta': {'object_name': 'Idioma'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'registro.idiomaspst': {
            'Meta': {'object_name': 'IdiomasPst'},
            'dato_especifico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.DatoEspecifico']"}),
            'escribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'habla': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idioma': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Idioma']"}),
            'lee': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        u'registro.registromercantil': {
            'Meta': {'object_name': 'RegistroMercantil'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'registro.registropaso': {
            'Meta': {'object_name': 'RegistroPaso'},
            'es_opcional': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paso': ('django.db.models.fields.IntegerField', [], {}),
            'proceso': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'registro.representantecontacto': {
            'Meta': {'object_name': 'RepresentanteContacto'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'archivo_cedula': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_rif': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cargo_empresa': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'cedula': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina_web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'telefono_celular': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_fijo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'registro.solicitudcambioperfil': {
            'Meta': {'object_name': 'SolicitudCambioPerfil'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha_generacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_verificacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
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
        u'registro.sunacoop': {
            'Meta': {'object_name': 'Sunacoop'},
            'archivo_comprobante': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'registro.tipopst': {
            'Meta': {'object_name': 'TipoPst'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tipo_persona': ('django.db.models.fields.IntegerField', [], {})
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

    complete_apps = ['registro']