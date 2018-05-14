from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from apps.actas.views import VerificacionView as verificacion
from apps.verificacion import views


urlpatterns = patterns('',
                       url(r'^$',
                           verificacion.VerificacionListView.as_view(),
                           name='funcionario_verificaciones'),

                       url(r'^(?P<pk>\d+)/$',
                           verificacion.VerificacionDetailView.as_view(),
                           name='funcionario_detalle_verificacion'),

                       url(r'^solicitud/de/aprobacion/1/$',
                           TemplateView.as_view(template_name='verificacion/funcionario/solicitud_aprobacion.html'),
                           name='funcionario_solicitud_de_aprobacion_verificacion'),

                       url(r'^seleccionar/candidato/$',
                           TemplateView.as_view(template_name='verificacion/funcionario/candidatos.html'),
                           name='funcionario_seleccionar_candidato_verificacion'),

                       url(r'^nueva/grupal/$',
                           TemplateView.as_view(template_name='verificacion/funcionario/nueva_grupal.html'),
                           name='funcionario_nueva_verificacion_grupal'),

                       url(r'^nueva/$',
                           TemplateView.as_view(
                               template_name='verificacion/funcionario/verificaciones_solicitudes.html'),
                           name='funcionario_verificaciones_solicitudes'),

                       url(r'^edicion/$',
                           TemplateView.as_view(template_name='verificacion/funcionario/edicion_gerente.html'),
                           name='funcionario_edicion_gerente'),

                       url(r'^gerente/$',
                           TemplateView.as_view(template_name='verificacion/funcionario/verificacion_gerente.html'),
                           name='funcionario_verificacion_gerente'),

                       # utilities views
                       url(r'^get/codigo/ajax/$',
                           verificacion.VerificacionGetCodigoView.as_view(),
                           name='ajax_codigo_verificacion'),

                       url(r'^get/data/ajax/$',
                           verificacion.VerificacionGetDataView.as_view(),
                           name='ajax_data_verificacion'),

                       url(r'^eliminar/acta/(?P<pk>\d+)/para/verificacion/(?P<pk_verificacion>\d+)/$',
                           verificacion.VerificacionEliminarActaView.as_view(),
                           name='eliminar_nueva_acta_verificacion'),

                       url(r'^nueva/acta/para/verificacion/(?P<pk>\d+)/$',
                           verificacion.VerificacionCrearActaView.as_view(),
                           name='crear_nueva_acta_verificacion'),

                       url(r'^editar/acta/para/verificacion/(?P<pk>\d+)/$',
                           verificacion.VerificacionEditarActaView.as_view(),
                           name='editar_nueva_acta_verificacion'),

                       url(r'^anular/acta/providencia/para/verificacion/(?P<pk>\d+)/$',
                           verificacion.AnularActaProvidencia.as_view(),
                           name='anular_providencia_acta_verificacion'),


                       # pdf
                       url(r'^pdf/(.+)/$',
                           views.Pdf.as_view(),
                           name='verificacion_pdf'),

                       # ajax
                       url(r'^concluir.json$',
                           views.concluir_verificacion_json,
                           name='verificacion_concluir_json'),

                       url(r'^registrar_observaciones.json$',
                           views.registrar_observaciones_json,
                           name='verificacion_registrar_observaciones_json'),
)
