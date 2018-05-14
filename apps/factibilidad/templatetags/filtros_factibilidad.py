# -*- coding: utf-8 -*-

"""
Filtros personalizados para persona natural.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from os import path
import json
from re import compile as regex_compile
from re import split as regex_split
from apps.factibilidad.models import *
from django import template
from apps.factibilidad import models

# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FILENAME_REGEX = regex_compile(r'_\d+')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Global Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
register = template.Library()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@register.filter(name='none_to_text')
def type(field):
    """ convierte None a '' """
    if field == None:
        return ""
    return field

@register.filter(name='listar_unidades')
def type(fields):
    """ 
    Obtiene el texto del tipo de proyecto 
    parametros:
        - field (object): UnidadTransporte
    """
    transportes = []
    if fields is not None:
        for f in fields:
            transportes.append(UNIDAD_TRANSPORTE[f.tipo][1])
        return ', '.join(transportes)

    return ""


@register.filter(name='tipo_indole')
def type(value):
    if value is not None:
        return models.TIPOS_INDOLE[value][1]
    return ""

@register.filter(name='tipo_aspecto')
def type(value):
    if value is not None: 
        return models.TIPOS_ASPECTOS[value][1]
    return ""

@register.filter(name='tipo_unidad_transporte')
def type(value):
    if value is not None: 
        return models.UNIDAD_TRANSPORTE[value][1]
    return ""

@register.filter(name='tipo_actividad')
def type(value):
    if value is not None: 
        return models.TIPO_ACTIVIDAD[value][1]
    return ""

@register.filter(name='tipo_proyecto')
def type(value):
    if value is not None: 
        return models.TIPO_PROYECTO[value][1]
    return ""

@register.filter(name='tipo_solicitud')
def type(value):
    if value is not None: 
        return models.TIPO_SOLICITUD[value][1]
    return ""

@register.filter(name='caracteristica_topografica')
def type(value):
    if value is not None: 
        return models.CARACTERISTICAS_TOPOGRAFICAS[value][1]
    return ""

@register.filter(name='vialidad')
def type(value):
    if value is not None: 
        return models.TIPOS_VIALIDADES[value][1]
    return ""

@register.filter(name='range')
def type(value):
    if value is not None: 
        return range(value)
    return None

@register.filter(name='nombre_estado')
def type(value):
    if value is not None: 
        return models.ESTADOS_FACTIBILIDAD[value][1]

@register.filter(name='get_class')
def type(value):
    if value == ACTIVO:
        return "bg-orange"

    if value == APROBADO:
        return "bg-status-success"

    if value == ANULADO:
        return "bg-status-rejected"     


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
