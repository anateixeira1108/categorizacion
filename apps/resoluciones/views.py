# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from apps.configuracion import models as cfg_models
from apps.cuentas.models import MinturUser
from apps.pagos import models as pagos_models
from apps.resoluciones import models
from apps.resoluciones import textos
from apps.verificacion import models as vrf_models
from declaraciones import models as dcl_models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.serializers import serialize
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponse
from django.http import QueryDict
from django.views.generic import TemplateView
from django.views.generic import View
from json import loads as json_loads
from registro import models as reg_models
from registro.models import Direccion
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import KeepTogether
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from utils import views_helpers as helpers
from utils.factory import FactoryCodigoActas
from utils.gluon.storage import Storage

import datetime
import os

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas (Clases) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Aprobaciones(TemplateView):
    template_name = 'resoluciones/funcionario/resoluciones_aprobaciones.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Aprobaciones, self).get_context_data(*args, **kwargs)
        context['resoluciones'] = models.Resolucion.objects.filter(
            estatus=u'Aprobación Solicitada'
        )
        return context


class ResolucionDetalle(TemplateView):
    template_name = 'resoluciones/funcionario/resolucion_detalle.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ResolucionDetalle, self).get_context_data(
            *args, **kwargs
        )
        resolucion = models.Resolucion.objects.get(
            pk=kwargs['pk']
        )
        context['resolucion'] = resolucion
        ilicito_queryset = models.Ilicito.objects.filter(
            resolucion=resolucion
        ).order_by('periodo', 'sancion')
        sancion_set = set(
            ilicito.sancion for ilicito in ilicito_queryset
        )
        context['pst'] = (
            resolucion.pst
        )
        context['sanciones'] = {
            sancion: [row for row in ilicito_queryset.filter(sancion=sancion)]
            for sancion in sancion_set
        }
        context['concurrencia'] = models.Resolucion.calc_concurrencia(
            resolucion
        )
        context['intereses_moratorios'] = (
            dcl_models.InteresMoratorio.get_intereses_moratorios(
                resolucion.pst,
                resolucion.verificacion.desde,
                resolucion.verificacion.hasta,
            )
        )
        context['total_intereses_moratorios'] = sum(
            row.monto_interes for row in context['intereses_moratorios']
        )
        context['total_pagar'] = (
            sum(decimal for decimal in context['concurrencia'][1].itervalues())
            + context['total_intereses_moratorios']
            + context['concurrencia'][0][1]
        )
        return context


