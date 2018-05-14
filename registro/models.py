# coding=utf-8
from re import compile as re_compile
from json import dumps as json_dumps
from json import loads as json_loads
from datetime import datetime
from os import path

from django.core import serializers
from django.db import models
from django.db import transaction
from django.conf import settings
from venezuela.models import Estado, Municipio, Parroquia

from apps.cuentas.models import MinturUser
from utils import models as custom_models
from utils.gluon.storage import Storage
from utils.validate_files import ContentTypeRestrictedFileField


RUTA_DOCUMENTOS = "."  # Definir la ruta real donde se guardaran los archivos
NO_APLICA = 0

PERSONA_JURIDICA = 1
PERSONA_NATURAL = 2
OTRAS = 3
TIPO_PERSONA = (
    (OTRAS, u'Otras'),
    (PERSONA_JURIDICA, u'Persona Jurídica'),
    (PERSONA_NATURAL, u'Persona Natural')
)

GRADO_LICENCIA = (
    (10, u'Segundo Grado'),
    (20, u'Tercer Grado'),
    (30, u'Cuarto Grado'),
    (40, u'Quinto Grado'),
)

ESTATUS_REGISTRO_EN_ESPERA = 0
ESTATUS_REGISTRO_SIN_COMPLETAR = 1
ESTATUS_REGISTRO_COMPLETADO = 2
ESTATUS_REGISTRO_PRIMERA_CERTIFICACION = 3
ESTATUS_REGISTRO_SEGUNDA_CERTIFICACION = 4
ESTATUS_EN_CIERRE_DE_ACTIVIDAD_COMERCIAL_TEMPORAL = 5
ESTATUS_EN_CIERRE_DE_ACTIVIDAD_COMERCIAL_DEFINITIVO = 6
ESTATUS_FALLECIDO = 7
ESTATUS_QUIEBRA = 8
ESTATUS_AUSENTE_DEL_PAIS = 9

ESTATUS_REGISTRO = (
    (ESTATUS_REGISTRO_EN_ESPERA, u'En espera de actualización'),
    (ESTATUS_REGISTRO_SIN_COMPLETAR, u'Registro sin completar'),
    (ESTATUS_REGISTRO_COMPLETADO, u'Registro completado'),
    (ESTATUS_REGISTRO_PRIMERA_CERTIFICACION, u'Primera certificación'),
    (ESTATUS_REGISTRO_SEGUNDA_CERTIFICACION, u'Segunda certificación'),
    (
        ESTATUS_EN_CIERRE_DE_ACTIVIDAD_COMERCIAL_TEMPORAL,
        u'En Cierre de Actividad Comercial Temporal'
    ),
    (
        ESTATUS_EN_CIERRE_DE_ACTIVIDAD_COMERCIAL_DEFINITIVO,
        u'En Cierre de Actividad Comercial Definitivo'
    ),
    (ESTATUS_FALLECIDO, u'Fallecido'),
    (ESTATUS_QUIEBRA, u'En Quiebra'),
    (ESTATUS_AUSENTE_DEL_PAIS, u'Ausente del País'),
)

COMPANIA_ANONIMA = 1
SOCIEDAD_ANONIMA = 2
COOPERATIVA = 3
ASOCIACIONES_CIVILES = 4
SRL = 5
FUNDACIONES = 6
COMANDITA_SIMPLE = 7
COMANDITA_POR_ACCIONES = 8

TIPOS_PERSONAS_JURIDICA = (
    (COMPANIA_ANONIMA, u'Compañía Anónima'),
    (SOCIEDAD_ANONIMA, u'Sociedad Anónima'),
    (COOPERATIVA, u'Cooperativa'),
    (ASOCIACIONES_CIVILES, u'Asociación civil'),
    (SRL, u'SRL: Sociedad Responsabilidad Limitada'),
    (FUNDACIONES, u'Fundación'),
    (COMANDITA_SIMPLE, u'Comandita simple'),
    (COMANDITA_POR_ACCIONES, u'Comandita Por Acciones'),
)

ORIGINAL = 0
MODIFICACION = 1

TIPO_ACTA_CONSTITUTIVA = (
    (ORIGINAL, u'Original'),
    (MODIFICACION, u'Modificación'),
)

REPRESENTANTE = 0

CONTACTO = 1

TIPO_REPRESENANTE = (
    (REPRESENTANTE, u'Representante'),
    (CONTACTO, u'Contacto'),
)

TAMANO_MAXIMO_ARCHIVO = 10485760  # 10 megas

TIPO_CERTIFICACION_RECHAZADA = 1
TIPO_CERTIFICACION_PRIMERA = 2
TIPO_CERTIFICACION_SEGUNDA = 3
TIPO_CERTIFICACION_FACTIBILIDAD = 3

