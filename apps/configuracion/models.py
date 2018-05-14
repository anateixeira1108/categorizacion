# ~º~ coding: UTF-8 ~º~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import timedelta, date
from decimal import Decimal
from django.db import models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TIPO_FECHA_BANCARIO = 10

TIPO_FECHA_FERIADO = 20

TIPO_FECHA_SEQUENCE = (
    (TIPO_FECHA_BANCARIO, u'BANCARIO'),
    (TIPO_FECHA_FERIADO, u'FERIADO'),
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modelos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Area(models.Model):
    nombre = models.CharField(max_length=60, blank=False, null=False)
    acronimo = models.CharField(max_length=10, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return u'[{activo}] {acronimo}{nombre}'.format(
            activo=(u'A' if self.activo else u'I'),
            acronimo=(self.acronimo + u' - ' if self.acronimo else ''),
            nombre=self.nombre
        )


class CalendarioLaboral(models.Model):
    fecha = models.DateField(
        null=False, blank=False, unique=True
    )
    tipo = models.IntegerField(
        choices=TIPO_FECHA_SEQUENCE, null=False, blank=False
    )
    activo = models.BooleanField(
        null=False, blank=True, default=True
    )

    @classmethod
    def _es_laborable(cls, fecha):
        if fecha.weekday() in [5, 6]:
            return False

        if cls.objects.filter(fecha=fecha, activo=True).exists():
            return False

        return True

    @classmethod
    def _get_siguiente_dia_laboral(cls, fecha):
        while True:
            fecha = fecha + timedelta(days=1)

            if cls._es_laborable(fecha):
                break

        return fecha

    @classmethod
    def get_n_siguiente_dia_laborable(cls, n, fecha):
        assert isinstance(n, int) and n > 0

        while n > 0:
            fecha = cls._get_siguiente_dia_laboral(fecha)
            n -= 1

        return fecha

    def __unicode__(self):
        return u'{} :: {} :: {}Activo'.format(
            self.fecha.strftime('%d/%m/%Y'),
            self.get_tipo_display(),
            ('' if self.activo else 'No ')
        )


class Configuracion(models.Model):
    art66cot = models.DecimalField(
        null=False, max_digits=4, decimal_places=2, default=Decimal('1.2')
    )
    dias_vencimiento_planilla_pago = models.IntegerField(
        default=15, null=False, blank=False
    )
    activo = models.BooleanField(
        default=False, null=False, blank=False
    )


class UnidadTributaria(models.Model):
    valor = models.DecimalField(
        null=False, blank=False, max_digits=8, decimal_places=2
    )
    valido_desde = models.DateField(
        null=False, blank=False, auto_now_add=True
    )
    valido_hasta = models.DateField(
        null=False, blank=False
    )

    @classmethod
    def get_valor_para_fecha(cls, fecha):
        for row in cls.objects.all().order_by('-valido_desde'):
            if row.valido_desde <= fecha <= row.valido_hasta:
                return row.valor

        return None

    def __unicode__(self):
        return u'UT = {} Bs. Desde: {} - Hasta: {}'.format(
            self.valor,
            self.valido_desde.strftime('%d/%m/%Y'),
            self.valido_hasta.strftime('%d/%m/%Y')
        )


class Horarios(models.Model):
    valido_desde = models.DateField(
        null=False, blank=False, auto_now_add=True
    )
    valido_hasta = models.DateField(
        null=False, blank=False
    )
    horario_atencion = models.ManyToManyField(
        'Dias', through='HorariosAtencion'
    )

    def __unicode__(self):
        return "Desde:{} - Hasta:{}".format(self.valido_desde, self.valido_hasta)

    @classmethod
    def get_horario_activo(cls):
        fecha_actual = date.today()
        try:
            horario = cls.objects.get(
                valido_desde__lte=fecha_actual,
                valido_hasta__gte=fecha_actual
            )

            atencion = horario.horariosatencion_set.all()
            atencion_list = []
            for dias_atencion in atencion:
                dias_dict = {
                    "dia_id": dias_atencion.dia.id,
                    "dia": dias_atencion.dia.nombre,
                    "desde": dias_atencion.desde.strftime("%I:%M %p"),
                    "hasta": dias_atencion.hasta.strftime("%I:%M %p")
                }
                atencion_list.append(dias_dict)

            import itertools, operator
            horarios_atencion = []
            for key, items in itertools.groupby(atencion_list, operator.itemgetter('dia_id')):
                horarios_atencion.append(list(items))

            result = []
            for dia_atencion in horarios_atencion:
                horario =  []
                for d in dia_atencion:
                    horario.append({
                        'desde': d['desde'],
                        'hasta': d['hasta']
                    })
                    nombre = d['dia']
                    dia_id = d['dia_id']

                result.append({
                    'dia_id': dia_id,
                    'nombre': nombre,
                    'horario': horario
                })

            return result

        except cls.DoesNotExist:
            return None


class Dias(models.Model):
    nombre = models.CharField(
        null=False, blank=False, max_length=20
    )

    def __unicode__(self):
        return "{}".format(self.nombre)


class HorariosAtencion(models.Model):
    horario = models.ForeignKey(Horarios)
    dia = models.ForeignKey(Dias)
    desde = models.TimeField()
    hasta = models.TimeField()


class TasaInteresBCV(models.Model):
    periodo = models.DateField(
        null=False, blank=False
    )
    tasa_interes = models.DecimalField(
        null=False, blank=False, max_digits=4, decimal_places=2
    )

    @classmethod
    def get_tasa_interes_para_periodo(cls, periodo_date):
        return cls.objects.filter(periodo=periodo_date).first().tasa_interes

    def __unicode__(self):
        return u'Tasa de interés de {} para el periodo de {}'.format(
            self.tasa_interes, self.periodo.strftime('%B-%Y')
        )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
