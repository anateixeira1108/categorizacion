# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.resoluciones import views
from django.conf.urls import patterns, url
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# URLs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
urlpatterns = patterns('',
    url(
        '^aprobaciones/$',
        views.Aprobaciones.as_view(),
        name='funcionario_resoluciones_aprobaciones'
    ),
    url(
        '^detalle/(?P<pk>[1-9][0-9]*)/$',
        views.ResolucionDetalle.as_view(),
        name='funcionario_resolucion_detalle'
    ),
    url(
        '^buscar_sancion.json$',
        views.buscar_sancion_rest,
        name='buscar_sancion_rest'
    ),
    url(
        '^ilicito.json$',
        views.ilicito_rest,
        name='ilicito_rest'
    ),
    url(
        '^resolucion.json$',
        views.resolucion_rest,
        name='resolucion_rest'
    ),
    url(
        '^solicitar_aprobacion.json$',
        views.resolucion_solicitar_aprobacion_json,
        name='resolucion_solicitar_aprobacion_json'
    ),
    url(
        '^aprobar.json$',
        views.resolucion_aprobar_json,
        name='resolucion_aprobar_json'
    ),
    url(
        '^rechazar.json$',
        views.resolucion_rechazar_json,
        name='resolucion_rechazar_json'
    ),
    url(
        '^pdf/(?P<pk>[1-9][0-9]*)/$',
        views.ResolucionPdf.as_view(),
        name='resolucion_pdf'
    ),
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
