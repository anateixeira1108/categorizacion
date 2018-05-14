from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from apps.reportes import views

urlpatterns = patterns('',

                       # ~~~~~~~~ PST ~~~~~~~~~~~~~~~~~~~~~~
                       url(r'^pst/$',
                           views.IndexReportes.as_view(),
                           name='funcionario_reportes'),

                       url(r'^pst/filtrar_reportes/$',
                           views.FiltrarReportes.as_view(),
                           name='filtrar_reportes'),

                       url(r'^pst/expediente/$',
                           views.Expediente.as_view(),
                           name='reportes_expediente'),

                       url(r'^pst/pdf/(.+)/$',
                           views.PdfExpediente.as_view(),
                           name='reporte_pdf_natural'),

                       url(r'^pst/pdf_lista/$',
                           views.PdfReporteLista.as_view(),
                           name='reporte_lista_pdf'),

                       url(r'^pst/xls_lista/$',
                           views.XlsReporteLista.as_view(),
                           name='reporte_lista_xls'),

                      # ~~~~~~~~~ PST en mora ~~~~~~~~~~~~~~~

                       url(r'^pst_en_mora/$',
                           views.IndexReportesEnMora.as_view(),
                           name='funcionario_reportes_en_mora'),
                       )
