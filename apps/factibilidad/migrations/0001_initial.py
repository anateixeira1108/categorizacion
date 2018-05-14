# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Proyecto'
        db.create_table(u'factibilidad_proyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('alojamiento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.UnidadesAlojamiento'], null=True, blank=True)),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Categoria'], null=True, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('monto', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('tipo_proyecto', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tipo_actividad', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tipo_solicitud', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('empleos_directos', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('empleos_indirectos', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('otra_indole', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('otro_aspecto', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('creado_el', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('justificacion', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'factibilidad', ['Proyecto'])

        # Adding model 'DireccionProyecto'
        db.create_table(u'factibilidad_direccionproyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Estado'])),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Municipio'])),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Parroquia'])),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Proyecto'])),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zona_urbana', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('zona_rural', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('zit_mintur', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('parque_nacional', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('superficie', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('tipografia', self.gf('django.db.models.fields.IntegerField')()),
            ('otra_topografia', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vialidad', self.gf('django.db.models.fields.IntegerField')()),
            ('otra_vialidad', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('otro_servicio', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'factibilidad', ['DireccionProyecto'])

        # Adding model 'ServicioProyecto'
        db.create_table(u'factibilidad_servicioproyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Proyecto'])),
            ('servicio_basico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.ServicioBasico'])),
        ))
        db.send_create_signal(u'factibilidad', ['ServicioProyecto'])

        # Adding model 'ServicioBasico'
        db.create_table(u'factibilidad_serviciobasico', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'factibilidad', ['ServicioBasico'])

        # Adding model 'UnidadesAlojamiento'
        db.create_table(u'factibilidad_unidadesalojamiento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('numero_habitaciones', self.gf('django.db.models.fields.IntegerField')()),
            ('numero_apartamentos', self.gf('django.db.models.fields.IntegerField')()),
            ('numero_suites', self.gf('django.db.models.fields.IntegerField')()),
            ('numero_cabanias', self.gf('django.db.models.fields.IntegerField')()),
            ('otro_alojamiento', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'factibilidad', ['UnidadesAlojamiento'])

        # Adding model 'AspectoSocial'
        db.create_table(u'factibilidad_aspectosocial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Proyecto'])),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'factibilidad', ['AspectoSocial'])

        # Adding model 'Indole'
        db.create_table(u'factibilidad_indole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Proyecto'])),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'factibilidad', ['Indole'])

        # Adding model 'UnidadTransporte'
        db.create_table(u'factibilidad_unidadtransporte', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Proyecto'])),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'factibilidad', ['UnidadTransporte'])

        # Adding model 'Categoria'
        db.create_table(u'factibilidad_categoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hotel', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hotel_residencia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('posada', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('posada_familiar', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('parador_turistico', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('balneario', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('campamentos_estancias', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'factibilidad', ['Categoria'])

        # Adding model 'SocioTecnicoProyecto'
        db.create_table(u'factibilidad_sociotecnicoproyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factibilidad.Proyecto'])),
            ('archivo_titulo_propiedad', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_contrato', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_autorizacion', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_uso_turistico', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_memoria_descriptiva', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_presupuesto', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_conformidad_competente', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_factura_proforma', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_visto_bueno', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_factibilidad_economica', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('archivo_conformidad_aval', self.gf('utils.validate_files.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'factibilidad', ['SocioTecnicoProyecto'])


    def backwards(self, orm):
        # Deleting model 'Proyecto'
        db.delete_table(u'factibilidad_proyecto')

        # Deleting model 'DireccionProyecto'
        db.delete_table(u'factibilidad_direccionproyecto')

        # Deleting model 'ServicioProyecto'
        db.delete_table(u'factibilidad_servicioproyecto')

        # Deleting model 'ServicioBasico'
        db.delete_table(u'factibilidad_serviciobasico')

        # Deleting model 'UnidadesAlojamiento'
        db.delete_table(u'factibilidad_unidadesalojamiento')

        # Deleting model 'AspectoSocial'
        db.delete_table(u'factibilidad_aspectosocial')

        # Deleting model 'Indole'
        db.delete_table(u'factibilidad_indole')

        # Deleting model 'UnidadTransporte'
        db.delete_table(u'factibilidad_unidadtransporte')

        # Deleting model 'Categoria'
        db.delete_table(u'factibilidad_categoria')

        # Deleting model 'SocioTecnicoProyecto'
        db.delete_table(u'factibilidad_sociotecnicoproyecto')


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
        u'factibilidad.aspectosocial': {
            'Meta': {'object_name': 'AspectoSocial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Proyecto']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'factibilidad.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'balneario': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campamentos_estancias': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hotel': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hotel_residencia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parador_turistico': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'posada': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'posada_familiar': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'factibilidad.direccionproyecto': {
            'Meta': {'object_name': 'DireccionProyecto'},
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Estado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Municipio']"}),
            'otra_topografia': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'otra_vialidad': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'otro_servicio': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parque_nacional': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venezuela.Parroquia']"}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Proyecto']"}),
            'superficie': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'tipografia': ('django.db.models.fields.IntegerField', [], {}),
            'vialidad': ('django.db.models.fields.IntegerField', [], {}),
            'zit_mintur': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'zona_rural': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'zona_urbana': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'factibilidad.indole': {
            'Meta': {'object_name': 'Indole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Proyecto']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'factibilidad.proyecto': {
            'Meta': {'object_name': 'Proyecto'},
            'alojamiento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.UnidadesAlojamiento']", 'null': 'True', 'blank': 'True'}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Categoria']", 'null': 'True', 'blank': 'True'}),
            'creado_el': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'empleos_directos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'empleos_indirectos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'justificacion': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'monto': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'otra_indole': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'otro_aspecto': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'tipo_actividad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tipo_proyecto': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tipo_solicitud': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"})
        },
        u'factibilidad.serviciobasico': {
            'Meta': {'object_name': 'ServicioBasico'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'factibilidad.servicioproyecto': {
            'Meta': {'object_name': 'ServicioProyecto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Proyecto']"}),
            'servicio_basico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.ServicioBasico']"})
        },
        u'factibilidad.sociotecnicoproyecto': {
            'Meta': {'object_name': 'SocioTecnicoProyecto'},
            'archivo_autorizacion': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_conformidad_aval': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_conformidad_competente': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_contrato': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_factibilidad_economica': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_factura_proforma': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_memoria_descriptiva': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_presupuesto': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_titulo_propiedad': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_uso_turistico': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'archivo_visto_bueno': ('utils.validate_files.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Proyecto']"})
        },
        u'factibilidad.unidadesalojamiento': {
            'Meta': {'object_name': 'UnidadesAlojamiento'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_apartamentos': ('django.db.models.fields.IntegerField', [], {}),
            'numero_cabanias': ('django.db.models.fields.IntegerField', [], {}),
            'numero_habitaciones': ('django.db.models.fields.IntegerField', [], {}),
            'numero_suites': ('django.db.models.fields.IntegerField', [], {}),
            'otro_alojamiento': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'factibilidad.unidadtransporte': {
            'Meta': {'object_name': 'UnidadTransporte'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['factibilidad.Proyecto']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
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

    complete_apps = ['factibilidad']