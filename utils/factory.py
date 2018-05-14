# -*- coding: utf-8 -*-

from datetime import datetime

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from utils.gluon.storage import Storage
from apps.actas.models import ANULADA, ActaDocumentos, TipoActa
from apps.verificacion.models import Verificacion
from apps.fiscalizacion.models import Fiscalizacion
from apps.resoluciones.models import Resolucion


class FactoryCodigoActas(object):
    """
        Clase utilizada para generar el codigo de cada tipo de acta a verificar o fiscalizar
        Si se va a crear un acta:
            * Providencia:
                data_factory = Storage(
                    tipo_procedimiento=FactoryCodigoActas.TIPO_VERIFICACION,
                    objeto_tipo_acta=TipoActa.objects.get(nombre="Providencia")
                    objeto = Fiscalizacion.objects.get(pk=1)
                )

                factory = FactoryCodigoActas(data_factory)
                codigo = factory.make_codigo()


            * Acta Normal(Con una providencia - Para generar este tipo de acta se debe tener una providencia):
                data = Storage(
                    tipo_procedimiento=FactoryCodigoActas.TIPO_FISCALIZACION,
                    objeto_tipo_acta=TipoActa.objects.get(nombre="Acta de reparo"),
                    objeto=Fiscalizacion.objects.get(pk=1)
                )

                factory = FactoryCodigoActas(data)
                codigo = factory.make_codigo()
    """
    ORGANISMO_PROCEDENCIA = u'INATUR'
    DIRECCION_EJECUTIVA = u'DE'
    GERENCIA_RECAUDACION_FISCALIZACION = u'GRF'

    TIPO_VERIFICACION = 1
    TIPO_FISCALIZACION = 2

    TIPOS_PROCEDIMIENTOS = (
        (TIPO_VERIFICACION, u'VDFP'),  # verificacion
        (TIPO_FISCALIZACION, u'FSC'),  # fiscalizacion
    )

    VERIFICACION_DEBERES_FORMALES_CON_PROVIDENCIA = 1
    VERIFICACION_DEBERES_FORMALES_SEDE_ADMINISTRATIVA_SIN_PROVIDENCIA = 2
    VERIFICACION_DEBERES_FORMALES_AUTOMATICAMENTE_SIN_PROVIDENCIA = 3

    TIPOS_VERIFICACIONES = (
        (VERIFICACION_DEBERES_FORMALES_CON_PROVIDENCIA, u'VDFP'),
        (VERIFICACION_DEBERES_FORMALES_SEDE_ADMINISTRATIVA_SIN_PROVIDENCIA, u'VDFE'),
        (VERIFICACION_DEBERES_FORMALES_AUTOMATICAMENTE_SIN_PROVIDENCIA, u'VDFA'),
    )

    def __init__(self, data):
        if isinstance(data, Storage):
            # datos para generar codigo de resolucion
            self.es_una_resolucion = data.es_una_resolucion
            self.es_una_tarea_cron = data.es_una_tarea_cron
            self.objeto_verificacion = data.objeto_verificacion
            # datos para generar codigo de actas
            self.tipo_procedimiento = data.tipo_procedimiento
            self.objeto_tipo_acta = data.objeto_tipo_acta
            self.objeto = data.objeto

            self.validar_datos()
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


    def get_codigo_documento(self):
        """
            Funcion que retorna el codigo de documento del tipo de acta al que se quiere generar el codigo
        """
        return self.objeto_tipo_acta.codigo_documento


    def get_tipo_procedimiento(self):
        """
            Funcion que retorna el tipo de procedimiento en la opciones
            Verificacion => VDF
            Fiscalizacion => FSC
        """
        return self.TIPOS_PROCEDIMIENTOS[self.tipo_procedimiento - 1][1]


    def get_consecutivo_anyo(self):
        """
            Funcion que retorna el consecutivo del año en el siguiente formato: 2014 => 14, 2015 => 15
        """
        anyo_str = str(datetime.now().year)
        return anyo_str[2:4] if len(anyo_str) > 2 else anyo_str  # 2014 => 14


    def get_object_acta_tipo_providencia(self):
        """
            Funcion que retorna tipo de acta = providencia
        """
        return TipoActa.objects.get(nombre='Providencia')


    def get_consecutivo_providencia(self):
        """
            Funcion que cuenta todos los documentos de tipo providencia y le suma 1
        """
        return (ActaDocumentos.objects.filter(tipo=self.get_object_acta_tipo_providencia()).count() + 1)


    def get_consecutivo_resolucion(self):
        """
            Funcion que cuenta todos los documentos de tipo providencia y le suma 1
        """
        return str(Resolucion.objects.filter(verificacion=self.objeto_verificacion).count() + 1)


    def get_consecutivo_dentro_providencia(self):
        """
            Funcion que cuenta todos los documentos que pertenezcan a ese providencia, pero que no sea providencias y le suma 1
        """
        data = Storage()
        if self.tipo_procedimiento == self.TIPO_VERIFICACION:
            data.verificacion = self.objeto
        else:
            data.fiscalizacion = self.objeto

        consecutivo_dentro_providencia = (
            ActaDocumentos.objects.
            filter(
                ~Q(estatus=ANULADA),
                **data
            ).
            exclude(
                tipo=self.get_object_acta_tipo_providencia()).
            count() + 1
        )

        return consecutivo_dentro_providencia


    def get_object_providencia(self):
        """
            Funcion que retorna el objeto providencia de la verificacion pasada como parametro
            y que no tenga estatus anulada
        """
        data = Storage(
            tipo=self.get_object_acta_tipo_providencia(),
        )
        if self.tipo_procedimiento == self.TIPO_VERIFICACION:
            data.verificacion = self.objeto
        else:
            data.fiscalizacion = self.objeto

        try:
            objeto_providencia = ActaDocumentos.objects.get(
                ~Q(estatus=ANULADA),
                **data
            )
        except ObjectDoesNotExist:
            # solo tiene providencia ANULADA o no tiene, puede ingresar otra providencia
            objeto_providencia = None
        return objeto_providencia


    def is_in_tipos_procedimientos(self, numero_tipo):
        """
            Funcion que retorna True si el tipo esta en las opciones de TIPOS_PROCEDIMIENTOS
            retorna False en caso contrario
        """
        # Se recorre la lista y compara cada valor con el numero de tipo
        # Retorna una lista booleana, si algun (function any) valor dentro de esa lista es True entonces retorna True
        return any([i[0] == numero_tipo for i in self.TIPOS_PROCEDIMIENTOS])


    def validar_datos(self):
        """
            Funcion que valida si los parametros enviados son correctos
        """
        if self.es_una_resolucion:
            if self.objeto_verificacion == None:
                raise NameError(
                    'Error de Tipo. El objeto de verificacion no puede ser None'
                )
        else:
            if self.objeto == None:
                raise NameError(
                    'Error de Tipo. El objeto no puede ser None'
                )

            if not isinstance(self.objeto, Verificacion) and \
                    not isinstance(self.objeto, Fiscalizacion):
                raise NameError(
                    'Error de Tipo. El atributo objeto debe ser una instancia de Verificacion o Fiscalizacion'
                )

            if isinstance(self.objeto, Verificacion) and \
                    not self.get_tipo_procedimiento() == self.TIPOS_PROCEDIMIENTOS[self.TIPO_VERIFICACION - 1][1]:
                raise NameError(
                    'Error de Tipo. El tipo de procedimiento no corresponde con el tipo de objeto'
                )

            if isinstance(self.objeto, Fiscalizacion) and \
                    not self.get_tipo_procedimiento() == self.TIPOS_PROCEDIMIENTOS[self.TIPO_FISCALIZACION - 1][1]:
                raise NameError(
                    'Error de Tipo. El tipo de procedimiento no corresponde con el tipo de objeto'
                )

            if not isinstance(self.objeto_tipo_acta, TipoActa):
                raise NameError(
                    'Error de Tipo. El atributo objeto_tipo_acta debe ser una instancia TipoActa'
                )
            if not self.is_in_tipos_procedimientos(self.tipo_procedimiento):
                raise NameError(
                    'Error de Tipo. El atributo tipo_procedimiento debe estar incluido en las opciones de la tupla TIPOS_PROCEDIMIENTOS'
                )


    def __make_codigo_acta(self):
        """
            Función privada utilzada para generar el codigo de las actas
        """
        if self.es_una_resolucion:
            raise NameError(
                'Error de Tipo. No se puede crear el codigo, se indico otra configuración'
            )
        """
        Formato:
            organismo_procedencia/
            direccion_ejecutiva/
            gerencia_recaudacion_fiscalizacion/
            tipo_procedimiento/
            tipo_documento/
            consecutivo_anyo
            id_providencia
            id_tipo_acta
            consecutivo_dentro_providencia

        Ejemplo:
            INATUR/DE/GRF/VDF/RQ 14 00001 0001 0002  => VDF = Verificacion

            INATUR/DE/GRF/FSC/RQ 14 00001 0001 0002  => FSC = Fiscalizacion
        """
        codigo = self.ORGANISMO_PROCEDENCIA + "/" + \
                 self.DIRECCION_EJECUTIVA + "/" + \
                 self.GERENCIA_RECAUDACION_FISCALIZACION + "/" + \
                 self.get_tipo_procedimiento() + "/" + \
                 self.get_codigo_documento() + \
                 self.get_consecutivo_anyo()

        # si el tipo de acta es de tipo providencia
        if self.get_object_acta_tipo_providencia() == self.objeto_tipo_acta:
            # genera el codigo de la providencia
            codigo += str(self.get_consecutivo_providencia()).zfill(6)
        else:
            # si tiene providencia, agrega el codigo de la providencia y el consecutivo del acta a agregar
            codigo += str(self.get_object_providencia().codigo[-6:])
            codigo += str(self.get_consecutivo_dentro_providencia()).zfill(4)
        return codigo


    def __make_codigo_resolucion(self):
        """
            Función privada utilizada para generar el código de las resoluciones
        """
        if not self.es_una_resolucion:
            raise NameError(
                'Error de Tipo. No se puede crear el codigo, se indico otra configuración'
            )
        """
        Formato:
            organismo_procedencia/
            direccion_ejecutiva/
            gerencia_recaudacion_fiscalizacion/
            tipo_procedimiento/
            tipo_documento/
            consecutivo_anyo
            consecutivo de la resolucion

        Ejemplo:
            INATUR/DE/GRF/VDF/RS 1400001

        """
        codigo = self.ORGANISMO_PROCEDENCIA + "/" + \
                 self.DIRECCION_EJECUTIVA + "/" + \
                 self.GERENCIA_RECAUDACION_FISCALIZACION + "/"
        if self.es_una_tarea_cron:
            tipo_cron = self.VERIFICACION_DEBERES_FORMALES_AUTOMATICAMENTE_SIN_PROVIDENCIA
            tipo = self.TIPOS_VERIFICACIONES[tipo_cron - 1][1]
            codigo += tipo
        else:
            tipo_sede = self.VERIFICACION_DEBERES_FORMALES_SEDE_ADMINISTRATIVA_SIN_PROVIDENCIA
            tipo = self.TIPOS_VERIFICACIONES[tipo_sede - 1][1]
            codigo += tipo

        codigo += u'RS' + \
                  self.get_consecutivo_anyo() + \
                  self.get_consecutivo_resolucion().zfill(6)
        return codigo


    def make_codigo(self):
        """
            Función encargada de generar el código para las actas y/o resoluciones
        """
        if self.es_una_resolucion:
            codigo = self.__make_codigo_resolucion()
        else:
            codigo = self.__make_codigo_acta()
        return codigo





