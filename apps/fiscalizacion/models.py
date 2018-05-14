# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from utils.gluon.storage import Storage
from registro.models import Pst
from apps.cuentas.models import MinturUser as User

EN_PROCESO = 1

CONCLUIDA = 2

ESTATUS_FISCALIZACION = (
    (EN_PROCESO, u'En proceso'),
    (CONCLUIDA, u'Concluida')
)


class Fiscalizacion(models.Model):
    """
    Modelo Direcciones
    Contiene las direcciones para cada prestador de servicio turístico
    """
    pst = models.ForeignKey(Pst)
    rif = models.CharField(max_length=20, blank=False)
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    estatus = models.IntegerField(choices=ESTATUS_FISCALIZACION, default=EN_PROCESO)
    conclusiones = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)


class FuncionariosFiscalizacion(models.Model):
    """
    Modelo FuncionariosFiscalizacion
    Contiene las direcciones para cada prestador de servicio turístico
    """
    es_coordinador = models.BooleanField(default=False)
    es_apoyo = models.BooleanField(default=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL)
    fiscalizacion = models.ForeignKey(Fiscalizacion)
    asignado_el = models.DateTimeField()
