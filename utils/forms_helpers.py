# -*- coding: utf-8 -*-

u""" Utilidades de uso general para los formularios de la aplicación. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import datetime
from decimal import Decimal
from decimal import ROUND_UP
from django import forms
from os import path
from re import compile as re_compile
from unicodedata import normalize
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FILE_PATH = re_compile(
    r'^((?:[0-9a-fA-F]{4}[\/\\]){10})?(.+)$'
)

SPECIAL_CHARACTERES = re_compile(
    r'[\t !"#$%&\'()*/<=>?@\[\\\]^`{|},:]+'
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ModelFormBaseClass(forms.ModelForm):
    def __init__(self, unrequired_fields=[], *args, **kwargs):
        super(ModelFormBaseClass, self).__init__(*args, **kwargs)
        
        print "=================="
        print "DESDE ModelFormBaseClass en __init__"
        print "=================="
        
        for field in self.fields.iterkeys():
            print field

            self.fields[field].error_messages['required'] = (
                u'Este campo es requerido.'
            )
            self.fields[field].error_messages['invalid'] = (
                u'La información proporcionada no es válida.'
            )

            if field not in unrequired_fields:
                self.fields[field].required = True

                if not field.startswith('archivo'):
                    self.fields[field].widget.attrs['required'] = True

            if field.startswith('fecha'):
                setattr(
                    self, 'clean_' + field, clean_fechas_closure(self, field)
                )

            if field.startswith('archivo'):
                print "StartsWith"                
                setattr(
                    self, 'clean_' + field, clean_archivos_closure(self, field)
                )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clean_fechas_closure(instance, field_name):
    def clean_fechas():
        fecha = instance.cleaned_data[field_name]

        specials = (
            'fecha_vencimiento_licencia',
            'fecha_vencimiento_certificado'
        )

        if isinstance(fecha, str) or isinstance(fecha, unicode):
            try:
                fecha = datetime.strptime(fecha.strip(), '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError(
                    'La fecha proporcionada es invalida.'
                    ' Debe tener un formato dd/mm/yyyy.'
                )

        if isinstance(fecha, datetime):
            fecha = fecha.date()

        if field_name in specials and fecha <= datetime.now().date():
            raise forms.ValidationError(
                'No se permiten fechas ubicadas en el pasado o el presente.'
            )

        specials = (
            'fecha_hasta',
            'fecha_vencimiento_certificado',
            'fecha_vencimiento_licencia',
        )

        if field_name not in specials and fecha > datetime.now().date():
            raise forms.ValidationError(
                'No se permiten fechas ubicadas en el futuro.'
            )
        return fecha
    return clean_fechas


def clean_archivos_closure(instance, field_name):
    def clean_archivos():
        filepath_split = FILE_PATH.split(
            instance.cleaned_data[field_name].name
        )
        slugifyed_basename = slugify(
            filepath_split[2]
        )
        instance.cleaned_data[field_name].name = path.join(
            (filepath_split[1] or '')[:-1], slugifyed_basename
        )
        m = instance.cleaned_data[field_name]
        print "EN CLOSURE" , m
        return m
    return clean_archivos


def decimal_round(decimal_number, exp=2):
    return decimal_number.quantize(Decimal(10) ** -exp, rounding=ROUND_UP)


def slugify(text, delim=u'-'):
    return unicode(delim.join(
        normalize('NFKD', word).encode('ascii', 'ignore')
        for word in SPECIAL_CHARACTERES.split(text.lower()) if word
    ))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
