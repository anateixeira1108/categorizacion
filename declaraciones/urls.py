# -*- coding: utf-8 -*-

u""" URLs para las declaraciones. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón U.
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.conf.urls import patterns, url

from views import DeclaracionesListaView
from views import PlanillaFormView
from views import PlanillaSaveView
from views import PlanillaVerView
from views import declaraciones_rest
import views

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# URLs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
urlpatterns = patterns('',
                       url(r'^pst/$',
                           DeclaracionesListaView.as_view(),
                           name='declaraciones_pst_declaraciones'
                       ),

                       url(r'^pst/declaracion/formulario/$',
                           PlanillaFormView.as_view(),
                           name='declaraciones_pst_declaracion_formulario'
                       ),

                       url(r'^pst/declaracion/ver/(?P<declaracion_id>\d+)$',
                           PlanillaVerView.as_view(),
                           name='declaraciones_pst_declaracion_ver'
                       ),

                       url(r'^pst/declaracion/vista_previa/$',
                           PlanillaSaveView.as_view(),
                           name='declaraciones_pst_declaracion_vista_previa'
                       ),

                       url(r'^pst/pdf/(.+)/$',
                           views.Pdf.as_view(),
                           name='declaracion_pdf'
                       ),

                       url(r'^pst/anular/$',
                           views.AnularDeclaracion.as_view(),
                           name='declaraciones_pst_anular'
                       ),

                       url(r'^declaraciones-periodo$',
                           declaraciones_rest,
                           name='declaraciones-periodo'
                       ),

                       url(r'^funcionario/anulacion/$',
                           views.FuncionarioAnulacionListView.as_view(),
                           name='funcionario_declaracion_por_anular'
                       ),

                       url(r'^funcionario/declaracion/ver/(?P<declaracion_id>\d+)$',
                           views.FuncionarioPlanillaVerView.as_view(),
                           name='declaraciones_funcionario_declaracion_ver'
                       ),

                       url(r'^funcionario/declaracion/anular/$',
                           views.FuncionarioAnularDeclaracion.as_view(),
                           name='funcionario_anular_declaracion'
                       ),

                       url(r'^funcionario/declaracion/rechazar-anulacion/$',
                           views.FuncionarioRechazarAnulacion.as_view(),
                           name='funcionario_rechazar_anulacion'
                       ),

                       url(r'^funcionario/declaracion/anulada/busqueda/$',
                           views.BusquedaDeclaracionesAnuladasPorRifView,
                           name='funcionario_declaracion_busqueda_por_rif'),

)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