class ResolucionPdf(View):
    def get(self, request, *args, **kwargs):
        gerente = MinturUser.objects.get(groups=Group.objects.get(name='gerente_dggt'))
        context = ResolucionDetalle.as_view()(self.request, *args, **kwargs).context_data
        direccion = Direccion.objects.get(pst=context['resolucion'].pst)

        output = PdfFileWriter()
        #create response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Resolucion.pdf'

        buffer = StringIO()
        doc = SimpleDocTemplate(buffer,pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=-50,bottomMargin=100)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize = 12, leading = 15))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, fontSize = 12, leading = 15))
        styles.add(ParagraphStyle(name='tit',
                                  alignment=TA_CENTER, leftIndent=25, rightIndent=25,
                                  fontSize = 12, leading = 15))

        Story = []

        codigo = context['resolucion'].numero_documento
        fecha = textos.fecha_encabezado(datetime.date.today())
        primer_titulo = 'RESOLUCIÓN DE AJUSTES E IMPOSICIÓN DE SANCIONES VERIFICACION DE DEBERES FORMALES'
        seccion_uno = 'I. DE LOS HECHOS CONSTATADOS:'
        seccion_dos = 'II. DE LA CONCURRENCIA:'
        seccion_tres = 'III. DEL MONTO TOTAL DE LAS SANCIONES A PAGAR:'
        seccion_intereses_moratorios = 'III. DE LOS INTERESES MORATORIOS:'

        #CABECERA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ptext = '<font size=12>%s</font>' % codigo
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        ptext = '<font size=12>%s</font>' % fecha
        Story.append(Paragraph(ptext, styles["Right"]))
        Story.append(Spacer(1, 12))

        data = [['SUJETO PASIVO',context['resolucion'].pst.nombre_o_razon()],
                ['RIF Nº.:',context['resolucion'].pst.rif],
                ['RTN Nº:',context['resolucion'].pst.rtn],
                ['DOMICILIO:',Paragraph(unicode(direccion), styles["Normal"])]
                ]
        Story.append(Table(data, colWidths=[100, 350], style=[('GRID',(0,0),(-1,-1), 0.25, colors.black),
                                                              ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
        Story.append(Spacer(1, 12))

        #MEMBRETE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ptext = '<u><b>%s</b></u>' % primer_titulo
        Story.append(Paragraph(ptext, styles["tit"]))
        Story.append(Spacer(1, 12))

        ptext = textos.primer_parrafo(datetime.date.today(), gerente)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        #SECCION UNO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ptext = '<font size=12><b>%s</b></font>' % seccion_uno
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        ptext = textos.seccion_uno_inicio()
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        sancion_numero = 1
        for sancion, ilicitos in context['sanciones'].iteritems():
            ptext = textos.segundo_parrafo(sancion_numero, context['resolucion'], sancion, ilicitos)
            Story.append(Paragraph(ptext, styles["Justify"]))
            Story.append(Spacer(1, 12))
            sancion_numero += 1

            th = [Paragraph('Periodo', styles['Center']),
                  Paragraph(u'Sanción (UT)', styles['Center']),
                  Paragraph(u'Incremento por Reincidencia (UT)', styles['Center']),
                  Paragraph('Total (UT)', styles['Center']),
                  Paragraph('Valor de la UT a la Fecha', styles['Center']),
                  Paragraph('Equivalencia en Bs.', styles['Center'])]
            if ilicitos[0].declaracion:
                th.insert(1, Paragraph(u'Fecha Límite de Declaración', styles['Center']))
                th.insert(2, Paragraph(u'Fecha de Declaración', styles['Center']))
            data = [th,]
            for ilicito in ilicitos:
                tr = [ilicito.periodo.strftime('%x'),
                      ilicito.sancion.ut_min,
                      ilicito.sancion_ut - ilicito.sancion.ut_min,
                      ilicito.sancion_ut,
                      ilicito.resolucion.valor_ut,
                      ilicito.sancion_ut * ilicito.resolucion.valor_ut]
                if ilicitos[0].declaracion:
                    tr.insert(1, ilicito.fecha_limite_declaracion.strftime('%x'))
                    tr.insert(2, ilicito.declaracion.fecha_presentacion.strftime('%x'))
                data.append(tr)
            Story.append(KeepTogether(Table(data, style=[('GRID',(0,0),(-1,-1), 0.25, colors.black),
                                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                        ('ALIGN',(0,0),(-1,-1),'CENTER')])))
            Story.append(Spacer(1, 12))

        #SECCION DOS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ptext = '<font size=12><b>%s</b></font>' % seccion_dos
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        ptext = textos.seccion_dos_inicio()
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        data = [[u'Ilícito', u'Sanción (BsF)', u'Tipo de Sanción', u'Total Sanción Agravada (BsF)'],]
        for sancion, decimal in context['concurrencia'][1].iteritems():
            data.append([u'Art. ' + unicode(sancion.cot_articulo),
                         decimal * 2,
                         u'Mitad de la Sanción',
                         decimal ])
        data.append([u'Art. ' + unicode(context['concurrencia'][0][0].cot_articulo),
                     context['concurrencia'][0][1],
                     u'Sanción más Grave',
                     context['concurrencia'][0][1] ])
        Story.append(KeepTogether(Table(data, style=[('GRID',(0,0),(-1,-1), 0.25, colors.black),
                                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                        ('ALIGN',(0,0),(-1,-1),'CENTER')])))
        Story.append(Spacer(1, 12))

        # INTERESES MORATORIOS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if context['intereses_moratorios']:
            seccion_tres = seccion_tres.replace(u'III', u'IV')

            periodos = [
                (lambda periodo: periodo[0].upper() + periodo[1:])(
                    interes.declaracion.periodo.strftime('%B-%Y')
                ) for interes in context['intereses_moratorios']
            ]

            ptext = '<font size=12><b>%s</b></font>' % seccion_intereses_moratorios
            Story.append(Paragraph(ptext, styles["Normal"]))
            Story.append(Spacer(1, 12))

            ptext = textos.seccion_intereses_moratorios_inicio(periodos)
            Story.append(Paragraph(ptext, styles["Justify"]))
            Story.append(Spacer(1, 12))

            data = [
                [
                    u'Periodo',
                    u'Fecha de\nVencimiento de\nla Obligación',
                    u'Fecha de\nPago',
                    u'Días de\nMora',
                    u'Tributo Pagado\nExtemporaneamente\n(BsF)',
                    u'Tasa de Interés\nFijada por el\nBCV según\nG.O. (%)',
                    (
                        u'Tasa de Interés\npara Cálculo de\nInterés de Mora\n'
                        u'Art. 66 C.O.T.\n(%)'
                    ),
                    u'Factor',
                    u'Monto\nIntereses\nMoratorios\n(BsF)',
                ]
            ]

            for interes in context['intereses_moratorios']:
                pago = interes.declaracion.concepto_pago.pago

                data.append([
                    (lambda periodo: periodo[0].upper() + periodo[1:])(
                        interes.declaracion.periodo.strftime('%b-%y')
                    ),
                    pago.fecha_vencimiento.strftime('%d/%m/%Y'),
                    pago.fecha_liquidacion.strftime('%d/%m/%Y'),
                    interes.dias_mora,
                    pago.total,
                    interes.tasa_interes_bcv,
                    interes.art66cot,
                    interes.factor,
                    interes.monto_interes,
                ])

            Story.append(KeepTogether(Table(
                data,
                style=[
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER')
                ]
            )))

            Story.append(Spacer(1, 12))

        #SECCION TRES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ptext = '<font size=12><b>%s</b></font>' % seccion_tres
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        ptext = textos.seccion_tres_inicio(context['resolucion'].pst.nombre_o_razon())
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        data = [['Concepto', u'Sanción (BsF)'],]
        for sancion, decimal in context['concurrencia'][1].iteritems():
            data.append([u'Sanción Nº ' + unicode(sancion.codigo), decimal])
        data.append([u'Sanción Nº ' + unicode(context['concurrencia'][0][0].codigo), context['concurrencia'][0][1]])

        if context['total_intereses_moratorios']:
            data.append([
                (
                    u'Intereses moratorios por pago extemporáneo'
                    u'(Art. 66 del COT)'
                ),
                context['total_intereses_moratorios']
            ])

        data.append([u'Total General a Pagar:', context['total_pagar']])
        Story.append(KeepTogether(Table(data, style=[('GRID',(0,0),(-1,-1), 0.25, colors.black),
                                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                        ('ALIGN',(0,0),(-1,-1),'CENTER')])))
        Story.append(Spacer(1, 12))

        ptext = textos.seccion_tres_fin(context['resolucion'].pst.nombre_o_razon())
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        #FOOTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Story.append(Spacer(1, 10 * 12))

        ptext = textos.footer_texto(gerente)
        footer_texto = Paragraph(ptext, styles["tit"])

        ptext = textos.footer_firma()
        footer_firma = Paragraph(ptext, styles["Left"])
        Story.append(KeepTogether([footer_texto,
                                  Spacer(1, 12),
                                  footer_firma]))

        Story.append(PageBreak())

        doc.build(Story)

        watermark = PdfFileReader(buffer)
        for page in xrange(watermark.getNumPages()):
            input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'blanco.pdf'), 'rb'))
            tmp = input.getPage(0)
            tmp.mergePage(watermark.getPage(page))
            output.addPage(tmp)

        output.write(response)
        return response
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas (Funciones) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
def buscar_sancion_rest(request):
    if request.method != 'GET':
        return helpers.json_response({'error': -1, 'msg': 'Bad HTTP Method'})

    if 'query' not in request.GET or not request.GET['query']:
        return helpers.json_response(
            {'error': -2, 'msg': 'Por favor, indique la sanción a buscar.'}
        )

    if request.GET['query'].isdigit():
        sanciones = models.Sancion.objects.filter(
            codigo__contains=request.GET['query']
        ).order_by('codigo')

    else:
        sanciones = models.Sancion.objects.filter(
            descripcion__contains=request.GET['query'].upper()
        ).order_by('codigo')

    return helpers.json_response({
        'error': 0, 'result': serialize('json', sanciones)
    })