TIPO_CERTIFICACION = (
    (TIPO_CERTIFICACION_RECHAZADA, u'Rechazada'),
    (TIPO_CERTIFICACION_PRIMERA, u'Primera Certificación'),
    (TIPO_CERTIFICACION_SEGUNDA, u'Segunda Certificación'),
    (TIPO_CERTIFICACION_FACTIBILIDAD, u'Factibilidad'),
)

JUNTA_DIECTIVA = 1
OBJETIVO_SOCIAL = 2
DOMICILIO_FISCAL = 3
ACCIONES = 4
CAPITAL = 5
OTROS = 6

TIPO_MODIFICACION = (
    (JUNTA_DIECTIVA, u'Junta Directiva'),
    (OBJETIVO_SOCIAL, u'Objetivo Social'),
    (DOMICILIO_FISCAL, u'Domicilio Fiscal'),
    (ACCIONES, u'Acciones'),
    (CAPITAL, u'Capital'),
    (OTROS, u'Otros')
)

ACTIVIDAD_PRINCIPAL = 1
ACTIVIDAD_SECUNDARIA = 2

TIPO_ACTIVIDAD = (
    (ACTIVIDAD_PRINCIPAL, u'Actividad Principal'),
    (ACTIVIDAD_SECUNDARIA, u'Actividad Secundaria'),
)

ACTIVO = 0
INACTIVO = 1
ESTADO_DEL_CONTRIBUYENTE = (
    (ACTIVO, u'Activo'),
    (INACTIVO, u'Inactivo'),
)

# REGEXES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DATETIME_REGEX = re_compile(r'^(\d{4}-\d{2}-\d{2})(?:(.+))?$')

FILE_REGEX = re_compile(r'^(?:\w{4}/){10}.*$')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class CachedManager(models.Manager):
    def _check_constraints(self, kwargs, cache):
        cache_obj = self._convert_cache(kwargs, cache)

        for field in kwargs:
            if kwargs[field] != getattr(cache_obj, field):
                raise self.model.DoesNotExist

    def _convert_cache(self, kwargs, cache):
        datos_json = json_loads(cache.datos_json)[0]
        cached_fields = datos_json['fields']

        foreign_key_fields = (
            field for field in self.model._meta.fields
            if isinstance(field, models.ForeignKey)
            and cached_fields[field.name]
        )
        cached_fields.update({
            field.name: field.rel.to.objects.get(
                pk=cached_fields[field.name]
            ) for field in foreign_key_fields
        })

        date_fields = (
            field for field in self.model._meta.fields
            if isinstance(field, models.DateField)
            and cached_fields[field.name]
        )
        cached_fields.update({
            field.name: self._convert_date(cached_fields[field.name])
            for field in date_fields
        })

        dirpath = custom_models.gen_path_str_from_key_str(
            self._get_pst(cached_fields, 'rif')
        )

        file_fields = (field for field in self.model._meta.fields if (
            isinstance(field, models.FileField)
            and cached_fields[field.name]
        ))
        cached_fields.update({
            field.name: path.join(dirpath, cached_fields[field.name])
            for field in file_fields
        })

        return self.model(pk=datos_json['pk'], **cached_fields)

    def _convert_date(self, date_str):
        date, time = DATETIME_REGEX.match(
            date_str.replace('Z', '').replace('T', ' ')
        ).groups()

        if time:
            return datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S.%f')

        return datetime.strptime(date, '%Y-%m-%d').date()

    def _get_pst(self, kwargs, attr=None):
        if 'user' in kwargs:
            obj = Pst.objects.get(user=kwargs['user'])

        elif 'pst' in kwargs:
            obj = kwargs['pst']

        elif 'dato_especifico' in kwargs:
            obj = kwargs['dato_especifico'].pst

        elif ('pk' in kwargs or 'id' in kwargs) and self.model == Pst:
            obj = Pst.objects.get(pk=kwargs.get('pk', kwargs.get('id', None)))

        if 'obj' not in locals() or not obj:
            raise AssertionError(
                'Es imposible determinar el PST asociado a este modelo'
            )

        return getattr(obj, attr) if attr else obj

    def filter(self, *args, **kwargs):
        cached_data = kwargs.pop('cached', False)

        if not cached_data:
            return super(CachedManager, self).filter(*args, **kwargs)

        fields = [
            field.name for field in self.model._meta.fields
            if field.name in kwargs
        ]

        fields.extend(['pk'] if 'pk' in kwargs else [])

        try:
            cached_rows = Cache.objects.filter(
                tabla=self.model._meta.db_table,
                relacion_id=self._get_pst(kwargs, 'id'),
            )

        except AssertionError:
            cached_rows = Cache.objects.filter(
                tabla=self.model._meta.db_table
            )

        result_rows = set(
            row for row in (
                self._convert_cache(kwargs, cache) for cache in cached_rows
            ) if all(getattr(row, fld) == kwargs[fld] for fld in fields)
        )

        result_rows.update(set(
            row for row in super(CachedManager, self).filter(*args, **kwargs)
        ))

        return list(result_rows)

    def get(self, *args, **kwargs):
        cached_data = kwargs.pop('cached', False)

        if not cached_data:
            return super(CachedManager, self).get(*args, **kwargs)

        try:
            cache = Cache.objects.get(
                tabla=self.model._meta.db_table,
                relacion_id=self._get_pst(kwargs, 'id'),
            )
            self._check_constraints(kwargs, cache)

        except Cache.DoesNotExist:
            return super(CachedManager, self).get(*args, **kwargs)

        except Cache.MultipleObjectsReturned:
            cached_rows = self.filter(*args, cached=True, **kwargs)

            if len(cached_rows) == 0:
                raise self.model.DoesNotExist

            if len(cached_rows) == 1:
                return cached_rows[0]

            raise self.model.MultipleObjectsReturned()

        else:
            return self._convert_cache(kwargs, cache)


