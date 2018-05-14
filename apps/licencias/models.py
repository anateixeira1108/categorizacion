# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from apps.cuentas.models import MinturUser
from registro.models import Sucursales
from mintur import fields as custom_fields
from utils.validate_files import ContentTypeRestrictedFileField


USER_MODEL = MinturUser
SUCURSAL = Sucursales

TAMANO_MAXIMO_ARCHIVO = 10485760  # 10 megas

ESTADO_INSPECCION_CHOICE = (
    ('False', u'Sin realizar'),
    ('True', u'Realizada'),
)

INSPE_ESPERA = 1
INSPE_APROBADA = 2
INSPE_NEGADA = 3


ESTADO_SOLIC_INSPECCION_CHOICE = (
    (INSPE_ESPERA, u'En espera'),
    (INSPE_APROBADA, u'Aprobada'),
    (INSPE_NEGADA, u'Negada'),
)

FORM_SOLICITUD = 1
FORM_INSPECCION = 2


TIPO_FORMULARIO_CHOICE = (
    (INSPE_ESPERA, u'Formulario de solicitud'),
    (INSPE_APROBADA, u'Formulario de inspeccion'),
)


LICEN_ACTIVA = 1
LICEN_REVOCADA = 2
LICEN_VENCIDA = 3


ESTADO_LICENCIA_CHOICE = (
    (LICEN_ACTIVA, u'Activa'),
    (LICEN_REVOCADA, u'Revocada'),
    (LICEN_VENCIDA, u'Vencida'),
)

TIPO_USUARIO_INSPEC = (
    (False, u"Analista"),
    (True, u"Pst"),
)


