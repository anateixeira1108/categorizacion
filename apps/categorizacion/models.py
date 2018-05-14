# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

"""
    models.py

    Archivo de configuracion de modelos a ser utilizados dentro
    del modulo de calidad turistica
"""

try:
    # Importando modelos necesarios de fase 1
    
    import json
    import HTMLParser
    from django.db import models
    from datetime import datetime
    from django.db.models import Q
    from collections import OrderedDict
    from django.core.exceptions import *
    from utils.gluon.storage import Storage
    from django.utils.html import format_html
    from apps.cuentas.models import MinturUser
    from registro.models import Pst, Sucursales, TipoPst
    from django.core.exceptions import SuspiciousOperation
    from utils.validate_files import ContentTypeRestrictedFileField
    from venezuela.models import Ciudad, Estado, Municipio, Parroquia
    from django.core.validators import MaxValueValidator, MinValueValidator
   
    """
        Los siguientes modulos deben ser cargados al momento
        de realizar la integracion con fase 1
    """
    from django.core.exceptions import ValidationError
    from mintur import fields as custom_fields
    from apps.categorizacion.helpers.validations import *
    from apps.licencias import models as modelos_licencias
    from apps.cuentas.models import ROLE_PST, ROLE_FUNCIONARIO
    from apps.categorizacion.helpers.validaciones_tabulador import *
    from apps.categorizacion.helpers.constants import TIPO_DATO, INT
    from apps.categorizacion.helpers.model_list import get_pst_file_path
    from apps.categorizacion.helpers.model_list import get_comprobante_file_path
    from apps.categorizacion.helpers.model_list import get_folio_file_path
    from apps.categorizacion.helpers.model_list import get_funcionario_file_path
    from apps.categorizacion.helpers.model_list import get_funcionario_signature_file_path 
    from apps.categorizacion.helpers.model_list import get_archivo_file_path

except Exception, e:

    print "[!] Errores al momento de resolver dependencias. Imposible continuar."
    raise e


TAMANO_MAXIMO_ARCHIVO = 10485760  # 10MB

# Declaracion de constantes
USER_MODEL = MinturUser


"""
    Modelos sin claves foraneas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

#Fixtures made for the evaluation instrument construction
class TipoMedida(models.Model):
    nombre = models.CharField("Nombre", max_length= 255, blank = False, null=False)    
    descripcion = models.TextField(u"Descripción", max_length = 255, blank = True, null=True)
    administrable = True
    exclude = None
    grupo = "Tabulador"
    prioridad = 1
    show_name = "Tipo de medida"

    def __unicode__(self):
        return u'%s' % (self.nombre)

    def to_json(self):
        return OrderedDict([
            ('id',self.pk),
            ('Nombre',self.nombre),
            (u'Descripción',self.descripcion)
        ])     


#Fixtures made for the evaluation instrument construction
class TipoRespuesta(models.Model):
    nombre = models.CharField(
        "Nombre", 
        max_length = 255, 
        blank=False, 
        null=False
    )
    input_type = models.CharField(
        "Tipo de Campo",
        max_length = 255, 
        blank = False, 
        null = False
    )
    codigo = models.CharField(
        "Código", 
        max_length="10", 
        blank=False, 
        null=False
    )
    administrable=False
    exclude = None
    grupo = None
    show_name = "Tipo de respuesta"

    def __unicode__(self):
        return u'%s' %(self.nombre)

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Nombre', self.nombre),
            ('Tipo de Campo', self.input_type)
        ])


class Direccion(models.Model):
    nombre = models.CharField("Nombre", blank=False, max_length=255)
    descripcion = models.TextField(u"Descripción", blank=True)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5)
    administrable = False
    prioridad = None
    exclude = None
    grupo = None
    show_name = "Dirección"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),        
        (u'Abreviación', self.abreviacion)
        ]
    )


class Categoria(models.Model):
    nombre = models.CharField("Nombre", unique=True, blank=False, max_length=255)
    abreviacion = models.CharField(u"Abreviación", unique=True, blank=False, max_length=5)
    valor = models.IntegerField("Valor", blank=False, validators=[validate_negative, max_integer])
    tope_porcentual = models.FloatField("Tope Porcentual", blank=False, default= 15.0, validators=[validate_negative, max_integer])

    tipo_pst = models.ForeignKey(
        modelos_licencias.TipoLicencia,
        verbose_name = "Tipo de Prestador",
        blank=False,
        null=False
    )
    administrable = True
    exclude = None
    prioridad = 3
    show_name = "Categoría"
    grupo = 'Categorias'

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion),
        ('Valor', self.valor),
        ('Tipo de Prestador', self.tipo_pst.nombre.capitalize())
        ])


class TipoIcono(models.Model):
    representacion = models.CharField(
        u"Representación", 
        blank=False, 
        max_length=255
    )
    nombre = models.CharField(
        "Nombre", 
        blank=False,
        max_length=255
    )
    tipo_pst = models.ForeignKey(
        modelos_licencias.TipoLicencia,
        verbose_name = "Tipo de Prestador",
        blank=False,
        null=False,
        unique=True, 
    )
    administrable = True
    exclude = None
    prioridad = 1
    show_name = u"Representación por Categoría"
    grupo = 'Categorias'

    def __unicode__(self):
        return "%s - %s - %s" % (
            self.representacion, 
            self.nombre, 
            self.tipo_pst.nombre.capitalize()
        )

    def to_json(self):
        return OrderedDict([
         ('id',self.pk),
         (u'Representación',self.representacion),
         ('Nombre',self.nombre),
         ("Tipo de Prestador", self.tipo_pst.nombre.capitalize())
        ])

"""
    Seccion de parametros de configuracion
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
class ParametroConfiguracionManager(models.Manager):
    def get_queryset(self):
        return super(ParametroConfiguracionManager, self).get_queryset().filter(editable=True)


class ParametroConfiguracion(models.Model):
    clave = models.CharField(
        "Clave",
        max_length=255,
        unique = True,
        blank=False,
        null=False
    )
    valor = models.TextField("Valor", max_length=2048)
    tipo = models.IntegerField(
        "Tipo de Dato",
        blank = False,
        null = False,
        choices = TIPO_DATO,
        default = INT)
    editable = models.BooleanField('Editable', default=True,null = False, blank=False)
    prioridad = 1
    grupo = "Sistema"
    administrable = True
    exclude = ('clave', 'tipo', 'editable')
    show_name = "Parámetro de configuración"
    objects = ParametroConfiguracionManager()

    #Override
    def delete(self, *args, **kwargs):
        raise SuspiciousOperation(
            "Operacion no autorizada para instancia de \
            parametro de configuración"
            )
    
    #Override
    def save(self, *args, **kwargs):
        if self.pk is not None and self.editable:            
            super(ParametroConfiguracion, self).save(*args, **kwargs)
        else:
            raise SuspiciousOperation(
                "Operacion no autorizada para instancia de \
                parametro de configuración"
                )

    def __unicode__(self):
        return self.clave.capitalize()

    def to_json(self):
       return OrderedDict([
        ('id',self.pk),
        ('Clave',self.clave),
        ('Valor',self.valor),
        ])

"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class PlantillaDocumento(models.Model):
    formato = models.CharField("Formato", unique=True, max_length=255)# Ruta a la plantilla
    administrable = False
    exclude = None
    show_name = "Plantilla de documento"
    grupo = None
    prioridad = None

    def __unicode__(self):
        return self.formato.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Formato', self.formato)
        ])


class TipoAsignacion(models.Model):
    nombre = models.CharField("Nombre", max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5, blank=False)
    administrable = False
    exclude = None
    prioridad = None
    grupo = None
    show_name = "Tipo de asignación"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion)
        ])


class TipoComentario(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5, blank=False)
    administrable = False
    prioridad = 3
    exclude = None
    grupo = "Encuesta LSR"
    show_name = "Tipo de comentario"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion)
        ])


class TipoDocumentoIdentidad(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=False)
    administrable = False
    prioridad = 6
    exclude = None
    grupo = "Encuesta LSR"
    show_name = "Tipo de documento de identidad"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize())
        ])


class TipoRequisitoPago(models.Model):
    nombre = models.CharField("Nombre", max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5, blank=False)
    administrable = False
    prioridad = 1
    exclude = None
    grupo = "Solicitudes de Libros"
    show_name = "Tipo de requisito de pago"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion)
        ])


class TipoRol(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=False)
    descripcion = models.TextField(u"Descripción", blank=False)
    administrable = False
    exclude = None
    prioridad = None
    grupo = None
    show_name = "Tipo de rol"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Descripción', self.descripcion)
        ])

class TipoSolicitud(models.Model):
    nombre = models.CharField("Nombre", max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5, blank=False)
    administrable = False
    exclude = None
    prioridad = None
    grupo = None
    show_name = "Tipo de solicitud"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion)
        ])


