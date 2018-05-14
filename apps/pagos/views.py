# -*- coding: utf-8 -*-

u""" Vistas para los compromisos de pago. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón U.
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.cuentas.mixins import MenuPSTMixin
from apps.pagos import models
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from json import loads as json_loads
from registro.models import Pst
from utils.views_helpers import json_response
from django.conf import settings
import os
import platform
import locale
from PyPDF2 import PdfFileWriter, PdfFileReader
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# init ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if 'Windows' in platform.platform():
    locale.setlocale(locale.LC_ALL, 'esp_ven')
else:
    locale.setlocale(locale.LC_ALL, 'es_VE.UTF-8')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CompromisosListaView(TemplateView, MenuPSTMixin):
    template_name = 'pagos/pst/compromisos_pago.html'

    def get_context_data(self, **kwargs):
        context = super(CompromisosListaView, self).get_context_data(**kwargs)

        conceptos = models.Concepto.objects.filter(
            pst=Pst.objects.get(user=self.request.user)
        ).order_by('pago', '-fecha_generacion', '-estatus')

        paginator_handler = paginator.Paginator(conceptos, 15)
        page = self.request.GET.get('page')

        try:
            context['conceptos'] = paginator_handler.page(page)

        except paginator.PageNotAnInteger:
            context['conceptos'] = paginator_handler.page(1)

        except paginator.EmptyPage:
            context['conceptos'] = paginator_handler.page(
                paginator_handler.num_pages
            )
        return context


class PagoIndebidoView(TemplateView, MenuPSTMixin):
    template_name = 'pagos/pst/pago_indebido.html'


class CesionesPagoIndebidoView(TemplateView, MenuPSTMixin):
    template_name = 'pagos/pst/reconocimiento_pago_indebido.html'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
def compromiso_pago_json(request):
    if 'concepto_id' not in request.GET:
        return json_response({'error': -1, 'msg': 'Se requiere el concepto.'})

    try:
        concepto = models.Concepto.objects.get(
            pst=Pst.objects.get(user=request.user),
            id=request.GET['concepto_id']
        )

    except models.Concepto.DoesNotExist:
        return json_response({'error': -2, 'msg': 'El concepto no existe'})

    return json_response({
        'error': 0,
        'result': serializers.serialize('json', [concepto]),
        'attached': {
            'tipo': concepto.concepto_tipo.nombre,
            'pago': None if concepto.pago is None else {
                'id': concepto.pago.id,
                'numero_documento': concepto.pago.numero_documento,
            }
        },
    })


@login_required(login_url=reverse_lazy('cuentas_login'))
@require_http_methods(['POST'])
def compromiso_pago_nuevo(request):
    if 'conceptos' not in request.POST:
        return json_response({
            'error': -1, 'msg': 'Se requieren los conceptos.'
        })

    conceptos = json_loads(request.POST['conceptos'])

    if not isinstance(conceptos, list) or not conceptos:
        return json_response({
            'error': -2, 'msg': 'Argumento invalido para los conceptos.'
        })

    conceptos = models.Concepto.objects.filter(
        pst=Pst.objects.get(user=request.user),
        pago=None,
        id__in=conceptos
    )

    if not conceptos:
        return json_response({
            'error': -3,
            'msg': 'No hay conceptos a los cuales asociar el nuevo pago.'
        })

    with transaction.atomic():
        pago = models.Pago(
            pst=Pst.objects.get(user=request.user), total=0
        )
        pago.save()

        conceptos.update(pago=pago)

        pago.total = sum(
            concepto.monto for concepto in pago.concepto_set.all()
        )
        pago.save()

    return json_response({
        'error': 0, 'result': serializers.serialize('json', [pago])
    })


@login_required(login_url=reverse_lazy('cuentas_login'))
def planilla_pago_pdf(request, pk):
    pago = models.Pago.objects.get(id=pk)
    conceptos = models.Concepto.objects.filter(pago=pago.id)

    output = PdfFileWriter()
    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'forma_PPL-01.pdf'), 'rb'))
    #create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=PPL-01.pdf'

    # fill page
    buffer = StringIO() # create string buffer for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 8)

    data = [['DATOS DEL CONTRIBUYENTE','','','','','','',''],
            ['','','','','','','',''],
            ['RIF','','RAZON SOCIAL DEL CONTRIBUYENTE','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['DATOS DEL PAGO','','','','','','',''],
            ['','','','','','','',''],
            [u'Nº DE DOCUMENTO','','','','FECHA DE GENERACIÓN','FECHA DE VENCIMIENTO','','PORCION'],
            ['','','','','','','',''],
            ['CODIGO','CONCEPTO','','','','MONTO Bs.','',''],
            ]
    data[3][0] = unicode(pago.pst.rif)
    data[3][2] = unicode(pago.pst.razon_social)
    data[2][5] = u'Nº {} {} {} {}'.format(pago.numero_documento[:4],
                                                      pago.numero_documento[4:6],
                                                      pago.numero_documento[6:8],
                                                      pago.numero_documento[8:])
    data[8][0] =  unicode(pago.numero_documento[:4])
    data[8][1] =  unicode(pago.numero_documento[4:6])
    data[8][2] =  unicode(pago.numero_documento[6:8])
    data[8][3] =  unicode(pago.numero_documento[8:])
    data[8][4] =  pago.fecha_generacion.strftime("%d/%m/%Y")
    data[8][5] =  pago.fecha_vencimiento.strftime("%d/%m/%Y")
    data[8][7] =  unicode(pago.porcion)
    for concepto in conceptos:
        data.append([unicode(concepto.concepto_tipo.codigo),
                     unicode(concepto.concepto_tipo.nombre),'','','',
                     locale.currency(concepto.monto, symbol=False, grouping=True),'',''])
    data.append(['TOTAL','','','','',locale.currency(pago.total, symbol=False, grouping=True),'',''])
    data.append(['','','','','','','',''])
    data.append(['PARA SER LLENADO POR EL CONTRIBUYENTE O REPRESENTANTE LEGAL','','','','','','',''])
    data.append(['','','','','','','',''])
    data.append(['FORMA DE PAGO','','','','DATOS DEL DEPOSITANTE','','',''])
    data.append(['EFECTIVO','','','','NOMBRE Y APELLIDO','','',''])
    data.append(['CHEQUE DE GERENCIA','','','','FIRMA','','',''])
    data.append(['','','','','','','',''])
    data.append(['VALIDACION DEL BANCO RECEPTOR','','','','','','',''])

    t=Table(data, rowHeights=[18 for i in xrange(19 + len(conceptos))])

    t.setStyle(TableStyle([('GRID',(0,0),(-1,-1), 0.25, colors.black),
                           ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('BACKGROUND',(0,0),(-1,0), colors.grey),
                           ('SPAN',(0,0),(-1,0)),
                           ('SPAN',(0,1),(-1,1)),
                           ('SPAN',(0,2),(1,2)),
                           ('SPAN',(2,2),(4,2)),
                           ('SPAN',(5,2),(7,3)),
                           ('SPAN',(0,3),(1,3)),
                           ('SPAN',(2,3),(4,3)),
                           ('SPAN',(0,4),(-1,4)),
                           ('SPAN',(0,5),(-1,5)),
                           ('BACKGROUND',(0,5),(-1,5), colors.grey),
                           ('SPAN',(0,6),(-1,6)),
                           ('SPAN',(0,7),(3,7)),
                           ('SPAN',(0,7),(3,7)),
                           ('SPAN',(5,7),(6,7)),
                           ('SPAN',(5,8),(6,8)),
                           ('SPAN',(1,9),(4,9)),
                           ('SPAN',(5,9),(7,9)),
                           ('SPAN',(0,-9),(4,-9)),
                           ('SPAN',(5,-9),(7,-9)),
                           ('SPAN',(0,-8),(-1,-8)),
                           ('SPAN',(0,-7),(-1,-7)),
                           ('BACKGROUND',(0,-7),(-1,-7), colors.grey),
                           ('SPAN',(0,-6),(-1,-6)),
                           ('SPAN',(0,-5),(3,-5)),
                           ('SPAN',(4,-5),(7,-5)),
                           ('SPAN',(0,-4),(1,-4)),
                           ('SPAN',(2,-4),(3,-4)),
                           ('SPAN',(4,-4),(5,-4)),
                           ('SPAN',(6,-4),(7,-4)),
                           ('SPAN',(0,-3),(1,-3)),
                           ('SPAN',(2,-3),(3,-3)),
                           ('SPAN',(4,-3),(5,-3)),
                           ('SPAN',(6,-3),(7,-3)),
                           ('SPAN',(0,-2),(-1,-2)),
                           ('SPAN',(0,-1),(-1,-1)),
                           ('BACKGROUND',(0,-1),(-1,-1), colors.grey),
                           ('ALIGN',(0,-9),(4,-9), 'RIGHT'),
                           ('FACE',(0,-9),(4,-9), 'Helvetica-Bold'),
                           ('FACE',(0,0),(-1,0), 'Helvetica-Bold'),
                           ('FACE',(0,2),(3,2), 'Helvetica-Bold'),
                           ('FACE',(0,5),(-1,5), 'Helvetica-Bold'),
                           ('FACE',(0,7),(-1,7), 'Helvetica-Bold'),
                           ('FACE',(0,9),(-1,9), 'Helvetica-Bold'),
                           ('FACE',(0,-5),(0,-1), 'Helvetica-Bold'),
                           ('FACE',(4,-5),(4,-1), 'Helvetica-Bold'),
                           ('FACE',(0,-7),(-1,-7), 'Helvetica-Bold'),
                           ]))
    r = 9
    for concepto in conceptos:
        r += 1
        t.setStyle(TableStyle([('SPAN',(1,r),(4,r)),
                               ('SPAN',(5,r),(7,r))]))
    t.wrapOn(pdf, 200, 300)
    t.drawOn(pdf, 35, 670 - t._height)

    pdf.save()
    # put on watermark from buffer
    watermark = PdfFileReader(buffer)
    page1 = input.getPage(0)

    page1.mergePage(watermark.getPage(0))

    # add processed pdf page
    output.addPage(page1)
    output.write(response)
    return response
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
