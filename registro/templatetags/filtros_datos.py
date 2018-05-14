# -*- coding: utf-8 -*-

"""
Filtros personalizados para persona natural.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from os import path
from re import compile as regex_compile
from re import split as regex_split
import json

from django import template

from apps.actas.models import ESTATUS_ACTA
from apps.factibilidad.models import TIPO_SOLICITUD, ESTADOS_FACTIBILIDAD
from apps.verificacion.models import TIPO_VERIFICACION
from registro.models import ACTIVIDAD_PRINCIPAL
from registro.models import ActividadComercial
from registro.models import TIPOS_PERSONAS_JURIDICA
from registro.models import TIPO_MODIFICACION

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FILENAME_REGEX = regex_compile(r'_\d+')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Global Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
register = template.Library()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@register.filter
def basename(fobj):
    basename = path.basename(fobj.name)
    return u''.join(regex_split(FILENAME_REGEX, basename))


@register.filter(name='obj_type')
def check_type(obj, stype):
    """
    filtros para comprobar el tipo de objetos
    - uso en el html:
        {% if form|obj_type:'mycustomdata' %}
            <form class="custom" action="">
        {% else %}
            <form action="">
        {% endif %}
    """
    try:
        t = obj.__class__.__name__
        print t
        return t.lower() == str(stype).lower()
    except:
        pass
    return False


@register.filter
def field_type(field, ftype):
    """
    filtros para comprobar el campo del formulario
    Ej.
    - uso en el html:
        {% if field|field_type:'checkboxinput' %}
            <label class="cb_label">{{ field }} {{ field.label }}</label>
        {% else %}
            <label for="id_{{ field.name }}">{{ field.label }}</label> {{ field }}
        {% endif %}
    """
    return check_type(field.field.widget, ftype)


@register.filter
def get_tipo_pst(pst_obj):
    try:
        return ActividadComercial.objects.get(
            pst=pst_obj, tipo_actividad=ACTIVIDAD_PRINCIPAL, cached=True
        ).actividad.nombre
    except:
        return None


@register.filter
def get_tipo_usuario(pst_obj):
    return (
        u'Emprendedor' if pst_obj.emprendedor
        else u'Prestador de Servicios Turísticos'
    )


@register.filter
def get_tipo_usuario_short(pst_obj):
    return (u'Emprendedor' if pst_obj.emprendedor else u'PST')


@register.filter
def key(dictionary, key):
    return dictionary.get(unicode(key)) if dictionary else None


@register.filter
def boolean_to_text(field):
    """
    Convierte una variable boolean en texto (Si ó No)
    Ej.
    - uso en html
        {{ accionista.director|boolean_to_text }}
    """
    if field == True:
        return 'Si'

    return 'No'


@register.filter
def text_acta(field):
    """
    Convierte una variable integer en texto correspondiente
    Solo se aplica en actas
    Ej.
    - uso en html
        {{ field|text_acta }}
    """
    opts = {key: value for key, value in TIPO_MODIFICACION}
    return opts.get(int(field), '')


@register.filter
def unicode_to_txt(field):
    """
    Convierte una variable integer en texto correspondiente
    Solo se aplica en actas
    Ej.
    - uso en html
        {{ accionista.director|unicode_to_txt }}
    """
    return json.dumps(field, ensure_ascii=True)


@register.filter(name='tipo_persona_juridica')
def tipo_persona_juridica(value):
    return TIPOS_PERSONAS_JURIDICA[value][1]


@register.filter(name='tipo_verificacion')
def tipo_verificacion(value):
    value -= 1
    return TIPO_VERIFICACION[value][1]


@register.filter(name='tipo_solicitud')
def tipo_solicitud(value):
    return TIPO_SOLICITUD[value][1]


@register.filter(name='estado_factibilidad')
def estado_factibilidad(value):
    return ESTADOS_FACTIBILIDAD[value][1]


@register.filter(name='estatus_acta_documento')
def estatus_acta_documento(value):
    value -= 1
    return ESTATUS_ACTA[value][1]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@register.filter(name='times')
def times(number):
    return range(number)