# -*- coding: utf-8 -*-

u""" Vistas para el registro de una persona natural. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.cuentas.mixins import MenuPSTMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from json import dumps as json_dumps
from registro import forms
from registro import models
from utils import views_helpers as helpers
from utils.gluon.storage import Storage
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TABLA_PASO4 = {
    models.TipoPst.objects.get(nombre=u'Agente Turístico').id: (
        reverse_lazy('cuentas_natural_4_agente')
    ),
    models.TipoPst.objects.get(nombre=u'Conductor Turístico').id: (
        reverse_lazy('cuentas_natural_4_conductor')
    ),
    models.TipoPst.objects.get(nombre=u'Guía Turístico').id: (
        reverse_lazy('cuentas_natural_4_guia')
    ),
}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Paso1View(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'registro/natural_paso1.html'
    success_url = reverse_lazy('cuentas_natural_2')
    form_class = forms.natural.Paso1Form

    def get_initial(self):
        self.pst = helpers.get_object_or_none(
            models.Pst, user=self.request.user, cached=True
        )

        initial_data = super(Paso1View, self).get_initial(
            models.Pst, {'user': self.request.user, 'cached': True}
        )

        self.actividad_principal = helpers.get_object_or_none(
            models.ActividadComercial,
            pst=self.pst,
            tipo_actividad=models.ACTIVIDAD_PRINCIPAL,
            cached=True
        )

        if self.actividad_principal:
            initial_data.update({
                'actividad': self.actividad_principal.actividad.pk,
                'actividad_principal_licencia': (
                    self.actividad_principal.licencia
                )
            })
        return initial_data

    def get_context_data(self, *args, **kwargs):
        context = super(Paso1View, self).get_context_data(*args, **kwargs)
        pst_obj = models.Pst.objects.get(user=self.request.user)
        actividades_list = []
        act_sec = []
        tipos = models.TipoPst.objects.filter(
            tipo_persona__in=[models.PERSONA_NATURAL, models.OTRAS]
        )
        for t in tipos:
            group="Actividades relacionadas con turismo"
            if t.tipo_persona == models.OTRAS:
                group="Otras"
            
            actividades_list.append({
                "id": t.id, "nombre": t.nombre, "group": group,
            })

        actividades_secundarias = models.ActividadComercial.objects.filter(
            pst=pst_obj,
            tipo_actividad=models.ACTIVIDAD_SECUNDARIA,
            cached=True,
        )

        for a in actividades_secundarias:
            group="Actividades relacionadas con turismo"
            if a.actividad.tipo_persona == models.OTRAS:
                group="Otras"
            act_sec.append({
                "id": a.id, 
                "nombre": a.actividad.nombre,
                "licencia": a.licencia, 
                "actividad_id": a.actividad.id,
                "group": group
            })

        context.update({
            'profile': (
                'Emprendedor' if pst_obj.emprendedor
                else 'Prestador de Servicios Turísticos'
            ),
            'estatus': pst_obj.get_estatus_display(),
            'tipo_figura_display': pst_obj.get_tipo_figura_display(),
            'actividades_list': json_dumps(actividades_list, ensure_ascii=True),
            'actividades_secundarias': json_dumps(act_sec, ensure_ascii=True)
        })

        return context

    @helpers.registrar_paso(1, 'natural')
    def form_valid(self, form):
        user = self.request.user
        data = helpers.get_files_from_form(form)
        data.update({
            'apellidos': form.cleaned_data['apellidos'],
            'cedula': form.cleaned_data['cedula'],
            'nombres': form.cleaned_data['nombres'],
            'rif': form.cleaned_data['rif'],
            'rtn': form.cleaned_data['rtn'],
            'telefono_celular': form.cleaned_data['telefono_celular'],
            'telefono_fijo': form.cleaned_data['telefono_fijo'],
            'tipo_figura': form.cleaned_data['tipo_figura'],
            'estado_contribuyente': form.cleaned_data['estado_contribuyente'],
            'inicio_actividad_comercial': form.cleaned_data['inicio_actividad_comercial'],
            'user': user,
        })

        data.update({
            'razon_social': data['nombres'] + u' ' + data['apellidos']
        })

        helpers.save_or_update(models.Pst, {'user': user}, data)

        data = {
            'actividad': form.cleaned_data['actividad'],
            'tipo_actividad': models.ACTIVIDAD_PRINCIPAL,
            'licencia': form.cleaned_data['actividad_principal_licencia'],
        }

        helpers.save_or_update(models.ActividadComercial, {
            'pst': self.pst, 'tipo_actividad': models.ACTIVIDAD_PRINCIPAL
            }, data
        )

        if self.pst.estatus != models.ESTATUS_REGISTRO_SIN_COMPLETAR:
            random_field = helpers.get_datos_especificos_para_pst_natural(
                self.pst, Storage(
                    actividad=Storage(nombre=unicode(data['actividad']))
                )
            ).items()[0][1]

            consider_change_on_actividad_principal = (
                self.actividad_principal is not None
                and self.actividad_principal.actividad != data['actividad']
                and not random_field
            )

            pst = models.Pst.objects.get(user=user)
            models.RegistroPaso.objects.filter(pst=pst, paso=4).delete()

            if consider_change_on_actividad_principal:
                pst.estatus = models.ESTATUS_REGISTRO_EN_ESPERA

            else:
                pst.estatus = models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
                models.RegistroPaso(
                    pst=pst, paso=4, proceso='natural', es_opcional=False
                ).save()

            pst.save(force=True)

        return super(Paso1View, self).form_valid(form)


class Paso2View(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'registro/natural_paso2.html'
    success_url = reverse_lazy('cuentas_natural_3')
    form_class = forms.natural.Paso2Form

    def get_initial(self):
        self.pst = helpers.get_object_or_none(
            models.Pst, user=self.request.user, cached=True
        )

        initial_data = super(Paso2View, self).get_initial(
            models.Direccion, {'pst': self.pst, 'cached': True}
        )

        return initial_data

    @helpers.registrar_paso(2, 'natural')
    def form_valid(self, form):
        data = {
            'avenida_calle': form.cleaned_data['avenida_calle'],
            'codigo_postal': form.cleaned_data['codigo_postal'],
            'edificio': form.cleaned_data['edificio'],
            'estado': form.cleaned_data['estado'],
            'municipio': form.cleaned_data['municipio'],
            'oficina_apartamento': form.cleaned_data['oficina_apartamento'],
            'parroquia': form.cleaned_data['parroquia'],
            'pst': self.pst,
            'punto_referencia': form.cleaned_data['punto_referencia'],
            'urbanizacion': form.cleaned_data['urbanizacion'],
        }
        helpers.save_or_update(models.Direccion, {'pst': self.pst}, data)

        return super(Paso2View, self).form_valid(form)


class Paso3View(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'registro/natural_paso3.html'
    success_url = reverse_lazy('cuentas_natural_4')
    form_class = forms.natural.Paso3Form

    def get_initial(self):
        self.pst = models.Pst.objects.get(
            user=self.request.user, cached=True
        )
        initial_data = super(Paso3View, self).get_initial(
            models.Acta, {'pst': self.pst, 'cached': True}
        )
        return initial_data

    @helpers.registrar_paso(3, 'natural')
    def get(self, request):
        return super(Paso3View, self).get(request)

    @helpers.registrar_paso(3, 'natural')
    def form_valid(self, form):
        data = helpers.get_files_from_form(form)
        data.update({
            'circuito_circunscripcion': form.cleaned_data[
                'circuito_circunscripcion'
            ],
            'fecha_registro': form.cleaned_data['fecha_registro'],
            'numero_tomo': form.cleaned_data['numero_tomo'],
            'pst': self.pst,
            'registro_mercantil': form.cleaned_data['registro_mercantil'],
            'tomo': form.cleaned_data['tomo'],
        })
        helpers.save_or_update(models.Acta, {'pst': self.pst}, data)

        return super(Paso3View, self).form_valid(form)


class Paso4AgenteView(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'registro/natural_paso4_agente.html'
    success_url = reverse_lazy('cuentas_natural_5')
    form_class = forms.natural.Paso4AgenteForm

    def get_initial(self):
        self.pst = models.Pst.objects.get(
            user=self.request.user, cached=True
        )
        initial_data = super(Paso4AgenteView, self).get_initial(
            models.DatoEspecifico, {'pst': self.pst, 'cached': True}
        )
        return initial_data

    @helpers.registrar_paso(4, 'natural')
    def form_valid(self, form):
        data = helpers.get_files_from_form(form)
        data.update({
            'anios_experiencia': form.cleaned_data['anios_experiencia'],
            'pst': self.pst,
            'titulo_universitario': form.cleaned_data['titulo_universitario'],
        })
        helpers.save_or_update(models.DatoEspecifico, {'pst': self.pst}, data)

        return super(Paso4AgenteView, self).form_valid(form)


class Paso4ConductorView(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'registro/natural_paso4_conductor.html'
    success_url = reverse_lazy('cuentas_natural_5')
    form_class = forms.natural.Paso4ConductorForm

    def get_initial(self):
        self.pst = models.Pst.objects.get(
            user=self.request.user, cached=True
        )
        initial_data = super(Paso4ConductorView, self).get_initial(
            models.DatoEspecifico, {'pst': self.pst, 'cached': True}
        )
        return initial_data

    @helpers.registrar_paso(4, 'natural')
    def form_valid(self, form):
        data = helpers.get_files_from_form(form)
        data.update({
            'grado_licencia': form.cleaned_data['grado_licencia'],
            'certificado_medico': form.cleaned_data['certificado_medico'],
            'fecha_vencimiento_certificado': form.cleaned_data[
                'fecha_vencimiento_certificado'
            ],
            'fecha_vencimiento_licencia': form.cleaned_data[
                'fecha_vencimiento_licencia'
            ],
        })
        helpers.save_or_update(models.DatoEspecifico, {'pst': self.pst}, data)

        return super(Paso4ConductorView, self).form_valid(form)


class Paso4GuiaView(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'registro/natural_paso4_guia.html'
    success_url = reverse_lazy('cuentas_natural_5')
    form_class = forms.natural.Paso4GuiaForm

    def get_initial(self):
        self.pst = models.Pst.objects.get(
            user=self.request.user, cached=True
        )
        initial_data = super(Paso4GuiaView, self).get_initial(
            models.DatoEspecifico, {'pst': self.pst, 'cached': True}
        )
        return initial_data

    @helpers.registrar_paso(4, 'natural')
    def form_valid(self, form):
        data = helpers.get_files_from_form(form)
        data.update({
            'ciudad_primeros_auxilios': form.cleaned_data[
                'ciudad_primeros_auxilios'
            ],
            'egresado_instituto': form.cleaned_data['egresado_instituto'],
            'fecha_curso': form.cleaned_data['fecha_curso'],
            'fecha_primeros_auxilios': form.cleaned_data[
                'fecha_primeros_auxilios'
            ],
            'guia_especializado': form.cleaned_data['guia_especializado'],
            'nombre_curso': form.cleaned_data['nombre_curso'],
            'presta_servicio': form.cleaned_data['presta_servicio'],
            'primeros_auxilios': form.cleaned_data['primeros_auxilios'],
        })
        helpers.save_or_update(models.DatoEspecifico, {'pst': self.pst}, data)

        return super(Paso4GuiaView, self).form_valid(form)


class Paso5View(TemplateView, MenuPSTMixin):
    template_name = 'registro/natural_paso5.html'

    @helpers.verificar_pasos('natural', 4)
    def get(self, *args, **kwargs):
        return super(Paso5View, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Paso5View, self).get_context_data(*args, **kwargs)

        pst = helpers.get_object_or_none(models.Pst, user=self.request.user)

        if pst.estatus == models.ESTATUS_REGISTRO_EN_ESPERA:
            pst.estatus = models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
            pst.save(force=True)

        pst = helpers.get_object_or_none(
            models.Pst, user=self.request.user, cached=True
        )

        context.update({'pst': pst, 'user': self.request.user})

        context['actividad_principal'] = helpers.get_object_or_none(
            models.ActividadComercial,
            pst=pst,
            tipo_actividad=models.ACTIVIDAD_PRINCIPAL,
            cached=True
        )

        context['actividades_secundarias'] = helpers.filter_object_or_list(
            models.ActividadComercial,
            pst=pst,
            tipo_actividad=models.ACTIVIDAD_SECUNDARIA,
            cached=True
        )

        context['datos_especificos'] = (
            helpers.get_datos_especificos_para_pst_natural(
                pst, context['actividad_principal']
            )
        )

        context['direccion'] = helpers.get_object_or_none(
            models.Direccion, pst=pst, cached=True
        )

        return context


class Paso6View(TemplateView, MenuPSTMixin):
    template_name = 'registro/natural_paso6.html'

    @helpers.verificar_pasos('natural', 4)
    def get(self, request):
        return super(Paso6View, self).get(request)

    def post(self, request, *args, **kwargs):
        if request.POST['csrfmiddlewaretoken']:
            pst = models.Pst.objects.get(user=request.user, cached=True)

            if pst.emprendedor:
                pst.estatus = models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
                pst.save()
                helpers.CertificarRegistro.certificar(pst)

            else:
                pst = models.Pst.objects.get(user=request.user)
                pst.estatus = models.ESTATUS_REGISTRO_COMPLETADO
                pst.save(force=True)

        return redirect(reverse_lazy('cuentas_natural_7'))


class Paso7View(TemplateView, MenuPSTMixin):
    template_name = 'registro/natural_paso7.html'

    @helpers.verificar_pasos('natural', 4)
    def get(self, request):
        return super(Paso7View, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(Paso7View, self).get_context_data(**kwargs)
        context.update({
            'emprendedor': models.Pst.objects.get(
                user=self.request.user
            ).emprendedor
        })
        return context
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
def paso4_view(request):
    pst = helpers.get_object_or_none(
        models.Pst, user=request.user, cached=True
    )

    actividad = helpers.get_object_or_none(
        models.ActividadComercial,
        pst=pst,
        cached=True,
        tipo_actividad=models.ACTIVIDAD_PRINCIPAL
    )

    if not pst or not actividad:
        return redirect(reverse_lazy('cuentas_natural_1'))

    tipo_pst = actividad.actividad.id

    if tipo_pst not in TABLA_PASO4:
        tipo_pst = TABLA_PASO4.keys()[0]

    return redirect(TABLA_PASO4[tipo_pst])


@login_required(login_url=reverse_lazy('cuentas_login'))
def tiene_firma_personal_rest(request):
    pst = models.Pst.objects.get(
        user=request.user, cached=True
    )

    if 'tiene_firma_personal' in request.POST:
        pst.tiene_firma_personal = (
            request.POST['tiene_firma_personal'] == 'true'
        )
        pst.save()

    return helpers.json_response(
        {'tiene_firma_personal': pst.tiene_firma_personal}
    )


@login_required(login_url=reverse_lazy('cuentas_login'))
def idiomas_rest(request):
    idiomas = models.Idioma.objects.all()

    return helpers.json_response({
        'error': 0,
        'result': serializers.serialize('json', idiomas)
    })


@login_required(login_url=reverse_lazy('cuentas_login'))
def idiomas_pst_rest(request):
    try:
        dato_especifico = models.DatoEspecifico.objects.get(
            pst=models.Pst.objects.get(user=request.user)
        )
    except models.DatoEspecifico.DoesNotExist:
        dato_especifico = models.DatoEspecifico(
            pst=models.Pst.objects.get(user=request.user)
        )
        dato_especifico.save(force=True)

    if request.method == 'GET':
        idiomas_pst = models.IdiomasPst.objects.filter(
            dato_especifico=dato_especifico
        )
        idiomas = [
            row.idioma.nombre for row in idiomas_pst
        ]
        return helpers.json_response({
            'error': 0,
            'result': serializers.serialize('json', idiomas_pst),
            'attached': idiomas
        })

    if request.method == 'POST':
        data = {
            'idioma': models.Idioma.objects.get(
                id=request.POST.get('idioma_id')
            ),
            'lee': request.POST.get('lee'),
            'habla': request.POST.get('habla'),
            'escribe': request.POST.get('escribe'),
        }

        for value in data.itervalues():
            if value is None:
                return helpers.json_response({
                    'error': -1, 'result': [], 'msg': 'Faltan parámetros.'
                })

        for destreza in ['lee', 'habla', 'escribe']:
            data[destreza] = (data[destreza] == 'true')

        idiomas_pst = models.IdiomasPst.objects.filter(
            dato_especifico=dato_especifico,
            idioma=data['idioma']
        )

        if idiomas_pst.exists():
            return helpers.json_response({
                'error': -2,
                'result': [],
                'msg': 'Este idioma ya está registrado'
            })

        idioma_pst = models.IdiomasPst(
            dato_especifico=dato_especifico, **data
        )
        idioma_pst.save()

        return helpers.json_response({
            'error': 0,
            'result': serializers.serialize('json', [idioma_pst]),
            'attached': idioma_pst.idioma.nombre
        })


@login_required(login_url=reverse_lazy('cuentas_login'))
@require_http_methods(['POST'])
def idiomas_pst_del(request):
    try:
        dato_especifico = models.DatoEspecifico.objects.get(
            pst=models.Pst.objects.get(user=request.user)
        )
    except models.DatoEspecifico.DoesNotExist:
        dato_especifico = models.DatoEspecifico(
            pst=models.Pst.objects.get(user=request.user)
        )
        dato_especifico.save()

    try:
        idioma_pst = models.IdiomasPst.objects.get(
            id=request.POST.get('idioma_pst_id')
        )
    except models.IdiomasPst.DoesNotExist:
        return helpers.json_response({
            'error': -3,
            'result': [],
            'msg': 'No existe ese IdiomasPst'
        })

    idioma_pst.delete()

    return helpers.json_response({'error': 0, 'result': []})
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
