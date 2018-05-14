from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from apps.inteligencia_tributaria import views


urlpatterns = patterns('',
           url(r'^$',
              views.ListarSolicitudes.as_view(),
              name='funcionario_solicitudes'),

           url(r'^nueva/$',
              views.IndexCrearSolicitud.as_view(),
              name='funcionario_crear_solicitud'),

           url(r'^buscar_candidatos/$',
              views.BuscarCandidatos.as_view(),
              name='buscar_candidatos'),

          url(r'^buscar_funcionario/$',
              views.BuscarFuncionarios.as_view(),
              name='buscar_funcionario'),

          url(r'^crear_solicitud/$',
              views.CrearSolicitud.as_view(),
              name='crear_solicitud'),

          url(r'^gerente/$',
              views.VerificacionGerente.as_view(),
              name='verificar_solicitud_gerente'),

          url(r'^editar/(?P<pk>\d+)/$',
            views.EditarSolicitud.as_view(),
            name='editar_solicitud_gerente'),

          url(r'^funcionario_apoyo/agregar/$',
            views.AgregarFuncionarioApoyo.as_view(),
            name='agregar_funcionario_apoyo'),
)