# -*- coding: utf-8 -*-

"""
Formularios para el registro de una persona natural.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import datetime
from django import forms
from registro import models
from utils import checkers
from utils import forms_helpers as helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Formularios ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Paso1Form(helpers.ModelFormBaseClass):
    """
    Formulario que comprende los datos básicos de la persona que se va a
    registrar en el portal.
    """

    class Meta:
        model = models.Pst
        fields = (
            'apellidos',
            'archivo_cedula',
            'archivo_pasaporte',
            'archivo_rif',
            'archivo_servicio',
            'cedula',
            'nombres',
            'rif',
            'rtn',
            'telefono_celular',
            'telefono_fijo',
            'tipo_figura',
            'inicio_actividad_comercial',
            'estado_contribuyente'
        )

    actividad = forms.ModelChoiceField(
        queryset=models.TipoPst.objects.filter(
            tipo_persona=models.PERSONA_NATURAL
        ),
        required=True,
    )

    actividad_principal_licencia = forms.IntegerField(
        required=True,
        widget=forms.TextInput(),
    )

    rtn = forms.IntegerField(
        required=False,
        widget=forms.TextInput(),
    )

    def __init__(self, *args, **kwargs):
        unrequired_fields = [
            'actividad_principal_licencia',
            'rtn',
            'telefono_celular',
            'tipo_pst',
        ]

        super(Paso1Form, self).__init__(unrequired_fields, *args, **kwargs)

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

    def clean_cedula(self):
        """ Valida el documento de identidad """

        cedula = self.cleaned_data['cedula']

        if not checkers.is_valid(cedula, 'documento-identidad'):
            msg = (
                u'El formato del documento de identidad proporcionado no es'
                u' correcto.'
            )
            raise forms.ValidationError(msg)

        return cedula

    def clean_rif(self):
        """ Valida el RIF y verifica que éste sea único """

        pst = models.Pst.objects.filter(rif=self.cleaned_data['rif'])

        if not checkers.is_valid(self.cleaned_data['rif'], 'rif'):
            msg = u'El formato del RIF proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        if pst and pst[0].rif != self.initial.get('rif'):
            msg = u'Este RIF ya está en uso, por favor ingrese uno diferente'
            raise forms.ValidationError(msg)

        return self.cleaned_data['rif']

    def clean_rtn(self):
        """ Valida el RTN y verifica que éste sea único """

        pst = models.Pst.objects.filter(rtn=self.cleaned_data['rtn'])

        # TODO validar el número del comprobante

        if pst and pst[0].rtn != self.initial.get('rtn'):
            msg = (
                u'Este número de comprobante ya está en uso, por favor'
                u' ingrese uno diferente'
            )
            raise forms.ValidationError(msg)

        return self.cleaned_data['rtn']

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


class Paso2Form(helpers.ModelFormBaseClass):
    """
    Formulario que comprende los datos de residencia (dirección) del usuario.
    """

    class Meta:
        model = models.Direccion
        fields = (
            'avenida_calle',
            'codigo_postal',
            'edificio',
            'estado',
            'municipio',
            'oficina_apartamento',
            'parroquia',
            'punto_referencia',
            'urbanizacion',
        )

    codigo_postal = forms.IntegerField(
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        unrequired_fields = ['oficina_apartamento', 'punto_referencia']

        super(Paso2Form, self).__init__(unrequired_fields, *args, **kwargs)

        self.fields['estado'].choices = sorted(
            self.fields['estado'].choices, key=lambda item: item[1]
        )
        self.fields['municipio'].choices = sorted(
            self.fields['municipio'].choices, key=lambda item: item[1]
        )
        self.fields['parroquia'].choices = sorted(
            self.fields['parroquia'].choices, key=lambda item: item[1]
        )

    def clean_codigo_postal(self):
        """ Valida el código postal """

        codigo_postal = self.cleaned_data['codigo_postal']

        if not checkers.is_valid(str(codigo_postal), 'codigo-postal'):
            msg = u'El formato del código postal proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        return codigo_postal


class Paso3Form(helpers.ModelFormBaseClass):
    class Meta:
        model = models.Acta
        fields = (
            'archivo_acta_constitutiva',
            'circuito_circunscripcion',
            'fecha_registro',
            'numero_tomo',
            'registro_mercantil',
            'tomo',
        )

    numero_tomo = forms.IntegerField(
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super(Paso3Form, self).__init__([], *args, **kwargs)


class Paso4AgenteForm(helpers.ModelFormBaseClass):
    """
    Formulario que comprende los datos del agente turístico
    """

    class Meta:
        model = models.DatoEspecifico
        fields = (
            'anios_experiencia',
            'archivo_curriculum',
            'titulo_universitario',
        )

    anios_experiencia = forms.IntegerField(
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        unrequired = ['titulo_universitario']

        super(Paso4AgenteForm, self).__init__(unrequired, *args, **kwargs)


class Paso4ConductorForm(helpers.ModelFormBaseClass):
    """
    Formulario que comprende los datos del conductor turístico
    """

    class Meta:
        model = models.DatoEspecifico
        fields = (
            'archivo_certificado',
            'archivo_licencia',
            'certificado_medico',
            'fecha_vencimiento_certificado',
            'fecha_vencimiento_licencia',
            'grado_licencia',
        )

    fecha_vencimiento_certificado = forms.CharField(
        widget=forms.DateInput()
    )
    fecha_vencimiento_licencia = forms.CharField(
        widget=forms.DateInput()
    )

    def __init__(self, *args, **kwargs):
        super(Paso4ConductorForm, self).__init__(
            [], *args, **kwargs
        )

    def clean_fecha_vencimiento_certificado(self):
        fecha = self.cleaned_data['fecha_vencimiento_certificado']
        return datetime.strptime(fecha, '%d/%m/%Y').date()

    def clean_fecha_vencimiento_licencia(self):
        fecha = self.cleaned_data['fecha_vencimiento_licencia']
        return datetime.strptime(fecha, '%d/%m/%Y').date()


class Paso4GuiaForm(helpers.ModelFormBaseClass):
    """
    Formulario que comprende los datos del guía turístico
    """

    class Meta:
        model = models.DatoEspecifico
        fields = (
            'ciudad_primeros_auxilios',
            'egresado_instituto',
            'fecha_curso',
            'fecha_primeros_auxilios',
            'guia_especializado',
            'archivo_certificado_guia_especializado',
            'nombre_curso',
            'presta_servicio',
            'primeros_auxilios',
            'archivo_constancia_curso_primeros_auxilios',
        )

    fecha_curso = forms.CharField(
        widget=forms.DateInput()
    )
    fecha_primeros_auxilios = forms.CharField(
        widget=forms.DateInput()
    )

    def __init__(self, *args, **kwargs):
        unrequired_fields = [
            'archivo_certificado_guia_especializado',
            'archivo_constancia_curso_primeros_auxilios',
            'egresado_instituto',
            'fecha_curso',
            'guia_especializado',
            'nombre_curso',
            'presta_servicio',
        ]

        super(Paso4GuiaForm, self).__init__(unrequired_fields, *args, **kwargs)

    def clean_archivo_certificado_guia_especializado(self):
        """
        Valida que el certificado sea proporcionado si es guía especializado
        """

        if self.cleaned_data['guia_especializado']:
            if not self.cleaned_data['archivo_certificado_guia_especializado']:
                raise forms.ValidationError(u'Este campo es requerido.')

        return self.cleaned_data['archivo_certificado_guia_especializado']

    def clean_fecha_curso(self):
        """ Valida que la fecha del curso sea indicada si éste se realizó """

        fecha_curso = self.cleaned_data['fecha_curso']

        if self.cleaned_data['egresado_instituto'] and not fecha_curso:
            msg = u'Por favor, indique la fecha del curso.'
            raise forms.ValidationError(msg)

        return datetime.strptime(fecha_curso, '%d/%m/%Y').date()

    def clean_fecha_primeros_auxilios(self):
        fecha = self.cleaned_data['fecha_primeros_auxilios']
        return datetime.strptime(fecha, '%d/%m/%Y').date()

    def clean_nombre_curso(self):
        """ Valida que el nombre del curso sea indicado si éste se realizó """

        nombre_curso = self.cleaned_data['nombre_curso']

        if self.cleaned_data['egresado_instituto'] and not nombre_curso:
            msg = u'Por favor, indique el nombre del curso.'
            raise forms.ValidationError(msg)

        return nombre_curso
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
