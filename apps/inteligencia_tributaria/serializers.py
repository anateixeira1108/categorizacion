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
from registro.models import Pst, ActividadComercial, ACTIVIDAD_PRINCIPAL
from apps.cuentas.models import MinturUser as User
from apps.inteligencia_tributaria.models import FuncionariosSolicitud
    

class PstSerializer(serializers.Serializer):
    """
    Clase serializadora para el objeto pst
    """
    pk = serializers.Field()
    rif = serializers.CharField(max_length=20)
    razon_social = serializers.CharField(max_length=75)
    tipo_pst = serializers.RelatedField()
    ultima_verificacion = serializers.DateField(format=None, input_formats=None)
    ultima_fiscalizacion = serializers.DateField(format=None, input_formats=None)
    actividad_primaria = serializers.SerializerMethodField('get_primary_activity')
    
    class Meta:
        model = Pst
        fields = (
            'pk', 
            'rif', 
            'razon_social', 
            'ultima_verificacion', 
            'ultima_fiscalizacion', 
            'actividad_primaria'
        )

    def restore_object(self, attrs, instance=None):
        """
        Crear o actualizar una nueva instancia del objeto, dado un diccionario
        de deserializan valores de campo.
        """
        if instance:
            instance.rif = attrs.get('rif', instance.rif)
            instance.tipo_pst = attrs.get('tipo_pst', instance.tipo_pst)
            instance.razon_social = attrs.get('razon_social', instance.razon_social)
            instance.ultima_fiscalizacion = attrs.get('ultima_fiscalizacion', instance.ultima_fiscalizacion)
            instance.ultima_verificacion = attrs.get('ultima_verificacion', instance.ultima_verificacion)
            instance.pst = attrs.get('pst', instance.pst)
            return instance

        return Pst(**attrs)

    def get_primary_activity(self, obj):
        """
        Medoto que obtiene la acividad primaria
        """
        try:
            filter=dict(pst=obj.pk, tipo_actividad=ACTIVIDAD_PRINCIPAL)
            return ActividadComercial.objects.get(**filter)
        except ActividadComercial.DoesNotExist:
            return ""
        

class UserSerializer(serializers.Serializer):
    """
    Clase serializadora para el objeto usuario
    """
    pk = serializers.Field()
    rif = serializers.CharField(max_length=20)
    cedula = serializers.CharField(max_length=20)
    nombres = serializers.CharField(max_length=255)
    apellidos = serializers.CharField(max_length=255)
    role = serializers.IntegerField()


    def restore_object(self, attrs, instance=None):
        """
        Crear o actualizar una nueva instancia del objeto, dado un diccionario
        se deserializan valores de campo.
        """
        if instance:
            instance.rif = attrs.get('rif', instance.rif)
            instance.cedula = attrs.get('cedula', instance.cedula)
            instance.nombres = attrs.get('nombres', instance.nombres)
            instance.apellidos = attrs.get('apellidos', instance.apellidos)
            instance.role = attrs.get('role', instance.role)
            return instance

        return User(**attrs)


class FuncionarioSerializer(serializers.Serializer):
    """
    Clase serializadora para el objeto Funcionario
    """
    pk = serializers.Field()
    funcionario = serializers.RelatedField()
    solicitud = serializers.RelatedField()
    es_coordinador = serializers.BooleanField()
    nombres = serializers.CharField(source='funcionario.nombres', max_length=255)
    apellidos = serializers.CharField(source='funcionario.apellidos', max_length=255)
    rif = serializers.CharField(source='funcionario.rif', max_length=255)
    usuario_id = serializers.IntegerField(source='funcionario.id')
    es_apoyo = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        """
        Crear o actualizar una nueva instancia del objeto, dado un diccionario
        se deserializan valores de campo.
        """
        if instance:
            instance.funcionario = attrs.get('funcionario', instance.funcionario)
            instance.solicitud = attrs.get('solicitud', instance.solicitud)
            instance.es_coordinador = attrs.get('es_coordinador', instance.es_coordinador)
            instance.es_apoyo = attrs.get('es_apoyo', instance.es_apoyo)
            return instance

        return FuncionariosSolicitud(**attrs)
        