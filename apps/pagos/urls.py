from apps.pagos import views
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

                       url(r'^estado/de/cuenta/$',
                           views.CompromisosListaView.as_view(),
                           name='pst_compromisos_pago'),

                       url(r'^compromisos/de/pago.json/$',
                           views.compromiso_pago_json,
                           name='pst_compromisos_pago_json'),

                       url(r'^compromisos/de/pago/nuevo/$',
                           views.compromiso_pago_nuevo,
                           name='pst_compromisos_pago_nuevo'),

                       url(r'^compromisos/de/pago/pdf/(?P<pk>\d+)/$',
                           views.planilla_pago_pdf,
                           name='pst_compromisos_pago_pdf'),

                       url(r'^compromisos/de/pago/1/$',
                           TemplateView.as_view(template_name='pagos/pst/detalle_compromiso_pago.html'),
                           name='pst_detalle_compromiso_pago'),

                       url(r'^indebido/$',
                           views.PagoIndebidoView.as_view(),
                           name='pst_pago_indebido'),

                       url(r'^indebido/reconocimientos/$',
                           views.CesionesPagoIndebidoView.as_view(),
                           name='pst_reconocimientos_pago_indebido'),

                       )
