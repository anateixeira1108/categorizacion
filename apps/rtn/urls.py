from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from apps.rtn import views


urlpatterns = patterns('',

                       url(r'^funcionario/$',
                           TemplateView.as_view(template_name='rtn/funcionario/dashboard.html'),
                           name='funcionario_dashboard'),

                       url(r'^funcionario/solicitudes/$',
                           views.ListPstView.as_view(),
                           name='rtn_funcionario_solicitudes'),

                       url(r'^funcionario/solicitudes/registro/persona/juridica/(?P<pk>\d+)/$',
                           views.PstDetailJuridicaView.as_view(),
                           name='rtn_funcionario_detalle_pst_juridica_solicitud'),

                       url(r'^funcionario/solicitudes/registro/persona/natural/(?P<pk>\d+)/$',
                           views.PstDetailNaturalView.as_view(),
                           name='rtn_funcionario_detalle_pst_natural_solicitud'),

                       url(r'^funcionario/solicitudes/certificar/persona/juridica/(?P<pk>\d+)/$',
                           views.PstCertificarPersonaJuridicaView.as_view(),
                           name='rtn_funcionario_certificar_documentos_juridica'),

                       url(r'^funcionario/solicitudes/certificar/persona/natural/(?P<pk>\d+)/$',
                           views.PstCertificarPersonaNaturalView.as_view(),
                           name='rtn_funcionario_certificar_documentos_natural'),
                       url(r'^funcionario/solicitud/de/aprobacion/persona/natural/(?P<pk>\d+)/$',
                           views.PstSolicitudAprobacionNaturalView.as_view(),
                           name='funcionario_solicitud_aprobacion_rtn_natural'),

                       url(r'^funcionario/solicitud/de/aprobacion/persona/juridica/(?P<pk>\d+)/$',
                           views.PstSolicitudAprobacionJuridicaView.as_view(),
                           name='funcionario_solicitud_aprobacion_rtn_juridica'),
                       url(r'^certificacion/pst/certificar/(?P<pk>\d+)/aprobar/$',
                           views.PstAceptarCertificacionView.as_view(),
                           name='registro_funcionario_rtn_certificar_documentos_aprobar'),

                       url(r'^certificacion/pst/certificar/(?P<pk>\d+)/rechazar/$',
                           views.PstRechazarCertificacionView.as_view(),
                           name='registro_funcionario_rtn_certificar_documentos_rechazar'),

                       url(r'^certificacion/pst/(?P<pk>\d+)/persona/natural/imprimir/certificado/$',
                           views.ImprimirCertificadoPersonaNaturalView.as_view(),
                           name='registro_funcionario_rtn_imprimir_certificado_persona_natural'),

                       url(r'^certificacion/pst/(?P<pk>\d+)/persona/juridica/imprimir/certificado/$',
                           views.ImprimirCertificadoPersonaJuridicaView.as_view(),
                           name='registro_funcionario_rtn_imprimir_certificado_persona_juridica'),
                       url(r'^certificacion/pst/busqueda/$',
                           views.BusquedaPstPorRifView,
                           name='registro_funcionario_rtn_busqueda_por_rif'),


)
