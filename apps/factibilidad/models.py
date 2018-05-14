# -*- coding: utf-8 -*-

from django.db import models
from venezuela.models import Estado, Municipio, Parroquia

from registro.models import Pst
from apps.cuentas.models import MinturUser as User
from utils.validate_files import ContentTypeRestrictedFileField


CONSTRUCCION = 0
AMPLIACION = 1
DOTACION_EQUIPAMIENTO = 2
REMODELACION = 3
ADQUISICION_ESTABLECIMIENTO = 4
REPARACION = 5

TIPO_PROYECTO = (
    (CONSTRUCCION, u'Construcción'),
    (AMPLIACION, u'Ampliación'),
    (DOTACION_EQUIPAMIENTO, u'Dotación y Equipamiento'),
    (REMODELACION, u'Remodelación'),
    (ADQUISICION_ESTABLECIMIENTO, u'Adquisición establecimiento'),
    (REPARACION, u'Reparación')
)

TERRESTE = 0
ACUATICO = 1
AEREO = 2

UNIDAD_TRANSPORTE = (
    (TERRESTE, u'Terrestre'),
    (ACUATICO, u'Acuático'),
    (AEREO, u'Aéreo')
)

ESTABLECIMIENTO_TURISTICO = 0
TRANSPORTES_TURISTICOS = 1
ACTIVIDADES_RECREATIVAS = 2

TIPO_ACTIVIDAD = (
    (ESTABLECIMIENTO_TURISTICO, u'Establecimientos turístico'),
    (TRANSPORTES_TURISTICOS, u'Transportes turística'),
    (ACTIVIDADES_RECREATIVAS, u'Actividades recreativas')
)

SOLICITUD = 0
RENOVACION = 1

TIPO_SOLICITUD = (
    (SOLICITUD, u'Solicitud'),
    (RENOVACION, u'Renovación')
)

PLANO = 0
ACIDENTADO = 1
INCLINADO = 2

CARACTERISTICAS_TOPOGRAFICAS = (
    (PLANO, u'Plano'),
    (ACIDENTADO, u'Accidentado'),
    (INCLINADO, u'Inclinado')
)

CARRETERA = 0
CALLE = 1
AVENIDA = 2
VIA_PENETRACION = 3

TIPOS_VIALIDADES = (
    (CARRETERA, u'Carretera'),
    (CALLE, u'Calle'),
    (AVENIDA, u'Avenida'),
    (VIA_PENETRACION, u'Vía de penetracion')
)

RECREACIONAL = 0
TRANSPORTE = 1
ALIMENTACION = 2
SERVICIOS = 3
COMUNALES = 4

TIPOS_ASPECTOS = (
    (RECREACIONAL, u'Recreacional'),
    (TRANSPORTE, u'Transporte'),
    (ALIMENTACION, u'Alimentación'),
    (SERVICIOS, u'Servicios'),
    (COMUNALES, u'Comunales'),
)

TIPOS_INDOLE = (
    (RECREACIONAL, u'Recreacional'),
    (TRANSPORTE, u'Transporte'),
    (ALIMENTACION, u'Alimentación'),
    (SERVICIOS, u'Servicios'),
    (COMUNALES, u'Comunales'),
)

ACTIVO = 0
APROBADO = 1
ANULADO = 2
ESTADOS_FACTIBILIDAD = (
    (ACTIVO, u'Activo'),
    (APROBADO, u'Aprobado'),
    (ANULADO, u'Anulado'),
)

TAMANO_MAXIMO_ARCHIVO = 10485760  # 10 megas
RUTA_DOCUMENTOS = "."  # Definir la ruta real donde se guardaran los archivos


class Proyecto(models.Model):
    pst = models.ForeignKey(Pst)
    alojamiento = models.ForeignKey("UnidadesAlojamiento", null=True, blank=True)
    categoria = models.ForeignKey("Categoria", null=True, blank=True)
    nombre = models.CharField(max_length=75, null=True, blank=True)
    monto = models.CharField(null=True, blank=True, max_length=75)
    tipo_proyecto = models.IntegerField(choices=TIPO_PROYECTO, null=True, blank=True)
    tipo_actividad = models.IntegerField(choices=TIPO_ACTIVIDAD, null=True, blank=True)
    tipo_solicitud = models.IntegerField(choices=TIPO_SOLICITUD, null=True, blank=True)
    empleos_directos = models.IntegerField(null=True, blank=True)
    empleos_indirectos = models.IntegerField(null=True, blank=True)
    otra_indole = models.CharField(max_length=75, blank=True)
    otro_aspecto = models.CharField(max_length=75, blank=True)
    creado_el = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User)
    justificacion = models.TextField(max_length=250, null=True, blank=True)
    estado = models.IntegerField(null=True, blank=True, choices=ESTADOS_FACTIBILIDAD, default=ACTIVO)


class DireccionProyecto(models.Model):
    estado = models.ForeignKey(Estado)
    municipio = models.ForeignKey(Municipio)
    parroquia = models.ForeignKey(Parroquia)
    proyecto = models.ForeignKey(Proyecto)
    direccion = models.CharField(max_length=200)
    zona_urbana = models.CharField(max_length=75)
    zona_rural = models.CharField(max_length=75)
    zit_mintur = models.CharField(max_length=75)
    parque_nacional = models.CharField(max_length=200)
    superficie = models.CharField(max_length=75)
    tipografia = models.IntegerField(choices=CARACTERISTICAS_TOPOGRAFICAS)
    otra_topografia = models.CharField(max_length=100)
    vialidad = models.IntegerField(choices=TIPOS_VIALIDADES)
    otra_vialidad = models.CharField(max_length=100)
    otro_servicio = models.CharField(max_length=100)


class ServicioProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    servicio_basico = models.ForeignKey("ServicioBasico")


class ServicioBasico(models.Model):
    nombre = models.CharField(max_length=75)


class UnidadesAlojamiento(models.Model):
    numero_habitaciones = models.IntegerField()
    numero_apartamentos = models.IntegerField()
    numero_suites = models.IntegerField()
    numero_cabanias = models.IntegerField()
    otro_alojamiento = models.CharField(max_length=75)


class AspectoSocial(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    tipo = models.IntegerField(choices=TIPOS_ASPECTOS)


class Indole(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    tipo = models.IntegerField(choices=TIPOS_INDOLE)


class UnidadTransporte(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    tipo = models.IntegerField(choices=UNIDAD_TRANSPORTE)


class Categoria(models.Model):
    hotel = models.IntegerField(null=True, blank=True)
    hotel_residencia = models.IntegerField(null=True, blank=True)
    posada = models.IntegerField(null=True, blank=True)
    posada_familiar = models.IntegerField(null=True, blank=True)
    parador_turistico = models.IntegerField(null=True, blank=True)
    balneario = models.IntegerField(null=True, blank=True)
    campamentos_estancias = models.IntegerField(null=True, blank=True)


class SocioTecnicoProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    # # Recaudos Establecimientos turísticos:
    archivo_titulo_propiedad = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_contrato = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_autorizacion = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_uso_turistico = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_memoria_descriptiva = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_presupuesto = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    ## Recaudos Transporte Turistico
    archivo_conformidad_competente = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_factura_proforma = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_visto_bueno = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    archivo_factibilidad_economica = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
    ## Actividades recreativas
    archivo_conformidad_aval = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS, content_types='application/pdf',
        max_upload_size=TAMANO_MAXIMO_ARCHIVO, blank=True, null=True,
    )