@login_required(login_url=reverse_lazy('cuentas_login'))
def ilicito_rest(request):
    if request.method == 'GET':
        return ilicito_rest_get(request)

    if request.method == 'POST':
        return ilicito_rest_post(request)

    if request.method == 'PUT':
        return ilicito_rest_put(request)

    if request.method == 'DELETE':
        return ilicito_rest_delete(request)

    return helpers.json_response({'error': -1, 'msg': u'Método no soportado.'})


@login_required(login_url=reverse_lazy('cuentas_login'))
def resolucion_rest(request):
    if request.method == 'GET':
        return resolucion_rest_get(request)

    if request.method == 'POST':
        return resolucion_rest_post(request)

    if request.method == 'DELETE':
        return resolucion_rest_delete(request)

    return helpers.json_response({'error': -1, 'msg': u'Método no soportado.'})


@login_required(login_url=reverse_lazy('cuentas_login'))
def resolucion_solicitar_aprobacion_json(request):
    if request.method != 'PUT':
        return helpers.json_response({
            'error': -1, 'msg': u'Método no soportado.'
        })

    request.PUT = QueryDict(request.body)

    if 'resolucion_id' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar el ID de la resolución a borrar.'
        })

    if not request.PUT['resolucion_id'].isdigit():
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar el ID de la resolución a borrar.'
        })

    try:
        resolucion = models.Resolucion.objects.get(
            pk=request.PUT['resolucion_id']
        )

    except models.Resolucion.DoesNotExist:
        return helpers.json_response({
            'error': -2, 'msg': 'No existe resolución con el ID proporcionado.'
        })

    else:
        resolucion.estatus = u'Aprobación Solicitada'
        resolucion.save()

        return helpers.json_response({
            'error': 0, 'result': serialize('json', [resolucion])
        })

    return helpers.json_response({
        'error': -2, 'msg': 'Algo ha ido muy mal en el servidor.'
    })