class TipoSubseccion(models.Model):
    nombre = models.CharField("Nombre", max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", max_length=5, blank=False)
    tipopadre = models.ForeignKey(
        'TipoSubseccion', 
        verbose_name = "Tipo Subseccion Padre",
        null=True, 
        blank=True,
        default = None
    )
    prioridad = 0
    exclude = None
    grupo = "Tabulador"
    administrable = False
    show_name = "Tipo de subsección"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Nombre', self.nombre.capitalize()),
            (u'Abreviación', self.abreviacion),
            (u"Tipo Subsección Padre", self.tipopadre.nombre if self.tipopadre is not None else 'N/A')
        ])


"""
    Modelos con claves foraneas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
class Solicitud(models.Model):
    pst = custom_fields.BigForeignKey(Pst, verbose_name = "Prestador", related_name="pst_genera_solicitudes_de_categorizacion")
    estatus = models.ForeignKey('Estatus', verbose_name = "Estatus")    
    fecha_apertura = models.DateTimeField("Fecha de apertura", auto_now_add=True)
    sucursal = models.ForeignKey(Sucursales, blank=True, null=True, verbose_name = "Sucursal")
    fecha_modificacion_estado=models.DateTimeField('Fecha de modificacion de estado', blank=True, null=True)
    fecha_clausura = models.DateTimeField("Fecha de clausura", blank=True, null=True)
    funcionario = models.ForeignKey('Funcionario', verbose_name = "Funcionario Actual", blank=True, null=True, related_name="funcionario")
    funcionario_extra = custom_fields.BigForeignKey('Funcionario', verbose_name = "Funcionario Extra", blank=True, null=True, related_name="funcionario_extra")
    pst_categoria_doc = custom_fields.BigForeignKey('PstCategoriaDocumentoCompuesto', verbose_name = "Documento compuesto de categoría", blank=True, null=True)
    permitir_prorroga = models.BooleanField('¿Inhabilitar Prorroga?', default=True)
    renovar =  models.BooleanField('Renovacion', default=False)
    dias_prorroga = models.PositiveIntegerField(u"Días de prórroga", max_length=255, null=True)
    """
        Asociacion para mecanismo de control de versiones
        con respecto a tabulador actual.
    """
    tabulador = custom_fields.BigForeignKey(
        'Tabulador', 
        verbose_name = "Tabulador Asociado", 
        blank = False, null = False
    )
    administrable = False
    grupo = None
    prioridad = None
    exclude = ('fecha_apertura', 'fecha_clausura',)
    show_name = "Solicitud"

    def __unicode__(self):
        funcionario = '-'
        if self.funcionario :
            funcionario +=" "+self.funcionario.nombre + " " + self.funcionario.apellido
        return (self.pst.nombres + " - " + self.estatus.nombre + funcionario)


    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Prestador', self.pst.nombres),
            ('Estatus', self.estatus.nombre.capitalize()),
            ('Sucursal', self.sucursal.nombre.capitalize() if self.sucursal is not None else "Sede Principal"),
            ('Fecha de apertura', self.fecha_apertura.strftime('%d/%m/%Y') if self.fecha_apertura is not None else '-'),
            ('Fecha de clausura', self.fecha_clausura.strftime('%d/%m/%Y') if self.fecha_clausura is not None else '-')
        ])


class Asignacion(models.Model):
    funcionario = custom_fields.BigForeignKey('Funcionario', verbose_name = "Funcionario")
    tipo_asignacion = models.ForeignKey('TipoAsignacion', verbose_name = "Tipo de Asignación")
    solicitud = custom_fields.BigForeignKey('Solicitud', null=True, verbose_name = "Solicitud")
    solicitud_libro = custom_fields.BigForeignKey('SolicitudLibro', null=True, verbose_name = "Solicitud LSR")
    fecha_asignacion = models.DateTimeField("Fecha de asignacion", auto_now_add=True)
    asignacion_habilitada = models.BooleanField(
        'Asignacion Habilitada', 
        default=True, 
        blank=False, 
        null=False
    )
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Asignación"
    
    def __unicode__(self):
        return '%s - %s' %(self.funcionario, self.tipo_asignacion)

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Funcionario', "%s %s" % (self.funcionario.nombre, self.funcionario.apellido)),
            (u'Tipo de Asignación', self.tipo_asignacion.nombre),
            ('Solicitud', self.solicitud.pk)
        ])


class AspectoFundamental(models.Model):
    respuesta_tabulador = custom_fields.BigForeignKey('RespuestaTabulador', verbose_name = "Tabulador del Prestador")
    nombre = models.CharField("Nombre", max_length=2048, blank=False)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Aspecto Fundamental"

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Nombre', self.nombre),
            ('Tabulador del Prestador', self.respuesta_tabulador.pk)
        ])


class TipoAspectoFundamental(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255,blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, blank=False, max_length=5)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Tipo de Aspecto Fundamental"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Nombre', self.nombre),
            ('Abreviación', self.abreviacion)
        ])


class AspectoFundamentalConfig(models.Model):
    nombre = models.CharField(
        "Nombre",
        max_length=255,
        blank=False
    )
    tabulador = custom_fields.BigForeignKey( "Tabulador", verbose_name="Tabulador" )
    
    peso_porcentual = models.FloatField(
        verbose_name = "Peso porcentual",
        validators = [ MinValueValidator(0), MaxValueValidator(100.0) ],
        blank = True,
        null = True
    )    
    tipo_aspecto = models.ForeignKey(
        'TipoAspectoFundamental', 
        blank= False, null= False, verbose_name = "Tipo de aspecto fundamental"
    )
    administrable = False
    prioridad = 5
    exclude = None
    grupo = "Tabulador"
    show_name = "Configuración de Aspectos Fundamentales"

    def __unicode__(self):
        return "%s-v%d - %s" % (
            self.tabulador.nombre,
            self.tabulador.version,
            self.nombre.capitalize()
        )

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Nombre', self.nombre),
            ('Tabulador', "%s-v%d" % (self.tabulador.nombre, self.tabulador.version))
        ])


class TipoDocumentoCompuesto(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255,blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, blank=False, max_length=5)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Tipo de Documento"

    def __unicode__(self):
        return self.nombre.capitalize()

class Documento(models.Model):
    plantilla_documento = models.ForeignKey('PlantillaDocumento', verbose_name = "Plantilla Documento", null=True)
    fecha_emision = models.DateTimeField(u"Fecha de emisión", auto_now_add=True) # Debe ser excluido en el render de los formularios
    fecha_aprobacion = models.DateTimeField(u"Fecha de aprobación", blank=True, null=True) # Debe ser excluido en el render de los formularios
    nombre = models.CharField("Nombre", unique=True, max_length=255,blank=False)
    tipo_documento_compuesto = models.ForeignKey('TipoDocumentoCompuesto', verbose_name = "Tipo Documento Compuesto", blank=False, null=True)
    extension = models.CharField(u"Extensión", max_length=255, blank=False)
    ruta_documento = ContentTypeRestrictedFileField(
        upload_to = get_funcionario_file_path,
        content_types=['application/pdf'],
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
        max_length = 255,
    )

    firmado = models.BooleanField("Firmado", default=False)
    eliminado = models.BooleanField("Eliminado", default=False)
    
    #Campos importados de fase 1 de la tabla DocumentoElectronico para incluir firmas digitales

    firmado_por = custom_fields.BigForeignKey(USER_MODEL,null=True, blank=True)
    firmado_el = models.DateTimeField(null=True)
    coletillado = models.BooleanField(default=False)
    coletillado_el = models.DateTimeField(null=True)

    administrable = False
    exclude = ('fecha_emision','fecha_aprobacion',)
    grupo = None
    prioridad = None
    show_name = "Documento"

    def __unicode__(self):
        return (self.nombre +" - "+ str(self.fecha_emision) +" - "+ str(self.fecha_aprobacion))

    def to_json(self):
        if self.fecha_aprobacion is not None:
            return OrderedDict([
            ('id', self.pk),
            ('Nombre', self.nombre.capitalize()),
            (u'Extensión', self.extension),
            ('Ruta del Documento', self.ruta_documento)
            (u'Fecha Emisión', self.fecha_emision.strftime('%d/%m/%Y')),
            (u'Fecha de Aprobación', self.fecha_aprobacion.strftime('%d/%m/%Y'))
        ])

    @classmethod
    def create(cls, data):
        if isinstance(data, Storage):
            obj = cls()
            obj.nombre = data.nombre
            obj.extension = data.extension
            obj.fecha_emision = data.fecha_emision
            obj.fecha_aprobacion = data.fecha_aprobacion
            obj.plantilla_documento = data.plantilla_documento
            obj.ruta_documento = data.ruta_documento
            obj.tipo_documento_compuesto = data.tipo_documento_compuesto

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

class CredencialesOtorgadas(models.Model):
    """
    Clase que guarda los usuarios que tienen firma delegada
    user: Instancia del usuario mintur User
    tiene_firma_delegada: boolean que identifica que tenga la firma activa
    coletilla: Condiciones de otorgamientos para la firma electronica
    area: Area a la que pertenece el usuario que tiene la firma
    creado_el: Fecha de creacion
    """
    user = custom_fields.BigForeignKey(USER_MODEL, null=True)
    tiene_firma_delegada = models.BooleanField(default=True)
    coletilla = models.TextField(max_length=500, null=False, blank=False)
    cargo = models.CharField(max_length=150, null=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None

    def __unicode__(self):
        return (self.user +" - "+ self.cargo )

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Funcionario', self.user),        
            ('Tiene firma delegada', self.tiene_firma_delegada),
            ('Coletilla', self.coletilla),
            ('Cargo', self.cargo),
            ('Creado el', self.creado_el)
        ])

class Estatus(models.Model):
    tipo_solicitud = models.ForeignKey('TipoSolicitud', verbose_name = "Tipo de Solicitud")
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=False)
    descripcion = models.CharField(u"Descripción", max_length=255)
    abreviacion = models.CharField(u"Abreviación", unique=True, blank=False, max_length=5)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Estatus"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            ('Tipo de Solicitud', self.tipo_solicitud.nombre),        
            ('Nombre', self.nombre),
            (u'Descripción', self.descripcion),
            (u'Abreviación', self.abreviacion)
        ])


class Folio(models.Model):
    lsr_fisico = custom_fields.BigForeignKey('LsrFisico', verbose_name = "LSR Físico")
    consignacion = custom_fields.BigForeignKey('Consignacion', verbose_name = "Consignación", null=True)
    file_path = ContentTypeRestrictedFileField(
        upload_to = get_folio_file_path,
        content_types=['application/pdf', 'image/jpeg', 'image/png'],
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
        max_length = 255,
    )
    numero = models.PositiveIntegerField(u"Número", max_length=255)
    extension = models.CharField(u"Extensión", max_length=255, null=True)
    fecha_carga = models.DateTimeField("Fecha de Carga", auto_now_add=True)
    fecha_notificacion = models.DateTimeField(u"Fecha notificación", blank=True, null=True)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Folio"

    def to_json(self):
        return OrderedDict([
            ('id', self.pk),
            (u'LSR Físico', self.lsr_fisico.pk),
            ('File path', self.file_path),
            ('Nombre', self.nombre),
            (u'Extensión', self.extension),
            ('Fecha de Carga', str(self.fecha_carga))
        ])

    @classmethod
    def create(cls, data):
        if isinstance(data, Storage):
            obj = cls()
            obj.lsr_fisico = data.lsr_fisico
            obj.file_path = data.file_path
            obj.extension = data.extension
            obj.numero = data.numero
            obj.fecha_carga = data.fecha

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

class Funcionario(models.Model):
    nombre = models.CharField("Nombre", max_length=255, blank=False)
    apellido = models.CharField("Apellido", max_length=255, blank=False)
    user = models.ForeignKey(
        USER_MODEL,
        verbose_name="Usuario",
        blank=False,
        null=False,
        unique = True
    )
    direccion = custom_fields.BigForeignKey('Direccion', verbose_name="Dirección", blank=False, null=False)
    tiporol = models.ForeignKey('TipoRol', verbose_name="Tipo Rol", blank=False, null=False)
    cedula = models.CharField('Cedula',unique=True,max_length=20,blank=False)
    habilitado = models.BooleanField("Habilitado")
    administrable = True
    prioridad = 1
    exclude = None
    grupo = "Funcionarios Internos"
    show_name = "Funcionario"

    class Meta:
        unique_together = ("user", "direccion")

    def __unicode__(self):
        return u'%s %s' % (self.nombre.capitalize(),self.apellido.capitalize())

    def to_json(self):
        return OrderedDict([
                ('id',self.pk),
                ('Cedula',self.cedula),
                ('Nombre',self.nombre),
                ('Apellido',self.apellido),
                ('Habilitado', "Si" if self.habilitado else "No")
            ])

    # Override
    # Permitir la insercion solo de un usuario del tipo ministro
    # y viceministro una sola vez
    def save(self, *args, **kwargs):        
        if self.tiporol.nombre in ['ministro', 'viceministro']:
            if not self.pk and not len(Funcionario.objects.filter(
                tiporol__nombre=self.tiporol.nombre)):
                super(Funcionario, self).save(*args, **kwargs)
            else:
                raise FieldError("""
                    Campo TipoRol :%s duplicado, solo se permite una
                    instancia de este tipo de funcionario. Instancia encontrada (%s)
                    """ % (
                        self.tiporol.nombre,
                        Funcionario.objects.get(tiporol__nombre=self.tiporol.nombre)
                    )
                )
        else:
            self.habilitado = True if self.tiporol.nombre == 'administrador' else self.habilitado
            super(Funcionario, self).save(*args, **kwargs)
        

"""
    Cuerpo de los tabuladores de encuesta para los Libros de Sugerencia y Reclamos
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