class CachedModel(custom_models.CustomFileAllocatorModel):
    objects = CachedManager()

    class Meta:
        abstract = True

    def _get_cached_row(self, rows):
        if self.id is not None:
            for row in rows:
                if self.id == json_loads(row.datos_json)[0]['pk']:
                    return row

        return rows.first()

    def _get_pst(self, attr=None):
        if hasattr(self, 'pst'):
            return getattr(self.pst, attr) if attr else self.pst

        if hasattr(self, 'dato_especifico'):
            return (
                getattr(self.dato_especifico.pst, attr)
                if attr else self.dato_especifico.pst
            )

        if hasattr(self, 'rif'):
            return getattr(self, attr) if attr else self

        raise AssertionError(
            'Es imposible determinar el PST asociado a este modelo'
        )

    def _save_files(self):
        dirpath = custom_models.gen_path_str_from_key_str(
            self._get_pst('rif')
        )

        for fld in self._meta.fields:
            if isinstance(fld, models.FileField) and getattr(self, fld.name):
                file_field = getattr(self, fld.name)

                if not file_field:
                    continue

                if FILE_REGEX.match(file_field.name):
                    setattr(self, fld.name, path.basename(file_field.name))
                    continue

                newpath = file_field.storage.save(
                    path.join(dirpath, file_field.name), file_field.file,
                )
                setattr(self, fld.name, path.basename(newpath))

    def delete(self, cached=False):
        if cached:
            cache_rows = Cache.objects.filter(
                tabla=self._meta.db_table,
                relacion_id=self._get_pst('id')
            )

            for row in cache_rows:
                if json_loads(row.datos_json)[0]['pk'] == self.id:
                    return row.delete()

        return super(CachedModel, self).delete()

    def save(self, force=False, force_cached=False):
        if force:
            return super(CachedModel, self).save()

        self._save_files()

        rows = Cache.objects.filter(
            tabla=self._meta.db_table,
            relacion_id=self._get_pst('id')
        )

        if not rows.exists() or force_cached:
            with transaction.atomic():
                cache = Cache(
                    tabla=self._meta.db_table,
                    relacion_id=self._get_pst('id'),
                )
                cache.save()

                self.id = self.id if self.id is not None else cache.id
                cache.datos_json = serializers.serialize('json', [self])
                cache.save()

        else:
            cached_row = self._get_cached_row(rows)
            cached_row.datos_json = serializers.serialize('json', [self])
            cached_row.save()


class Cache(models.Model):
    tabla = models.CharField(max_length=100, null=False)
    relacion_id = models.IntegerField(null=False)
    datos_json = models.TextField(null=False)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'Cache: #{} :: <{}> :: #{}'.format(
            self.id, self.tabla, self.relacion_id
        )


class TipoPst(models.Model):
    """
    Modelo Tipo_pst = Tipo prestador de servicio turístico
    """
    nombre = models.CharField( max_length = 255 )
    tipo_persona = models.IntegerField( choices=TIPO_PERSONA )
    descripcion = models.CharField( max_length=75, null=True, blank=True )

    @classmethod
    def create(cls, nombre, tipo_persona, descripcion):
        """
        Crea una nueva instancia del objeto TipoPst a partir de la información suministrada.
        - nombre (str): Tipo de persona juridica
        - tipo_persona (int): Rif del PST [juridico, natural]
        - descripcion (str): descripción del tipo de actividad
        """
        if isinstance(nombre, str) & isinstance(tipo_persona, int) & isinstance(descripcion, str):
            obj = cls()
            obj.nombre = nombre
            obj.tipo_persona = tipo_persona
            obj.descripcion = descripcion

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def __unicode__(self):
        return u'{}'.format(self.nombre)


