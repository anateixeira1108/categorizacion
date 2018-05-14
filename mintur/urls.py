from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from settings import MEDIA_URL
from utils import vzla as restVenezuela
from utils import validaciones
from apps.cuentas.views import DetectarUsuarioView
from views import files_view

admin.autodiscover()

urlpatterns = patterns('',

  url(r'^admin/', include(admin.site.urls)),

  # App para la creacion de cuentas y auth
  url(r'^cuentas/', include('apps.cuentas.urls')),

  # App que maneja todo lo referente al registro de PST
  url(r'^registro/', include('registro.urls')),

  # App que maneja todo lo referente a RTN
  url(r'^rtn/', include('apps.rtn.urls')),

  # App que maneja todo lo referente a Licencias
  url(r'^licencias/', include('apps.licencias.urls')),

  # App que maneja todo lo referente a Factibilidad
  url(r'^factibilidad/', include('apps.factibilidad.urls')),

  # App que maneja todo lo referente a Declaraciones
  url(r'^declaraciones/', include('declaraciones.urls')),

  # App que maneja todo lo referente a Verificacion
  url(r'^verificacion/', include('apps.verificacion.urls')),

  # App que maneja todo lo referente a Fiscalizacion
  url(r'^fiscalizacion/', include('apps.fiscalizacion.urls')),

  # App que maneja todo lo referente a Pagos
  url(r'^pagos/', include('apps.pagos.urls')),

  # App que maneja todo lo referente a Metas
  url(r'^metas/', include('apps.metas.urls')),

  # App que maneja todo lo referente a Metas
  url(r'^reportes/', include('apps.reportes.urls')),

  # App que maneja todo lo referente a Resoluciones
  url(r'^resoluciones/', include('apps.resoluciones.urls')),

  # App que maneja todo lo referente a las Solicitudes
  url(r'^inteligencia_tributaria/', include('apps.inteligencia_tributaria.urls')),

  # App que maneja todo lo referente a la configuracion
  url(r'^configuracion/', include('apps.configuracion.urls')),

  # Vista que se encarga de enviar el usuario a la vista que le corresponde
  url(r'^$',
     DetectarUsuarioView.as_view(),
     name='cuentas_detectar_usuario'),

  url(r'^funcionario/$',
     RedirectView.as_view(url=reverse_lazy('registro_funcionario_solicitudes'))),


  url(r'^404$',
     TemplateView.as_view(template_name='404.html'),
     name='404'),

  url(r'^500$',
     TemplateView.as_view(template_name='500.html'),
     name='500'),

  url(r'^municipios/(?P<pk>\d+)/$', restVenezuela.municipios_json,
    name='municipios_json'),

  url(r'^parroquias/(?P<pk>\d+)/$', restVenezuela.parroquias_json,
    name='parroquias_json'),

  url(r'^' + MEDIA_URL[1:] + '(?P<fpath>.*)$', files_view, name="files_view"),

  url(r'^validar_rif$', validaciones.ValidarUnicoRif.as_view(), name='validar_rif'),

  url(r'^validar_cedula$', validaciones.ValidarUnicoDocumento.as_view(), name='validar_cedula'),
  #reportes

  # Modulo de Categorizacion
  url(r'^categorizacion/', include('apps.categorizacion.urls'))

  )

