# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Area'
        db.create_table(u'configuracion_area', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('acronimo', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'configuracion', ['Area'])

        # Adding model 'CalendarioLaboral'
        db.create_table(u'configuracion_calendariolaboral', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'configuracion', ['CalendarioLaboral'])

        # Adding model 'Configuracion'
        db.create_table(u'configuracion_configuracion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('art66cot', self.gf('django.db.models.fields.DecimalField')(default='1.2', max_digits=4, decimal_places=2)),
            ('dias_vencimiento_planilla_pago', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'configuracion', ['Configuracion'])

        # Adding model 'UnidadTributaria'
        db.create_table(u'configuracion_unidadtributaria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('valido_desde', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('valido_hasta', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'configuracion', ['UnidadTributaria'])

        # Adding model 'Horarios'
        db.create_table(u'configuracion_horarios', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valido_desde', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('valido_hasta', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'configuracion', ['Horarios'])

        # Adding model 'Dias'
        db.create_table(u'configuracion_dias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'configuracion', ['Dias'])

        # Adding model 'HorariosAtencion'
        db.create_table(u'configuracion_horariosatencion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('horario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuracion.Horarios'])),
            ('dia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuracion.Dias'])),
            ('desde', self.gf('django.db.models.fields.TimeField')()),
            ('hasta', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'configuracion', ['HorariosAtencion'])

        # Adding model 'TasaInteresBCV'
        db.create_table(u'configuracion_tasainteresbcv', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('periodo', self.gf('django.db.models.fields.DateField')()),
            ('tasa_interes', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
        ))
        db.send_create_signal(u'configuracion', ['TasaInteresBCV'])


    def backwards(self, orm):
        # Deleting model 'Area'
        db.delete_table(u'configuracion_area')

        # Deleting model 'CalendarioLaboral'
        db.delete_table(u'configuracion_calendariolaboral')

        # Deleting model 'Configuracion'
        db.delete_table(u'configuracion_configuracion')

        # Deleting model 'UnidadTributaria'
        db.delete_table(u'configuracion_unidadtributaria')

        # Deleting model 'Horarios'
        db.delete_table(u'configuracion_horarios')

        # Deleting model 'Dias'
        db.delete_table(u'configuracion_dias')

        # Deleting model 'HorariosAtencion'
        db.delete_table(u'configuracion_horariosatencion')

        # Deleting model 'TasaInteresBCV'
        db.delete_table(u'configuracion_tasainteresbcv')


    models = {
        u'configuracion.area': {
            'Meta': {'object_name': 'Area'},
            'acronimo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'configuracion.calendariolaboral': {
            'Meta': {'object_name': 'CalendarioLaboral'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'configuracion.configuracion': {
            'Meta': {'object_name': 'Configuracion'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'art66cot': ('django.db.models.fields.DecimalField', [], {'default': "'1.2'", 'max_digits': '4', 'decimal_places': '2'}),
            'dias_vencimiento_planilla_pago': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'configuracion.dias': {
            'Meta': {'object_name': 'Dias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'configuracion.horarios': {
            'Meta': {'object_name': 'Horarios'},
            'horario_atencion': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['configuracion.Dias']", 'through': u"orm['configuracion.HorariosAtencion']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valido_desde': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'valido_hasta': ('django.db.models.fields.DateField', [], {})
        },
        u'configuracion.horariosatencion': {
            'Meta': {'object_name': 'HorariosAtencion'},
            'desde': ('django.db.models.fields.TimeField', [], {}),
            'dia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['configuracion.Dias']"}),
            'hasta': ('django.db.models.fields.TimeField', [], {}),
            'horario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['configuracion.Horarios']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'configuracion.tasainteresbcv': {
            'Meta': {'object_name': 'TasaInteresBCV'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodo': ('django.db.models.fields.DateField', [], {}),
            'tasa_interes': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
        },
        u'configuracion.unidadtributaria': {
            'Meta': {'object_name': 'UnidadTributaria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valido_desde': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'valido_hasta': ('django.db.models.fields.DateField', [], {}),
            'valor': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        }
    }

    complete_apps = ['configuracion']