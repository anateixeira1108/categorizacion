from django.conf.urls import patterns, url

from registro import views


urlpatterns = \
    patterns('',
             # URLs compartidas
             url(r'^cambio-de-perfil/$',
                 views.CambioPerfil.as_view(),
                 name='cuentas_cambio_de_perfil'),

             url(r'^cambio-de-perfil/solicitar.json$',
                 views.cambio_de_perfil_solicitar_json,
                 name='cuentas_cambio_de_perfil_solicitar_json'),

             url(r'^cambio-de-perfil/cancelar.json$',
                 views.cambio_de_perfil_cancelar_json,
                 name='cuentas_cambio_de_perfil_cancelar_json'),


             # URLs de persona juridica
             url(r'^juridica/paso/1/$',
                 views.juridica.Paso1View.as_view(),
                 name='cuentas_juridica_1'),

             url(r'^juridica/paso/2/$',
                 views.juridica.Paso2View.as_view(),
                 name='cuentas_juridica_2'),

             url(r'^juridica/paso/3/$',
                 views.juridica.Paso3View.as_view(),
                 name='cuentas_juridica_3'),

             url(r'^juridica/paso/4/$',
                 views.juridica.Paso4View.as_view(),
                 name='cuentas_juridica_4'),

             url(r'^juridica/paso/5/$',
                 views.juridica.Paso5View.as_view(),
                 name='cuentas_juridica_5'),

             url(r'^juridica/paso/6/$',
                 views.juridica.Paso6View.as_view(),
                 name='cuentas_juridica_6'),

             url(r'^juridica/paso/7/$',
                 views.juridica.Paso7View.as_view(),
                 name='cuentas_juridica_7'),

             url(r'^juridica/paso/8/$',
                 views.juridica.Paso8View.as_view(),
                 name='cuentas_juridica_8'),

             url(r'^juridica/paso/9/$',
                 views.juridica.Paso9View.as_view(),
                 name='cuentas_juridica_9'),

             url(r'^juridica/paso/10/$',
                 views.juridica.Paso10View.as_view(),
                 name='cuentas_juridica_10'),

             url(r'^juridica/paso/11/$',
                 views.juridica.Paso11View.as_view(),
                 name='cuentas_juridica_11'),

             url(r'^juridica/pdf/$', views.pdf.Juridica.as_view(), name="print_registro_juridica_pdf"),

             url(r'^juridica/modificacionActa$',
                 views.juridica.ModificacionActa.as_view(),
                 name='modificacion_acta'),

             url(r'^juridica/registro_accionista$',
                 views.juridica.RegistroAccionista.as_view(),
                 name='registro_accionista'),

             url(r'^juridica/eliminar_accionista$',
                 views.juridica.EliminarAccionista.as_view(),
                 name='eliminar_accionista'),

             url(r'^juridica/editar_accionista/(?P<pk>\d+)/$',
                 views.juridica.EditarAccionista.as_view(),
                 name='editar_accionista_get'),

             url(r'^juridica/editar_accionista$',
                 views.juridica.EditarAccionista.as_view(),
                 name='editar_accionista_post'),

             url(r'^juridica/eliminar_modificacion_acta$',
                 views.juridica.EliminarModificacionActa.as_view(),
                 name='eliminar_modificacion_acta'),

             url(r'^juridica/registrar_sucursal$',
                 views.juridica.RegistroSucursal.as_view(),
                 name='registrar_sucursal'),

             url(r'^juridica/eliminar_sucursal$',
                 views.juridica.EliminarSucursal.as_view(),
                 name='eliminar_sucursal'),

             url(r'^juridica/obtener_acta/(?P<pk>\d+)/$',
                 views.juridica.ObtenerModificacionActa.as_view(),
                 name='obtener_modificacion_acta'),

             url(r'^juridica/editar_acta$',
                 views.juridica.EditarModificacionActa.as_view(),
                 name='editar_acta_post'),

             url(r'^agregar_actividad$',
                 views.juridica.AgregarActividadSecundaria.as_view(),
                 name='agregar_actividad'),

             url(r'^eliminar_actividad$',
                 views.juridica.EliminarActividadSecundaria.as_view(),
                 name='eliminar_actividad'),


             # URLS DE REGISTRO DE PERSONA NATURAL
             url(r'^natural/paso/1/$',
                 views.natural.Paso1View.as_view(),
                 name='cuentas_natural_1'),

             url(r'^natural/paso/2/$',
                 views.natural.Paso2View.as_view(),
                 name='cuentas_natural_2'),

             url(r'^natural/paso/3/$',
                 views.natural.Paso3View.as_view(),
                 name='cuentas_natural_3'),

             url(r'^natural/paso/4/$',
                 views.natural.paso4_view,
                 name='cuentas_natural_4'),

             url(r'^natural/paso/4/agente/$',
                 views.natural.Paso4AgenteView.as_view(),
                 name='cuentas_natural_4_agente'),

             url(r'^natural/paso/4/conductor/$',
                 views.natural.Paso4ConductorView.as_view(),
                 name='cuentas_natural_4_conductor'),

             url(r'^natural/paso/4/guia/$',
                 views.natural.Paso4GuiaView.as_view(),
                 name='cuentas_natural_4_guia'),

             url(r'^natural/paso/5/$',
                 views.natural.Paso5View.as_view(),
                 name='cuentas_natural_5'),

             url(r'^natural/paso/6/$',
                 views.natural.Paso6View.as_view(),
                 name='cuentas_natural_6'),

             url(r'^natural/paso/7/$',
                 views.natural.Paso7View.as_view(),
                 name='cuentas_natural_7'),

             url(r'^natural/firma_personal/tiene$',
                 views.natural.tiene_firma_personal_rest,
                 name='tiene_firma_personal_rest'),

             url(r'^natural/idiomas$',
                 views.natural.idiomas_rest,
                 name='cuentas_natural_idiomas_rest'),

             url(r'^natural/idiomas/pst$',
                 views.natural.idiomas_pst_rest,
                 name='cuentas_natural_idiomas_pst_rest'),

             url(r'^natural/idiomas/pst/del$',
                 views.natural.idiomas_pst_del,
                 name='cuentas_natural_idiomas_pst_del'),

             url(r'^natural/pdf/$', views.pdf.Natural.as_view(), name="print_registro_natural_pdf"),

             # URLs de Funcionarios

             url(r'^certificacion/pendientes/$',
                 views.funcionario.ListPstView.as_view(),
                 name='registro_funcionario_solicitudes'),

             url(r'^certificacion/persona/juridica/(?P<pk>\d+)/$',
                 views.funcionario.PstDetailJuridicaView.as_view(),
                 name='registro_funcionario_detalle_persona_juridica_solicitud'),

             url(r'^certificacion/persona/natural/(?P<pk>\d+)/$',
                 views.funcionario.PstDetailNaturalView.as_view(),
                 name='registro_funcionario_detalle_persona_natural_solicitud'),

             url(r'^certificacion/pst/certificar/persona/juridica/(?P<pk>\d+)/$',
                 views.funcionario.PstCertificarPersonaJuridicaView.as_view(),
                 name='registro_funcionario_certificar_documentos_juridica'),

             url(r'^certificacion/pst/certificar/persona/natural/(?P<pk>\d+)/$',
                 views.funcionario.PstCertificarPersonaNaturalView.as_view(),
                 name='registro_funcionario_certificar_documentos_natural'),

             url(r'^certificacion/pst/(?P<pk>\d+)/certificar/registrar/rechazo/$',
                 views.funcionario.PstRegistrarRechazo.as_view(),
                 name='registro_funcionario_certificar_registrar_rechazo_registro'),

             url(r'^certificacion/pst/certificar/(?P<pk>\d+)/aprobar/riftur/$',
                 views.funcionario.PstAceptarCertificacionRIFTURView.as_view(),
                 name='registro_funcionario_certificar_documentos_aprobar_riftur'),

             url(r'^certificacion/pst/certificar/(?P<pk>\d+)/rechazar/$',
                 views.funcionario.PstRechazarCertificacionView.as_view(),
                 name='registro_funcionario_certificar_documentos_rechazar'),

             url(r'^RIFTUR/(?P<pk>\d+)/$',
                 views.pdf.RIFTUR.as_view(),
                 name='RIFTUR_PDF'),

             url(r'^RTN/(?P<pk>\d+)/$',
                 views.pdf.RTN.as_view(),
                 name='RTN_PDF'),

             url(r'^certificacion/pst/(?P<pk>\d+)/persona/natural/imprimir/certificado/riftur/$',
                 views.funcionario.ImprimirCertificadoPersonaNaturalView.as_view(),
                 name='registro_funcionario_imprimir_certificado_riftur_persona_natural'),

             url(r'^certificacion/pst/(?P<pk>\d+)/persona/juridica/imprimir/certificado/riftur/$',
                 views.funcionario.ImprimirCertificadoPersonaJuridicaView.as_view(),
                 name='registro_funcionario_imprimir_certificado_riftur_persona_juridica'),

             url(r'^certificacion/pst/(?P<pk>\d+)/persona/natural/imprimir/certificado/pst/riftur/$',
                 views.funcionario.ImprimirCertificadoRIFTURPersonaNaturalPstMenuView.as_view(),
                 name='registro_funcionario_imprimir_certificado_riftur_persona_natural_menu'),

             url(r'^certificacion/pst/(?P<pk>\d+)/persona/juridica/imprimir/certificado/pst/riftur/$',
                 views.funcionario.ImprimirCertificadoRIFTURPersonaJuridicaPstMenuView.as_view(),
                 name='registro_funcionario_imprimir_certificado_riftur_persona_juridica_menu'),

             url(r'^certificacion/pst/(?P<pk>\d+)/persona/natural/imprimir/certificado/pst/rtn/$',
                 views.funcionario.ImprimirCertificadoRTNPersonaNaturalPstMenuView.as_view(),
                 name='registro_funcionario_imprimir_certificado_rtn_persona_natural_menu'),

             url(r'^certificacion/pst/(?P<pk>\d+)/persona/juridica/imprimir/certificado/pst/rtn/$',
                 views.funcionario.ImprimirCertificadoRTNPersonaJuridicaPstMenuView.as_view(),
                 name='registro_funcionario_imprimir_certificado_rtn_persona_juridica_menu'),

             url(r'^certificacion/pst/busqueda/$',
                 views.funcionario.BusquedaPstPorRifView,
                 name='registro_funcionario_busqueda_por_rif'),

             url(r'^cambio-de-perfil/aprobar.json$',
                 views.funcionario.cambio_de_perfil_aprobar_json,
                 name='registro_funcionario_cambio_de_perfil_aprobar_json'),

             url(r'^cambio-de-perfil/rechazar.json$',
                 views.funcionario.cambio_de_perfil_rechazar_json,
                 name='registro_funcionario_cambio_de_perfil_rechazar_json'),

             url(r'^print_report/$', views.funcionario.TestPDFView.as_view()),
    )