class Entrada(models.Model):
    tipo_comentario = models.ForeignKey(
        'TipoComentario',
        verbose_name = "Tipo de Comentario"
    )
    turista = custom_fields.BigForeignKey(
        'Turista',
        verbose_name = "Turista"
    )
    lsr = custom_fields.BigForeignKey(
        'LsrDigital',
        verbose_name = "LSR Digital"
    )
    severidad = models.ForeignKey(
        'Severidad',
        verbose_name = "Severidad",
        blank=True,
        null=True
    )
    estatus = models.ForeignKey(
        'Estatus',
        verbose_name = "Estatus"
    )   
    comentario = models.CharField(
        "Comentario",
        max_length=100,
        blank=False
    )
    fecha_entrada = models.DateTimeField(
        "Fecha de Entrada",
        auto_now_add=True
    )  
    es_anonimo = models.BooleanField(
        default = False, 
        verbose_name = u"¿Desea permanecer anónimo?",
        null = False
    )
    show_name = "Entrada"
    administrable = False
    exclude = None
    prioridad = None
    grupo = None    

    def __unicode__(self):
        return self.comentario

    def to_json(self):
        return{
        'id': self.pk,
        'Tipo de Comentario': self.tipo_comentario.pk,
        'Turista': self.turista.pk,
        'LSR Digital': self.lsr,
        'Severidad': self.severidad.pk,
        'Estatus': self.estatus.pk,
        'Ciudad': self.ciudad.pk,
        'Comentario': self.comentario,
        'Fecha': self. fecha_entrada.strftime( '%d-%m-%Y' )
        }


class SeccionEncuesta(models.Model):    
    nombre = models.CharField("Nombre", unique=True, max_length=255)
    administrable = False
    exclude = None
    prioridad = 3
    grupo = "Encuesta LSR"
    show_name = "Sección de encuesta"

    def __unicode__(self):
        return "pito"

    def to_json(self):
        return OrderedDict([
        ('id',self.pk),        
        ('Nombre',self.nombre)
        ])


class Encuesta(models.Model):    
    nombre = models.CharField(
        "Nombre",
        unique=True,
        max_length=255
    )
    tipo_pst = models.ForeignKey(
        modelos_licencias.TipoLicencia,
        verbose_name="Tipo de Pst"
    )
    prioridad = 2
    exclude = None
    administrable = False
    grupo = "Encuesta LSR"
    show_name = "Encuesta"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id',self.pk),        
        ('Nombre',self.nombre)
        ])


class ElementoEncuestaSeccionEncuesta(models.Model):    
    elemento_encuesta = custom_fields.BigForeignKey(
        'ElementoEncuesta',
        verbose_name="Elemento Encuesta"
    )
    seccion_encuesta = custom_fields.BigForeignKey(
        'SeccionEncuesta',
        verbose_name="Sección Encuesta"
    )
    encuesta = custom_fields.BigForeignKey(
        'Encuesta',
        verbose_name = "Encuesta Asociada"
    )
    administrable = False
    exclude = None
    prioridad = 5
    grupo = "Encuesta LSR"
    show_name = "Relación Encuesta"

    def __unicode__(self):
        return "%s - %s - %s" % (
            self.seccion_encuesta.nombre,
            self.elemento_encuesta.nombre,
            self.encuesta.nombre
        )

    def to_json(self):
        return OrderedDict([
        ('id',self.pk), 
        (u'Sección', self.seccion_encuesta.nombre),
        ('Elemento', self.elemento_encuesta.nombre), 
        ('Encuesta', self.encuesta.nombre)     
        ])


class ElementoEncuesta(models.Model):
    nombre = models.CharField(
        "Nombre",
        unique=True,
        max_length=255,blank=False
    )    
    tipo_valoracion = models.ForeignKey(
        "TipoValoracion",
        verbose_name = u"Tipo de Valoración"
    )
    administrable = False
    prioridad = 4
    exclude = None
    grupo = "Encuesta LSR"
    show_name = "Elemento de Encuesta"

    def __unicode__(self):
        return u"Nombre: %s" %(
            self.nombre.capitalize()
            )

    def to_json(self):
        return OrderedDict([
        ('id',self.pk),
        ('Nombre', self.nombre.capitalize())
        ])
       

