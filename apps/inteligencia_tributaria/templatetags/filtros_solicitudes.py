# -*- coding: utf-8 -*-
"""
Filtros personalizados para las solicitudes.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edwin Caminero
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from os import path
from re import compile as regex_compile
from re import split as regex_split

from django import template

from apps.verificacion.models import EN_SEDE, DOMICILIO_FISCAL, GRUPAL
from apps.inteligencia_tributaria.models import FuncionariosSolicitud
from apps.inteligencia_tributaria.models import TIPO_SOLICITUD, TIPO_VERIFICACION
from registro.models import TIPOS_PERSONAS_JURIDICA
from apps.actas.models import ESTATUS_ACTA


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


@register.filter
def color_class(field):
    """
    Convierte una variable integer el el color de la clase
    correspondiente
    Ej.
    - uso en html
        {{ variable_a_convertir|color_class }}
    """
    if field == EN_SEDE:
        return 'bg-navy'
    if field == DOMICILIO_FISCAL:
        return 'bg-olive'
    if field == GRUPAL:
        return 'bg-maroon'


@register.filter
def get_functionary(solicitud):
    """
    Obtiene una lista de funcionarios por la solicitud requerida
    Ej.
    - uso en html
        {{ variable_a_convertir|get_functionary }}
    """
    if solicitud:
        funcionarios = FuncionariosSolicitud.objects.filter(solicitud=solicitud)
        nombre_apellido = ""
        funcionario_list = []
        for f in funcionarios:
            if f.funcionario:
                asignacion = "(F)"
                if f.es_apoyo == True:
                    asignacion = "(A)"
                if f.es_coordinador==True:
                    asignacion = "(C)"

                nombre_apellido = "<li><a>%s %s %s </a></li>" % (f.funcionario.nombres, f.funcionario.apellidos, asignacion)
            funcionario_list.append(nombre_apellido)
        funcionario = "".join(funcionario_list)
    
    return funcionario


@register.filter
def format_date(field):
    """
    Ajusta el formato de la fecha a mes-año
    Ej.
    - uso en html
        {{ variable_a_convertir|color_class_estatus }}
    """
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo",
        4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre",
        10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    if field:
        return '%s-%d' % (meses[field.month], field.year)
    return ""


@register.filter
def funcionario_coordinador(field):
    """
    Ajusta el formato de la fecha a mes-año
    Ej.
    - uso en html
        {{ variable_a_convertir|color_class_estatus }}
    """
    if field == True:
        return "Coordinador"
    return "Funcionario"


@register.filter
def get_name_request(solicitud):
    """
    Obtiene el nombre de la solicitud a base de un int
    Ej.
    - uso en html
        {{ variable_a_convertir|get_name }}
    """
    return TIPO_SOLICITUD[solicitud][1]


@register.filter
def tipo_verificacion(solicitud):
    """
    Obtiene el nombre del tipo verificacion a base de un int
    Ej.
    - uso en html
        {{ variable_a_convertir|get_name }}
    """
    print(solicitud, type(solicitud))
    return TIPO_VERIFICACION[solicitud][1]


@register.filter(name='tipo_persona_juridica')
def type(value):
    value -= 1
    return TIPOS_PERSONAS_JURIDICA[value][1]


@register.filter(name='tipo_verificacion')
def type(value):
    value -= 1
    return TIPO_VERIFICACION[value][1]


@register.filter(name='estatus_acta_documento')
def type(value):
    value -= 1
    return ESTATUS_ACTA[value][1]

@register.filter(name='split_list')
def type(value):
    html_list = []
    items_list = value[1:-1].replace('"', '')
    items_list = items_list.split(",")

    for i in items_list:
        item = "<li><a> %s </a></li>" % i
        html_list.append(item)
    html_list = "".join(html_list)

    return html_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
