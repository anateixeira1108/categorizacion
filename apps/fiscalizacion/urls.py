from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from apps.actas.views import FiscalizacionView as fiscalizacion
from apps.fiscalizacion.views import Pdf
from apps.fiscalizacion.views import concluir_fiscalizacion_json
from apps.fiscalizacion.views import guardar_acta_reparo_json
from apps.fiscalizacion.views import guardar_nueva_acta_reparo_json
from apps.fiscalizacion.views import obtener_acta_reparo_json
from apps.fiscalizacion.views import registrar_observaciones_json


urlpatterns = patterns('',
                       url(r'^$',
                           fiscalizacion.FiscalizacionListView.as_view(),
                           name='funcionario_fiscalizaciones'),

                       url(r'^(?P<pk>\d+)/$',
                           fiscalizacion.FiscalizacionDetailView.as_view(),
                           name='funcionario_detalle_fiscalizacion'),

                       url(r'^solicitud/de/aprobacion/1/$',
                           TemplateView.as_view(template_name='fiscalizacion/funcionario/solicitud_aprobacion.html'),
                           name='funcionario_solicitud_de_aprobacion_fiscalizacion'),

                       url(r'^seleccionar/candidato/$',
                           TemplateView.as_view(template_name='fiscalizacion/funcionario/candidatos.html'),
                           name='funcionario_seleccionar_candidato_fiscalizacion'),

                       url(r'^nueva/$',
                           TemplateView.as_view(template_name='fiscalizacion/funcionario/nueva.html'),
                           name='funcionario_nueva_fiscalizacion'),

                       url(r'^gerente/$',
                           TemplateView.as_view(template_name='fiscalizacion/funcionario/fiscalizacion_gerente.html'),
                           name='funcionario_fiscalizacion_gerente'),

                       url(r'^edicion/$',
                           TemplateView.as_view(template_name='fiscalizacion/funcionario/edicion_fiscalizacion.html'),
                           name='funcionario_edicion_fiscalizacion'),

                       # utilities views
                       url(r'^get/codigo/ajax/$',
                           fiscalizacion.FiscalizacionGetCodigoView.as_view(),
                           name='ajax_codigo_fiscalizacion'),

                       url(r'^get/data/ajax/$',
                           fiscalizacion.FiscalizacionGetDataView.as_view(),
                           name='ajax_data_fiscalizacion'),

                       url(r'^eliminar/acta/(?P<pk>\d+)/para/fiscalizacion/(?P<pk_fiscalizacion>\d+)/$',
                           fiscalizacion.FiscalizacionEliminarActaView.as_view(),
                           name='eliminar_nueva_acta_fiscalizacion'),

                       url(r'^nueva/acta/para/fiscalizacion/(?P<pk>\d+)/$',
                           fiscalizacion.FiscalizacionCrearActaView.as_view(),
                           name='crear_nueva_acta_fiscalizacion'),

                       url(r'^editar/acta/para/fiscalizacion/(?P<pk>\d+)/$',
                           fiscalizacion.FiscalizacionEditarActaView.as_view(),
                           name='editar_nueva_acta_fiscalizacion'),

                       url(r'^anular/acta/providencia/para/verificacion/(?P<pk>\d+)/$',
                           fiscalizacion.AnularActaProvidencia.as_view(),
                           name='anular_providencia_acta_fiscalizacion'),
                       # pdf
                       url(r'^pdf/(.+)/$',
                           Pdf.as_view(),
                           name='fiscalizacion_pdf'),

                       url(r'^lista/actas/para/aprobar/$',
                           fiscalizacion.ActaListView.as_view(),
                           name='actas_lista_para_aprobar'),

                       # ajax
                       url(r'^concluir.json$',
                           concluir_fiscalizacion_json,
                           name='fiscalizacion_concluir_json'),

                       url(r'^guardar_acta_reparo.json$',
                           guardar_acta_reparo_json,
                           name='fiscalizacion_guardar_acta_reparo_json'),

                       url(r'^guardar_nueva_acta_reparo.json$',
                           guardar_nueva_acta_reparo_json,
                           name='fiscalizacion_guardar_nueva_acta_reparo_json'),

                       url(r'^obtener_acta_reparo.json$',
                           obtener_acta_reparo_json,
                           name='fiscalizacion_obtener_acta_reparo_json'),

                       url(r'^registrar_observaciones.json$',
                           registrar_observaciones_json,
                           name='fiscalizacion_registrar_observaciones_json'),

                       url(r'^actas/solicitar-aprobacion.json$',
                           fiscalizacion.solicitar_aprobacion_json,
                           name='fiscalizacion_solicitar_aprobacion_json'),
)