class Pst(CachedModel):
    """
    Modelo PST = Prestador de servicio turístico
    """
    tipo_pst = models.ForeignKey('TipoPst', null=True, blank=True)  # # Eliminar este item
    tipo_figura = models.IntegerField(choices=TIPO_PERSONA, blank=True, null=True, default=PERSONA_JURIDICA)
    tipo_juridica = models.IntegerField(blank=True, null=True, choices=TIPOS_PERSONAS_JURIDICA, default=NO_APLICA)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    rif = models.CharField(max_length=20, blank=False)
    nombres = models.CharField(max_length=50, null=True, blank=True)
    apellidos = models.CharField(max_length=50, null=True, blank=True)
    razon_social = models.CharField(max_length=75, null=True, blank=True)
    denominacion_comercial = models.CharField(max_length=50, null=True, blank=True)
    estatus = models.IntegerField(choices=ESTATUS_REGISTRO, default=ESTATUS_REGISTRO_SIN_COMPLETAR)
    estado_contribuyente = models.IntegerField(choices=ESTADO_DEL_CONTRIBUYENTE, default=ACTIVO) 
    creado_el = models.DateTimeField(auto_now_add=True)
    modificado_el = models.DateTimeField(auto_now=True)
    pagina_web = models.URLField(null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
    telefono_celular = models.CharField(max_length=20, null=True, blank=True)
    correo_electronico = models.EmailField(max_length=75, null=True, blank=True)
    emprendedor = models.BooleanField(default=True)
    tiene_firma_personal = models.BooleanField(default=False)
    ultima_verificacion = models.DateField(blank=True, null=True)
    ultima_fiscalizacion = models.DateField(blank=True, null=True)
    inicio_actividad_comercial = models.DateField(blank=True, null=True)
    rtn = models.BigIntegerField(null=True, blank=True)
    numero_contribuyente = models.CharField(max_length=100, null=True, blank=True)
    archivo_cedula = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_rif = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_pasaporte = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types=['image/jpeg', 'image/png'],
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_servicio = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types=['application/pdf', 'image/jpeg', 'image/png'],
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Pst a partir de la información suministrada.
        El Storage data debe contener
        - tipo_juridica (int): Tipo de persona juridica
        - rif (str): Rif del PST [juridico, natural]
        - razon_social (str): Razon social del PST [juridico]
        - pagina_web (str): Pagina web del PST [juridico]
        - denominacion_comercial (str): Denominacion comercial del PST [juridico]
        - tipo_figura (str): Tipo figura juridica del PST [juridico, natural]
        - rtn (int): RTN o certificado comercial del PST [juridico, natural]
        - user (object): objeto usuario que lo creo [juridico, natural]
        - cedula (str):  cedula del PST natural [natural]
        - nombres (str): nombre del PST [natural]
        - apellidos (str): apellido del PST [natural]
        - estatus (int): estatus actual del registro del PST [juridico, natural] ----
        - tipo_pst (int): tipo de persona juridica PST [juridico, natural]
        - telefono_fijo (str): telefono del PST [natural]
        - telefono_celular (str): telefono celular del PST [natural]
        - correo_electronico (str): correo electronico del PST [natural]
        - emprendedor (boolean): boleano que detemina si es emprendedor el PST [juridico, natural]
        - archivo_pasaporte (file): archivo de tipo PDF con copia del pasaporte [natural]
        - archivo_cedula (file): archivo de tipo PDF con copia de la cedula [natural]
        - archivo_rif (file): archivo de tipo PDF con copia del rif [natural]
        """
        if isinstance(data, Storage):
            obj = cls()
            obj.tipo_juridica = data.tipo_juridica
            obj.rif = data.rif
            obj.razon_social = data.razon_social
            obj.pagina_web = data.pagina_web
            obj.denominacion_comercial = data.denominacion_comercial
            obj.tipo_figura = data.tipo_figura
            obj.rtn = data.rtn
            obj.user = data.user
            obj.cedula = data.cedula
            obj.nombres = data.nombres
            obj.apellidos = data.apellidos
            obj.telefono_fijo = data.telefono_fijo
            obj.telefono_celular = data.telefono_celular
            obj.correo_electronico = data.correo_electronico
            obj.emprendedor = data.emprendedor
            obj.archivo_pasaporte = data.archivo_pasaporte
            obj.archivo_cedula = data.archivo_cedula
            obj.archivo_rif = data.archivo_rif
            obj.tipo_pst = data.tipo_pst

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def save(self, *args, **kwargs):
        super(Pst, self).save(*args, **kwargs)
        try:
            DatoEspecifico.objects.get(pst=self)
        except DatoEspecifico.DoesNotExist:
            DatoEspecifico(pst=self).save(force=True)

    def __unicode__(self):
        if self.tipo_figura == PERSONA_NATURAL:
            nombre = u'{nombres} {apellidos}'.format(nombres=self.nombres, apellidos=self.apellidos)
        else:
            nombre = u'{razon_social}'.format(razon_social=self.razon_social)

        return u'{rif} - {nombre}'.format(rif=self.rif, nombre=nombre)

    def nombre_o_razon(self):
        if self.tipo_figura == PERSONA_NATURAL:
            nombre = u'{nombres} {apellidos}'.format(nombres=self.nombres, apellidos=self.apellidos)
        else:
            nombre = u'{razon_social}'.format(razon_social=self.razon_social)

        return u'{nombre}'.format(rif=self.rif, nombre=nombre)


class Direccion(CachedModel):
    """
    Modelo Direcciones
    Contiene las direcciones para cada prestador de servicio turístico
    """
    pst = models.ForeignKey('Pst')
    estado = models.ForeignKey(Estado)
    municipio = models.ForeignKey(Municipio)
    parroquia = models.ForeignKey(Parroquia)
    urbanizacion = models.CharField(max_length=150, null=True, blank=True)
    avenida_calle = models.CharField(max_length=150, null=True, blank=True)
    edificio = models.CharField(max_length=150, null=True, blank=True)
    oficina_apartamento = models.CharField(max_length=30, null=True, blank=True)
    codigo_postal = models.IntegerField(null=True, blank=False)
    punto_referencia = models.TextField(max_length=250, null=True, blank=True)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Dirección a partir de la información suministrada.
        El Storage data debe contener
        - pst (int): Objeto Pst
        - estado (int): Objeto Estado
        - municipio (int): Objeto Municipio
        - parroquia (int): Objeto Parroquia
        - urbanizacion (str): Direccion de la Urbanización/Sector
        - avenida_calle (str): Direccion de la Avenida/Calle/Carrera
        - edificio (str): Nombre del Edificio/Casa
        - oficina_apartamento (str): numero de la Oficina/Apto
        - codigo_postal (str): Numero de odigo postal
        - punto_referencia (str): Punto de referencia de la localizacion
        """
        if isinstance(data, Storage):
            obj = cls()
            obj.pst = data.pst
            obj.estado = data.estado
            obj.municipio = data.municipio
            obj.parroquia = data.parroquia
            obj.urbanizacion = data.urbanizacion
            obj.avenida_calle = data.avenida_calle
            obj.edificio = data.edificio
            obj.oficina_apartamento = data.oficina_apartamento
            obj.codigo_postal = data.codigo_postal
            obj.punto_referencia = data.punto_referencia

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def __unicode__(self):
        return u'{}, {}, {}, {}{}, {}, {}, Código Postal: {}.'.format(
            self.urbanizacion,
            self.avenida_calle,
            self.edificio,
            (
                self.oficina_apartamento + ', '
                if self.oficina_apartamento else ''
            ),
            self.estado,
            self.parroquia,
            self.municipio,
            self.codigo_postal
        )


class RepresentanteContacto(CachedModel):
    """
    Modelo Representantes
    Contiene los Representantes de cada prestador de servicio turístico de tipo juridico
    """
    pst = models.ForeignKey('Pst')
    nombres = models.CharField(max_length=50, null=True, blank=True)
    apellidos = models.CharField(max_length=50, null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    rif = models.CharField(max_length=20, null=True, blank=False)
    cargo_empresa = models.CharField(max_length=75, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
    telefono_celular = models.CharField(max_length=20, null=True, blank=True)
    correo_electronico = models.EmailField(max_length=75, null=True, blank=True)
    tipo = models.IntegerField(choices=TIPO_REPRESENANTE, default=REPRESENTANTE)
    pagina_web = models.URLField(null=True, blank=True)
    archivo_cedula = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_rif = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )


    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto RepresentanteContacto a partir de la información
        suministrada.
        El Storage data debe contener
        - pst (int): Objeto Pst
        - nombres (str): nombre del representante o contacto
        - apellidos (str): apellidos del representante o contacto
        - rif (str): rif del representante o contacto
        - cargo_empresa (str): cargo en la empresa
        - telefono_fijo (str): telefono fijo del representante o contacto
        - telefono_celular (str): telefono celular del representante o contacto
        - correo_electronico (str): correo electronico del representante o contacto
        - archivo_cedula (file): copia de la cedula del representante o contacto
        - archivo_rif (file): copia de la rif del representante o contacto
        - tipo (int): tipo  representante o contacto
        """
        if isinstance(data, Storage):
            obj = cls()
            obj.pst = data.pst
            obj.nombres = data.nombres
            obj.apellidos = data.apellidos
            obj.cedula = data.cedula
            obj.rif = data.rif
            obj.cargo_empresa = data.cargo_empresa
            obj.telefono_fijo = data.telefono_fijo
            obj.telefono_celular = data.telefono_celular
            obj.correo_electronico = data.correo_electronico
            obj.archivo_cedula = data.archivo_cedula
            obj.archivo_rif = data.archivo_rif
            obj.tipo = data.tipo

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class Accionista(CachedModel):
    """
    Modelo Accionista
    Contiene los Accionistas de cada prestador de servicio turístico de tipo juridico
    """
    pst = models.ForeignKey('Pst')
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=20)
    rif = models.CharField(max_length=20)
    fecha_incorporacion = models.DateField(blank=True)
    numero_acciones = models.IntegerField()
    director = models.BooleanField(default=False, blank=True)

    archivo_cedula = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_rif = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Accionista a partir de la información suministrada.
        El Storage data debe contener
        - pst (obj): Objeto Pst
        - nombres (str): nombre accionista
        - apellidos (int): apellidos del accionista
        - cedula (str): cedula del accionista
        - rif (str): rif del accionista
        - fecha_incorporacion (date): fecha de incorporacion
        - numero_acciones (int): numero de acciones
        - archivo_cedula (file): archivo con copia la cedula
        - archivo_rif (str): archivo con copia del rif
        - director (boolean): True, False para identificar si es director el contacto
        """
        if isinstance(data, Storage):
            obj = cls()
            obj.pst = data.pst
            obj.nombres = data.nombres
            obj.apellidos = data.apellidos
            obj.cedula = data.cedula
            obj.rif = data.rif
            obj.fecha_incorporacion = data.fecha_incorporacion
            obj.numero_acciones = data.numero_acciones
            obj.archivo_cedula = data.archivo_cedula
            obj.archivo_rif = data.archivo_rif
            obj.director = data.director

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class DatoEspecifico(CachedModel):
    """
    Atributos para el objeto DatosEspecifico
    Contiene los datos_especificos de cada prestador de servicio turístico de tipo natural
    """
    pst = models.ForeignKey('Pst')
    guia_especializado = models.CharField(max_length=75, null=True, blank=True)
    egresado_instituto = models.CharField(max_length=75, null=True, blank=True)
    nombre_curso = models.CharField(max_length=100, null=True, blank=True)
    presta_servicio = models.CharField(max_length=75, null=True, blank=True)
    primeros_auxilios = models.CharField(max_length=75, null=True, blank=True)
    ciudad_primeros_auxilios = models.CharField(max_length=75, null=True, blank=True)
    anios_experiencia = models.IntegerField(null=True, blank=True)
    titulo_universitario = models.CharField(max_length=75, null=True, blank=True)
    grado_licencia = models.IntegerField(choices=GRADO_LICENCIA, null=True, blank=True)
    certificado_medico = models.CharField(max_length=75, null=True, blank=True)
    fecha_primeros_auxilios = models.DateField(null=True, blank=True)
    fecha_vencimiento_licencia = models.DateField(null=True, blank=True)
    fecha_vencimiento_certificado = models.DateField(null=True, blank=True)
    fecha_curso = models.DateField(null=True, blank=True)
    idiomas = models.ManyToManyField('Idioma', through='IdiomasPst', null=True, blank=True)
    archivo_certificado = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_licencia = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_curriculum = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_certificado_guia_especializado = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )
    archivo_constancia_curso_primeros_auxilios = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )


