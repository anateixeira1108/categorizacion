from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from apps.licencias import views

urlpatterns = patterns('',

                       #url(r'^funcionario/solicitudes/$',
                       #    TemplateView.as_view(template_name='licencias/funcionario/solicitudes.html'),
                       #    name='funcionario_licencias_solicitudes'),

                       url(r'^funcionario/solicitudes/$',
                           views.SolicitudesFuncionario.as_view(),
                           name='funcionario_licencias_solicitudes'),

                       url(r'^funcionario/solicitudes/asignadas/$',
                           views.SolicitudesAsignadas.as_view(),
                           name='funcionario_licencias_solicitudes_asignadas'),

                       url(r'^funcionario/otorgadas/$',
                           views.SolicitudesOtorgadas.as_view(),
                           name='funcionario_licencias_otorgadas'),

                       url(r'^asignar_solicitud/(?P<ide>\d+)/$',
                           views.AsignarSolicitud.as_view(),
                           name='asignar_solicitud'),

                       url(r'^funcionario/solicitud/de/aprobacion/1/$',
                           TemplateView.as_view(template_name='licencias/funcionario/solicitud_aprobacion.html'),
                           name='funcionario_solicitud_aprobacion_licencias'),
 

                       # url(r'^pst/solicitudes/$',
                       #     TemplateView.as_view(template_name='licencias/pst/solicitudes.html'),
                       #     name='pst_solicitudes_licencias'),

                       url(
                           r'^pst/solicitudes/$',
                           views.SolicitudesPst.as_view(),
                           name='pst_solicitudes_licencias'
                       ),
                       url(
                           r'^pst/licencias_asignadas/$',
                           views.LicenciasAsignadas.as_view(),
                           name='pst_licencias_asignadas'
                       ),

                       url(
                           r'^obtener_sublicencias/(?P<id_select>\w+)$',
                           views.AjaxObtenerTipoLicencias.as_view(),
                           name='obtener_sub_licencias'
                          ),
                       url(
                           r'^obtener_sucursales/(?P<id_select>\d+)/(?P<id_otros>\w+)$',
                           views.AjaxObtenerSucursales.as_view(),
                           name='obtener_sucursales'
                          ),
                       url(
                           r'^obtener_principal/(?P<id_select>\d+)/(?P<id_otros>\w+)$',
                           views.AjaxObtenerPrincipal.as_view(),
                           name='obtener_principal'
                          ),

                       # url(
                       #     r'^formulario_licencia/',
                       #     views.FormularioLicencia.as_view(),
                       #     name='formulario_licencia'
                       #    ),
                       # url(
                       #     r'^solicitud_licencia/(?P<id_select>\w+)/(?P<id_otros>\w+)/(?P<id_otros1>\d+)$',
                       #     views.SolicitudLicencias.as_view(),
                       #     name='formulario_solicitud_licencia'
                       #    ),

                       url(
                           r'^solicitud_licencia/$',
                           views.SolicitudLicencias.as_view(),
                           name='formulario_solicitud_licencia'
                          ),

                       url(
                           r'^agregar_solicitud/$',
                           views.AgregarSolicitud.as_view(),
                           name='agregar_solicitud'
                          ),

                    

                       )