class RespuestaEncuesta(models.Model):
    entrada = custom_fields.BigForeignKey(
        'Entrada',
        verbose_name = "Entrada Asociada",
        null=False, blank=False
        )
    valoracion = models.ForeignKey(
        'Valoracion',
        verbose_name = "Valoración",
        null=False, blank=False
        )
    observacion = models.TextField(
        'Observaciones',
        max_length = 255,
        null = True, blank = True
        )
    elemento_encuesta = custom_fields.BigForeignKey(
        'ElementoEncuesta',
        verbose_name = "Elemento que responde"
        ,null=False, blank=False
        )
    seccion_encuesta = custom_fields.BigForeignKey(
        'SeccionEncuesta',
        verbose_name = "Sección que responde"
        ,null=False, blank=False
        )
    administrable = True
    exclude = None
    grupo = None
    prioridad = None

    def __unicode__(self):
        return u"Entrada realizada por: %s %s - Elemento: %s - Valoracion: %s" % (
            self.entrada.turista.nombre,
            self.entrada.turista.apellido,
            self.elemento_encuesta.nombre,
            self.valoracion
            )

    def to_json(self):
        return OrderedDict([
            ('Entrada realizada por', self.entrada.turista),
            ('Elemento', self.elemento_encuesta.nombre),
            (u'Valoración',self.valoracion)
            ])


class Valoracion(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5, blank=False)
    puntaje = models.IntegerField(verbose_name='Puntaje', null=False, blank = True, default=0)
    tipo_valoracion = models.ForeignKey(
        "TipoValoracion",
        verbose_name = u"Tipo de Valoración"        
    )
    administrable = False
    prioridad = 1
    exclude = None
    grupo = "Encuesta LSR"
    show_name = "Valoración"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion)
        ])


class Severidad(models.Model):
    nombre = models.CharField("Nombre", max_length=255, blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5, blank=False)
    valor = models.IntegerField("Valor", unique=True, blank=False, validators=[validate_negative, max_integer])
    administrable = False
    exclude = None
    prioridad = 10
    grupo = "Encuesta LSR"
    show_name = "Severidad"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre.capitalize()),
        (u'Abreviación', self.abreviacion),
        ('Valor', self.valor)
        ])


class TipoValoracion(models.Model):
    nombre = models.CharField(
        "Nombre", 
        max_length = 255, 
        blank=False, 
        null= False
    )
    abreviacion = models.CharField(
        u"Abreviación", 
        unique = True, 
        max_length = 5, 
        blank = False
    )
    prioridad = 0
    administrable = False    
    exclude = None        
    grupo = "Encuesta LSR"
    show_name = u"Tipo Valoración"


    def __unicode__(self):
        return "%s - %s" % (self.nombre, self.abreviacion)

    def to_json(self):
        return OrderedDict([
        ('id', self.pk),
        ('Nombre', self.nombre),
        (u'Abreviación', self.abreviacion)
        ])
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class LsrDigital(models.Model):
    pst = custom_fields.BigForeignKey(Pst, verbose_name = "Prestador")
    sucursal = custom_fields.BigForeignKey(Sucursales, blank=True, null=True, verbose_name = "Sucursal")
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "LSR Digital"

    def __unicode__(self):
        return "Pst: %s %s - Sucursal: %s" % (
            self.pst.nombres,self.pst.apellidos, 
            self.sucursal.nombre if self.sucursal is not None else "Sede Principal")

    def to_json(self):
        return{
        'id': self.pk,
        'Prestador': self.pst.nombres,
        'Sucursal': self.sucursal.nombre if self.sucursal is not None else "Sede Principal",
        }


class LsrFisico(models.Model):

    pst = custom_fields.BigForeignKey(
        Pst,
        verbose_name = "Prestador"
    )

    sucursal = custom_fields.BigForeignKey(
        Sucursales, 
        blank=True, 
        null=True, 
        verbose_name = "Sucursal"
    )

    solicitud_libro = custom_fields.BigForeignKey(
        'SolicitudLibro',
        verbose_name = u"Número de Solicitud"
    )

    identificador = models.CharField(
        "Identificador",
        unique=True,
        max_length=255
        #validator=validate_negative
    )

    grupo = None
    exclude = None
    administrable = False
    show_name = u"LSR Físico"

    def to_json(self):
        return{
        'id': self.pk,
        'Prestador': self.pst.nombres,
        'Sucursal': self.sucursal.nombre if self.sucursal is not None else "Sede Principal",
        u'Número de Solicitud': self.solicitud_libro.pk,
        'Identificador': self.identificadors
        }


class Consignacion(models.Model):

    solicitud_libro = custom_fields.BigForeignKey(
        'SolicitudLibro',
        verbose_name = u"Número de Solicitud"
    )

    estatus = models.ForeignKey(
        'Estatus',
        verbose_name = "Estatus"
    )

    funcionario = models.ForeignKey(
        'Funcionario', 
        verbose_name = 
        "Funcionario Actual", 
        blank=True, 
        null=True, 
        related_name="funcionarioconsignacion"
    )

    observacion = models.TextField(
        u"Observación",
         default='No se han registrado observaciones'
    )

    lsr_fisico = models.ForeignKey(
        'LsrFisico',
        verbose_name="Libro Físico"
    )

    documento = custom_fields.BigForeignKey(
        'Documento', 
        verbose_name = "Documento",
        null=True
    )
    

    grupo = None
    exclude = None
    administrable = False
    show_name = u"Consignación"

    def to_json(self):
        return{
        'id': self.pk,
        u'Número de Solicitud': self.solicitud_libro.pk,
        'Estatus': self.estatus,
        'Funcionario': self.funcionario.nombre + " " + self.funcionario.apellido if self.funcionario else "",
        }


class Notificacion(models.Model):
    emisor = custom_fields.BigForeignKey(USER_MODEL, related_name='notificacion_tiene_emisor', verbose_name = "Emisor")
    receptor = custom_fields.BigForeignKey(USER_MODEL, related_name='notificacion_tiene_receptor', verbose_name = "Receptor")
    solicitud = custom_fields.BigForeignKey('Solicitud', verbose_name = "Solicitud", null=True)
    solicitud_libro = custom_fields.BigForeignKey('SolicitudLibro', verbose_name = "Solicitud Libro", null=True)
    asunto = models.CharField("Asunto", max_length=255, blank=True, null=True)
    observacion = models.TextField(u"Observación", blank=True, default='No se han registrado observaciones')
    fecha_emision = models.DateTimeField(u"Fecha de Emisión", auto_now_add=True) 
    estatus_actual= models.ForeignKey('Estatus', verbose_name = "Estatus Actual", blank=False, null=False, related_name="estatus_actual")
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Notificación"

    def __unicode__(self):
        return self.observacion

    def to_json(self):
        return{
        'id': self.pk,
        'Emisor': self.emisor.pk,
        'Receptor': self.receptor.pk,
        'Solicitud': self.solicitud.pk,
        'Solicitud Libro': self.solicitud_libro.pk,
        'Estado': self.estatus_actual.pk,
        'Asunto': self.asunto,
        u'Observación': self.observacion,
        u'Fecha de Emisión': self.fecha_emision.strftime('%d/%m/%Y')
        }

    @classmethod
    def create(cls, data):
        if isinstance(data, Storage):
            obj = cls()
            obj.emisor = data.emisor
            obj.receptor = data.receptor
            obj.solicitud = data.solicitud
            obj.asunto = data.asunto
            obj.observacion = data.observacion
            obj.fecha_emision = data.fecha_emision
            obj.estatus_actual = data.estatus_actual
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class NotificacionBackup(models.Model):
    emisor = custom_fields.BigForeignKey(USER_MODEL, related_name='notificacion_backup_emisor', verbose_name = "Emisor")
    receptor = custom_fields.BigForeignKey(USER_MODEL, related_name='notificacion_backup_receptor', verbose_name = "Receptor")
    solicitud = custom_fields.BigForeignKey('Solicitud', verbose_name = "Solicitud")
    asunto = models.CharField("Asunto", max_length=255, blank=True, null=True, default=None)
    observacion = models.TextField(u"Observación", blank=True, default='No se han registrado observaciones')
    fecha_emision = models.DateTimeField(u"Fecha de Emisión") 
    estatus_actual= models.ForeignKey('Estatus', related_name="estatus_backup_actual", verbose_name = "Estatus Actual", blank=False, null=False)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Notificación Backup"

    def to_json(self):
        return{
            'id': self.pk,
            'Emisor': self.emisor.pk,
            'Receptor': self.receptor.pk,
            'Solicitud': self.solicitud.pk,
            'Estado': self.estado.pk,
            'Asunto': self.asunto,
            u'Observación': self.observacion,
            u'Fecha de Emisión': self.fecha_emision.strftime('%d/%m/%Y')
        }


