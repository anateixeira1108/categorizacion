# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django import template
from registro.models import ACTIVIDAD_PRINCIPAL
from registro.models import ActividadComercial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Global Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
register = template.Library()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@register.filter
def capall(string):
    return string.upper()


@register.filter
def get_licencia(pst_obj):
    try:
        return ActividadComercial.objects.get(
            pst=pst_obj, tipo_actividad=ACTIVIDAD_PRINCIPAL, cached=True
        ).licencia
    except:
        return None


@register.filter
def mypprint(string):
    return ' '.join(word[0].upper() + word[1:] for word in string.split('_'))


@register.filter
def not_in(value, list_str):
    return value not in list_str.split(',')


@register.filter
def basename(string):
    return string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
