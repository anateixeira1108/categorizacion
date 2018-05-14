# coding=utf-8

from django.db import models

from utils.gluon.storage import Storage
from registro.models import Pst
from apps.fiscalizacion.models import Fiscalizacion
from apps.verificacion.models import Verificacion
from apps.cuentas.models import MinturUser

NO_NOTIFICADA = 1
NOTIFICADA = 2
CONCLUIDA = 3
ANULADA = 4
APROBACION_SOLICITADA = 5
APROBADA = 6

ESTATUS_ACTA = (
    (NO_NOTIFICADA, u'No notificada'),
    (NOTIFICADA, u'Notificada'),
    (CONCLUIDA, u'Concluida'),
    (ANULADA, u'Anulada'),
    (APROBACION_SOLICITADA, u'Aprobación solicitada'),
    (APROBADA, u'Aprobada'),
)


class TipoActa(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    codigo_documento = models.CharField(max_length=10, blank=False, null=False, default="")

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto TipoActa a partir
        de la información suministrada.
        Parametros:
        Storage data debe contener
        - nombre (str): Nombre del tipo de acta
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.nombre = data.nombre
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class ActaDocumentos(models.Model):
    codigo = models.CharField(max_length=250, blank=True, null=True, unique=True)
    tipo = models.ForeignKey(TipoActa)
    providencia = models.ForeignKey('self', blank=True, null=True)
    estatus = models.IntegerField(choices=ESTATUS_ACTA, blank=True, null=True)
    pst = models.ForeignKey(Pst, related_name='pst_actas_v_f', blank=True, null=True)
    verificacion = models.ForeignKey(Verificacion, null=True, blank=True, default=None)
    fiscalizacion = models.ForeignKey(Fiscalizacion, null=True, blank=True, default=None)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_notificacion = models.DateField(blank=True, null=True)
    observaciones = models.TextField(max_length=250, null=True, blank=True)
    hallazgos_materia = models.TextField(max_length=250, null=True, blank=True)
    hallazgos_condicion = models.TextField(max_length=250, null=True, blank=True)
    hallazgos_criterio = models.TextField(max_length=250, null=True, blank=True)
    hallazgos_efecto = models.TextField(max_length=250, null=True, blank=True)
    hallazgos_evidencia = models.TextField(max_length=250, null=True, blank=True)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Acta a partir
        de la información suministrada.
        Parametros:
        Storage data debe contener
        - codigo (str): Nombre del tipo de acta
        - tipo (object): Tipo de acta
        - providencia (object): Acta padre del modelo
        - estatus (int): Estado del acta
        - pst (object): Nombre del tipo de acta
        - verificacion (object): Verificación asociada al acta
        - fiscalizacion (object): Fiscalización asociada al acta
        - fecha_generacion (date): Fecha en la que se genera el acta
        - fecha_notificacion (date): Fecha en la que se genera la notificacion
        - observaciones (str): Observaciones del acta
        - hallazgos_materia (str): Materia
        - hallazgos_condicion (str): Condicion
        - hallazgos_criterio (str): Criterio
        - hallazgos_efecto (str): Efecto
        - hallazgos_evidencia (str): Evidencia
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.codigo = data.codigo
            obj.tipo = data.tipo
            obj.providencia = data.providencia
            obj.estatus = data.estatus
            obj.pst = data.pst
            obj.verificacion = data.verificacion
            obj.fiscalizacion = data.fiscalizacion
            obj.fecha_generacion = data.fecha_generacion
            obj.fecha_notificacion = data.fecha_notificacion
            obj.observaciones = data.observaciones
            obj.justificacion_cambio_de_estatus = data.justificacion_cambio_de_estatus
            obj.hallazgos_materia = data.hallazgos_materia
            obj.hallazgos_condicion = data.hallazgos_condicion
            obj.hallazgos_criterio = data.hallazgos_criterio
            obj.hallazgos_efecto = data.hallazgos_efecto
            obj.hallazgos_evidencia = data.hallazgos_evidencia
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def mostrar_boton_solicitud(self):
        return (
            self.tipo.nombre == u'Acta de reparo' and self.estatus == 1
        )


class ActaReparoAtributos(models.Model):
    periodo = models.CharField(max_length=250, blank=True, null=True, unique=True)
    ingresos_brutos = models.FloatField()
    calculo_segun_fiscalizacion = models.FloatField()
    monto_pagado_segun_declaracion = models.FloatField()
    diferencia_por_pagar = models.FloatField()
    acta = models.ForeignKey(ActaDocumentos)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Acta a partir
        de la información suministrada.
        Parametros:
        Storage data debe contener
        - periodo (str):
        - ingresos_brutos (float):
        - calculo_segun_fiscalizacion (float):
        - monto_pagado_segun_declaracion (float):
        - diferencia_por_pagar (float):
        - acta (Object):
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.periodo = data.periodo
            obj.ingresos_brutos = data.ingresos_brutos
            obj.calculo_segun_fiscalizacion = data.calculo_segun_fiscalizacion
            obj.monto_pagado_segun_declaracion = data.monto_pagado_segun_declaracion
            obj.diferencia_por_pagar = data.diferencia_por_pagar
            obj.acta = data.acta
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class Requisito(models.Model):
    requisito = models.TextField(max_length=250, null=True, blank=True)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Requisito a partir
        de la información suministrada.
        Parametros:
        Storage data debe contener
        - requisito (str): Requisito a guardar
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.requisito = data.requisito
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def __unicode__(self):
        return self.requisito


class ActaRequisito(models.Model):
    acta = models.ForeignKey(ActaDocumentos, related_name='actas_v_f')
    requisito = models.ForeignKey(Requisito)
    entrego = models.BooleanField(default=False)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto ActaRequisito a partir
        de la información suministrada.
        Parametros:
        Storage data debe contener
        - acta (str): Referencia al acta
        - requisito (str): Requisito a guardar
        - entrego (str): Entregó o no el requisito
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.acta = data.acta
            obj.requisito = data.requisito
            obj.entrego = data.entrego
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class ActaLogCambiarStatus(models.Model):
    acta = models.ForeignKey(ActaDocumentos, related_name='actas_log_c_s')
    estatus = models.IntegerField(choices=ESTATUS_ACTA)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_notificacion = models.DateField(blank=True, null=True)
    justificacion_cambio_de_estatus = models.TextField(max_length=250, null=True, blank=True)
    funcionario = models.ForeignKey(MinturUser)
    pst = models.ForeignKey(Pst)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto ActaRequisito a partir
        de la información suministrada.
        Parametros:
        Storage data debe contener
        - acta (str): Referencia al acta
        - requisito (str): Requisito a guardar
        - entrego (str): Entregó o no el requisito
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.acta = data.acta
            obj.estatus = data.estatus
            obj.fecha_generacion = data.fecha_generacion
            obj.fecha_notificacion = data.fecha_notificacion
            obj.justificacion_cambio_de_estatus = data.justificacion_cambio_de_estatus
            obj.funcionario = data.funcionario
            obj.pst = data.pst
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')