class NotificacionDocumentoCompuesto(models.Model):
    notificacion = custom_fields.BigForeignKey(
        'Notificacion',
        verbose_name = "Notificación",
        null=True, 
        blank=True
    )
    documento = custom_fields.BigForeignKey('Documento', verbose_name = "Documento")
    notificacion_backup = custom_fields.BigForeignKey('NotificacionBackup', verbose_name = "Notificación Backup", blank=True, null=True)
    administrable = False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Notificación de Documento Compuesto"
    
    def to_json(self):
        return{
        'id': self.pk,
        u'Notificación': self.notificacion.pk,
        'Documento': self.documento.pk
        }


class ObservacionGeneral(models.Model):
    funcionario = custom_fields.BigForeignKey(
        'Funcionario', 
        verbose_name = "Funcionario"
    )
    observacion = models.TextField(
        u"Observación", 
        blank=False,
        default = "No se han registrado observaciones"
    )
    subseccion = custom_fields.BigForeignKey(
        "Subseccion",
        verbose_name = u"Subseccion Observación",
        blank = False,
        null = False,
    )
    administrable = False
    exclude = None
    grupo = None
    show_name = "Observación General"

    def to_json(self):
        return{
        'id': self.pk,
        u'Observación': self.observacion,
        'Funcionario': self.funcionario.pk,
        'Aspecto Fundamental': self.aspecto_fundamental.pk
        }


class PstCategoriaDocumentoCompuesto(models.Model):
    categoria = models.ForeignKey(
        'Categoria', 
        verbose_name = "Categoría"
        )
    documento = custom_fields.BigForeignKey(
        'Documento', 
        unique=True, 
        verbose_name = "Documento",
        null = True
        )
    fecha_categorizacion = models.DateTimeField(
        u"Fecha de Categorización", 
        auto_now_add=True
        )
    calificacion = models.IntegerField(
        u"Calificación", 
        validators=[validate_negative, max_integer]
        )    
    calificacion_definitiva = models.BooleanField(
        default = False,
        verbose_name = u'Calificación Definitiva'
    )

    administrable = False
    exclude = ('fecha_categorizacion','documento')
    show_name = "Relación PST Categoría Documento compuesto"
    grupo = None
    prioridad = None

    def __unicode__(self):
        return "%s - %s - %s - %f - %s" % (
            self.categoria.nombre,
            self.documento.nombre,
            self.fecha_categorizacion.strftime('%d/%m/%Y'),
            self.calificacion,
            "Si" if self.calificacion_definitiva else "No"
            )

    def to_json(self):
        return{
        'id': self.pk,        
        u'Categoría': self.categoria.pk,
        'Documento': self.documento.pk,
        'Solicitud': self.solicitud.pk,
        u'Fecha de Categorización': self.fecha_categorizacion.strftime('%d/%m/%Y'),
        u'Calificación': self.calificacion
        }


class RequisitoDigital(models.Model):
    solicitud = custom_fields.BigForeignKey('Solicitud', verbose_name = "Solicitud")
    file_path = ContentTypeRestrictedFileField(
        null = True,
        blank = True,
        max_length = 255,
        upload_to = get_pst_file_path,
        max_upload_size = TAMANO_MAXIMO_ARCHIVO,
        content_types = ['application/pdf', 'image/jpeg', 'image/png'],
        )
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=True)
    extension = models.CharField(u"Extensión", max_length=255)
    fecha_carga = models.DateTimeField("Fecha de Carga", auto_now_add=True)
    administrable = False
    grupo = None
    exclude = None
    prioridad = None
    show_name = "Requisito Digital"

    def to_json(self):
        return{
        'id': self.pk,
        'Solicitud': self.solicitud.pk,
        'File Path': self.file_path,
        'Nombre': self.nombre.capitalize(),
        u'Extensión': self.extension,
        'Fecha de Carga': self.fecha_carga.strftime('%d/%m/%Y')
        }

    @classmethod
    def create(cls, data):
        if isinstance(data, Storage):
            obj = cls()
            obj.solicitud = data.solicitud
            obj.file_path = data.file_path
            obj.nombre = data.nombre
            obj.extension = data.extension
            return obj
        else:
            raise NameError(
                'Error de Tipo. Los parametros enviados no son correctos'
                )


class RequisitosPago(models.Model):
    solicitud = custom_fields.BigForeignKey('SolicitudLibro', verbose_name = "Solicitud")
    tipo_requisito_pago = models.ForeignKey('TipoRequisitoPago', verbose_name = "Tipo de Requisito de Pago")
    file_path = models.CharField("File path", unique=True, max_length=255, blank=False)
    nombre = models.CharField("Nombre", unique=True, max_length=255, blank=False)
    extension = models.CharField(u"Extensión", max_length=255, blank=False)
    fecha_carga = models.DateTimeField("Fecha de Carga", auto_now_add=True)
    administrable = False
    grupo = None
    exclude = None
    prioridad = None
    show_name = "Requisitos de Pago"

    def to_json(self):
        return{
        'id': self.pk,
        'Solicitud': self.solicitud.pk,
        'Tipo de requisito de pago': self.tipo_requisito_pago.pk,
        'File path': self.file_path,
        'Nombre': self.nombre,
        u'Extensión': self.extension,
        'Fecha de carga': self.fecha_carga.strftime('%d/%m/%Y')
        }


class RespuestaLsr(models.Model):
    emisor = custom_fields.BigForeignKey(Pst, verbose_name = "Emisor")
    comentario = models.TextField("Comentario")
    entrada = custom_fields.BigForeignKey(Entrada)
    administrable = False
    grupo = None
    exclude = None
    prioridad = None
    show_name = "Respuesta del LSR"

    def to_json(self):
       return {
        'id': self.pk,
        'Emisor': self.emisor.pk,
        'Comentario': self.comentario,
        'Respuesta': self.respuesta.pk if  self.respuesta is not None else '-',
        'Entrada': self.entrada.pk
        }

class RespuestaTabulador(models.Model):
    pst = custom_fields.BigForeignKey(Pst, verbose_name = 'Prestador')
    tabulador = custom_fields.BigForeignKey('Tabulador')
    nombre = models.CharField("Nombre", max_length=255)
    fecha_creacion = models.DateTimeField(u"Fecha de creación", auto_now_add=True)
    """
        Solicitud permite colocar la solicitud de categorizacion
        que ha originado esta entrada en el tabulador de respuestas
    """
    solicitud = models.ForeignKey(
        "Solicitud", 
        verbose_name = "Solicitud Asociada",
        blank = False,
        null = False,
        unique = True
    )
    
    administrable=False
    grupo = None
    exclude = None
    prioridad = None
    show_name = "Respuesta del Tabulador"

    def to_json(self):
        return{
        'id': self.pk,
        'Tabulador': self.tabulador.to_json(),
        'Prestador': self.pst.to_json(),
        'Nombre': self.nombre,
        u'Fecha de creación': self.fecha_creacion
        }


class SolicitudLibro(models.Model):
    estatus = custom_fields.BigForeignKey('Estatus', verbose_name = "Estatus")
    pst = custom_fields.BigForeignKey(Pst, verbose_name = "Prestador", related_name = "pst_genera_solicitudes_de_libros")
    sucursal = custom_fields.BigForeignKey(Sucursales, verbose_name = "Sucursal", null=True, blank=True, default=None)
    oficina = custom_fields.BigForeignKey('OficinaRegional', verbose_name = "Oficina")
    #Esta fecha de culminacion se esta colocando para poder validar si no ha subido ningun folio en 2 meses una vez asignado el lsr fisico
    fecha_culminacion = models.DateTimeField(u"Fecha de Culminación", blank=True, null=True)
    fecha_realizacion = models.DateTimeField(u"Fecha de Realización", auto_now_add=True)
    funcionario = models.ForeignKey('Funcionario', verbose_name = "Funcionario Actual", blank=True, null=True, related_name="funcionariolsr")

    # Control de comprobante de pago para libro 
    numero_comprobante = models.BigIntegerField(
        null = True,
        unique = True,
        blank  = False,
        verbose_name=u"Número de Comprobante de Pago",
    )

    # Imagen de comprobante de pago
    archivo_comprobante = ContentTypeRestrictedFileField(
        null = True,
        blank = False,
        max_length = 255,
        upload_to = get_comprobante_file_path ,
        max_upload_size = TAMANO_MAXIMO_ARCHIVO,
        content_types = ['image/jpeg', 'image/png', 'image/jpg']
    )

    administrable=False
    grupo = None
    exclude = None
    prioridad = None
    show_name = "Solicitud de libro"

    def to_json(self):
        return{
        'id': self.pk,
        'Estatus': self.estatus.to_json(),
        'Prestador': self.pst.to_json(),
        'Sucursal': self.sucursal.nombre if self.sucursal is not None else "Sede Principal",
        'Oficina': self.oficina.to_json(),
        u'Fecha de realización': self.fecha_realizacion,
        u'Comprobante de Pago': self.numero_comprobante
        }

    @classmethod
    def create(cls, data):
        if isinstance(data, Storage):
            obj = cls()
            obj.archivo_comprobante = data.archivo_comprobante
            obj.estatus = data.estatus
            obj.pst = data.pst
            obj.sucursal = data.sucursal
            obj.oficina = data.oficina
            obj.fecha_realizacion = data.fecha_realizacion
            obj.funcionario = data.funcionario
            obj.numero_comprobante = data.numero_comprobante
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

