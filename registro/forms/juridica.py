# -*- coding: utf-8 -*-

"""
formularios para el registro de una persona juridica.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import re
from datetime import datetime

from django import forms
from venezuela.models import Estado, Municipio, Parroquia

from registro.models import PERSONA_JURIDICA
from registro.models import Pst, Direccion, RepresentanteContacto
from registro.models import TipoPst, Circunscripcion, RegistroMercantil
from registro.models import Sunacoop, Acta, ActividadComercial
from utils import checkers
from utils import forms_helpers as helpers
from django.core.exceptions import ObjectDoesNotExist

# Variables estaticas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PATRON_DOCUMENTO_IDENTIDAD = '^[VE][-][0-9]{6,8}$'
PATRON_RIF = '^[JGVEP][-][0-9]{8}[-][0-9]$'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Classes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Paso1Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el primer paso del registro para el prestador de servicio juridico
    Datos generales
    """
    rtn = forms.IntegerField(
        required=False,
        widget=forms.TextInput(),
    )

    pagina_web = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'http://www.dominio.com'}),
    )

    class Meta:
        model = Pst
        fields = (
            'tipo_juridica',
            'tipo_figura',
            'rif',
            'razon_social',
            'pagina_web',
            'denominacion_comercial',
            'rtn',
            'archivo_rif',
            'inicio_actividad_comercial',
            'estado_contribuyente'
        )

    def __init__(self, *args, **kwargs):
        unrequired_fields = ['rtn']

        super(Paso1Form, self).__init__(unrequired_fields, *args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required'] = u'Este campo es requerido.'

        self.fields['rtn'].required = False

    def clean_pagina_web(self):
        """ Valida la pagina web"""
        pagina_web = self.cleaned_data['pagina_web']

        if checkers.is_valid(pagina_web, 'web'):
            new_pagina_web = pagina_web
        else:
            msg = u'El formato de la url debe ser: http://www.example.com.'
            raise forms.ValidationError(msg)

        return new_pagina_web

    def clean_rif(self):
        """ Valida el RIF y verifica que éste sea único """

        rif = self.cleaned_data['rif']

        if not checkers.is_valid(rif, 'rif'):
            msg = u'El formato del RIF proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        if rif != self.initial.get('rif') and Pst.objects.filter(rif__exact=rif):
            msg = u'Este RIF ya está en uso, por favor ingrese uno diferente'
            raise forms.ValidationError(msg)

        return rif

    def clean_rtn(self):
        """ Valida el RTN y verifica que éste sea único """

        rtn = self.cleaned_data['rtn']

        # TODO validar el número del comprobante

        if rtn != self.initial['rtn'] and Pst.objects.filter(rtn__exact=rtn) and rtn is not None:
            msg = (
                u'Este número de comprobante ya está en uso, por favor'
                u' ingrese uno diferente'
            )
            raise forms.ValidationError(msg)

        return rtn

    def clean_estado_contribuyente(self):
        return int(self.cleaned_data['estado_contribuyente'])


class Paso2Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el segundo paso del registro para el prestador de servicio juridico
    Dirección
    """
    default = [('', 'Seleccione')]

    choices = default + [(e.id, e.estado) for e in Estado.objects.all().order_by('estado')]
    estado = forms.ChoiceField(
        widget=forms.Select(),
        choices=choices
    )

    choices = default + [(m.id, m.municipio) for m in Municipio.objects.all().order_by('municipio')]
    municipio = forms.ChoiceField(
        widget=forms.Select(),
        choices=choices
    )

    choices = default + [(p.id, p.parroquia) for p in Parroquia.objects.all().order_by('parroquia')]
    parroquia = forms.ChoiceField(
        widget=forms.Select(),
        choices=choices
    )

    punto_referencia = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '', 'rows': ''}),
    )


    class Meta:
        model = Direccion
        fields = (
            'estado',
            'municipio',
            'parroquia',
            'avenida_calle',
            'edificio',
            'oficina_apartamento',
            'codigo_postal',
            'punto_referencia',
            'urbanizacion',
        )

    codigo_postal = forms.IntegerField(
        widget=forms.TextInput(),
    )

    def __init__(self, *args, **kwargs):
        super(Paso2Form, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required'] = u'Este campo es requerido.'

    def clean_codigo_postal(self):
        """ Valida el código postal """

        codigo_postal = self.cleaned_data['codigo_postal']

        if not checkers.is_valid(str(codigo_postal), 'codigo-postal'):
            msg = u'El formato del código postal proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        return codigo_postal

    def clean_estado(self):
        """
        Valida que la seleccion del estado sea valido
        - estado(unicode): unicode con el numero del estado
        Retorna
        - estado(Object): Objeto Estado
        """

        try:
            estado = Estado.objects.get(pk=int(self.cleaned_data['estado']))
        except Estado.DoesNotExist:
            raise forms.ValidationError(u"El registro no existe.")

        return estado


    def clean_municipio(self):
        """
        Valida que la seleccion del tipo de pst sea valido
        - municipio(unicode): Unicode con el numero del municipio
        Retorna
        - municipio(Object): Objeto Municipio
        """
        try:
            municipio = Municipio.objects.get(pk=int(self.cleaned_data['municipio']))
        except Municipio.DoesNotExist:
            raise forms.ValidationError(u"El registro no existe.")

        return municipio

    def clean_parroquia(self):
        """
        Valida que la seleccion del tipo de pst sea valido
        - parroquia(unicode): unicode con el numero del parroquia
        Retorna
        - parroquia(Object): Objeto Parroquia
        """
        try:
            parroquia = Parroquia.objects.get(pk=int(self.cleaned_data['parroquia']))
        except Parroquia.DoesNotExist:
            raise forms.ValidationError(u"El registro no existe.")

        return parroquia


class Paso3Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el tercer paso del registro para el prestador de servicio juridico
    Datos del RepresentanteContacto
    """

    telefono_celular = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '0426-4544554'}),
    )

    telefono_fijo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '0212-4554554'}),
    )

    class Meta:
        model = RepresentanteContacto
        fields = (
            'nombres',
            'apellidos',
            'cedula',
            'rif',
            'cargo_empresa',
            'telefono_fijo',
            'telefono_celular',
            'correo_electronico',
            'archivo_cedula',
            'archivo_rif',
        )

    def __init__(self, *args, **kwargs):
        super(Paso3Form, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required'] = u'Este campo es requerido.'

    def clean_nombres(self):
        """ Valida los nombres """

        nombres = self.cleaned_data['nombres'].strip()

        if not checkers.is_valid(nombres, 'nombres/apellidos'):
            msg = (
                u'Solo se permiten vocales, consonantes y espacios.'
            )
            raise forms.ValidationError(msg)

        return nombres

    def clean_apellidos(self):
        """ Valida los apellidos """

        apellidos = self.cleaned_data['apellidos'].strip()

        if not checkers.is_valid(apellidos, 'nombres/apellidos'):
            msg = (
                u'Solo se permiten vocales, consonantes y espacios.'
            )
            raise forms.ValidationError(msg)

        return apellidos

    def clean_rif(self):
        """ Valida que el rif cumpla con el patron"""

        if not re.search(PATRON_RIF, self.cleaned_data['rif']):
            msg = u"El formato del Rif. proporcionado no coincide."
            raise forms.ValidationError(msg)

        return self.cleaned_data['rif']

    def clean_cargo_empresa(self):
        """ Validar que el cargo en la empresa cumpla con el patrón.

        Valida que el cargo en la empresa esté compuesto solo por caracteres
        alfabéticos.
        """

        cargo_empresa = self.cleaned_data['cargo_empresa'].strip()

        if not checkers.is_valid(cargo_empresa, 'nombres/apellidos'):
            raise forms.ValidationError(
                u"El cargo en la empresa debe estar formado solo por"
                u" caracteres alfabéticos."
            )

        return cargo_empresa

    def clean_cedula(self):
        """ Valida que la cedula cumpla con el patron"""
        if not re.search(PATRON_DOCUMENTO_IDENTIDAD, self.cleaned_data['cedula']):
            msg = u"El formato del documento de identidad proporcionado no coincide."
            raise forms.ValidationError(msg)

        return self.cleaned_data['cedula']

    def clean_telefono_celular(self):
        """ Valida el teléfono celular """
        celular = self.cleaned_data['telefono_celular']
        if celular and not checkers.is_valid(celular, 'telefono'):
            msg = u'El formato del teléfono proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        return celular

    def clean_telefono_fijo(self):
        """ Valida el teléfono fijo """

        fijo = self.cleaned_data['telefono_fijo']

        if not checkers.is_valid(fijo, 'telefono'):
            msg = u'El formato del teléfono proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        return fijo


class Paso4Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el tercer paso del registro para el prestador de servicio juridico
    Datos de la persona de contactos
    """

    telefono_celular = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '0426-4544554'}),
    )

    telefono_fijo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '0212-4554554'}),
    )

    class Meta:
        model = RepresentanteContacto
        fields = (
            'correo_electronico',
            'archivo_cedula',
            'archivo_rif',
            'telefono_celular',
            'telefono_fijo',
            'cargo_empresa',
            'cedula',
            'rif',
            'apellidos',
            'nombres')

    def __init__(self, *args, **kwargs):
        super(Paso4Form, self).__init__(*args, **kwargs)
        self.fields['archivo_cedula'].error_messages = {
            'invalid': u'Ingrese un Email valido'
        }

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required'] = u'Este campo es requerido.'

    def clean_nombres(self):
        """ Valida los nombres """

        nombres = self.cleaned_data['nombres'].strip()

        if not checkers.is_valid(nombres, 'nombres/apellidos'):
            msg = (
                u'Solo se permiten vocales, consonantes y espacios.'
            )
            raise forms.ValidationError(msg)

        return nombres

    def clean_apellidos(self):
        """ Valida los apellidos """

        apellidos = self.cleaned_data['apellidos'].strip()

        if not checkers.is_valid(apellidos, 'nombres/apellidos'):
            msg = (
                u'Solo se permiten vocales, consonantes y espacios.'
            )
            raise forms.ValidationError(msg)

        return apellidos

    def clean_rif(self):
        """ Valida que el rif cumpla con el patron"""

        if not re.search(PATRON_RIF, self.cleaned_data['rif']):
            msg = u"El formato del Rif. proporcionado no coincide."
            raise forms.ValidationError(msg)

        return self.cleaned_data['rif']

    def clean_cargo_empresa(self):
        """ Validar que el cargo en la empresa cumpla con el patrón.

        Valida que el cargo en la empresa esté compuesto solo por caracteres
        alfabéticos.
        """

        cargo_empresa = self.cleaned_data['cargo_empresa'].strip()

        if not checkers.is_valid(cargo_empresa, 'nombres/apellidos'):
            raise forms.ValidationError(
                u"El cargo en la empresa debe estar formado solo por"
                u" caracteres alfabéticos."
            )

        return cargo_empresa

    def clean_cedula(self):
        """ Valida que la cedula cumpla con el patron"""
        if not re.search(PATRON_DOCUMENTO_IDENTIDAD, self.cleaned_data['cedula']):
            msg = u"El formato del documento de identidad proporcionado no coincide."
            raise forms.ValidationError(msg)

        return self.cleaned_data['cedula']

    def clean_telefono_celular(self):
        """ Valida el teléfono celular """
        celular = self.cleaned_data['telefono_celular']
        if celular and not checkers.is_valid(celular, 'telefono'):
            msg = u'El formato del teléfono proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        return celular

    def clean_telefono_fijo(self):
        """ Valida el teléfono fijo """

        fijo = self.cleaned_data['telefono_fijo']

        if not checkers.is_valid(fijo, 'telefono'):
            msg = u'El formato del teléfono proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        return fijo


class Paso5Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el quinto paso del registro para el prestador de servicio juridico
    Tipo de Prestador de Servicios Turísticos
    """
    default = [('', 'Seleccione')]
    listTipos = default + [(t.id, t.nombre) for t in TipoPst.objects.filter(tipo_persona=PERSONA_JURIDICA)]
    actividad = forms.ChoiceField(
        widget=forms.Select(),
        choices=listTipos,
        required=True,
    )

    actividad_principal_licencia = forms.IntegerField(
        required=True,
        widget=forms.TextInput(),
    )

    class Meta:
        model = ActividadComercial
        fields = ('actividad',)

    def __init__(self, *args, **kwargs):
        unrequired_fields = ['actividad_principal_licencia']

        super(Paso5Form, self).__init__(unrequired_fields, *args, **kwargs)

        self.fields['actividad'].error_messages = {
            'required': u'Este campo es requerido.',
            'invalid': u'Ingrese una selecion valida.'
        }

    def clean_actividad(self):
        """
        Valida que la seleccion del tipo de pst sea valido
        parametros
        - actividad (unicode) : unicode con el numero del tipo del pst
        Retorna
        - actividad (Object TipoPst): objeto con el tipo del pst
        """
        try:
            actividad = TipoPst.objects.get(pk=int(self.cleaned_data['actividad']))
        except (TipoPst.DoesNotExist, KeyError):
            raise forms.ValidationError(u"Tipo de persona no existe.")

        return actividad 



class Paso6Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el sexto paso del registro para el prestador de servicio juridico
    Detalles del acta constitutiva
    """

    circuito_circunscripcion = forms.ModelChoiceField(
        queryset=Circunscripcion.objects.all()
    )

    registro_mercantil = forms.ModelChoiceField(
        queryset=RegistroMercantil.objects.all()
    )

    class Meta:
        model = Acta
        fields = (
            'tomo',
            'numero_tomo',
            'duracion',
            'capital_suscrito',
            'capital_pagado',
            'registro_mercantil',
            'circuito_circunscripcion',
            'fecha_ultima_asamblea',
            'fecha_registro',
            'archivo_acta_constitutiva'
        )

    capital_pagado = forms.FloatField(
        widget=forms.TextInput(),
    )

    capital_suscrito = forms.FloatField(
        widget=forms.TextInput(),
    )

    duracion = forms.IntegerField(
        widget=forms.TextInput()
    )

    numero_tomo = forms.IntegerField(
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super(Paso6Form, self).__init__(*args, **kwargs)
        self.fields['registro_mercantil'].error_messages = {
            'invalid': u'Ingrese una seleción valida.'
        }

        self.fields['circuito_circunscripcion'].error_messages = {
            'invalid': u'Ingrese una seleción valida.'
        }

        self.fields['archivo_acta_constitutiva'].error_messages = {
            'invalid': u'Ingrese una seleción valida.'
        }

        self.fields['fecha_ultima_asamblea'].error_messages = {
            'invalid': u'La fecha de la ultima asamblea es invalida debe tener un formato dd/mm/yyyy.'
        }

        self.fields['fecha_registro'].error_messages = {
            'invalid': u'La fecha de registro es invalida, debe tener un formato dd/mm/yyyy.'
        }

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required'] = u'Este campo es requerido.'


class Paso8Form(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el octavo paso del registro para el prestador de servicio juridico
    Registro en el SUNACOOP
    """

    fecha = forms.CharField(
        required=True,
        widget=forms.DateTimeInput()
    )

    numero = forms.CharField(required=True)
    archivo_comprobante = forms.FileField(required=True)


    class Meta:
        model = Sunacoop
        fields = (
            'numero',
            'fecha',
            'archivo_comprobante',
        )

    def __init__(self, *args, **kwargs):
        super(Paso8Form, self).__init__(*args, **kwargs)
        self.fields['numero'].error_messages = {
            'required': u'Este campo es requerido.',
            'invalid': u'debe agregar un numero valido.'
        }

        self.fields['fecha'].error_messages = {
            'required': u'Este campo es requerido.',
            'invalid': u'La fecha de la ultima asamblea es invalida, debe tener un formato  dd/mm/yyyy.'
        }

        self.fields['archivo_comprobante'].error_messages = {
            'required': u'Este campo es requerido.',
        }

    def clean_fecha(self):
        """
        Cambia el formato de la fecha para guardar
        return
        - registro (str): fecha con el formato YYYY-mm-dd
        """
        try:
            date = self.cleaned_data['fecha']
            registro = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
        except Exception as e:
            raise forms.ValidationError(u"Error al convertir la fecha de registro.")

        return registro

