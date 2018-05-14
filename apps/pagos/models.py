# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.configuracion import models as cfg_models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from hmac import new as hmac_new
from registro.models import Pst
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modelos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Concepto(models.Model):
    concepto_tipo = models.ForeignKey(
        'ConceptoTipo', null=False, blank=False
    )
    fecha_generacion = models.DateTimeField(
        auto_now_add=True, blank=True
    )
    monto = models.DecimalField(
        decimal_places=3, max_digits=11, null=False, blank=False
    )
    pago = models.ForeignKey(
        'Pago', null=True, blank=True
    )
    pst = models.ForeignKey(
        Pst, null=False, blank=False
    )
    estatus = models.CharField(
        max_length=20, default='Pendiente', null=False, blank=False
    )

    def __unicode__(self):
        return u'Concepto: Nº {:010} por un monto de {} Bs.'.format(
            self.id, self.monto
        )


class ConceptoTipo(models.Model):
    codigo = models.CharField(
        max_length=100, null=False, blank=False
    )
    nombre = models.CharField(
        max_length=100, null=False, blank=False
    )

    def __unicode__(self):
        return u'ConceptoTipo: Nº {} - "{}"'.format(self.codigo, self.nombre)


class Pago(models.Model):
    auth_code = models.CharField(
        max_length=40, null=True, blank=True
    )
    fecha_generacion = models.DateTimeField(
        auto_now_add=True, blank=True
    )
    fecha_liquidacion = models.DateTimeField(
        null=True, blank=True
    )
    fecha_vencimiento = models.DateTimeField(
        default=lambda: gen_fecha_vencimiento(), null=False, blank=True
    )
    numero_documento = models.CharField(
        max_length=20, default=lambda: gen_numero_documento(), blank=True
    )
    numero_liquidacion = models.CharField(
        max_length=40, null=True, blank=True
    )
    porcion = models.CharField(
        max_length=20, default='ÚNICO', blank=True
    )
    pst = models.ForeignKey(
        Pst, null=False, blank=False
    )
    estatus = models.CharField(
        max_length=20, default='Por Pagar', null=False, blank=False
    )
    total = models.DecimalField(
        decimal_places=3, max_digits=11, null=False, blank=False
    )

    def __unicode__(self):
        return u'Pago: Nº {} a nombre de "{}" por un total de {} Bs.'.format(
            self.numero_documento, self.pst.razon_social, self.total
        )

    def save(self):
        super(Pago, self).save()
        self.auth_code = u'{}'.format(hmac_new(
            self.pst.rif.encode('utf-8'),
            self.numero_documento.encode('utf-8'),
        ).hexdigest())
        super(Pago, self).save()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def gen_fecha_vencimiento():
    dias_vencimiento_planilla_pago = cfg_models.Configuracion.objects.filter(
        activo=True
    ).first().dias_vencimiento_planilla_pago

    siguiente_mes = datetime.now() + relativedelta(months=1)
    fecha_partida = datetime(siguiente_mes.year, siguiente_mes.month, 1)

    return cfg_models.CalendarioLaboral.get_n_siguiente_dia_laborable(
        dias_vencimiento_planilla_pago, fecha_partida
    )


def gen_numero_documento():
    """ Número en la forma 2014 06 29 [0000001 - 9999999]"""

    date_str = datetime.now().strftime('%Y%m%d')
    last_row = Pago.objects.all().last()

    if not last_row or not last_row.numero_documento.startswith(date_str):
        return date_str + '1'.zfill(7)

    ultimo_numero_documento = int(last_row.numero_documento[8:])
    nuevo_numero_documento = str(ultimo_numero_documento + 1).zfill(7)

    return u'{}'.format(date_str + nuevo_numero_documento)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
