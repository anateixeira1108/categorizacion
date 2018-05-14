# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from utils.gluon.storage import Storage
from registro.models import Pst
from apps.cuentas.models import MinturUser as User


EN_SEDE = 0

DOMICILIO_FISCAL = 1

GRUPAL = 2

TIPO_VERIFICACION = (
    (EN_SEDE, u'En sede administrativa'),
    (DOMICILIO_FISCAL, u'En domicilio fiscal'),
    # (GRUPAL, u'Grupal')
)

EN_PROCESO = 1

CONCLUIDA = 2

ESTATUS_VERIFICACION = (
    (EN_PROCESO, u'En proceso'),
    (CONCLUIDA, u'Concluida')
)


class Verificacion(models.Model):
    """
    Modelo Direcciones
    Contiene las direcciones para cada prestador de servicio turístico
    """
    pst = models.ForeignKey(Pst)
    rif = models.CharField(max_length=20, blank=False)
    tipo_verificacion = models.IntegerField(choices=TIPO_VERIFICACION, default=EN_SEDE)
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(choices=ESTATUS_VERIFICACION, default=EN_PROCESO)
    observaciones = models.TextField(null=True, blank=False)
    conclusiones = models.TextField(null=True, blank=True)


class FuncionariosVerificacion(models.Model):
    """
    Modelo Direcciones
    Contiene las direcciones para cada prestador de servicio turístico
    """
    es_coordinador = models.BooleanField(default=False)
    es_apoyo = models.BooleanField(default=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL)
    verificacion = models.ForeignKey(Verificacion)
    asignado_el = models.DateTimeField()