class Idioma(models.Model):
    """
    Atributos para el objeto Idiomas
    Contiene todos los idiomas disponibles para los prestadores de servicios
    """
    nombre = models.CharField(max_length=75)

    def __unicode__(self):
        return u'{}'.format(self.nombre)


class IdiomasPst(models.Model):
    """
    Atributos para el objeto IdiomasPst
    Contiene los idiomas aprendidos para cada prestador de servicio turístico de tipo natural
    """
    idioma = models.ForeignKey('Idioma')
    dato_especifico = models.ForeignKey(DatoEspecifico)
    lee = models.BooleanField(blank=True, default=False)
    habla = models.BooleanField(blank=True, default=False)
    escribe = models.BooleanField(blank=True, default=False)


class Acta(CachedModel):
    """
    Atributos para el objeto Acta
    Contiene los actas constitutivas para cada prestador de servicio turístico de tipo juririco
    """
    pst = models.ForeignKey('Pst')
    circuito_circunscripcion = models.ForeignKey('Circunscripcion')
    registro_mercantil = models.ForeignKey('RegistroMercantil')
    tomo = models.CharField(max_length=20, blank=True)
    numero_tomo = models.IntegerField(null=True)
    fecha_registro = models.DateField(blank=True)
    fecha_ultima_asamblea = models.DateField(null=True, blank=True)
    duracion = models.IntegerField(null=True)
    capital_suscrito = models.FloatField(blank=True, null=True)
    capital_pagado = models.FloatField(blank=True, null=True)
    objetivo_modificacion = models.IntegerField(choices=TIPO_MODIFICACION, blank=True, null=True)
    tipo_acta = models.IntegerField(choices=TIPO_ACTA_CONSTITUTIVA, blank=True, null=True, default=ORIGINAL)
    motivo_modificacion = models.TextField(max_length=250, null=True, blank=True)
    archivo_acta_constitutiva = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Acta a partir de la información suministrada.
        El Storage data debe contener
        - pst (int): Objeto Pst
        - circuito_circunscripcion (int): Objeto Circunscripcion
        - registro_mercantil (int): Objeto RegistroMercanti
        - tomo (str): tomo de la acta constitutiva
        - numero_tomo (int): numero de tomo
        - fecha_registro (date): fecha de registro
        - fecha_ultima_asamblea (date): fecha de la ultima asamblea realizada
        - duracion (str): Duración de la empresa
        - capital_suscrito (float): capital suscrito
        - capital_pagado (float): copia de la rif del representante o contacto
        - archivo_acta_constitutiva (file): Copia del acta constitutiva
        - tipo_acta (int): tipo de acta (modificacion, Original)
        - objetivo_modificacion (str): Descripción del motivo de la modificación de la acta
        """
        if isinstance(data, Storage):
            obj = cls()
            obj.pst = data.pst
            obj.circuito_circunscripcion = data.circuito_circunscripcion
            obj.registro_mercantil = data.registro_mercantil
            obj.tomo = data.tomo
            obj.numero_tomo = data.numero_tomo
            obj.fecha_registro = data.fecha_registro
            obj.fecha_ultima_asamblea = data.fecha_ultima_asamblea
            obj.duracion = data.duracion
            obj.capital_suscrito = data.capital_suscrito
            obj.capital_pagado = data.capital_pagado
            obj.archivo_acta_constitutiva = data.archivo_acta_constitutiva
            obj.objetivo_modificacion = data.objetivo_modificacion
            obj.motivo_modificacion = data.motivo_modificacion
            obj.tipo_acta = data.tipo_acta
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def getTipoActa(self, objPst):
        """
        Metodo que obtiene el tipo  de acta
        parametros
        - obejectPst (obj): objeto Pst
        retorna
            - MODIFICACION(int): cuando el acta es una modificación
            - ORIGINAL(int): cuando el acta es original
        """

        if isinstance(objPst, Pst):
            cantidad = Acta.objects.filter(pst=objPst).count()
            if cantidad > 0:
                return MODIFICACION

            return ORIGINAL

        else:
            raise NameError('Error de Tipo. Debe ser una instancia del objeto Pst')


class Sunacoop(CachedModel):
    """
    Modelo Sunacoop
    Contiene el registro de la superintendencia nacional de cooperativas para cada prestador de
    servicio turístico que sean de tipo juririco y tambien cooperativas
    """
    pst = models.ForeignKey('Pst')
    numero = models.IntegerField(null=True)
    fecha = models.DateField(blank=True)
    archivo_comprobante = ContentTypeRestrictedFileField(
        upload_to=RUTA_DOCUMENTOS,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO
    )

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Sunacoop a partir de la información suministrada.
        El Storage data debe contener
        - pst (Object): Objeto Pst
        - numero (int): Objeto Circunscripcion
        - comprobante (File): archivo pdf con el comprobarte del sunacoop
        """
        if isinstance(data, Storage):
            obj = cls()
            obj.pst = data.pst
            obj.numero = data.numero
            obj.fecha = data.fecha
            obj.archivo_comprobante = data.archivo_comprobante
            return obj

        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class Circunscripcion(models.Model):
    """
    Atributos para el objeto Idiomas
    Contiene todos los idiomas disponibles para los prestadores de servicios
    """
    nombre = models.CharField(max_length=255)

    @classmethod
    def create(cls, nombre):
        """
        Crea una nueva instancia del objeto Acta a partir de la información suministrada.
        El Storage data debe contener
        - nombre (str): nombre de la circunscripcion
        """
        if isinstance(data, str):
            obj = cls()
            obj.nombre = nombre
            return obj
        else:
            raise NameError(u'Error de Tipo. Los parametros enviados no son correctos')

    def __unicode__(self):
        return self.nombre


