# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.cuentas.mixins import MenuPSTMixin
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from registro import models
from utils import views_helpers as helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas específicas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import juridica as juridica
import natural as natural
import funcionario as funcionario
import pdf as pdf
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas comunes ~ (Clases) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CambioPerfil(TemplateView, MenuPSTMixin):
    template_name = 'registro/cambio-de-perfil.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CambioPerfil, self).get_context_data(
            *args, **kwargs
        )
        solicitudes = models.SolicitudCambioPerfil.objects.filter(
            pst=models.Pst.objects.get(user=self.request.user)
        ).order_by('-fecha_generacion')

        paginator_handler = paginator.Paginator(solicitudes, 5)
        page = self.request.GET.get('page')

        try:
            context['solicitudes'] = paginator_handler.page(page)

        except paginator.PageNotAnInteger:
            context['solicitudes'] = paginator_handler.page(1)

        except paginator.EmptyPage:
            context['solicitudes'] = paginator_handler.page(
                paginator_handler.num_pages
            )

        return context
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas comunes ~ (Funciones) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
def cambio_de_perfil_solicitar_json(request):
    if request.method != 'POST':
        return helpers.json_response({
            'error': -1, 'msg': 'Method not allowed.'
        })

    solicitudes = models.SolicitudCambioPerfil.objects.filter(
        pst=models.Pst.objects.get(user=request.user),
        activo=True
    )

    if solicitudes.count():
        return helpers.json_response({
            'error': -2, 'msg': '¡Ya tiene una solicitud pendiente!'
        })

    models.SolicitudCambioPerfil(
        pst=models.Pst.objects.get(user=request.user)
    ).save()

    return helpers.json_response({'error': 0, 'result': ''})


@login_required(login_url=reverse_lazy('cuentas_login'))
def cambio_de_perfil_cancelar_json(request):
    if request.method != 'POST':
        return helpers.json_response({
            'error': -1, 'msg': 'Method not allowed.'
        })

    solicitudes = models.SolicitudCambioPerfil.objects.filter(
        pst=models.Pst.objects.get(user=request.user),
        activo=True
    )

    if not solicitudes.count():
        return helpers.json_response({
            'error': -2,
            'msg': '¡Actualmente no posee solicitudes pendientes por aprobar!'
        })

    solicitudes.update(activo=False)

    return helpers.json_response({'error': 0, 'result': ''})
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
