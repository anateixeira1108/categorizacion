from django.conf.urls import patterns, url
from apps.categorizacion import views

urlpatterns = \
    patterns(
        '',

        url(
            r'^administrador/(?P<modelo>[a-z]+)?$',
            views.PanelAdministrativo.as_view(),
            name="home_panel_administrativo"
        ),

        url(
            r'^administrador/tabulador/agregar/$',
            views.AgregarTabulador.as_view(),
            name="agregar_tabulador"
        ),

        url(
            r'^administrador/tabulador/(?P<tabulador>\d+)?/reconstruir/$',
            views.ReconstruirTabulador.as_view(),
            name="reconstruir_tabulador"
        ),

        url(
            r'^administrador/tabulador/vista/(?P<tabulador>\d+)?/(?P<tipo>VE|RB|RE|\*)?$',
            views.VisorTabulador.as_view(),
            name= "ver_tabulador"
        ),

        url(
            r'^administrador/tabulador/get/(?P<tabulador>\d+)/$',
            views.GenerarTabulador.as_view(),
            name = 'generar_tabulador'
        ),

        url(
            r'^administrador/tabulador/get/(?P<tabulador>\d+)/(?P<solicitud>\d+)/$',
            views.GenerarTabulador.as_view(),
            name = 'generar_tabulador'
        ),

        url(
            r'^administrador/tabulador/get/(?P<tabulador>\d+)/(?P<solicitud>\d+)/(?P<tipo>\w+)/$',
            views.GenerarTabulador.as_view(),
            name = 'generar_tabulador'
        ),

        url(
            r'^administrador/tabulador/get/(?P<tabulador>\d+)/(?P<solicitud>\d+)/(?P<tipo>\w+)/(?P<desactivar>\d+)/$',
            views.GenerarTabulador.as_view(),
            name = 'generar_tabulador'
        ),

        url(
            r'^administrador/tabulador/get/(?P<tabulador>\d+)/(?P<solicitud>\d+)/(?P<tipo>\w+)/(?P<desactivar>\d+)/(?P<valores_asociados>\d+)/$',
            views.GenerarTabulador.as_view(),
            name = 'generar_tabulador'
        ),

        url(
            r'^administrador/tabulador/get/(?P<tabulador>\d+)/(?P<solicitud>\d+)/(?P<tipo>\w+)/(?P<desactivar>\d+)/(?P<valores_asociados>\d+)/(?P<operacion>\w+)/$',
            views.GenerarTabulador.as_view(),
            name = 'generar_tabulador'
        ),

        url(
            r'^administrador/(?P<modelo>[a-z]+)/agregar/$',
            views.AgregarRecurso.as_view(),
            name="agregar_recurso"
        ),

        url(
            r'^administrador/(?P<modelo>[a-z]+)/eliminar$',
            views.EliminarRecurso.as_view(),
            name="eliminar_recurso"
        ),

        url(
            r'^administrador/paginar/(?P<modelo>[a-z]+)$',
            views.Paginador.as_view(),
            name='paginar_recurso'
        ),

        url(
            r'^administrador/tabulador/(?P<tabulador>\d+)?/editar/$',
            views.AgregarTabulador.as_view(),
            name="agregar_tabulador"
        ),

        url(
            r'^administrador/tabulador/(?P<tabulador>\d+)?/(?P<flag>CLONAR|clonar)/$',
            views.AgregarTabulador.as_view(),
            name="clonar_tabulador"
        ),

        url(
            r'^administrador/(?P<modelo>[a-z]+)/(?P<id>\d+)/editar/$',
            views.PanelAdministrativoEditar.as_view(),
            name='editar_recurso_form'
        ),

        url(
            r'^pst/cargar-requisitos/(?P<solicitud>\d+)/$',
            views.CargarReqDoc.as_view(),
            name='cargar_requisitos'
        ),

        url(
            r'^requisitos_funcionales/(?P<solicitud>\d+)$',
            views.CargarValoresEspecificos.as_view(),
            name = 'requisitos_funcionales',
        ),

        url(
            r'^valoresespecificos/(?P<solicitud>\d+)$',
            views.CargarValoresEspecificos.as_view(),
            name = 'valores_especificos',
        ),

        url(
            r'^cargarrequisitosprincipales/(?P<solicitud>\d+)$',
            views.CargarElemValAg.as_view(),
            name = 'elementos_valor_agregado',            
        ),

        url(
            r'^requisitosprincipales/(?P<solicitud>\d+)/(?P<tipo>RB|RE)$',
            views.CargarRequisitosPrincipales.as_view(),
            name = 'requisitos_principales',            
        ),

        url(
            r'^pst/nueva_solicitud/(?P<sucursal>\d+)$',
            views.NuevaSolicitud.as_view(),
            name='comenzar_solicitud'
        ),

        url(
            r'^funcionario/bandeja$',
            views.Bandeja.as_view(),
            name='bandeja'
        ),

        url(
            r'^listado_requisitos_documentales/(?P<sucursal>\d+)$',
            views.ObtenerRequisitosDocumentales.as_view(),
            name='listado_requisitos_documentales'
        ),

        url(
            r'^funcionario/bandeja/buscar$',
            views.BusquedaAvanzada.as_view(),
            name='buscar-avanzada'
        ),

        url(
            r'^funcionario/bandeja-libro$',
            views.BandejaLibro.as_view(),
            name='bandeja_libro'
        ),

        url(
            r'^funcionario/porentregar$',
            views.PorEntregar.as_view(),
            name='por_entregar'
        ),
        
        url(
            r'^bandeja-placa$',
            views.BandejaPlaca.as_view(),
            name='bandeja_placa'
        ),

        url(
            r'^libro/(?P<operacion>[a-z]+)$',
            views.PstLibro.as_view(),
            name='pst_libro'
        ),

        url(
            r'^funcionario/libro/(?P<operacion>[a-z]+)$',
            views.FuncionarioLibro.as_view(),
            name='funcionario_libro'
        ),
        
        url(
            r'^funcionario/administrar_empleados$',
            views.Empleados.as_view(),
            name='empleados'
        ),

        url(
            r'^funcionario/proponeraprobacion$',
            views.ProponerAprobacion.as_view(),
            name='proponeraprobacion'
        ),

        url(
            r'^funcionario/respuesta/(?P<operacion>[a-z]+)$',
            views.Respuesta.as_view(),
            name='respuesta'
        ),

        url(
            r'^funcionario/noprocedencia$',
            views.ProponerNoProcedencia.as_view(),
            name='noprocedencia'
        ),

        url(
            r'^funcionario/incumplimientoreparacion$',
            views.IncumplimientoReparacion.as_view(),
            name='incumplimiento_reparacion'
        ),

        url(
            r'^funcionario/devolverobservaciones$',
            views.DevolverConObservaciones.as_view(),
            name='devolver'
        ),

        url(
            r'^analista/solicitud/(?P<id>\d+)/(?P<operacion>[a-z]+)$',
            views.AnalistaOperacion.as_view(),
            name='operacion_analista'
        ),
        
        url(
            r'^coordinador_dif/solicitud/(?P<id>\d+)/(?P<operacion>[a-z]+)$',
            views.CoordinadorDIFOperacion.as_view(),
            name ='operacion_coordinador_dif'
        ),
        
        url(
            r'^inspector/solicitud/(?P<id>\d+)/(?P<operacion>[a-z]+)$',
            views.InspectorOperacion.as_view(),
            name ='operacion_inspector'
        ),

        url(
            r'^coordinador_ct/solicitud/(?P<id>\d+)/(?P<operacion>[a-z]+)$',
            views.CoordinadorCTOperacion.as_view(),
            name ='operacion_coordinador_ct'
        ),

        url(
             r'^pst/(?P<id>\d+)/enviarsolicitud$',
             views.EnviarSolicitud.as_view(),
             name = 'enviar_solicitud_pst'
        ),

        url(
             r'^pst/solicitud/(?P<id>\d+)/solicitarprorroga$',
             views.SolicitarProrroga.as_view(),
             name = 'solicitar_prorroga_pst'
        ),

        url(
             r'^pst/solicitud/(?P<id>\d+)/finreparaciones$',
             views.FinReparaciones.as_view(),
             name = 'fin_reparaciones_pst'
        ),

        url(
             r'^oficioplaca$',
             views.OficioPlaca.as_view(),
             name = 'oficio_placa_pst'
        ),
        
        url(
             r'^solicitud/(?P<id>\d+)/reconsideracion$',
             views.Reconsideracion.as_view(),
             name = 'reconsideracion'
        ),    
        
        url(
            r'^verpdf$',
            views.VisorPDF.as_view(),
            name = "ver_pdf",
        ),

        url(
            r'^(?P<tiporol>[a-z_]+)/admin_empleados$',
            views.AdminEmpleados.as_view(),
            name = 'admin_empleados',
        ),

        url(
            r'^cambiar_version$',
            views.CambioVersion.as_view(),
            name = 'cargar_version_tabulador',
        ),

        url(
            r'^pst/mostrarsucursales$',
            views.MostrarSucursales.as_view(),
            name= 'mostrar_sucursales',
        ),

        url(
            r'^reportes/(?P<reporte>[a-z]+)$',
            views.Reportes.as_view(),
            name= 'reportes',
        ),

        url(
            r'^portallsr/(?P<operacion>[a-z]+)$',
            views.PortalLsr.as_view(),
            name= 'portallsr',
        ),

        url(
            r'^turista/(?P<operacion>[a-z]+)$',
            views.EntradaLibroLsr.as_view(),
            name= 'entrada_turista',
        ),

        url(
            r'^director_ct/(?P<operacion>[a-z]+)$',
            views.DirectorCTOperacion.as_view(),
            name= 'operacion_director',
        ),

        url(
            r'^funcionario/tabulador/(?P<tabulador>\d+)/(?P<solicitud>\d+)/(?P<subseccion>\d+)/(?P<operacion>\w+)',
            views.OperacionElemVal.as_view(),
            name= "operacion_elemval"
        ),

        url(
            r'^funcionario/tabulador/(?P<tabulador>\d+)/(?P<solicitud>\d+)/(?P<operacion>\w+)',
            views.OperacionElemVal.as_view(),
            name= "operacion_elemval"
        ),

        url(
            r'tipos-respuesta$',
            views.ObtenerTiposRespuesta.as_view(),
            name= "tipos-respuesta"
        ),

        url(
            r'obtener-form-elemento$',
            views.ObtenerFormularioElemento.as_view(),
            name= "tipos-respuesta"
        ),

        url(
            r'^lsr/oficios_respuesta/(?P<operacion>\w+)',
            views.OficiosRespuesta.as_view(),
            name= "oficios_respuesta"
        ),

        url(
            r'^pst/registrardocumento$',
            views.RegistrarDocumentosPST.as_view(),
            name= "registrar_nuevo_documento_pst"
        ),
        url(
            r'^funcionario/firmas/firmado$',
            views.FirmaCompleta.as_view(),
            name= "firma_completa"
        ),
        url(
            r'^funcionario/firmas/script/(?P<tipo>agregar|eliminar)$',
            views.FirmaScript.as_view(),
            name= "firma_script"
        ),               
    )
