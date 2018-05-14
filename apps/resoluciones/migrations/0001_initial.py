# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Graduacion'
        db.create_table(u'resoluciones_graduacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=26)),
        ))
        db.send_create_signal(u'resoluciones', ['Graduacion'])

        # Adding model 'Ley'
        db.create_table(u'resoluciones_ley', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('siglas', self.gf('django.db.models.fields.CharField')(default='ND', max_length=10)),
        ))
        db.send_create_signal(u'resoluciones', ['Ley'])

        # Adding model 'TipoTributo'
        db.create_table(u'resoluciones_tipotributo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('siglas', self.gf('django.db.models.fields.CharField')(default='ND', max_length=10)),
        ))
        db.send_create_signal(u'resoluciones', ['TipoTributo'])

        # Adding model 'TipoSancion'
        db.create_table(u'resoluciones_tiposancion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'resoluciones', ['TipoSancion'])

        # Adding model 'SubTipoSancion'
        db.create_table(u'resoluciones_subtiposancion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_sancion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.TipoSancion'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'resoluciones', ['SubTipoSancion'])

        # Adding model 'Sancion'
        db.create_table(u'resoluciones_sancion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aplicacion', self.gf('django.db.models.fields.IntegerField')()),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
            ('cot_articulo', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('deber_formal_articulo', self.gf('django.db.models.fields.IntegerField')()),
            ('deber_formal_literal', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('deber_formal_numeral', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('formulario_asociado', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('graduacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.Graduacion'])),
            ('ley', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.Ley'], null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tipo_sancion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.SubTipoSancion'])),
            ('tipo_tributo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.TipoTributo'])),
            ('ut_max', self.gf('django.db.models.fields.IntegerField')()),
            ('ut_min', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'resoluciones', ['Sancion'])

        # Adding model 'TipoResolucion'
        db.create_table(u'resoluciones_tiporesolucion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'resoluciones', ['TipoResolucion'])

        # Adding model 'Resolucion'
        db.create_table(u'resoluciones_resolucion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_resolucion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.TipoResolucion'])),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cuentas.MinturUser'])),
            ('pst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registro.Pst'])),
            ('verificacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['verificacion.Verificacion'], null=True, blank=True)),
            ('numero_documento', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('fecha_expedicion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.CharField')(default='Elaborada', max_length=60)),
            ('valor_ut', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('fecha_notificacion', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'resoluciones', ['Resolucion'])

        # Adding model 'Ilicito'
        db.create_table(u'resoluciones_ilicito', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resolucion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.Resolucion'])),
            ('sancion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resoluciones.Sancion'])),
            ('declaracion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['declaraciones.Declaracion'], null=True, blank=True)),
            ('periodo', self.gf('django.db.models.fields.DateField')()),
            ('fecha_limite_declaracion', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('valor_ut', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('sancion_ut', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'resoluciones', ['Ilicito'])


    def backwards(self, orm):
        # Deleting model 'Graduacion'
        db.delete_table(u'resoluciones_graduacion')

        # Deleting model 'Ley'
        db.delete_table(u'resoluciones_ley')

        # Deleting model 'TipoTributo'
        db.delete_table(u'resoluciones_tipotributo')

        # Deleting model 'TipoSancion'
        db.delete_table(u'resoluciones_tiposancion')

        # Deleting model 'SubTipoSancion'
        db.delete_table(u'resoluciones_subtiposancion')

        # Deleting model 'Sancion'
        db.delete_table(u'resoluciones_sancion')

        # Deleting model 'TipoResolucion'
        db.delete_table(u'resoluciones_tiporesolucion')

        # Deleting model 'Resolucion'
        db.delete_table(u'resoluciones_resolucion')

        # Deleting model 'Ilicito'
        db.delete_table(u'resoluciones_ilicito')


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
        u'declaraciones.declaracion': {
            'Meta': {'object_name': 'Declaracion'},
            'anticipo_declaracion': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['declaraciones.Declaracion']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'compensacion_adquiridos': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'compensacion_propios': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'concepto_pago': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagos.Concepto']", 'null': 'True', 'blank': 'True'}),
            'contribucion_especial_determinada': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fecha_desde': ('django.db.models.fields.DateField', [], {}),
            'fecha_hasta': ('django.db.models.fields.DateField', [], {}),
            'fecha_presentacion': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingresos_extraterritorial': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'justificacion_funcionario': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'justificacion_pst': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'periodo': ('django.db.models.fields.DateField', [], {}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'tipo_declaracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['declaraciones.TipoDeclaracion']"}),
            'total_compensacion': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'total_extraterritorial': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'total_pagar': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'total_ventas_determinacion': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'total_ventas_menos_anticipo': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'total_ventas_territorial': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'ventas_exportacion': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'ventas_internas_adicional': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'ventas_internas_general': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'ventas_internas_reducida': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'}),
            'ventas_propias': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3', 'blank': 'True'})
        },
        u'declaraciones.tipodeclaracion': {
            'Meta': {'object_name': 'TipoDeclaracion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'pagos.concepto': {
            'Meta': {'object_name': 'Concepto'},
            'concepto_tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagos.ConceptoTipo']"}),
            'estatus': ('django.db.models.fields.CharField', [], {'default': "'Pendiente'", 'max_length': '20'}),
            'fecha_generacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'pago': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagos.Pago']", 'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"})
        },
        u'pagos.conceptotipo': {
            'Meta': {'object_name': 'ConceptoTipo'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'pagos.pago': {
            'Meta': {'object_name': 'Pago'},
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'estatus': ('django.db.models.fields.CharField', [], {'default': "'Por Pagar'", 'max_length': '20'}),
            'fecha_generacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_liquidacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_vencimiento': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 22, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_documento': ('django.db.models.fields.CharField', [], {'default': "u'201409180000002'", 'max_length': '20', 'blank': 'True'}),
            'numero_liquidacion': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'porcion': ('django.db.models.fields.CharField', [], {'default': "'\\xc3\\x9aNICO'", 'max_length': '20', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'})
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
        u'resoluciones.graduacion': {
            'Meta': {'object_name': 'Graduacion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '26'})
        },
        u'resoluciones.ilicito': {
            'Meta': {'object_name': 'Ilicito'},
            'declaracion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['declaraciones.Declaracion']", 'null': 'True', 'blank': 'True'}),
            'fecha_limite_declaracion': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodo': ('django.db.models.fields.DateField', [], {}),
            'resolucion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.Resolucion']"}),
            'sancion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.Sancion']"}),
            'sancion_ut': ('django.db.models.fields.IntegerField', [], {}),
            'valor_ut': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'resoluciones.ley': {
            'Meta': {'object_name': 'Ley'},
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'siglas': ('django.db.models.fields.CharField', [], {'default': "'ND'", 'max_length': '10'})
        },
        u'resoluciones.resolucion': {
            'Meta': {'object_name': 'Resolucion'},
            'estatus': ('django.db.models.fields.CharField', [], {'default': "'Elaborada'", 'max_length': '60'}),
            'fecha_expedicion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_notificacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cuentas.MinturUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_documento': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registro.Pst']"}),
            'sanciones': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['resoluciones.Sancion']", 'through': u"orm['resoluciones.Ilicito']", 'symmetrical': 'False'}),
            'tipo_resolucion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.TipoResolucion']"}),
            'valor_ut': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'verificacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['verificacion.Verificacion']", 'null': 'True', 'blank': 'True'})
        },
        u'resoluciones.sancion': {
            'Meta': {'object_name': 'Sancion'},
            'aplicacion': ('django.db.models.fields.IntegerField', [], {}),
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            'cot_articulo': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'deber_formal_articulo': ('django.db.models.fields.IntegerField', [], {}),
            'deber_formal_literal': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'deber_formal_numeral': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'formulario_asociado': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'graduacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.Graduacion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ley': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.Ley']", 'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tipo_sancion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.SubTipoSancion']"}),
            'tipo_tributo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.TipoTributo']"}),
            'ut_max': ('django.db.models.fields.IntegerField', [], {}),
            'ut_min': ('django.db.models.fields.IntegerField', [], {})
        },
        u'resoluciones.subtiposancion': {
            'Meta': {'object_name': 'SubTipoSancion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tipo_sancion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resoluciones.TipoSancion']"})
        },
        u'resoluciones.tiporesolucion': {
            'Meta': {'object_name': 'TipoResolucion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'resoluciones.tiposancion': {
            'Meta': {'object_name': 'TipoSancion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'resoluciones.tipotributo': {
            'Meta': {'object_name': 'TipoTributo'},
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'siglas': ('django.db.models.fields.CharField', [], {'default': "'ND'", 'max_length': '10'})
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

    complete_apps = ['resoluciones']