"""
    Cuerpo del tabulador para los procesos de categorizacion
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

class SeccionConfig(models.Model):
    nombre = models.TextField(
        "Nombre", 
        max_length=2048
    )
    aspecto_config = models.ForeignKey(
        'AspectoFundamentalConfig', 
        blank= False, null= False, verbose_name = "Aspecto Fundamental"
    )
    seccion_padre_config = models.ForeignKey(
        'self',
         blank=True,
         null=True, 
         verbose_name = "Sección Padre"
    )
    administrable = False
    grupo = "Tabulador"
    prioridad = 6
    exclude = None
    show_name = "Configuración de Secciones"

    def __unicode__(self):
        return "%s - %s - v%d" % (
            self.nombre.capitalize(),
            self.aspecto_config.tabulador.nombre,
            self.aspecto_config.tabulador.version)

    def to_json(self):
        return OrderedDict([
        ('id',self.pk),
        ('Nombre',self.nombre.capitalize()),
        ('Aspecto Fundamental',self.aspecto_config.nombre.capitalize()),        
        (u'Sección Padre',self.seccion_padre_config.nombre.capitalize() if  self.seccion_padre_config is not None else '-'),
        ('Tabulador', "%s-v%d"% (self.aspecto_config.tabulador.nombre, self.aspecto_config.tabulador.version))
        ])


class Subseccion(models.Model):    
    nombre = models.CharField(
        max_length = 2048,        
        blank=False,
        null = False
    )
    observacion = models.TextField(
        u"Observación",
        blank=False,
        default= "No se han registrado observaciones"
    )
    tipo_subseccion = custom_fields.BigForeignKey(
        'TipoSubseccion',
        blank=False,
        verbose_name = "Tipo de Subsección"
    )
    subseccion_config = custom_fields.BigForeignKey(
        'SubseccionConfig',
        related_name='subseccion_config_id',
        blank=False,
        null=False,
        verbose_name = "Configuración de Subsección"
    )
    respuesta_tabulador = custom_fields.BigForeignKey(
        "RespuestaTabulador",
        verbose_name = u"Respuestas de Tabulador",
        null = False,
        blank = False
    )
    grupo = None
    exclude = None
    prioridad = None
    administrable=False
    show_name = "Subsección"

    def __unicode__(self):
        return u'%s - %s - %s' % (
            self.nombre,
            self.respuesta_tabulador.pst.rif,
            self.respuesta_tabulador.nombre
        )

    def to_json(self):
        return {}


class SubseccionConfig(models.Model):
    nombre = models.CharField("Nombre", max_length=2048, blank=False)
    seccion_config = custom_fields.BigForeignKey('SeccionConfig', blank= False, null=False, verbose_name = "Configuración de Sección")
    tipo_subseccion = models.ForeignKey('TipoSubseccion', blank= False, null= False, verbose_name = "Tipo de Subsección")
    respuesta_config = custom_fields.BigForeignKey('RespuestaConfig', blank= False, null= False, verbose_name = "Configuración de Respuesta")
    subseccion_config_padre = custom_fields.BigForeignKey('self', related_name='subseccion_config_tiene_subseccion_padre_config_id', blank=True, null=True, verbose_name = "Configuración de Subsección Padre")
    condicion_posneg = models.NullBooleanField('CondicionPositiva', blank= True, null=True)
    grupo_repetitivo = models.PositiveIntegerField(
        blank = True,
        null = True,
        default = 1,
        verbose_name = u"Grupo Repetitivo",
        validators = [validate_non_cero]
    )
    subs_imagen = models.BooleanField(
        u'¿Deben cargarse imagenes para esta subsección?',
        null=False, 
        blank=False, 
        default=False
    )
    creado_en = custom_fields.BigForeignKey(
        'Solicitud', 
        null=True, 
        verbose_name = "Solicitud"
    )
    suministrado = models.NullBooleanField(        
        verbose_name = "¿Es suministrado por el prestador?",
        blank = False,
        null = False
    )
    administrable = False
    grupo = "Tabulador"
    exclude = None
    prioridad = 7
    show_name = "Configuración de Subsecciones"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return OrderedDict([
        (u'id',self.pk),
        (u'Nombre',self.nombre.capitalize()),
        (u'Tipo de Subseccion',self.tipo_subseccion.nombre.capitalize())
        ])


class SubseccionArchivoRequisito(models.Model):
    subseccion = custom_fields.BigForeignKey('Subseccion', verbose_name = "Subsección")
    requisito_digital = custom_fields.BigForeignKey(RequisitoDigital, verbose_name = "Requisito Digital")
    administrable=False
    grupo = None
    exclude = None
    prioridad = None
    show_name = "Subsección archivo requisito"

    def to_json(self):
        return{
        'id': self.pk,
        u'Subsección': self.subseccion_id.to_json(),
        'Requisito Digital': self.requisitodigital_id.to_json()
        }


class Tabulador(models.Model):
    tipo_pst = models.ForeignKey(
        modelos_licencias.TipoLicencia,
        verbose_name = "Tipo de Prestador",
        blank = False,
        null=False
    )
    nombre = models.CharField(
        "Nombre",
        max_length=255,
        blank=False,
        null=False
    )
    fecha_creacion = models.DateTimeField(
        u"Fecha de creación",
        db_column='fecha_creacion',
        auto_now_add=True
    )

    """
        Mecanismo de control de versiones
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Permitir a un funcionario la creacion de una version de un tabulador
        asociado a un tipo de prestador de servicio turistico
    """
    version = models.PositiveIntegerField(
        blank = True,
        null = True,
        default = 1,
        verbose_name = u"Versión",
        validators = [validate_non_cero]
    )

    version_actual = models.BooleanField(
        default = False,
        verbose_name = u'Versión Actual'
    )

    prioridad = 4
    administrable = True
    grupo = "Tabulador"
    show_name = "Tabulador"
    exclude = ('fecha_creacion', 'version')

    def __unicode__(self):
        return "%d - %s" % (self.id, self.nombre.capitalize())

    def to_json(self):
        return OrderedDict([
            ('id',self.id),
            ('Nombre',self.nombre.capitalize()),
            ('Tipo de Prestador',self.tipo_pst.nombre  if self.tipo_pst is not None else '-'),
            (u'Fecha de Creación', self.fecha_creacion.strftime('%d/%m/%Y')),
            (u'Versión', self.version),
            (u'version_actual', self.version_actual),
            ])

    # Override
    def save(self, *args, **kwargs):
        if self.pk:
            super(Tabulador, self).save(*args, **kwargs)
        elif Tabulador.objects.filter(
                tipo_pst_id = self.tipo_pst, 
                version_actual = True
            ).exists():
            t = Tabulador.objects.filter(
                tipo_pst_id = self.tipo_pst
                ).order_by('-version').first()                
            self.version = t.version + 1 if t is not None else 1 
            self.version_actual = False           
            super(Tabulador, self).save(*args, **kwargs)
        else:
            t = Tabulador.objects.filter(
                        tipo_pst_id = self.tipo_pst
                    ).order_by('-version').first()            
            self.version = t.version + 1 if t is not None else 1
            super(Tabulador, self).save(*args, **kwargs)


class IncidenciaCondicional(models.Model):

    porcentaje_inferior = models.FloatField(
        verbose_name = "Porcentaje Inferior",
        blank = False,
        null = False
    )
    porcentaje_superior = models.FloatField(
        verbose_name = "Porcentaje Superior",
        blank = False,
        null = False
    )
    valor_incidencia = models.FloatField(
        verbose_name = u"Valor de incidencia",
        blank = False,
        null = False
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Incidencia condicional"
    exclude = None

    # Override
    def save(self, *args, **kwargs):
        """
            Si esta dentro del rango [porcentaje_inferior, porcentaje_superior]
            quiere decir que tendra una incidencia de un <<incidencia>> sobre la 
            calificacion final del prestador
        """
        if self.porcentaje_inferior >= self.porcentaje_superior:
            raise FieldError(
                "El valor del procentaje de incidencia inferior siempre debe ser menor y distinto al valor de procentaje de incidencia superior"
            )
        else:
            super(IncidenciaCondicional, self).save(*args, **kwargs)            

    def __unicode__(self):        
        return "Incidencia Condicional [%.4f - %.4f] => %.4f" % (
            self.porcentaje_inferior,
            self.porcentaje_superior,
            self.valor_incidencia
        )

    def to_json(self):
        return OrderedDict([
            ("id", self.pk),
            ("Porcentaje Inferior", self.porcentaje_inferior),
            ("Porcentaje Superior", self.porcentaje_superior),
            ("Valor de Incidencia", self.valor_incidencia)
        ])


class Incidencia(models.Model):

    incidencia_condicional = models.ForeignKey(
        "IncidenciaCondicional",
        verbose_name = "Incidencia sobre la calificacion",
        blank = False,
        null=False
    )

    tabulador = models.ForeignKey(
        "Tabulador",
        verbose_name = "Tabulador asociado",
        blank = False,
        null = False
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Incidencia"
    exclude = None

    def __unicode__(self):
        return "Incidencia: %d - %s" % (
            self.incidencia_condicional.id,
            "%s -  v%d" % (self.tabulador.nombre,self.tabulador.version)
        )

    def to_json(self):
        return OrderedDict([
            ('id',self.pk),
            ('Incidencia Condicional',self.incidencia_condicional.id),
            ('Tabulador',"%s -  v%d" % (self.tabulador.nombre,self.tabulador.version))
        ])


class Repeticion(models.Model):
    
    subseccion_config = models.ForeignKey(
        "SubseccionConfig",
        verbose_name = "Subseccion de configuracion asociada",
        blank = False,
        null = False
    )

    categoria = models.ForeignKey(
        "Categoria",
        verbose_name = "Categoria asociada",
        blank = False,
        null = False
    )

    repeticion_esperada = models.PositiveIntegerField(
        verbose_name = "Repeticiones esperadas",
        blank = False,
        null = False
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = u"Configuracion de Repetición"
    exclude = None

    def __unicode__(self):
        return "%s - %s - Repeticiones: %d" % (
            self.subseccion_config.nombre,
            self.categoria.nombre,
            self.repeticion_esperada
        )

    def to_json(self):
        return OrderedDict([
            ("id", self.pk),
            ('Subseccion de Configuracion', self.subseccion_config.nombre),
            ('Categoria Asociada',self.categoria.nombre),
            ('Repeticiones esperadas', self.repeticion_esperada)
        ])


class Relevancia(models.Model):

    categoria = models.ForeignKey(
        "Categoria",
        verbose_name = "Categoria",
        blank = False,
        null = False
    )

    subseccion_config = models.ForeignKey(
        "SubseccionConfig",
        verbose_name = "Subseccion de configuracion",
        blank = False,
        null = False
    )

    repeticion = models.IntegerField(        
        verbose_name = "Repeticion por categoria",
        blank = True,
        null = True
    )

    operador_logico = models.ForeignKey(
        'OperadorFormula',
        verbose_name = "Valor Logico de comparacion",
        null = True,
        blank = True
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Relevancia por Categoria"
    exclude = None

    def __unicode__(self):
        return "%s - %s" % (
            self.categoria.nombre,
            self.subseccion_config.nombre
        )

    def to_json(self):
        return OrderedDict([
            ("id", self.pk),
            ("Categoria", self.categoria.nombre),
            ("Subseccion de Configuracion", self.subseccion_config.nombre)
        ])


class OperadorFormula(models.Model):

    nombre = models.CharField(
        max_length = 255,
        verbose_name = "Nombre del operador",
        blank = False,
        null = False
    )

    representacion = models.CharField(        
        verbose_name = u"Representación",
        max_length = 10,        
        blank = False,
        null = False
    )

    aridad = models.PositiveIntegerField(
        verbose_name = "Aridad",
        default = 2,
        blank = False,
        null = False
    )

    logico = models.BooleanField(
        verbose_name = u"¿Es operador lógico?",
        default = False,
        blank = False,
        null = False
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Operadores"
    exclude = None

    def __unicode__(self):
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape( format_html( self.representacion ) )

    def to_json(self):
        return OrderedDict([
            ("id", self.pk),
            ("Nombre", self.nombre),
            (u"Representacion", self.representacion),
            ("Aridad", self.aridad),
            (u"¿Es operador lógico?", self.logico)
        ])


class Indicador(models.Model):

    nombre = models.CharField(
        max_length = 255,
        blank = False,
        null = False
    )

    tabulador = models.ForeignKey(
        'Tabulador',
        verbose_name = "Tabulador Perteneciente"
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Indices de Formula"
    exclude = None

    def __unicode__(self):
        return "%s" % ( self.nombre )

    def to_json(self):
        return OrderedDict([
            ("id", self.pk),
            ("Nombre", self.nombre)
        ])


class ValorIndicador(models.Model):

    respuesta_config = models.ForeignKey(
        "RespuestaConfig",
        blank = False,
        null = False
    )

    indicador = models.ForeignKey(
        "Indicador",
        blank = False,
        null = False
    )

    operador_derecho = models.ForeignKey(
        "OperadorFormula",
        verbose_name = "Operador Derecho",
        related_name = "operador_derecho",
        blank = True,
        null = True
    )

    operador_izquierdo = models.ForeignKey(
        "OperadorFormula",
        verbose_name = "Operador Izquierdo",
        related_name = "operador_izquierdo",
        blank = True,
        null = True
    )

    orden = models.PositiveIntegerField(
        blank = False,
        null = False
    )

    suministrado = models.NullBooleanField(        
        verbose_name = "¿Es suministrado por el prestador?",
        blank = False,
        null = False,
        default=True
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Valores de Indicadores"
    exclude = None

    def __unicode__(self):
        return "%s - %s - (%s,%s) - %d" % (
            self.respuesta_config.nombre,
            self.indicador.nombre,
            self.operador_izquierdo.representacion if self.operador_izquierdo is not None else "No tiene",
            self.operador_derecho.representacion if self.operador_derecho is not None else "No tiene" ,
            self.orden
        )

    def to_json(self):
        return OrderedDict([
            ("id", self.pk),
            ("Configuracion de respuesta", self.respuesta_config.nombre),
            ("Indicador", self.indicador.nombre),
            ("Operador Izquierdo",self.operador_izquierdo),
            ("Operador Derecho",self.operador_derecho),
            (u"Posición", self.orden)
        ])

    # Override
    def save(self, *args, **kwargs):
        if self.pk is not None:
            if ValorIndicador.objects.filter(
                respuesta_config = self.respuesta_config,
                orden = self.orden
            ).exists() :            
                raise FieldError("Ya existe un operador configurado para esta posicion relativa de la formula")
        
        super(ValorIndicador, self).save(*args, **kwargs)


class ValorCategoria(models.Model):

    categoria = models.ForeignKey(
        "Categoria",
        verbose_name = "Categoria Asociada",
        blank = False,
        null = False
    )

    indicador = models.ForeignKey(
        "Indicador",
        verbose_name = "Indicador",
        blank = False,
        null = False
    )

    operador = models.ForeignKey(
        "OperadorFormula",
        verbose_name = u"Operador Lógico",
        blank = True,
        null = True
    )

    valor_comparacion = models.FloatField(
        verbose_name = u"Valor de comparación",
        blank = True,
        null = True
    )

    valor = models.FloatField(
        verbose_name = "Valor",
        blank = True,
        null = True
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = "Valores por Categorias"
    exclude = None

    def to_json(self):
        return OrderedDict([
            ("Categoria",self.categoria.nombre),
            ("Indicador", self.indicador.nombre),
            (u"Operador delimitador", self.operador.representacion if self.operador is not None else "-"),
            (u"Valor de comparación", self.valor_comparacion if self.valor_comparacion is not None else "-"),
            ("Valor",self.valor)
        ])

    def __unicode__(self):
        return "%s - %s - %s - %s - %.4f" % (
            self.categoria.nombre,
            self.indicador.nombre,
            self.operador.representacion if self.operador is not None else "No posee",
            self.valor_comparacion if self.valor_comparacion is not None else "No posee",
            self.valor
        )

    @classmethod
    def getValoresCategoria(self, indicador):
        try:
            valores = ValorCategoria.objects.filter(
                indicador=indicador
            ).order_by("categoria__valor")
            response = []
            for v in valores:
                response.append(v.valor)
            return response
        except Exception, e:
            raise e


class OpcionesRepeticion(models.Model):

    seccion_config = models.ForeignKey(
        "SeccionConfig",
        verbose_name = u"Sección de configuración",
        blank = False,
        null = False
    ) 

    respuesta_config = models.ForeignKey(
        "RespuestaConfig",
        verbose_name = u"Configuración de respuesta",
        blank = False,
        null = False
    )

    prioridad = -1
    administrable = False
    grupo = "Tabulador"
    show_name = u"Opciones de Repetición"
    exclude = None

    def __unicode__(self):
        return "%s - %s" % (
            self.seccion_config.nombre,
            self.respuesta_config.nombre
        )

    def to_json(self):
        return OrderedDict([
            (u"Sección de configuración", self.seccion_config.nombre),
            (u"Configuración de respuesta", self.respuesta_config.nombre)
        ])

"""    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Turista(models.Model):
    nombre = models.CharField(
        "Nombre",
        max_length=255,
        blank=True,
        null=True
    )
    apellido = models.CharField(
        "Apellido", 
        max_length=255, 
        blank=True, 
        null=True
    )
    correo_electronico = models.EmailField(
        u"Correo electrónico",
        unique=True, 
        max_length=255
    )
    ciudad = models.ForeignKey(
        Ciudad, 
        verbose_name = u"Especifique su ciudad",
        null = True,
        blank = True
    )
    telefono_contacto = models.CharField(
        u"Teléfono de contacto",
        max_length=255,
        blank=True,
        null=True
    )
    numero_documento_identidad = models.CharField(
        u"Número de Documento de Identidad", 
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )    
    tipo_documento_identidad = models.ForeignKey(
        'TipoDocumentoIdentidad', 
        blank=True, 
        null=True, 
        verbose_name = 
        "Tipo de documento de identidad"
    )
    grupo = None
    exclude = None
    prioridad = None
    administrable = False
    show_name = "Turista"

    def __unicode__(self):
        return u"%s - %s %s" %(
            self.numero_documento_identidad,
            self.nombre,
            self.apellido
            )

    def to_json(self):
        return OrderedDict([
            ('id',self.pk),
            ('Nombre',self.nombre.capitalize()),
            ('Apellido',self.apellido.capitalize()),
            (u'Número de Documento de Identidad',self.numero_documento_identidad),
            ])        