@login_required(login_url=reverse_lazy('cuentas_login'))
def resolucion_aprobar_json(request):
    if request.method != 'PUT':
        return helpers.json_response({
            'error': -1, 'msg': u'Método no soportado.'
        })

    request.PUT = QueryDict(request.body)

    if 'resolucion_id_list' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar una lista de IDs.'
        })

    resolucion_id_list = json_loads(request.PUT['resolucion_id_list'])

    if not isinstance(resolucion_id_list, list):
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar una lista de IDs.'
        })

    resolucion_queryset = models.Resolucion.objects.filter(
        pk__in=resolucion_id_list
    )

    with transaction.atomic():
        resolucion_queryset.update(estatus=u'Aprobada')

        for resolucion in resolucion_queryset:
            concurrencia = models.Resolucion.calc_concurrencia(
                resolucion
            )
            total_pagar = (
                sum(decimal for decimal in concurrencia[1].itervalues())
                + concurrencia[0][1]
            )
            concepto_data = {
                'pst': resolucion.pst,
                'concepto_tipo': pagos_models.ConceptoTipo.objects.get(
                    nombre=u'Multa'
                ),
                'monto': total_pagar,
            }

            pagos_models.Concepto(**concepto_data).save()

            intereses_moratorios = (
                dcl_models.InteresMoratorio.get_intereses_moratorios(
                    resolucion.pst,
                    resolucion.verificacion.desde,
                    resolucion.verificacion.hasta,
                )
            )

            for interes_moratorio in intereses_moratorios:
                concepto_pago = pagos_models.Concepto(
                    pst=resolucion.pst,
                    concepto_tipo=pagos_models.ConceptoTipo.objects.get(
                        nombre=(
                            u'Intereses moratorios por pago extemporáneo'
                            u' (Art. 66 del COT)'
                        )
                    ),
                    monto=interes_moratorio.monto_interes,
                )
                concepto_pago.save()

                interes_moratorio.concepto_pago = concepto_pago
                interes_moratorio.save()

    return helpers.json_response({'error': 0, 'result': ''})


