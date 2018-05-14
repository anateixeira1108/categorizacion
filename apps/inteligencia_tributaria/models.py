# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from registro.models import Pst


EN_SEDE = 0
DOMICILIO_FISCAL = 1
GRUPAL = 2

TIPO_VERIFICACION = (
    (EN_SEDE, u'En sede administrativa'),
    (DOMICILIO_FISCAL, u'En domicilio fiscal'),
    # (GRUPAL, u'Grupal')
)

VERIFICACION = 0
FISCALIZACION = 1
VERIFICACION_FISCALIZACION = 2

TIPO_SOLICITUD = (
    (VERIFICACION, u'Verificación'),
    (FISCALIZACION, u'Fiscalización'),
    (VERIFICACION_FISCALIZACION, u'Fiscalización Y Verificación')
)

APROBACION_SOLICITUD = 0
SOLICITUD_APROBADA = 1
SOLICITUD_NEGADA = 2

TIPOS_ESTADOS = (
    (APROBACION_SOLICITUD, u'A espera de aprobacion de solicitud'),
    (SOLICITUD_APROBADA, u'Solicitud aprobada'),
    (SOLICITUD_NEGADA, u'Solicitud negada')
)

GUARDIA_NACIONAL = 0
INFORMATICO = 1
ABOGADO = 2

TIPO_APOYO = (
    (GUARDIA_NACIONAL, u'Guardia nacional'),
    (INFORMATICO, u'Informático'),
    (ABOGADO, u'Abogado')
)


class Solicitud(models.Model):
    """
    Modelo Solicitud
    Contiene las solicitudes de inteligencia tributaria
    para crear una Ferificación o Fiscalización
    """
    pst = models.ForeignKey(Pst)
    tipo_solicitud = models.IntegerField(choices=TIPO_SOLICITUD, default=VERIFICACION)
    tipo_verificacion = models.IntegerField(choices=TIPO_VERIFICACION, null=True, blank=True)
    estado = models.IntegerField(choices=TIPOS_ESTADOS, default=APROBACION_SOLICITUD)
    desde = models.DateField()
    hasta = models.DateField()
    criterio = models.TextField(null=False)
    creado_el = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(max_length=250, null=True, blank=True)
    rif = models.CharField(max_length=25)


class FuncionariosSolicitud(models.Model):
    """
    Modelo FuncionariosSolicitud
    Contiene las asignaciones de los funcionarios para cada solicitud
    """
    es_coordinador = models.BooleanField(default=False)
    es_apoyo = models.BooleanField(default=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL)
    solicitud = models.ForeignKey(Solicitud)
    asignado_el = models.DateTimeField(auto_now_add=True)


class FuncionarioTipoApoyo(models.Model):
    """
    Modelo FuncionariosApoyo
    Contiene los funcionarios que apoyan al proceso de crear una solicitud
    """
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL)
    tipo_apoyo = models.IntegerField(choices=TIPO_APOYO)