class OficinaRegional(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255)
    municipio = custom_fields.BigForeignKey(Municipio, verbose_name = "Municipio")
    direccion = models.TextField(u"Dirección")
    prioridad = 2
    exclude = None
    administrable=True
    grupo = "Solicitudes de Libros"
    show_name = "Oficina Regional"

    def __unicode__(self):
        return u'%s - %s' % (self.nombre.capitalize(), self.municipio.municipio)

    def to_json(self):
        return OrderedDict([
            ('id',self.pk),
            ('Nombre',self.nombre.capitalize()),
            ('Municipio',self.municipio.municipio.capitalize()),
            (u'Dirección',self.direccion),
            ])


class RespuestaConfig(models.Model):
    nombre = models.CharField(
        "Nombre", 
        max_length= 2048, 
        blank=False, 
        null=False
    )
    tipo_respuesta = custom_fields.BigForeignKey('TipoRespuesta', blank=False, null=False, verbose_name = "Tipo de Respuesta")
    tipo_medida = custom_fields.BigForeignKey('TipoMedida', blank=True, null=True, verbose_name = "Tipo de Medida")
    administrable = False
    prioridad = 2
    grupo = "Tabulador"
    exclude = None
    show_name = "Configuración de Respuestas"

    def __unicode__(self):
        return u' %s '%(self.nombre.capitalize())

    def to_json(self):
            return OrderedDict([
            ('id',self.pk),
            ('Nombre',self.nombre),
            ('Tipo de Respuesta', self.tipo_respuesta.nombre),
            ('Tipo de Medida',self.tipo_medida.nombre if self.tipo_medida is not None else '-'),
            ])

