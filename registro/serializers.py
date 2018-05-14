# -*- coding: utf-8 -*-
"""
Vistas para las solicitudes de revision de pst.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from django.forms import widgets
from rest_framework import serializers
from .models import Accionista, Pst
from os import path
from re import split as regex_split
from re import compile as regex_compile

FILENAME_REGEX = regex_compile(r'_\d+')

class AccionistaSerializer(serializers.Serializer):
    """
    Clase serializadora para el objeto Accionista
    """
    pk = serializers.Field()
    pst = serializers.RelatedField(source='pst.id')
    nombres = serializers.CharField(max_length=50)
    apellidos = serializers.CharField(max_length=50)
    cedula = serializers.CharField(max_length=20)
    rif = serializers.CharField(max_length=20)
    fecha_incorporacion = serializers.DateField(format='%d/%m/%Y')
    numero_acciones = serializers.IntegerField()
    director = serializers.BooleanField()
    archivo_cedula = serializers.FileField()
    nombre_archivo_cedula = serializers.SerializerMethodField('get_nombre_archivo_cedula')
    archivo_rif = serializers.FileField()
    nombre_archivo_rif = serializers.SerializerMethodField('get_nombre_archivo_rif')

    def restore_object(self, attrs, instance=None):
        """
        Crear o actualizar una nueva instancia del objeto, dado un diccionario
        de deserializan valores de campo.
        """
        if instance:
            instance.rif = attrs.get('rif', instance.rif)
            instance.pst = attrs.get('pst', instance.pst)
            instance.nombres = attrs.get('nombres', instance.nombres)
            instance.apellidos = attrs.get('apellidos', instance.apellidos)
            instance.cedula = attrs.get('cedula', instance.cedula)
            instance.fecha_incorporacion = attrs.get('fecha_incorporacion', instance.fecha_incorporacion)
            instance.numero_acciones = attrs.get('numero_acciones', instance.numero_acciones)
            instance.director = attrs.get('director', instance.director)
            instance.archivo_cedula = attrs.get('archivo_cedula', instance.archivo_cedula)
            instance.archivo_rif = attrs.get('archivo_rif', instance.archivo_rif)
            return instance

        return Accionista(**attrs)

    def get_nombre_archivo_cedula(self, obj):
        """
        Medoto que obtiene el nombre del archivo cedula
        """
        basename = path.basename(obj.archivo_cedula.name)
        return u''.join(regex_split(FILENAME_REGEX, basename))

    def get_nombre_archivo_rif(self, obj):
        """
        Medoto que obtiene el nombre del archivo rif
        """
        basename = path.basename(obj.archivo_rif.name)
        return u''.join(regex_split(FILENAME_REGEX, basename))


class ActaSerializer(serializers.Serializer):
    """
    Clase serializadora para el objeto Acta
    """    
    pk = serializers.Field()
    pst = serializers.RelatedField(source='pst.id')
    circuito_circunscripcion = serializers.RelatedField(source='circuito_circunscripcion.id')
    registro_mercantil = serializers.RelatedField(source='registro_mercantil.id')
    tomo = serializers.CharField(max_length=20)
    numero_tomo = serializers.IntegerField()
    fecha_registro = serializers.DateField(format='%d/%m/%Y')
    fecha_ultima_asamblea = serializers.DateField(format='%d/%m/%Y')
    objetivo_modificacion = serializers.IntegerField()
    motivo_modificacion = serializers.CharField(max_length=250)
    archivo_acta_constitutiva = serializers.FileField()
    nombre_archivo_acta = serializers.SerializerMethodField('get_nombre_archivo_acta')

    def restore_object(self, attrs, instance=None):
        """
        Crear o actualizar una nueva instancia del objeto, dado un diccionario
        de deserializan valores de campo.
        """
        if instance:
            instance.pst = attrs.get('pst', instance.pst)
            instance.numero_tomo = attrs.get('numero_tomo', instance.numero_tomo)
            instance.tomo = attrs.get('tomo', instance.tomo)
            instance.fecha_registro = attrs.get('fecha_registro', instance.fecha_registro)
            instance.circuito_circunscripcion = attrs.get('circuito_circunscripcion', 
                                                        instance.circuito_circunscripcion)
            instance.registro_mercantil = attrs.get('registro_mercantil', 
                                                    instance.registro_mercantil)
            instance.fecha_ultima_asamblea = attrs.get('fecha_ultima_asamblea', 
                                                        instance.fecha_ultima_asamblea)
            instance.objetivo_modificacion = attrs.get('objetivo_modificacion', 
                                                        instance.objetivo_modificacion)
            instance.motivo_modificacion = attrs.get('motivo_modificacion', 
                                                        instance.motivo_modificacion)
            instance.archivo_acta_constitutiva = attrs.get('archivo_acta_constitutiva', 
                                                        instance.archivo_acta_constitutiva)
            return instance

        return Acta(**attrs)

    def get_nombre_archivo_acta(self, obj):
        """
        Medoto que obtiene la el nombre del archivo acta
        """
        basename = path.basename(obj.archivo_acta_constitutiva.name)
        return u''.join(regex_split(FILENAME_REGEX, basename))