@login_required(login_url=reverse_lazy('cuentas_login'))
def resolucion_rechazar_json(request):
    if request.method != 'PUT':
        return helpers.json_response({
            'error': -1, 'msg': u'Método no soportado.'
        })

    request.PUT = QueryDict(request.body)

    if 'resolucion_id_list' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar una lista de IDs.'
        })

    resolucion_id_list = json_loads(request.PUT['resolucion_id_list'])

    if not isinstance(resolucion_id_list, list):
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar una lista de IDs.'
        })

    models.Resolucion.objects.filter(pk__in=resolucion_id_list).update(
        estatus=u'Rechazada', observaciones=request.PUT.get('observaciones', '')
    )

    return helpers.json_response({'error': 0, 'result': ''})
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ilicito_rest_get(request):
    if 'resolucion_id' not in request.GET:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar el ID de la resolución asociada.'
        })

    result = list(models.Ilicito.objects.filter(
        resolucion_id=request.GET['resolucion_id']
    ))

    attachment = [
        dict(
            declaracion=unicode(row.declaracion) if row.declaracion else None,
            sancion_codigo=row.sancion.codigo,
            ut_max=row.sancion.ut_max,
            ut_min=row.sancion.ut_min,
        ) for row in result
    ]

    return helpers.json_response({
        'error': 0, 'result': serialize('json', result), 'att': attachment
    })


def ilicito_rest_post(request):
    request.POST = QueryDict(request.body)

    if 'resolucion_id' not in request.POST:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar el ID de la resolución asociada.'
        })

    if 'ilicito_list' not in request.POST:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar los ilícitos a modificar.'
        })

    try:
        resolucion = models.Resolucion.objects.get(
            pk=request.POST['resolucion_id']
        )

    except models.Resolucion.DoesNotExist:
        return helpers.json_response({
            'error': -2, 'msg': u'No existe resolución con el ID indicado.'
        })
    else:
        try:
            parse_ilicito_list(request, resolucion)

        except AssertionError as e:
            return helpers.json_response({'error': -2, 'msg': str(e)})

    return helpers.json_response({'error': 0, 'result': ''})


def ilicito_rest_put(request):
    request.PUT = QueryDict(request.body)

    if 'resolucion_id' not in request.PUT:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar el ID de la resolución asociada.'
        })

    if 'ilicito_obj_list' not in request.PUT:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar los ilícitos a modificar.'
        })

    ilicito_obj_list = json_loads(request.PUT['ilicito_obj_list'])

    if not (ilicito_obj_list, list):
        return helpers.json_response({
            'error': -2, 'msg': u'Debe proporcionar una lista de ilícitos.'
        })

    try:
        with transaction.atomic():
            for ilicito in ilicito_obj_list:
                models.Ilicito.objects.filter(
                    pk=ilicito['pk'],
                    resolucion_id=request.PUT['resolucion_id'],
                ).update(sancion_ut=ilicito['sancion_ut'])

    except Exception:
        return helpers.json_response({
            'error': -2,
            'msg': u'Por favor, verifique los cambios introducidos'
        })

    return helpers.json_response({'error': 0, 'result': ''})


def ilicito_rest_delete(request):
    request.DELETE = QueryDict(request.body)

    if 'resolucion_id' not in request.DELETE:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar el ID de la resolución asociada.'
        })

    if 'ilicito_id_list' not in request.DELETE:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar los IDs de los ilícitos a borrar.'
        })

    ilicito_id_list = json_loads(request.DELETE['ilicito_id_list'])

    if not (ilicito_id_list, list):
        return helpers.json_response({
            'error': -2, 'msg': u'Debe proporcionar una lista de ilícitos.'
        })

    models.Ilicito.objects.filter(
        resolucion_id=request.DELETE['resolucion_id'],
        pk__in=ilicito_id_list,
    ).delete()

    return helpers.json_response({'error': 0, 'result': ''})