"""
    RespuestaValorRespuesta
    ~~~~~~~~~~~~~~~~~~~~~~~

    Modelo destinado a relacionar respuestas posibles con valores
    de respuestas.
"""

class RespuestaValorRespuesta(models.Model):
    pregunta_config = custom_fields.BigForeignKey(
        'RespuestaConfig',
        verbose_name="Pregunta",
        blank=False,
        null=False
    )
    respuesta_config = custom_fields.BigForeignKey(
        'ValorRespuestaConfig',
        verbose_name="Respuesta Asociada",
        blank=False,
        null=False
    )
    valor_minino_aceptacion = models.BooleanField(u'Valor minimo de aceptación', 
        default=False,
        null = False, 
        blank=False
    )
    administrable = False
    prioridad = 4
    grupo = "Tabulador"
    exclude = None
    show_name = u"Relación entre preguntas y respuestas"

    def __unicode__(self):
        return u'%s - %s' % (
            self.pregunta_config.nombre,
            self.respuesta_config.nombre,
        )

    def to_json(self):
        return OrderedDict([
            ('id',self.pk),
            ('Pregunta',self.pregunta_config.nombre ),
            ('Respuesta',self.respuesta_config.nombre),
        ])

class ValorRespuestaConfig(models.Model):
    nombre = models.CharField("Nombre", max_length = 255, blank = False)    
    limite_inferior = models.FloatField(u"Límite Inferior", blank = True, null = True, validators=[max_float])
    limite_superior = models.FloatField(u"Límite Superior", blank = True, null = True, validators=[max_float])
    categoria = custom_fields.BigForeignKey('Categoria', blank = True, null = True, verbose_name = "Categoria Asociada")
    administrable = False
    prioridad = 3
    grupo = "Tabulador"
    exclude = None
    show_name = "Posibles Valores de Respuestas"

    def __unicode__(self):
        return u'%s' % (self.nombre.capitalize())


    def to_json(self):
        if self.limite_superior and self.limite_superior is not None:
            return OrderedDict([
                ('id',self.pk),
                ('Nombre',self.nombre),                           
                (u'Límite Inferior',self.limite_inferior),
                (u'Límite Superior',self.limite_superior)
            ])
        else:
            return OrderedDict([
                ('id',self.pk),
                ('Nombre',self.nombre),                              
                (u'Límite Inferior','-'),
                (u'Límite Superior','-')
            ])


class ValorRespuesta(models.Model):
    valor = models.FloatField(
        blank = True, 
        default = 0.0, 
        null = True, 
        verbose_name = "Valor Dado"
    )
    subseccion = custom_fields.BigForeignKey(
        'Subseccion',
        blank=False, 
        null=False,
        verbose_name = "Subsección"
    )
    valor_respuesta = models.ForeignKey(
        'ValorRespuestaConfig',
        blank=True,
        null=True,
        verbose_name = "Tipo de Respuesta"
    )
    administrable=False
    exclude = None
    grupo = None
    prioridad = None
    show_name = "Valor de Respuesta"

    def __unicode__(self):
        return u'Valor respuesta: %s | Subseccion: %s | Posee valor: [%f]' % (
            self.valor_respuesta.nombre.capitalize() if self.valor_respuesta is not None else "No posee", 
            self.subseccion.nombre if self.subseccion is not None else "No posee",
            self.valor
        )

    def to_json(self):
        return OrderedDict([
            ('id',self.pk),
            ('Nombre',self.valor_respuesta.nombre if self.valor_respuesta is not None else "No posee"),  
            ('Subseccion', self.subseccion.nombre if self.subseccion is not None else "No posee"),
            ('Valor', self.valor)                            
        ])


class EspecificacionLegal(models.Model):
    identificador_legal = models.CharField(
        "Identificador Legal", 
        max_length = 255, 
        blank = True, 
        null=True
    )
    numero = models.IntegerField(
        u"Número", 
        blank = False, 
        validators=[validate_negative, max_integer]
    )
    contenido = models.CharField(
        "Contenido", 
        max_length = 1024, 
        blank = True, 
        null=True
    )
    fecha = models.DateTimeField(
        u"Fecha de publicación", 
        blank=True, 
        null=True
    )
    tipo_pst = models.ForeignKey(
        modelos_licencias.TipoLicencia,
        verbose_name = "Tipo de Prestador",
        blank=False,
        null=False
    )
    documento_asociado = models.ForeignKey(
        'TipoDocumentoCompuesto', 
        verbose_name = "Documento Asociado", 
        blank=False, 
        null=False
    )
    tipo_especificacion = models.ForeignKey(
        'TipoEspecificacion', 
        verbose_name = "Tipo de Especificación", 
        blank=False, 
        null=False
    )
    administrable = True
    exclude = None
    grupo = "Especificación Legal"
    prioridad = 1
    show_name = "Especificación Legal"

    def __unicode__(self):
        return u'%s' % (self.tipo_especificacion.nombre)

    def to_json(self):
        return {
            'id': self.pk,
            'Identificador Legal': self.identificador_legal if self.identificador_legal is not None else "-",
            u'Número': self.numero if self.numero is not None else "-",
            'Contenido': self.contenido if self.contenido is not None else "-",
            'Fecha': self.fecha.strftime('%d/%m/%Y') if self.fecha is not None else "-",
            'Tipo de Prestador': self.tipo_pst.nombre if self.tipo_pst is not None else "-",
            'Documento Asociado': self.documento_asociado.nombre if self.documento_asociado is not None else "-",
            u'Tipo de Especificación': self.tipo_especificacion.nombre if self.tipo_especificacion is not None else "-"
        }


class TipoEspecificacion(models.Model):
    nombre = models.CharField("Nombre", unique=True, max_length=255,blank=False)
    abreviacion = models.CharField(u"Abreviación", unique=True, max_length=5)
    administrable = False
    exclude = None
    grupo = "Especificación Legal"
    prioridad = 0
    show_name = "Tipo de Especificación"

    def __unicode__(self):
        return self.nombre.capitalize()

    def to_json(self):
        return {
            'id': self.pk,
            'Nombre': self.nombre,
            'Abreviación': self.abreviacion
        }


class Placa(models.Model):   
    pst = custom_fields.BigForeignKey(Pst, verbose_name = "Prestador")
    documento = custom_fields.BigForeignKey('Documento', verbose_name = "Documento", null=True)
    licencia_asignada = models.ForeignKey(modelos_licencias.LicenciaAsignada, verbose_name="Licencia asignada")
    administrable = False
    exclude = None
    grupo = "Placas"
    prioridad = 10
    show_name = "Placas"