class RegistroMercantil(models.Model):
    """
    Atributos para el objeto Idiomas
    Contiene todos los idiomas disponibles para los prestadores de servicios
    """
    nombre = models.CharField(max_length=75)

    @classmethod
    def create(cls, nombre):
        """
        Crea una nueva instancia del objeto Acta a partir de la información suministrada.
        El Storage data debe contener
        - nombre (str): nombre del registro mercantil
        """
        if isinstance(data, str):
            obj = cls()
            obj.nombre = nombre
            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def __unicode__(self):
        return self.nombre


class CertificacionesPST(models.Model):
    """
    Modelo creado para llevar un registro log de cada unas de las certificaciones
    realizadas por los usuarios de mintur
    """
    pst = models.ForeignKey(Pst)
    fecha_certificacion = models.DateTimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.IntegerField(choices=TIPO_CERTIFICACION)
    funcionario = models.ForeignKey(MinturUser)
    conclusiones_analisis = models.CharField(max_length=255, null=True, blank=True)
    observaciones_analisis = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'{0} - {1} - {2} - {3}'.format(self.pst,
                                               self.funcionario,
                                               self.observaciones,
                                               self.fecha_certificacion)


class CertificacionRIFTUR(models.Model):
    """
    Modelo creado para registrar el RIFTUR asociado a cada PST
        Formatos:
            numero_contribuyente = rif + consecutivo
            numero_comprobante = YYYYMMN0000000000002 => año + mes + consecutivo
    """
    pst = models.ForeignKey(Pst)
    fecha_certificacion = models.DateTimeField(auto_now_add=True)
    numero_comprobante = models.CharField(max_length=100, null=False, blank=False)
    numero_contribuyente = models.CharField(max_length=100, null=True, blank=True)
    funcionario = models.ForeignKey(MinturUser)

    def __unicode__(self):
        return u'{0} - {1} - {2} - {3}'.format(
            self.numero_comprobante,
            self.numero_contribuyente,
            self.pst,
            self.fecha_certificacion
        )


