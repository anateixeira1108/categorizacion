# -*- coding: utf-8 -*-

u""" Utilidades de uso general para las vistas de la aplicación. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.cuentas import models as cuentas_models
from collections import OrderedDict
from datetime import date
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from json import dumps as json_dumps
from json import loads as json_loads
from re import compile as re_compile
from registro import models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LISTED_FIELDS = {
    u'Agente Turístico': (
        ('anios_experiencia', u'Años de experiencia'),
        ('archivo_curriculum', u'Currículum Vitae'),
        ('titulo_universitario', u'Título universitario'),
    ),
    u'Conductor Turístico': (
        ('archivo_certificado', u'Copia del certificado médico'),
        ('archivo_licencia', u'Copia de la licencia de conducir'),
        ('certificado_medico', u'No. del Certificado Médico'),
        ('fecha_vencimiento_certificado', u'Vencimiento del certificado'),
        ('fecha_vencimiento_licencia', u'Vencimiento de la licencia'),
        ('get_grado_licencia_display', u'Grado de la licencia de conducir'),
    ),
    u'Guía Turístico': (
        ('guia_especializado', u'Nivel de guía especializado'),
        (
            'archivo_certificado_guia_especializado',
            u'Certificado de guía especializado'
        ),
        ('egresado_instituto', u'Instituto del cual egresó'),
        ('nombre_curso', u'Nombre del curso'),
        ('fecha_curso', u'Fecha del curso'),
        ('presta_servicio', u'Empresa donde presta servicio'),
        ('primeros_auxilios', u'Primeros auxilios (Instituto)'),
        ('ciudad_primeros_auxilios', u'Primeros auxilios (Ciudad)'),
        ('fecha_primeros_auxilios', u'Primeros auxilios (Fecha)'),
        (
            'archivo_constancia_curso_primeros_auxilios',
            u'Primeros auxilios (Constancia)'
        ),
    ),
}

TABLE_CLASS_MAP = {
    models.Accionista._meta.db_table: models.Accionista,
    models.Acta._meta.db_table: models.Acta,
    models.ActividadComercial._meta.db_table: models.ActividadComercial,
    models.DatoEspecifico._meta.db_table: models.DatoEspecifico,
    models.Direccion._meta.db_table: models.Direccion,
    models.Pst._meta.db_table: models.Pst,
    models.RepresentanteContacto._meta.db_table: models.RepresentanteContacto,
    models.Sucursales._meta.db_table: models.Sucursales,
    models.Sunacoop._meta.db_table: models.Sunacoop,
}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class FormViewBaseClass(FormView):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(FormViewBaseClass, self).dispatch(*args, **kwargs)

    def get_initial(self, cls, lookup):
        fields = (
            field for field in self.form_class.base_fields.iterkeys()
            if field not in ['idiomas', 'cached']
        )
        obj = get_object_or_none(cls, **lookup)

        return ({} if not obj else {
            field: process_field_value(getattr(obj, field)) for field in fields
            if field in obj._meta.get_all_field_names()
        })


class CertificarRegistro(object):
    @classmethod
    def _get_dummy_reg(cls, model_cls, pst, pk):
        field_name_list = [field.name for field in model_cls._meta.fields]

        if 'user' in field_name_list:
            dummy_reg = model_cls.objects.get(
                pk=pk, user=pst.user, cached=True
            )

        elif 'pst' in field_name_list:
            dummy_reg = model_cls.objects.get(
                pk=pk, pst=pst, cached=True
            )

        elif 'dato_especifico' in field_name_list:
            dummy_reg = model_cls.objects.get(
                pk=pk,
                dato_especifico=pst.datoespecifico_set.first(),
                cached=True
            )

        return dummy_reg

    @classmethod
    def certificar(cls, pst):
        assert isinstance(pst, models.Pst)

        with transaction.atomic():
            for cached_reg in models.Cache.objects.filter(relacion_id=pst.pk):
                model_cls = TABLE_CLASS_MAP[cached_reg.tabla]
                json_data = json_loads(cached_reg.datos_json)[0]
                dummy_reg = cls._get_dummy_reg(model_cls, pst, json_data['pk'])

                try:
                    model_reg = model_cls.objects.get(pk=json_data['pk'])

                except ObjectDoesNotExist:
                    dummy_reg.save(force=True)

                else:
                    for field in model_cls._meta.fields:
                        setattr(model_reg, field.name, getattr(
                            dummy_reg, field.name
                        ))
                    model_reg.save(force=True)

                cached_reg.delete()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_files_from_form(form):
    return {field: value for field, value in form.files.iteritems()}


def get_datos_especificos_para_pst_natural(pst, actividad_principal):
    dato_especifico = get_object_or_none(
        models.DatoEspecifico, pst=pst, cached=True
    )

    if dato_especifico is None:
        return {}

    if not actividad_principal or not actividad_principal.actividad:
        return {}

    fields = OrderedDict()

    for field, alias in LISTED_FIELDS[actividad_principal.actividad.nombre]:
        if hasattr(dato_especifico, field):
            fields[alias] = process_field_value(
                getattr(dato_especifico, field)
            )

    return fields


def get_object_or_none(cls, **kwargs):
    u""" Devuelve None si el registro solicitado no existe. """
    try:
        return cls.objects.get(**kwargs)
    except cls.DoesNotExist:
        return None


def filter_object_or_list(cls, **kwargs):
    u""" Devuelve una lista vacia si el registro solicitado no existe. """
    l = cls.objects.filter(**kwargs)
    return l or []


def json_response(data):
    return HttpResponse(json_dumps(data), content_type="application/json")


def make_datetime_tz_aware(datetime_obj):
    return (
        timezone.make_aware(
            datetime_obj, timezone.get_default_timezone()
        ) if timezone.is_naive(datetime_obj) else datetime_obj
    )


def process_field_value(value):
    u""" Da formato a cierto tipo de valores ante de su retorno a la vista. """
    if hasattr(value, 'pk'):
        return getattr(value, 'pk')
    if isinstance(value, date):
        return value.strftime('%d/%m/%Y')
    return value


def save_or_update(cls, lookup, data):
    u""" Actualiza el registro o crea uno nuevo si éste no existe. """
    try:
        if issubclass(cls, models.CachedModel):
            obj = cls.objects.get(cached=True, **lookup)
        else:
            obj = cls.objects.get(**lookup)

    except cls.DoesNotExist:
        data.update(lookup)

        if issubclass(cls, models.CachedModel):
            cls(**data).save(force_cached=True)
        else:
            cls(**data).save()

    else:
        for field, value in data.iteritems():
            setattr(obj, field, value)
        obj.save()


def get_dict_array(post, name, name_list=list()):
    """
    Convierte un arreglo de un form a un Dict de python
    Parametros
    - post (QueryDict): parametros Post del formulario
    - name (String): nombre del arreglo que deseas transformar
    - name_list [list]: nlista de campos que se desea obtener
    Retorna
    - dic (dictionary): con los elementos generados del POST

    Ej.
        Params:
        {u'friends[1][name]': [u'Anika'], u'friends[1][tel]': [u'443-421-344'],
         u'friends[0][name]': [u'Peter'], u'friends[0][tel]': [u'123-421-344'],}
        Return:
        {friends: [
            {name: 'Peter', tel: '123-421-344'},
            {name: 'Anika', tel: '443-421-344'}
           ]
        }
    """
    dic = {}
    for k in post.keys():
        if k.startswith(name):
            rest = k[len(name):]
            # divide la cadena en diferentes componentes
            parts = [p[:-1] for p in rest.split('[')][1:]
            try:
                id = int(parts[0])
            except Exception:
                id = str(parts[0])

            # agregar un nuevo diccionario si no existe todavía
            if id not in dic:
                dic[id] = {}
            # agrega la informacion al diccionario
            if parts[1] in name_list:
                dic[id][parts[1]] = post.getlist(k)
            else:
                dic[id][parts[1]] = post.get(k)
    return dic


def nx_get_dict_array(querydict):
    regex = re_compile(r'[\[\]]')

    result_dict = {}
    for fname, fvalue in querydict.iteritems():
        split = filter(None, regex.split(fname))

        if split[-1] == '$$hashKey':
            continue

        target_dict = result_dict
        for fpart in split[:-1]:
            target_dict = target_dict.setdefault(fpart, {})

        target_dict[split[-1]] = fvalue

    return result_dict
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Decoradores ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class requerir_funcionario(object):
    def __init__(self, view_function=False):
        self.view_function = view_function

    def __call__(self, wraped_view):
        def closure(*args, **kwargs):
            self.request = args[0] if self.view_function else args[0].request

            if self.request.user.role == cuentas_models.ROLE_FUNCIONARIO:
                return wraped_view(*args, **kwargs)
            raise Http404
        return closure


class registrar_paso(object):
    def __init__(self, paso_int, proceso_str, es_opcional=False):
        self.paso_int = paso_int
        self.proceso_str = proceso_str
        self.es_opcional = es_opcional

    def __call__(self, form_valid_method):
        def closure(instance, form):
            http_response = form_valid_method(
                instance, form
            )
            pst = models.Pst.objects.get(
                user=instance.request.user
            )
            data = dict(
                es_opcional=self.es_opcional,
                paso=self.paso_int,
                proceso=self.proceso_str,
                pst=pst
            )
            registro_paso = models.RegistroPaso.objects.filter(**data)

            if not registro_paso.exists():
                models.RegistroPaso(**data).save()

            return http_response
        return closure


class verificar_pasos(object):
    def __init__(self, proceso_str, total_pasos_int):
        self.proceso_str = proceso_str
        self.total_pasos_int = total_pasos_int

    def __call__(self, http_get_method):
        def closure(instance, request):
            pst = models.Pst.objects.get(
                user=request.user
            )
            registros_pasos = models.RegistroPaso.objects.filter(
                proceso=self.proceso_str, pst=pst, es_opcional=False
            )

            if registros_pasos.count() < self.total_pasos_int:
                instance.template_name = 'registro/registro_no_completado.html'

            return http_get_method(instance, request)
        return closure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
