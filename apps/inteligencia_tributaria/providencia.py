# -*- coding: utf-8 -*-
"""
Clase para generar la providencia para el pst.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from utils.gluon.storage import Storage
from registro.models import Pst
from apps.fiscalizacion.models import Fiscalizacion
from apps.verificacion.models import Verificacion
from apps.actas.models import TipoActa, ActaDocumentos
from apps.actas.models import NO_NOTIFICADA
from utils.factory import FactoryCodigoActas
from apps.verificacion.models import EN_SEDE


class Providencia(object):
    """
    Clase que genera la providencia para verificaciones y fiscalizaciones del pst
    """

    def __init__(self, pst, verificacion=None, fiscalizacion=None):
        self.pst = pst
        self.verificacion = verificacion
        self.fiscalizacion = fiscalizacion
        self.acta_documentos = None
        self.data = None
        self.tipo = None
        self.tipo_acta = "Providencia"
        self.validar_datos()
        self.iniciar_datos()

    def validar_datos(self):
        """
        Metodo que valida si los parametros enviados son correctos
        """
        if not isinstance(self.pst, Pst):
            raise NameError('Error de Tipo. El atributo pst debe ser una instancia Pst')

        if self.verificacion != None and not isinstance(self.verificacion, Verificacion):
            raise NameError('Error de Tipo. El atributo verificacion debe ser una instancia Verificacion')

        if self.fiscalizacion != None and not isinstance(self.fiscalizacion, Fiscalizacion):
            raise NameError('Error de Tipo. El atributo fiscalizacion debe ser una instancia Fiscalizacion')

    def crear(self):
        """
        Metodo que genera la providencia para una fiscalizacion o verificacion
        """
        if hasattr(self.verificacion, 'tipo_verificacion'):
            if self.verificacion.tipo_verificacion == EN_SEDE:
                return ""

        acta_documento = ActaDocumentos.create(self.data)
        acta_documento.save()
        acta_documento.codigo = self.generar_codigo()
        acta_documento.providencia = acta_documento
        acta_documento.save()
        return acta_documento

    def iniciar_datos(self):
        """
        Metodo que inicia el storage
        """
        if self.verificacion:
            self.tipo = FactoryCodigoActas.TIPO_VERIFICACION

        if self.fiscalizacion:
            self.tipo = FactoryCodigoActas.TIPO_FISCALIZACION

        self.data = Storage(
            pst=self.pst, verificacion=self.verificacion,
            fiscalizacion=self.fiscalizacion, providencia=None,
            tipo=TipoActa.objects.get(nombre=self.tipo_acta),
            estatus=NO_NOTIFICADA,
        )

    def generar_codigo(self):
        """
        Metodo que genera el codigo de la providencia
        """
        data_factory = Storage(
            tipo_procedimiento=self.tipo,
            objeto_tipo_acta=TipoActa.objects.get(nombre=self.tipo_acta)
        )

        if self.fiscalizacion:
            data_factory.objeto = self.fiscalizacion

        if self.verificacion:
            data_factory.objeto = self.verificacion

        factory = FactoryCodigoActas(data_factory)
        return factory.make_codigo()