class CertificacionRTN(models.Model):
    """
    Modelo creado para registrar el RTN asociado a un PST
    """
    pst = models.ForeignKey(Pst)
    fecha_certificacion = models.DateTimeField(auto_now_add=True)
    numero_comprobante = models.CharField(max_length=100, null=False, blank=False)
    rtn = models.CharField(max_length=100, null=True, blank=True)
    funcionario = models.ForeignKey(MinturUser)

    def __unicode__(self):
        return u'{0} - {1} - {2} - {3}'.format(
            self.numero_comprobante,
            self.rtn,
            self.pst,
            self.fecha_certificacion
        )


class Sucursales(CachedModel):
    """
    Modelo Sucursales
    Contiene las sucursales para cada prestador de servicio turístico
    """
    pst = models.ForeignKey('Pst')
    estado = models.ForeignKey(Estado)
    municipio = models.ForeignKey(Municipio)
    parroquia = models.ForeignKey(Parroquia)
    nombre = models.CharField(max_length=150, blank=True)
    urbanizacion = models.CharField(max_length=150, blank=True)
    avenida_calle = models.CharField(max_length=150, blank=True)
    edificio = models.CharField(max_length=150, blank=True)
    oficina_apartamento = models.CharField(max_length=30, blank=True)
    codigo_postal = models.IntegerField(null=True, blank=False)
    punto_referencia = models.TextField(max_length=250, blank=True)

    @classmethod
    def create(cls, data):
        """
        Crea una nueva instancia del objeto Sucursales a partir de la información suministrada.
        El Storage data debe contener
        - pst (int): Objeto Pst
        - estado (int): Objeto Estado
        - municipio (int): Objeto Municipio
        - parroquia (int): Objeto Parroquia
        - urbanizacion (str): Direccion de la Urbanización/Sector
        - avenida_calle (str): Direccion de la Avenida/Calle/Carrera
        - edificio (str): Nombre del Edificio/Casa
        - oficina_apartamento (str): numero de la Oficina/Apto
        - codigo_postal (str): Numero de odigo postal
        - punto_referencia (str): Punto de referencia de la localizacion
        - nombre (str): nombre de la sucursal
        """

        if isinstance(data, Storage):
            obj = cls()
            obj.pst = data.pst
            obj.estado = Estado.objects.get(pk=int(data.estado))
            obj.municipio = Municipio.objects.get(pk=int(data.municipio))
            obj.parroquia = Parroquia.objects.get(pk=int(data.parroquia))
            obj.nombre = data.nombre
            obj.urbanizacion = data.urbanizacion
            obj.avenida_calle = data.avenida_calle
            obj.edificio = data.edificio
            obj.oficina_apartamento = data.oficina_apartamento
            obj.codigo_postal = data.codigo_postal
            obj.punto_referencia = data.punto_referencia

            return obj
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')


class RegistroPaso(models.Model):
    es_opcional = models.BooleanField()
    paso = models.IntegerField()
    proceso = models.CharField(max_length=30)
    pst = models.ForeignKey('Pst')


class SolicitudCambioPerfil(models.Model):
    pst = models.ForeignKey(
        'Pst', null=False, blank=False
    )
    fecha_generacion = models.DateTimeField(
        auto_now_add=True, null=False, blank=False
    )
    fecha_verificacion = models.DateTimeField(
        null=True, blank=False
    )
    activo = models.BooleanField(
        default=True, null=False, blank=False
    )
    observaciones = models.TextField(
        null=True, blank=False
    )


class ActividadComercial(CachedModel):
    actividad = models.ForeignKey('TipoPst')
    pst = models.ForeignKey('Pst')
    tipo_actividad = models.IntegerField(choices=TIPO_ACTIVIDAD, default=ACTIVIDAD_PRINCIPAL)
    licencia = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'{}'.format(self.actividad)