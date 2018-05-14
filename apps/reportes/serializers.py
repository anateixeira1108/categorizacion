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
from registro.models import Pst
from apps.cuentas.models import MinturUser as User

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
            return instance

        return Pst(**attrs)
