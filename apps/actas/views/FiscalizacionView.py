# -*- coding: utf-8 -*-

"""
Vistas para el proceso de la primera certificación de los documentos por parte del funcionario.
"""

from braces.views import LoginRequiredMixin
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View

from Fiscalizacion import FiscalizacionObject
from apps.actas import models
from apps.fiscalizacion.models import CONCLUIDA, EN_PROCESO
from apps.fiscalizacion.models import Fiscalizacion, FuncionariosFiscalizacion
from utils import views_helpers as helpers
from utils.gluon.storage import Storage
from utils.mixins import JSONResponseMixin


# Ajax ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def solicitar_aprobacion_json(request):
    if request.method != 'PUT':
        return helpers.json_response({
            'error': -1, 'msg': 'Method not allowed.'
        })

    request.PUT = QueryDict(request.body)

    if 'acta_pk' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'You should provide the <acta_pk> field'
        })

    acta_documento_queryset = models.ActaDocumentos.objects.filter(
        pk=request.PUT['acta_pk']
    )

    if acta_documento_queryset.count() == 0:
        return helpers.json_response({
            'error': -2, 'msg': 'No existe acta alguna con la pk indicada.'
        })

    acta_documento_queryset.update(
        estatus=models.APROBACION_SOLICITADA
    )

    return helpers.json_response({
        'error': 0,
        'result': serializers.serialize('json', acta_documento_queryset)
    })


class FiscalizacionListView(LoginRequiredMixin, ListView):
    """
        Vista utilizada para cargar la lista de pst a fiscalizar
    """
    model = Fiscalizacion
    template_name = 'fiscalizacion/funcionario/fiscalizaciones.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FiscalizacionListView, self).get_context_data()
        context['fiscalizaciones'] = Fiscalizacion.objects.all()
        return context


class FiscalizacionDetailView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles la fiscalizacion
    """
    model = Fiscalizacion
    template_name = 'fiscalizacion/funcionario/fiscalizacion.html'

    def get_context_data(self, **kwargs):
        context = super(FiscalizacionDetailView, self).get_context_data()
        fiscalizacion = get_object_or_404(Fiscalizacion, pk=self.kwargs['pk'])
        context['funcionarios'] = FuncionariosFiscalizacion.objects.filter(fiscalizacion=fiscalizacion)
        context['documentos'] = models.ActaDocumentos.objects.filter(fiscalizacion=fiscalizacion)
        # se excluye la acta de conformidad de la lista de actas
        context['tipos_de_actas'] = models.TipoActa.objects.all().exclude(
            codigo_documento__in=['CF', 'RP']
        ).order_by('nombre')
        context['fiscalizacion'] = fiscalizacion
        return context


class FiscalizacionGetCodigoView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        data = Storage(
            post=request.POST,
            is_a_util=True
        )
        fiscalizacion = FiscalizacionObject(data)
        context = fiscalizacion.get_utils_codigo()
        return self.render_to_response(context)


class FiscalizacionGetDataView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        data = Storage(
            post=request.POST,
            is_a_util=True
        )
        fiscalizacion = FiscalizacionObject(data)
        context = fiscalizacion.get_utils_data()
        return self.render_to_response(context)


class FiscalizacionCrearActaView(LoginRequiredMixin, CreateView):
    """
        Vista que se utiliza para registrar actas de documentos a una fiscalizacion especifica
    """
    model = Fiscalizacion
    template_name = 'fiscalizacion/funcionario/fiscalizacion.html'
    context_object_name = "fiscalizacion"

    def post(self, request, *args, **kwargs):
        super(FiscalizacionCrearActaView, self).post(request, *args, **kwargs)
        data = Storage(
            post=request.POST,
            is_a_util=False
        )
        fiscalizacion = FiscalizacionObject(data)
        fiscalizacion.crear_acta()
        return fiscalizacion.redirigir()


class FiscalizacionEditarActaView(LoginRequiredMixin, CreateView):
    """
        Vista que se utiliza para registrar actas de documentos a una fiscalizacion especifica
    """
    model = Fiscalizacion
    template_name = 'fiscalizacion/funcionario/fiscalizacion.html'
    context_object_name = "fiscalizacion"

    def post(self, request, *args, **kwargs):
        super(FiscalizacionEditarActaView, self).post(request, *args, **kwargs)
        data = Storage(
            post=request.POST,
            is_a_util=False
        )
        fiscalizacion = FiscalizacionObject(data)
        fiscalizacion.editar_acta()
        return fiscalizacion.redirigir()


class FiscalizacionEliminarActaView(LoginRequiredMixin, DeleteView):
    """
        Vista que se utiliza para eliminar actas de documentos a una fiscalizacion especifica
    """
    model = models.ActaDocumentos
    template_name = 'fiscalizacion/funcionario/eliminar_acta.html'

    def get_object(self, *args, **kwargs):
        obj = super(FiscalizacionEliminarActaView, self).get_object(
            *args, **kwargs
        )

        if obj.tipo.nombre == u'Acta de reparo':
            Fiscalizacion.objects.filter(
                pk=self.kwargs['pk_fiscalizacion']
            ).update(estatus=EN_PROCESO)

        return obj

    def get_success_url(self):
        pk_fiscalizacion = self.kwargs['pk_fiscalizacion']
        return reverse('funcionario_detalle_fiscalizacion', kwargs={'pk': pk_fiscalizacion})


class AnularActaProvidencia(LoginRequiredMixin, UpdateView):
    """
        Vista que se utiliza para anular actas de tipo providencia
    """
    model = Fiscalizacion
    template_name = 'fiscalizacion/funcionario/fiscalizacion.html'
    context_object_name = "fiscalizacion"

    def post(self, request, *args, **kwargs):
        super(AnularActaProvidencia, self).post(request, *args, **kwargs)
        post = request.POST.copy()
        if 'codigo_providencia' in post and 'justificacion' in post:
            pk_fiscalizacion = int(self.kwargs['pk'])
            justificacion, codigo_providencia = post['justificacion'], post['codigo_providencia']

            estatus_anulada = models.ANULADA

            # cambia el estatus a la providencia
            acta = models.ActaDocumentos.objects.get(codigo=codigo_providencia)
            acta.estatus = estatus_anulada
            acta.save()

            # cambia el estatus a todos las actas que dependen de la providencia
            _ = [self.cambiar_estatus(acta, estatus_anulada) for acta in acta.actadocumentos_set.all()]

            # crea un registro en el log
            log = models.ActaLogCambiarStatus()
            log.acta = acta
            log.estatus = estatus_anulada
            log.funcionario = self.request.user
            log.justificacion_cambio_de_estatus = justificacion
            log.pst = acta.pst
            log.save()

            return redirect('funcionario_detalle_fiscalizacion', pk=pk_fiscalizacion)

    def cambiar_estatus(self, acta, estatus):
        acta.estatus = estatus
        acta.save()


# ##################################### Menu de actas en funcionario ###############################

class ActaListView(LoginRequiredMixin, ListView):
    """
        Vista utilizada para cargar la lista de pst a fiscalizar
    """
    model = Fiscalizacion
    template_name = 'fiscalizacion/actas/solicitudes.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ActaListView, self).get_context_data()
        # todo creacion de lista temporal a aprobar
        context['solicitudes'] = Fiscalizacion.objects.filter(estatus=CONCLUIDA)
        return context
