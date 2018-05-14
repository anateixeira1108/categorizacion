from django.conf.urls import patterns, url

from apps.factibilidad.views import FuncionarioView, PstView


urlpatterns = patterns('',
                       url(r'^funcionario/solicitudes/$',
                           FuncionarioView.ListFactibilidadView.as_view(),
                           name='funcionario_factibilidad_solicitudes'),

                       url(r'^funcionario/solicitud/de/aprobacion/(?P<pk>\d+)/$',
                           FuncionarioView.DetailFactibilidadView.as_view(),
                           name='funcionario_factibilidad_solicitud_aprobacion'),

                       url(r'^funcionario/solicitud/(?P<pk>\d+)/certificacion/$',
                           FuncionarioView.CertificarFactibilidadView.as_view(),
                           name='funcionario_factibilidad_certificar_documentos'),

                       url(r'^funcionario/solicitud/certificar/(?P<pk>\d+)/aprobar/$',
                           FuncionarioView.AceptarCertificacionFactibilidadView.as_view(),
                           name='funcionario_factibilidad_certificar_documentos_aprobar'),

                       url(r'^funcionario/solicitud/certificar/(?P<pk>\d+)/rechazar/$',
                           FuncionarioView.RechazarCertificacionFactibilidadView.as_view(),
                           name='funcionario_factibilidad_certificar_documentos_rechazar'),

                       # Templates para los pst
                       url(r'^pst/solicitudes/$',
                           PstView.IndexFactibilidad.as_view(),
                           name='pst_solicitudes_factibilidad'),

                       url(r'^pst/solicitudes/nueva/paso/uno/(?P<pk>\d+)/$',
                           PstView.FactibilidadPasoUno.as_view(),
                           name='pst_solicitudes_factibilidad_paso_uno'),

                       url(r'^pst/solicitudes/nueva/paso/dos/(?P<pk>\d+)/$',
                           PstView.FactibilidadPasoDos.as_view(),
                           name='pst_solicitudes_factibilidad_paso_dos'),

                       url(r'^pst/solicitudes/nueva/paso/tres/(?P<pk>\d+)/$',
                           PstView.FactibilidadPasoTres.as_view(),
                           name='pst_solicitudes_factibilidad_paso_tres'),

                       url(r'^pst/solicitudes/nueva/paso/cuatro/(?P<pk>\d+)/$',
                           PstView.FactibilidadPasoCuatro.as_view(),
                           name='pst_solicitudes_factibilidad_paso_cuatro'),

                       url(r'^pst/crear/solicitud$',
                           PstView.CrearNuevaFactibilidad.as_view(),
                           name='pst_crear_factibilidad'),

                       url(r'^pst/solicitudes/ver/(?P<pk>\d+)/$',
                           PstView.FactibilidadVistaPrevia.as_view(),
                           name='pst_factibilidad_vista_previa'),


                       url(r'^anular/$',
                           PstView.AnularFactibilidad.as_view(),
                           name='anular_factibilidad'),
)
