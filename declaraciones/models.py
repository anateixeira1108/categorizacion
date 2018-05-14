# -*- coding: utf-8 -*-

u""" Modelos para el módulo «declaraciones». """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón U.
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.configuracion import models as cfg_models
from apps.pagos import models as pagos_models
from datetime import date
from datetime import datetime
from decimal import Decimal
from django.db import models
from registro import models as reg_models
from utils import forms_helpers
from utils import models as custom_models
from utils.gluon.storage import Storage
from utils.validate_files import ContentTypeRestrictedFileField
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DECIMAL_PROPS = {
    'blank': True,
    'null': True,
    'decimal_places': 3,
    'default': 0.0,
    'max_digits': 11,
}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modelos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TipoDeclaracion(models.Model):
    nombre = models.CharField(max_length=80)

    def __unicode__(self):
        return self.nombre


class Declaracion(models.Model):
    pst = models.ForeignKey(reg_models.Pst)
    tipo_declaracion = models.ForeignKey('TipoDeclaracion')
    periodo = models.DateField()
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    fecha_presentacion = models.DateTimeField(auto_now=True)
    ventas_propias = models.DecimalField(**DECIMAL_PROPS)
    ventas_exportacion = models.DecimalField(**DECIMAL_PROPS)
    ventas_internas_general = models.DecimalField(**DECIMAL_PROPS)
    ventas_internas_adicional = models.DecimalField(**DECIMAL_PROPS)
    ventas_internas_reducida = models.DecimalField(**DECIMAL_PROPS)
    total_ventas_territorial = models.DecimalField(**DECIMAL_PROPS)
    ingresos_extraterritorial = models.DecimalField(**DECIMAL_PROPS)
    total_extraterritorial = models.DecimalField(**DECIMAL_PROPS)
    total_ventas_menos_anticipo = models.DecimalField(**DECIMAL_PROPS)
    total_ventas_determinacion = models.DecimalField(**DECIMAL_PROPS)
    contribucion_especial_determinada = models.DecimalField(**DECIMAL_PROPS)
    anticipo_declaracion = models.OneToOneField(
        'Declaracion', null=True, blank=True
    )
    # FIXME relacionar con resoluciones cuando éstas se implenten
    compensacion_propios = models.CharField(
        max_length=20, null=True, blank=True
    )
    compensacion_adquiridos = models.CharField(
        max_length=20, null=True, blank=True
    )
    # /FIXME
    total_compensacion = models.DecimalField(**DECIMAL_PROPS)
    total_pagar = models.DecimalField(**DECIMAL_PROPS)
    concepto_pago = models.ForeignKey(
        pagos_models.Concepto, null=True, blank=True
    )
    estatus = models.CharField(max_length=20, null=True, blank=True)
    justificacion_pst = models.CharField(max_length=512, null=True, blank=True)
    justificacion_funcionario = models.CharField(
        max_length=512, null=True, blank=True
    )

    @classmethod
    def get_declaraciones_extemporaneas(cls, pst, desde, hasta):
        assert isinstance(pst, reg_models.Pst)
        assert isinstance(desde, date) or isinstance(desde, datetime)
        assert isinstance(hasta, date) or isinstance(hasta, datetime)

        return cls.objects.filter(
            pst=pst,
            estatus=u'Pagada',
            periodo__gte=desde,
            periodo__lte=hasta,
            concepto_pago__pago__fecha_liquidacion__gt=models.F(
                'concepto_pago__pago__fecha_vencimiento'
            ),
        ).order_by('fecha_presentacion', 'periodo')

    @classmethod
    def get_extemporaneidad_pst_dict(cls, desde, hasta):
        """ Devuelve los PSTs que incurrieron en extemporaneidad.

        Si la fecha de liquidación de un pago con declaraciones asociadas es
        mayor que la fecha de vencimiento del mismo, se incurre en
        extemporaneidad.

        Recibe un rango de fechas indicado por los parámetros desde y hasta,
        ambos de tipo datetime.

        Retorna un diccionario pst: numero_de_faltas, donde pst es una
        instancia de la clase Pst y numero_de_faltas es un entero.
        """

        assert isinstance(desde, datetime)
        assert isinstance(hasta, datetime)

        queryset = cls.objects.filter(
            periodo__gte=desde,
            periodo__lte=hasta,
            concepto_pago__pago__fecha_liquidacion__gt=models.F(
                'concepto_pago__pago__fecha_vencimiento'
            ),
        ).order_by('-periodo', 'pst')

        return {
            pst: queryset.filter(pst=pst).count()
            for pst in set(row.pst for row in queryset)
        }

    @classmethod
    def get_omision_pst_dict(cls, desde, hasta):
        """ Devuelve los PSTs que incurrieron en omisión.

        Si la fecha de vencimiento de un pago con declaraciones asociadas pasó
        (relativo a la fecha actual) y éste no ha sido cancelado, se incurre en
        omisión.

        Recibe un rango de fechas indicado por los parámetros desde y hasta,
        ambos de tipo datetime.

        Retorna un diccionario pst: numero_de_faltas, donde pst es una
        instancia de la clase Pst y numero_de_faltas es un entero.
        """

        assert isinstance(desde, datetime)
        assert isinstance(hasta, datetime)

        queryset = cls.objects.filter(
            periodo__gte=desde,
            periodo__lte=hasta,
            concepto_pago__pago__fecha_liquidacion=None,
            concepto_pago__pago__fecha_vencimiento__lt=datetime.now(),
        ).order_by('-periodo', 'pst')

        return {
            pst: queryset.filter(pst=pst).count()
            for pst in set(row.pst for row in queryset)
        }

    @classmethod
    def get_ingresos_pst_dict(cls, desde, hasta, mode, value):
        """ Devuelve los PSTs con ingresos <= ó >= determinado valor.

        Recibe un rango de fechas indicado por los parámetros desde y hasta,
        ambos de tipo datetime. Adicionalmente, también recibe el modo, el cual
        puede ser: lt, gt, lte, gte; y el valor contra el cual comparar.

        Retorna un diccionario pst: ejemplares, donde pst es una instancia de
        la clase Pst y ejemplares es un entero
        """

        assert isinstance(desde, datetime)
        assert isinstance(hasta, datetime)
        assert isinstance(mode, str) and mode in ['lt', 'gt', 'lte', 'gte']
        assert isinstance(value, Decimal)

        dynamic_fields = {
            ('total_ventas_territorial__' + mode): value
        }

        queryset = cls.objects.filter(
            periodo__gte=desde, periodo__lte=hasta, **dynamic_fields
        ).order_by('-periodo', 'pst')

        return {
            pst: queryset.filter(pst=pst).count()
            for pst in set(row.pst for row in queryset)
        }

    def __unicode__(self):
        return u'{} del periodo {} por {} Bs.'.format(
            self.tipo_declaracion.nombre,
            self.periodo.strftime('%m/%y'),
            self.total_pagar,
        )


