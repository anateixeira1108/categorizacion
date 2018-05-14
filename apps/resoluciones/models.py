# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.cuentas import models as cuentas_models
from apps.verificacion import models as vrf_models
from decimal import Decimal
from declaraciones import models as declaraciones_models
from django.db import models
from registro import models as registro_models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modelos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graduacion(models.Model):
    nombre = models.CharField(
        null=False, blank=False, max_length=26
    )


class Ley(models.Model):
    codigo = models.IntegerField(
        null=False, blank=False
    )
    descripcion = models.CharField(
        null=False, blank=False, max_length=100
    )
    siglas = models.CharField(
        null=False, blank=False, default='ND', max_length=10
    )

    def __unicode__(self):
        return u'{} - {}'.format(
            self.codigo, self.siglas
        )


class TipoTributo(models.Model):
    codigo = models.IntegerField(
        null=False, blank=False
    )
    descripcion = models.CharField(
        null=False, blank=False, max_length=100
    )
    siglas = models.CharField(
        null=False, blank=False, default='ND', max_length=10
    )

    def __unicode__(self):
        return u'{} - {}'.format(
            self.codigo, self.siglas
        )


class TipoSancion(models.Model):
    nombre = models.CharField(
        null=True, blank=True, max_length=100
    )


class SubTipoSancion(models.Model):
    tipo_sancion = models.ForeignKey(
        'TipoSancion', null=False, blank=False
    )
    nombre = models.CharField(
        null=False, blank=False, max_length=100
    )


class Sancion(models.Model):
    aplicacion = models.IntegerField(
        null=False, blank=False
    )
    codigo = models.IntegerField(
        null=False, blank=False
    )
    cot_articulo = models.CharField(
        null=False, blank=False, max_length=10
    )
    deber_formal_articulo = models.IntegerField(
        null=False, blank=False
    )
    deber_formal_literal = models.CharField(
        null=True, blank=True, max_length=2
    )
    deber_formal_numeral = models.IntegerField(
        null=True, blank=True
    )
    descripcion = models.TextField(
        null=False, blank=False
    )
    formulario_asociado = models.CharField(
        null=True, blank=True, max_length=20
    )
    graduacion = models.ForeignKey(
        'Graduacion', null=False, blank=False
    )
    ley = models.ForeignKey(
        'Ley', null=True, blank=True
    )
    observaciones = models.TextField(
        null=True, blank=True
    )
    tipo_sancion = models.ForeignKey(
        'SubTipoSancion', null=False, blank=False
    )
    tipo_tributo = models.ForeignKey(
        'TipoTributo', null=False, blank=False
    )
    ut_max = models.IntegerField(
        null=False, blank=False
    )
    ut_min = models.IntegerField(
        null=False, blank=False
    )


class TipoResolucion(models.Model):
    nombre = models.CharField(
        null=False, blank=False, max_length=100
    )


class Resolucion(models.Model):
    tipo_resolucion = models.ForeignKey(
        TipoResolucion, null=False, blank=False
    )
    funcionario = models.ForeignKey(
        cuentas_models.MinturUser, null=False, blank=False
    )
    pst = models.ForeignKey(
        registro_models.Pst, null=False, blank=False
    )
    sanciones = models.ManyToManyField(
        Sancion, through='Ilicito', null=False, blank=False
    )
    verificacion = models.ForeignKey(
        vrf_models.Verificacion, null=True, blank=True,
    )
    numero_documento = models.CharField(
        null=False, blank=True, max_length=70
    )
    fecha_expedicion = models.DateTimeField(
        null=False, blank=True, auto_now_add=True
    )
    estatus = models.CharField(
        null=False, blank=False, max_length=60, default='Elaborada'
    )
    valor_ut = models.DecimalField(
        null=False, blank=False, max_digits=8, decimal_places=2
    )
    fecha_notificacion = models.DateTimeField(
        null=True, blank=True
    )
    observaciones = models.TextField(
        null=True, blank=True
    )

    @classmethod
    def _calc_valor_ut(cls, sancion_ut__sum, resolucion):
        return sancion_ut__sum * resolucion.valor_ut * Decimal('0.5')

    @classmethod
    def _proc_mayor_sancion(cls, result_dict):
        mayor_sancion = (None, 0)

        for key, value in result_dict.iteritems():
            if value > mayor_sancion[1]:
                mayor_sancion = (key, value)

        del result_dict[mayor_sancion[0]]

        return mayor_sancion[0], mayor_sancion[1] * Decimal('2')

    @classmethod
    def calc_concurrencia(cls, resolucion):
        """Calcula y retorna la concurrencia para la resolución dada.

        El objeto devuelto es una tupla de longitud igual a dos. El primer
        miembro es otra tupla de la forma (Sancion, Decimal), la cual
        representa la sanción de mayor denominación y que se paga completa, a
        diferencia del resto de las sanciones que se pagan fraccionadas a la
        mitad. El segundo miembro de la tupla es un diccionario
        Sancion~>Decimal que representa los ilícitos de la resolución agrupados
        por sanción junto a su respectiva multa en bolívares (ya fraccionado).
        """

        ilicito_list = Ilicito.objects.filter(
            resolucion=resolucion
        ).order_by('sancion')

        sancion_set = set(
            ilicito.sancion for ilicito in ilicito_list
        )

        sancion_ut_list = [
            ilicito_list.filter(
                sancion=sancion
            ).aggregate(models.Sum('sancion_ut')) for sancion in sancion_set
        ]

        result_dict = {
            key: cls._calc_valor_ut(value['sancion_ut__sum'], resolucion)
            for key, value in zip(sancion_set, sancion_ut_list)
        }

        return cls._proc_mayor_sancion(result_dict), result_dict


class Ilicito(models.Model):
    resolucion = models.ForeignKey(
        'Resolucion', null=False, blank=False
    )
    sancion = models.ForeignKey(
        'Sancion', null=False, blank=False
    )
    declaracion = models.ForeignKey(
        declaraciones_models.Declaracion, null=True, blank=True
    )
    periodo = models.DateField(
        null=False, blank=False
    )
    fecha_limite_declaracion = models.DateField(
        null=False, blank=True
    )
    valor_ut = models.DecimalField(
        null=False, blank=False, max_digits=8, decimal_places=2
    )
    sancion_ut = models.IntegerField(
        null=False, blank=False
    )

    @classmethod
    def _calc_incremento(cls, ilicito):
        if ilicito.sancion.graduacion.nombre == u'TÉRMINO MEDIO':
            return (ilicito.sancion.ut_min + ilicito.sancion.ut_max) / 6

        if ilicito.sancion.graduacion.nombre == u'INCREMENTO':
            return ilicito.sancion.ut_min

    @classmethod
    def calc_sancion(cls, ilicito):
        resolucion_list = cls.get_resoluciones_reincidencia(ilicito)
        incremento = cls._calc_incremento(ilicito)

        return min(
            ilicito.sancion.ut_min + (incremento * len(resolucion_list)),
            ilicito.sancion.ut_max
        )

    @classmethod
    def get_resoluciones_reincidencia(cls, ilicito):
        """Resoluciones tomadas en cuenta para la reincidencia del ilícito
        indicado.

        Retorna un Set con las resoluciones expedidas con anterioridad en las
        que se ha sancionado al PST por la misma razón al ilícito indicado.
        """
        return set(Resolucion.objects.filter(
            pst=ilicito.resolucion.pst,
            fecha_expedicion__lt=ilicito.resolucion.fecha_expedicion,
            sanciones__in=[ilicito.sancion]
        ))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