class ArchivoRecaudo(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    fecha_carga = models.DateTimeField(blank=False)
    recaudoid = models.ForeignKey('Recaudo', db_column='recaudoid')
    solicitud_licenciaid = models.ForeignKey('SolicitudLicencia', db_column='solicitud_licenciaid')
    certificado = models.BooleanField(blank=False, null=False, default=False)
    ruta = ContentTypeRestrictedFileField(
        upload_to='default/',
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )

    def __unicode__(self):

        return u'%s' % self.nombre

class ArchivoRespuesta(models.Model):
    nombre = models.CharField(max_length=255, blank=False)
    fecha = models.DateTimeField(blank=True, null=False)
    ruta = ContentTypeRestrictedFileField(
        upload_to='default/',
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % self.nombre


class EstatusSolicitud(models.Model):
    nombre = models.CharField(max_length=255, blank=False)
    codigo = models.CharField(max_length=50, unique=True)
    clase = models.CharField(max_length=255, blank=False, null=False, default='label-warning')
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s-%s' % (self.nombre, self.codigo)

class ValorPosible(models.Model):
    valor = models.CharField(max_length=255, blank=True)
    codigo = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return u'%s' % self.valor

class TipoRespuesta(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    codigo = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return u'%s' % self.nombre


class Pregunta(models.Model):
    item = models.CharField(max_length=255, blank=False)
    tipo_respuestaid = models.ForeignKey('TipoRespuesta', db_column='tipo_respuestaid')
    codigo = models.CharField(max_length=50, unique=True)
    valoresPosibles = models.ManyToManyField(ValorPosible,blank=True)


    def __unicode__(self):
        return u'%s' % self.item


class Formulario(models.Model):
    nombre = models.CharField(max_length=255, blank=False)
    fecha_creacion = models.DateTimeField(blank=True, null=False)
    tipo = models.IntegerField(choices=TIPO_FORMULARIO_CHOICE,blank=False, null=False)
    codigo = models.CharField(max_length=50, unique=True)
    preguntas = models.ManyToManyField(Pregunta)

    def __unicode__(self):
        return u'%s' % self.nombre


# class FormularioTienePregunta(models.Model):
#     formularioid = models.ForeignKey(Formulario, db_column='formularioid')
#     preguntaid = models.ForeignKey('Pregunta', db_column='preguntaid')


class HistoricoSolicitudesLicencias(models.Model):
    solicitud_licenciaid = models.ForeignKey('SolicitudLicencia', db_column='solicitud_licenciaid')
    usuariomodificar = models.ForeignKey(USER_MODEL)
    fecha = models.DateTimeField(blank=False, null=False)
    estatus_solicitudid = models.ForeignKey(EstatusSolicitud, db_column='estatus_solicitudid')
    observacion = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s' % self.solicitud_licenciaid


class Inspeccion(models.Model):
    fecha_creacion = models.DateTimeField(blank=False, null=False)
    fecha_inspeccion = models.DateTimeField(blank=False, null=False)
    solicitud_inspeccionid = models.ForeignKey('SolicitudInspeccion', db_column='solicitud_inspeccionid')
    estado = models.BooleanField(choices=ESTADO_INSPECCION_CHOICE,default=False)
    tipo_licenciaid = models.ForeignKey('TipoLicencia', db_column='tipo_licenciaid')
    inspectores = models.ManyToManyField(USER_MODEL, related_name='inspectores')




# class InspectoresDesignados(models.Model):
#     inspeccionid = models.ForeignKey(Inspeccion, db_column='inspeccionid')
#     auth_userid = models.ForeignKey(USER_MODEL)


class Notificacion(models.Model):
    asunto = models.CharField(max_length=255, blank=True)
    observacion = models.CharField(max_length=255, blank=False)
    fecha_emision = models.DateTimeField(blank=True, null=True)
    solicitud_licenciaid = models.ForeignKey('SolicitudLicencia', db_column='solicitud_licenciaid')
    estatus_solicitudid = models.ForeignKey(EstatusSolicitud, db_column='estatus_solicitudid')
    emisor = models.ForeignKey(USER_MODEL, related_name='emisor')
    receptor = models.ForeignKey(USER_MODEL, related_name='receptor')
    indicador = models.BooleanField(blank=False, null=False, default=False)

    def __unicode__(self):
        return u'%s' % self.observacion




# class PreguntaValorPosible(models.Model):
#     preguntaid = models.ForeignKey(Pregunta, db_column='preguntaid')
#     valores_posiblesid = models.ForeignKey('ValorPosible', db_column='valores_posiblesid')


class Recaudo(models.Model):
    nombre = models.CharField(max_length=600)
    codigo = models.CharField(max_length=50, unique=True)
    requerido= models.BooleanField(blank=False, default=False)
    sucursal= models.BooleanField(blank=False, default=False)

    def __unicode__(self):
        return u'%s-%s' % (self.codigo, self.nombre)


# class RecaudosTipolicencia(models.Model):
#     recaudosid = models.ForeignKey(Recaudos, db_column='recaudosid')
#     subtipo_licenciaid = models.ForeignKey('SubtipoLicencia', db_column='subtipo_licenciaid')


class Respuesta(models.Model):
    # preguntaid = models.ForeignKey(Pregunta, db_column='preguntaid')
    solicitud_licenciaid = models.ForeignKey('SolicitudLicencia', db_column='solicitud_licenciaid',blank=True, null=True)
    inspeccionid = models.ForeignKey(Inspeccion, db_column='inspeccionid', blank=True, null=True )
    fecha = models.DateTimeField(blank=True, null=True)
    auth_userid = models.ForeignKey(USER_MODEL)

# ESPECIALIZACION
class RespuestaDefinida(Respuesta):
    # respuestaid_respuesta = models.ForeignKey(Respuesta, db_column='respuestaid_respuesta', primary_key=True)
    respuesta_descripcion = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s' % self.respuesta_descripcion

class RespuestaIndefinida(Respuesta):
    # respuestaid_respuesta = models.ForeignKey(Respuesta, db_column='respuestaid_respuesta', primary_key=True)
    archivo_respuestaid = models.ForeignKey(ArchivoRespuesta, db_column='archivo_respuestaid')
    respuesta = models.CharField(max_length=255, blank=False)
    padre = models.ForeignKey('self', blank=True, null=True)
    significado = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.archivo_respuestaid


class SolicitudInspeccion(models.Model):
    solicitud_licenciaid = models.ForeignKey('SolicitudLicencia', db_column='solicitud_licenciaid')
    estado = models.IntegerField(choices=ESTADO_SOLIC_INSPECCION_CHOICE,default=INSPE_ESPERA)
    auth_userid = models.ForeignKey(USER_MODEL)
    tipo_usuario = models.BooleanField(choices=TIPO_USUARIO_INSPEC)
    fecha_solicitud = models.DateTimeField(blank=False, null=False)
    observacion = models.CharField(max_length=255, blank=True)
    

class SolicitudLicencia(models.Model):
    fecha_inicio = models.DateTimeField(blank=False, null=False)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    tipo_licenciaid = models.ForeignKey('TipoLicencia', db_column='tipo_licenciaid')
    estatus_solicitudid = models.ForeignKey(EstatusSolicitud, db_column='estatus_solicitudid')
    tipo_solicitudid = models.ForeignKey('TipoSolicitud', db_column='tipo_solicitudid')
    edicion = models.BooleanField(blank=False, default=False)
    usuario_pst_id = models.ForeignKey(USER_MODEL, related_name='Upst')
    analista_asignado = models.ForeignKey(USER_MODEL, related_name='analista', blank=True, null=True)
    result_inspeccion = models.BooleanField(blank=False, default=False)
    # sucursal = models.ForeignKey(SUCURSAL,blank=True, null=True)
    sucursal = custom_fields.BigForeignKey(SUCURSAL,blank=True, null=True)

    


# class SubtipoLicencia(models.Model):
#     nombre = models.CharField(max_length=255, blank=True)
#     tipo_licenciaid = models.ForeignKey('TipoLicencia', db_column='tipo_licenciaid')
#     codigo = modes.ls.CharField(max_length=50, unique=True)
#     recaudos = models.ManyToManyField(Recaudo)

#     def __unicode__(self):
#         return u'%s' % self.nombre


class TipoLicencia(models.Model):
    nombre = models.CharField(max_length=255, blank=False)
    codigo = models.CharField(max_length=50, unique=True)
    padre = models.ForeignKey('self', blank=True, null=True, related_name='tipo_padre_id')
    recaudos = models.ManyToManyField(Recaudo)
    formulario_id = models.ForeignKey(Formulario, db_column='formulario_id')
    url = models.CharField(max_length=255, blank=False, null=True)

    def __unicode__(self):
        return u'%s' % self.nombre


class TipoSolicitud(models.Model):
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return u'%s' % self.descripcion


class ValoresRdefinida(models.Model):
    valor_posibleid = models.ForeignKey(ValorPosible, db_column='valor_posibleid')
    descripcion = models.CharField(max_length=255)
    respuesta_definida = models.ForeignKey(RespuestaDefinida, db_column='respuesta_definidarespuesta')
    archivo_respuestaid = models.ForeignKey(ArchivoRespuesta, db_column='archivo_respuestaid')

    def __unicode__(self):
        return u'%s' % self.valor_posibleid

class LicenciaAsignada(models.Model):
    numero_licencia = models.IntegerField(blank=False, null=False)
    fecha_emision = models.DateTimeField(blank=False, null=False)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    fecha_renovacion = models.DateTimeField(blank=True, null=True)
    tipo_licenciaid = models.ForeignKey('TipoLicencia', db_column='tipo_licenciaid')
    solicitud_licenciaid = models.ForeignKey('SolicitudLicencia', db_column='solicitud_licenciaid')
    usuario_pst = models.ForeignKey(USER_MODEL)
    sucursal = custom_fields.BigForeignKey(SUCURSAL,blank=True, null=True)
    estatus = models.IntegerField(choices=ESTADO_LICENCIA_CHOICE,default=LICEN_ACTIVA)

    def __unicode__(self):
        return u'%s' % self.numero_licencia