class InteresMoratorio(models.Model):
    art66cot = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=4
    )
    concepto_pago = models.ForeignKey(
        pagos_models.Concepto, null=True, blank=True
    )
    declaracion = models.ForeignKey(
        Declaracion, null=False, blank=False
    )
    dias_mora = models.DecimalField(
        null=False, blank=False, decimal_places=0, max_digits=4
    )
    factor = models.DecimalField(
        null=False, blank=False, decimal_places=8, max_digits=10
    )
    monto_interes = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=10
    )
    tasa_interes_bcv = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=4
    )

    @classmethod
    def gen_intereses_moratorios(cls, pst, desde, hasta):
        declaraciones_extemporaneas = (
            Declaracion.get_declaraciones_extemporaneas(pst, desde, hasta)
        )
        periodo_set = set(
            declaracion.periodo for declaracion in declaraciones_extemporaneas
        )
        art66cot = (
            cfg_models.Configuracion.objects.get(activo=True).art66cot
        )
        calc_tasa_interes_bcv = lambda periodo: (
            cfg_models.TasaInteresBCV.get_tasa_interes_para_periodo(periodo)
        )
        calc_factor = lambda periodo: (
            calc_tasa_interes_bcv(periodo) * art66cot / Decimal(36000)
        )

        for periodo in periodo_set:
            declaracion = declaraciones_extemporaneas.filter(
                periodo=periodo
            ).last()

            dias_mora = (
                declaracion.concepto_pago.pago.fecha_liquidacion
                - declaracion.concepto_pago.pago.fecha_vencimiento
            ).days

            monto_intereses = forms_helpers.decimal_round(
                Decimal(dias_mora)
                * calc_factor(periodo)
                * declaracion.concepto_pago.pago.total
            )

            if declaracion.interesmoratorio_set.first() is not None:
                continue

            cls(
                art66cot=art66cot,
                declaracion=declaracion,
                dias_mora=dias_mora,
                factor=forms_helpers.decimal_round(calc_factor(periodo), 8),
                monto_interes=monto_intereses,
                tasa_interes_bcv=calc_tasa_interes_bcv(periodo),
            ).save()

    @classmethod
    def get_intereses_moratorios(cls, pst, desde, hasta):
        cls.gen_intereses_moratorios(pst, desde, hasta)

        declaraciones_extemporaneas = (
            Declaracion.get_declaraciones_extemporaneas(pst, desde, hasta)
        )
        intereses_moratorios = []

        for declaracion in declaraciones_extemporaneas:
            interes_moratorio = declaracion.interesmoratorio_set.first()

            if interes_moratorio:
                intereses_moratorios.append(interes_moratorio)

        return intereses_moratorios


class Prueba(custom_models.CustomFileAllocatorModel):
    declaracion = models.ForeignKey(Declaracion)
    archivo = ContentTypeRestrictedFileField(
        upload_to=reg_models.RUTA_DOCUMENTOS,
        content_types=['image/jpeg', 'image/png', 'application/pdf'],
        blank=True,
        max_upload_size=reg_models.TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