def resolucion_rest_get(request):
    if 'resolucion_id' in request.GET:
        query = {'pk': request.GET['resolucion_id']}

        if not request.GET['resolucion_id'].isdigit():
            return helpers.json_response({
                'error': -2, 'msg': 'Argumento mal formado para la ID.'
            })

    elif 'estatus' in request.GET:
        query = {'estatus': request.GET['estatus']}

    else:
        return helpers.json_response({
            'error': 0, 'result': [], 'attachment': []
        })

    resolucion_queryset = models.Resolucion.objects.filter(**query)

    return helpers.json_response({
        'error': 0,
        'result': serialize('json', resolucion_queryset),
        'attachment': [
            serialize('json', row.ilicito_set.filter())
            for row in resolucion_queryset
        ]
    })


def resolucion_rest_post(request):
    try:
        resolucion_data = {
            'funcionario': request.user,
            'pst': reg_models.Pst.objects.get(rif=request.POST['pst_rif']),
            'tipo_resolucion_id': request.POST['tipo_resolucion_id'],
            'verificacion_id': request.POST['acta_id'],
            'valor_ut': cfg_models.UnidadTributaria.get_valor_para_fecha(
                datetime.date.today()
            )
        }
        factory_resolucion = FactoryCodigoActas(Storage(
            es_una_resolucion=True,
            objeto_verificacion=vrf_models.Verificacion.objects.get(
                id=resolucion_data['verificacion_id']
            )
        ))
        resolucion_data['numero_documento'] = (
            factory_resolucion.make_codigo()
        )

        with transaction.atomic():
            nueva_resolucion = models.Resolucion(**resolucion_data)
            nueva_resolucion.save()

            parse_ilicito_list(request, nueva_resolucion)

        return helpers.json_response({
            'error': 0, 'result': serialize('json', [nueva_resolucion])
        })

    except Exception as e:
        return helpers.json_response({'error': -2, 'msg': str(e)})


def resolucion_rest_delete(request):
    request.DELETE = QueryDict(request.body)

    if 'resolucion_id' not in request.DELETE:
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar el ID de la resolución a borrar.'
        })

    if not request.DELETE['resolucion_id'].isdigit():
        return helpers.json_response({
            'error': -2, 'msg': 'Debe indicar el ID de la resolución a borrar.'
        })

    try:
        resolucion = models.Resolucion.objects.get(
            pk=request.DELETE['resolucion_id']
        )

    except models.Resolucion.DoesNotExist:
        return helpers.json_response({
            'error': -2, 'msg': 'No existe resolución con el ID proporcionado.'
        })

    else:
        return helpers.json_response({
            'error': 0, 'result': resolucion.delete()
        })

    return helpers.json_response({
        'error': -2, 'msg': 'Algo ha ido muy mal en el servidor.'
    })


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%d/%m/%Y')


def parse_ilicito_list(request, resolucion):
    if 'ilicito_list' not in request.POST:
        raise AssertionError('Debe indicar la lista de ilícitos.')

    ilicito_list = json_loads(request.POST['ilicito_list'])

    for ilicito in ilicito_list:
        if not ilicito['periodo'] or not ilicito['fecha_limite']:
            raise AssertionError(
                'Debe indicar el periodo asociado a toda sanción.'
            )

        ilicito_data = dict(
            resolucion=resolucion,
            sancion=models.Sancion.objects.get(
                codigo=ilicito['sancion_codigo']
            ),
            declaracion_id=(ilicito['declaracion_id'] or None),
            periodo=parse_date(ilicito['periodo']),
            fecha_limite_declaracion=parse_date(ilicito['fecha_limite']),
        )
        ilicito_data.update(dict(
            valor_ut=cfg_models.UnidadTributaria.get_valor_para_fecha(
                ilicito_data['periodo'].date()
            ),
        ))

        new_ilicito = models.Ilicito(**ilicito_data)
        new_ilicito.sancion_ut = models.Ilicito.calc_sancion(new_ilicito)
        new_ilicito.save()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
