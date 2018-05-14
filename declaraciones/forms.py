# -*- coding: utf-8 -*-

u""" Formularios para las declaraciones. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón U.
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from decimal import Decimal
from django import forms
from django.db.models import Q
from models import Declaracion
from registro.models import Pst
from utils import forms_helpers as helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Formularios ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlanillaForm(helpers.ModelFormBaseClass):
    class Meta:
        model = Declaracion
        fields = (
            'fecha_desde',
            'fecha_hasta',
            'periodo',
            'total_compensacion',
            'total_pagar',
            'ventas_exportacion',
            'ventas_internas_adicional',
            'ventas_internas_general',
            'ventas_internas_reducida',
            'ventas_propias',
            # Clean functions' order
            'tipo_declaracion',
            'anticipo_declaracion',
            'total_ventas_territorial',
            'total_ventas_menos_anticipo',
            'contribucion_especial_determinada',
        )

    def __init__(self, user, *args, **kwargs):
        unrequired_fields = (
            'anticipo_declaracion',
            'periodo',
            'total_compensacion',
            'total_ventas_menos_anticipo',
            'total_ventas_territorial',
            'ventas_exportacion',
            'ventas_internas_adicional',
            'ventas_internas_general',
            'ventas_internas_reducida',
            'ventas_propias',
        )
        super(PlanillaForm, self).__init__(unrequired_fields, *args, **kwargs)

        self.user = user

        self.fields['anticipo_declaracion'].queryset = (
            Declaracion.objects.filter(
                pst=Pst.objects.get(user=self.user),
                estatus=u'Pagada',
            )
        )

    def clean_tipo_declaracion(self):
        u""" Verifica restricciones de tipo en relación al periodo. """

        queryset = Declaracion.objects.filter(
            ~ Q(estatus=u'Anulada'),
            pst=Pst.objects.get(user=self.user),
            periodo=self.cleaned_data['periodo']
        )

        tipo_declaracion = self.cleaned_data['tipo_declaracion']

        if not queryset.exists():
            if tipo_declaracion.nombre == u'Declaración Sustitutiva':
                raise forms.ValidationError(
                    u'No se puede hacer una Declaración Sustitutiva'
                    u' de un periodo no declarado.'
                )

        elif tipo_declaracion.nombre == u'Declaración Definitiva':
            raise forms.ValidationError(
                u'Solo se permite una Declaración Definitiva por periodo.'
            )

        return tipo_declaracion

    def clean_anticipo_declaracion(self):
        anticipo_declaracion = self.cleaned_data['anticipo_declaracion']

        if anticipo_declaracion is None:
            anticipo_declaracion = Declaracion.objects.filter(
                ~ Q(estatus=u'Anulada'),
                pst=Pst.objects.get(user=self.user),
                periodo=self.cleaned_data['periodo'],
            ).order_by('fecha_presentacion').last()

            self.data = {
                key: value for key, value in self.data.iteritems()
            }
            self.data.update({
                'anticipo_declaracion': anticipo_declaracion
            })

        return anticipo_declaracion

    def clean_total_ventas_territorial(self):
        tipo_declaracion = self.cleaned_data['tipo_declaracion']

        if tipo_declaracion.nombre == u'Declaración Sustitutiva':
            anticipo_declaracion = self.cleaned_data['anticipo_declaracion']

            es_registrado_menor_que_declarado = (
                self.cleaned_data['total_ventas_territorial']
                < anticipo_declaracion.total_ventas_territorial
            )

            if es_registrado_menor_que_declarado:
                raise forms.ValidationError(
                    u'Verifique el Monto o Solicite Reconocimiento de Pago.'
                )

            if anticipo_declaracion.estatus != u'Pagada':
                raise forms.ValidationError(
                    u'La declaración previa para este periodo no está pagada.'
                )

        return self.cleaned_data['total_ventas_territorial']

    def clean_total_ventas_menos_anticipo(self):
        tipo_declaracion = self.cleaned_data['tipo_declaracion']

        if 'total_ventas_territorial' not in self.cleaned_data:
            return Decimal('0')

        if tipo_declaracion.nombre == u'Declaración Sustitutiva':
            anticipo_declaracion = self.cleaned_data['anticipo_declaracion']

            self.data = {
                key: value for key, value in self.data.iteritems()
            }

            self.data['total_ventas_menos_anticipo'] = helpers.decimal_round(
                self.cleaned_data['total_ventas_territorial']
                - anticipo_declaracion.total_ventas_menos_anticipo
            )

            return self.data['total_ventas_menos_anticipo']

        return self.cleaned_data['total_ventas_territorial']

    def clean_contribucion_especial_determinada(self):
        contribucion_especial_determinada = helpers.decimal_round(
            self.cleaned_data['total_ventas_menos_anticipo'] * Decimal('0.01')
        )

        self.data = {
            key: value for key, value in self.data.iteritems()
        }

        self.data['contribucion_especial_determinada'] = (
            contribucion_especial_determinada
        )

        return contribucion_especial_determinada
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
