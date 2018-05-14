# -*- coding: utf-8 -*-

"""
Vistas para el proceso de la primera certificación de los documentos por parte del funcionario.
"""

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from apps.resoluciones import models as resoluciones_models
from apps.verificacion.models import Verificacion, FuncionariosVerificacion
from apps.actas.models import ActaDocumentos, TipoActa, ANULADA, ActaLogCambiarStatus
from utils.mixins import JSONResponseMixin
from utils.gluon.storage import Storage
from Verificacion import VerificacionObject


class VerificacionListView(LoginRequiredMixin, ListView):
    """
        Vista utilizada para cargar la lista de pst a verificar
    """
    model = Verificacion
    template_name = 'verificacion/funcionario/verificaciones.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(VerificacionListView, self).get_context_data()
        context['verificaciones'] = Verificacion.objects.all()
        return context


class VerificacionDetailView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles de la verificacion
    """
    model = Verificacion
    template_name = 'verificacion/funcionario/verificacion.html'

    def get_context_data(self, **kwargs):
        context = super(VerificacionDetailView, self).get_context_data()
        verificacion = get_object_or_404(Verificacion, pk=self.kwargs['pk'])
        context['funcionarios'] = FuncionariosVerificacion.objects.filter(verificacion=verificacion)
        context['documentos'] = ActaDocumentos.objects.filter(verificacion=verificacion)
        context['tipos_de_actas'] = TipoActa.objects.all().exclude(nombre=None)
        context['verificacion'] = verificacion
        context['tipo_resolucion_list'] = (
            resoluciones_models.TipoResolucion.objects.all()
        )
        context['resolucion'] = (
            resoluciones_models.Resolucion.objects.filter(verificacion=verificacion).first()
        )
        return context


class VerificacionGetCodigoView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        data = Storage(
            post=request.POST,
            is_a_util=True
        )
        verificacion = VerificacionObject(data)
        context = verificacion.get_utils_codigo()
        return self.render_to_response(context)


class VerificacionGetDataView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        data = Storage(
            post=request.POST,
            is_a_util=True
        )
        verificacion = VerificacionObject(data)
        context = verificacion.get_utils_data()
        return self.render_to_response(context)


class VerificacionCrearActaView(LoginRequiredMixin, CreateView):
    """
        Vista que se utiliza para registrar actas de documentos a una verificacion especifica
    """
    model = Verificacion
    template_name = 'verificacion/funcionario/verificacion.html'
    context_object_name = "verificacion"

    def post(self, request, *args, **kwargs):
        super(VerificacionCrearActaView, self).post(request, *args, **kwargs)
        data = Storage(
            post=request.POST,
            is_a_util=False
        )
        verificacion = VerificacionObject(data)
        verificacion.crear_acta()
        return verificacion.redirigir()


class VerificacionEditarActaView(LoginRequiredMixin, CreateView):
    """
        Vista que se utiliza para registrar actas de documentos a una verificacion especifica
    """
    model = Verificacion
    template_name = 'verificacion/funcionario/verificacion.html'
    context_object_name = "verificacion"

    def post(self, request, *args, **kwargs):
        super(VerificacionEditarActaView, self).post(request, *args, **kwargs)
        data = Storage(
            post=request.POST,
            is_a_util=False
        )
        verificacion = VerificacionObject(data)
        verificacion.editar_acta()
        return verificacion.redirigir()


class VerificacionEliminarActaView(LoginRequiredMixin, DeleteView):
    """
        Vista que se utiliza para eliminar actas de documentos a una verificacion especifica
    """
    model = ActaDocumentos
    template_name = 'verificacion/funcionario/eliminar_acta.html'

    def get_success_url(self):
        pk_verificacion = self.kwargs['pk_verificacion']
        return reverse('funcionario_detalle_verificacion', kwargs={'pk': pk_verificacion})


class AnularActaProvidencia(LoginRequiredMixin, UpdateView):
    """
        Vista que se utiliza para anular actas de tipo providencia
    """
    model = Verificacion
    template_name = 'verificacion/funcionario/verificacion.html'
    context_object_name = "verificacion"

    def post(self, request, *args, **kwargs):
        super(AnularActaProvidencia, self).post(request, *args, **kwargs)
        post = request.POST.copy()
        if 'codigo_providencia' in post and 'justificacion' in post:
            pk_verificacion = int(self.kwargs['pk'])
            justificacion, codigo_providencia = post['justificacion'], post['codigo_providencia']
            # cambia el estatus a la providencia
            acta = ActaDocumentos.objects.get(codigo=codigo_providencia)
            acta.estatus = ANULADA
            acta.save()

            # cambia el estatus a todos las actas que dependen de la providencia
            _ = [self.cambiar_estatus(acta, ANULADA) for acta in acta.actadocumentos_set.all()]

            # crea un registro en el log
            log = ActaLogCambiarStatus()
            log.acta = acta
            log.estatus = ANULADA
            log.funcionario = self.request.user
            log.justificacion_cambio_de_estatus = justificacion
            log.pst = acta.pst
            log.save()

            return redirect('funcionario_detalle_verificacion', pk=pk_verificacion)

    def cambiar_estatus(self, acta, estatus):
        acta.estatus = estatus
        acta.save()
