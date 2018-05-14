# -*- coding: utf-8 -*-
"""
Formularios para factibilidad de pst.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import datetime
from django import forms
from .models import SocioTecnicoProyecto
from utils import checkers
from utils import forms_helpers as helpers

# Classes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RecaudosEstablecimientosForm(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el primer paso del registro de factibilidad del Pst
    Direccion del proyecto
    """
    class Meta:
        model = SocioTecnicoProyecto
        fields = (
            'archivo_titulo_propiedad',
            'archivo_contrato',
            'archivo_autorizacion',
            'archivo_uso_turistico',
            'archivo_memoria_descriptiva',
            'archivo_presupuesto'
        )
             
    def __init__(self, *args, **kwargs):
        super(RecaudosEstablecimientosForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required']= u'Este campo es requerido.'

class RecaudosTransporteTuristicoForm(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el primer paso del registro de factibilidad del Pst
    Direccion del proyecto
    """
    class Meta:
        model = SocioTecnicoProyecto
        fields = (
            'archivo_conformidad_competente',
            'archivo_factura_proforma',
            'archivo_visto_bueno',
            'archivo_factibilidad_economica',
            'archivo_memoria_descriptiva'
        )
             
    def __init__(self, *args, **kwargs):
        super(RecaudosTransporteTuristicoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required']= u'Este campo es requerido.'


class RecaudosActividadesRecreativasForm(helpers.ModelFormBaseClass):
    """
    Campos requeridos para el primer paso del registro de factibilidad del Pst
    Direccion del proyecto
    """
    class Meta:
        model = SocioTecnicoProyecto
        fields = (
            'archivo_conformidad_aval',
            'archivo_memoria_descriptiva',
            'archivo_presupuesto'
        )
             
    def __init__(self, *args, **kwargs):
        super(RecaudosActividadesRecreativasForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].error_messages['required']= u'Este campo es requerido.'

        self.fields['archivo_conformidad_aval'].required = False







            

 