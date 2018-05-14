# -*- coding: utf-8 -*-

u""" Vistas para las declaraciones. """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón U.
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import date
from decimal import Decimal
from json import dumps as json_dumps
from json import loads as json_loads
import locale
import os
import platform

from PyPDF2 import PdfFileWriter, PdfFileReader
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.serializers import serialize
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.base import TemplateView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from .templatetags import filtros_declaraciones as filtros

from apps.cuentas.mixins import MenuPSTMixin
from apps.pagos import models as pagos_models
from forms import PlanillaForm
from models import Declaracion, Prueba
from registro.models import Pst
from utils import views_helpers as helpers
from utils.email import MailMan


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# init ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if 'Windows' in platform.platform():
    locale.setlocale(locale.LC_ALL, 'esp_ven')
else:
    locale.setlocale(locale.LC_ALL, 'es_VE.UTF-8')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas (Clases) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlanillaFormView(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'declaraciones/pst/planilla.html'
    form_class = PlanillaForm

    def get_initial(self):
        self.pst = helpers.get_object_or_none(Pst, user=self.request.user)

        query_has_change = (
            'periodo' in self.request.GET
            and self.request.GET != self.request.session.get('query')
        )

        if query_has_change:
            self.request.session['query'] = self.request.GET

        return {'pst': self.pst, 'query': self.request.session.get('query')}

    def get_form_kwargs(self):
        kwargs = super(PlanillaFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        context.update({
            'clean_periodo': form.cleaned_data['periodo'],
            'form': form
        })
        return render(
            self.request,
            'declaraciones/pst/planilla_vista_previa.html',
            context
        )


class PlanillaSaveView(helpers.FormViewBaseClass, MenuPSTMixin):
    template_name = 'declaraciones/pst/planilla.html'
    success_url = reverse_lazy('declaraciones_pst_declaraciones')
    form_class = PlanillaForm

    def get_initial(self):
        self.pst = helpers.get_object_or_none(Pst, user=self.request.user)
        return {'pst': self.pst}

    def get_form_kwargs(self):
        kwargs = super(PlanillaSaveView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        data = {'pst': self.pst}

        data.update({
            field: form.cleaned_data[field]
            for field in self.form_class._meta.fields
        })

        data['total_ventas_territorial'] = (
            calc_total_ventas_territorial(data)
        )
        data['total_ventas_menos_anticipo'] = (
            calc_total_ventas_menos_anticipo(data)
        )
        data['contribucion_especial_determinada'] = (
            calc_contribucion_especial_determinada(data)
        )
        data['total_pagar'] = (
            calc_total_pagar(data)
        )

        concepto_data = {
            'pst': self.pst,
            'concepto_tipo': pagos_models.ConceptoTipo.objects.get(
                nombre=u'Declaración'
            ),
            'monto': data['total_pagar'],
        }

        with transaction.atomic():
            if concepto_data['monto'] > 0:
                concepto_pago = pagos_models.Concepto(**concepto_data)
                concepto_pago.save()

            if 'concepto_pago' in locals():
                data['concepto_pago'] = concepto_pago

            Declaracion(**data).save()

        MailMan.declaracion_nueva(
            data_dict={
                'razon_social': data['pst'].razon_social,
                'periodo': ((lambda s: s[0].upper() + s[1:])(
                    data['periodo'].strftime('%B-%Y')
                )),
            },
            receptor_email=data['pst'].user.correo_electronico
        )

        return super(PlanillaSaveView, self).form_valid(form)


class PlanillaVerView(TemplateView, MenuPSTMixin):
    template_name = 'declaraciones/pst/planilla_ver.html'

    def get_context_data(self, **kwargs):
        context = super(PlanillaVerView, self).get_context_data(**kwargs)
        context['declaracion'] = Declaracion.objects.get(
            id=context['declaracion_id']
        )
        return context


class DeclaracionesListaView(TemplateView, MenuPSTMixin):
    template_name = 'declaraciones/pst/declaraciones.html'

    def get_context_data(self, **kwargs):
        context = super(DeclaracionesListaView, self).get_context_data(**kwargs)

        declaraciones = Declaracion.objects.filter(
            pst=Pst.objects.get(user=self.request.user)
        ).order_by('-fecha_presentacion')

        paginator_handler = paginator.Paginator(declaraciones, 15)
        page = self.request.GET.get('page')

        try:
            context['declaraciones'] = paginator_handler.page(page)

        except paginator.PageNotAnInteger:
            context['declaraciones'] = paginator_handler.page(1)

        except paginator.EmptyPage:
            context['declaraciones'] = paginator_handler.page(
                paginator_handler.num_pages
            )
        return context


class AnularDeclaracion(View):
    def post(self, request):
        declaracion = Declaracion.objects.get(
            pk=request.POST['declaracion-id']
        )
        declaracion.estatus = u'Por anular'
        declaracion.justificacion_pst = request.POST['justificacion']

        for field, value in request.FILES.iteritems():
            Prueba(
                archivo=request.FILES[field], declaracion=declaracion
            ).save()

        with transaction.atomic():
            declaracion.save()

            if declaracion.concepto_pago is not None:
                declaracion.concepto_pago.estatus = u'Declaración por anular'
                declaracion.concepto_pago.save()

        return redirect('declaraciones_pst_declaraciones')


class FuncionarioAnulacionListView(LoginRequiredMixin, ListView):
    model = Declaracion
    template_name = 'declaraciones/funcionario/declaraciones_anulacion.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FuncionarioAnulacionListView, self).get_context_data()
        context['declaraciones'] = Declaracion.objects.filter(estatus=u'Por anular')
        return context


class FuncionarioPlanillaVerView(TemplateView):
    template_name = 'declaraciones/funcionario/planilla_ver.html'

    def get_context_data(self, **kwargs):
        context = super(FuncionarioPlanillaVerView, self).get_context_data(**kwargs)
        context['declaracion'] = Declaracion.objects.get(
            id=context['declaracion_id']
        )
        context['pruebas'] = Prueba.objects.filter(declaracion=context['declaracion'])
        return context


class FuncionarioRechazarAnulacion(View):
    def post(self, request):
        declaracion_id = request.POST['declaracion-id']
        declaracion = Declaracion.objects.get(id=declaracion_id)
        declaracion.estatus = 'Declarada'
        declaracion.justificacion_funcionario = request.POST['justificacion']

        with transaction.atomic():
            declaracion.save()

            if declaracion.concepto_pago is not None:
                declaracion.concepto_pago.estatus = u'Pendiente'
                declaracion.concepto_pago.save()

        MailMan.declaracion_anulacion_rechazada(
            data_dict={
                'razon_social': declaracion.pst.razon_social,
                'periodo': ((lambda s: s[0].upper() + s[1:])(
                    declaracion.periodo.strftime('%B-%Y')
                )),
            },
            receptor_email=declaracion.pst.user.correo_electronico
        )

        return redirect('funcionario_declaracion_por_anular')


class FuncionarioAnularDeclaracion(View):
    def post(self, request):
        declaracion_id = request.POST['declaracion-id']
        declaracion = Declaracion.objects.get(id=declaracion_id)
        declaracion.estatus = u'Anulada'

        with transaction.atomic():
            declaracion.save()

            if declaracion.concepto_pago is not None:
                declaracion.concepto_pago.estatus = u'Declaración anulada'
                declaracion.concepto_pago.save()

        MailMan.declaracion_anulacion_aprobada(
            data_dict={
                'razon_social': declaracion.pst.razon_social,
                'periodo': ((lambda s: s[0].upper() + s[1:])(
                    declaracion.periodo.strftime('%B-%Y')
                )),
            },
            receptor_email=declaracion.pst.user.correo_electronico
        )

        return redirect('funcionario_declaracion_por_anular')


def BusquedaDeclaracionesAnuladasPorRifView(request):
    """
        Vista encargada de realizar la busqueda de declaraciones por rif
    """
    if 'query' in request.GET:
        query = request.GET['query']
        if query:
            declaraciones = Declaracion.objects.filter(estatus=u'Por anular',
                                                       pst__rif__contains=query)
            if declaraciones:  #si hay registros en la busqueda
                error = False
            else:  #si no hay registros en la busqueda
                error = True
            context = {}
            context['error'] = error
            if not error:
                context['declaraciones'] = declaraciones
            return render(request,
                          'declaraciones/funcionario/declaraciones_anulacion.html',
                          context
            )
        else:  #si no ingreso nada en el campo de busqueda, busca todos los registros
            declaraciones = Declaracion.objects.filter(estatus=u'Por anular')
            return render(request,
                          'declaraciones/funcionario/declaraciones_anulacion.html',
                          {'declaraciones': declaraciones}
            )

    else:  #si se desconoce la busqueda
        return render(request,
                      'declaraciones/funcionario/declaraciones_anulacion.html',
                      {'error': True}
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas (Funciones) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
def declaraciones_rest(request):
    if 'periodo' in request.GET:
        try:
            period = map(int, request.GET['periodo'].split('/'))

        except ValueError:
            return helpers.json_response({
                'error': -2, 'msg': 'Bad value for the period.'
            })

        if not period or len(period) != 3:
            return helpers.json_response({
                'error': -2, 'msg': 'Bad value for the period.'
            })

        if 'pst' in request.GET:
            result = Declaracion.objects.filter(
                ~ Q(estatus=u'Anulada'),
                pst=helpers.get_object_or_none(Pst, rif=request.GET['pst']),
                periodo=date(*reversed(period))
            ).order_by('fecha_presentacion')

            if request.GET.get('detailed', False):
                return helpers.json_response({
                    'error': 0, 'result': serialize('json', result)
                })

            return helpers.json_response({
                'error': 0,
                'result': json_dumps([
                    {'pk': row.pk, 'repr': unicode(row)} for row in result
                ])
            })

        result = Declaracion.objects.filter(
            pst=helpers.get_object_or_none(Pst, user=request.user),
            periodo=date(*reversed(period))
        ).order_by('fecha_presentacion')

        allow_definitiva = (
            result.count() == 0
            or (
                result.last().tipo_declaracion.nombre == (
                    u'Declaración Definitiva'
                ) and result.last().estatus == u'Anulada'
            )
        )

        if allow_definitiva:
            return helpers.json_response(
                {'error': 0, 'result': json_loads(serialize('json', []))}
            )

        if result.last().estatus not in [u'Pagada', u'Anulada']:
            return helpers.json_response({
                'error': -2,
                'msg': (
                    'La última declaración para el'
                    ' periodo indicado no ha sido pagada.'
                )
            })

    elif 'id' in request.GET:
        result = Declaracion.objects.filter(
            pst=helpers.get_object_or_none(Pst, user=request.user),
            id=request.GET['id']
        )

    else:
        return helpers.json_response({
            'error': -1, 'msg': 'Debe indicar el periodo que va a declarar.'
        })

    return helpers.json_response(
        {'error': 0, 'result': json_loads(serialize('json', result))}
    )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# PDF Impresion ---------------------------------------------------------------
class Pdf(View):
    def get(self, request, declaracion_id):
        declaracion = Declaracion.objects.get(id=declaracion_id)
        output = PdfFileWriter()
        input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'declaracion', 'declaracion.pdf'), 'rb'))

        #create response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Declaracion.pdf'

        # fill first page
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 10)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize = 6, leading = 8))

        data = [['','','','','','','','','','',''] for i in xrange(34)]
        # A.- DATOS DEL CONTRIBUYENTE
        data[0][0] = u'A.- DATOS DEL CONTRIBUYENTE'
        data[2][0] = u'RIF'
        data[3][0] = pretty_string(declaracion.pst.rif)
        data[2][2] = u'RAZÓN SOCIAL DEL CONTRIBUYENTE'
        data[3][2] = pretty_string(declaracion.pst.razon_social)
        data[2][7] = u'RTN'
        data[3][7] = pretty_string(declaracion.pst.rtn)
        data[2][8] = u'LICENCIA'
        data[3][8] = filtros.get_licencia(declaracion.pst)

        try:
            data[3][8] = pretty_string(declaracion.pst.licencia)
        except:
            pass
        # B.- EJERCICIO GRAVABLE
        data[5][0] = u'B.- EJERCICIO GRAVABLE'
        data[7][0] = u'TIPO DE DECLARACIÓN'
        data[8][0] = pretty_tipo(declaracion.tipo_declaracion)
        data[7][2] = u'PERÍODO'
        data[8][2] = declaracion.periodo.strftime("%B - %Y")
        data[7][4] = u'DESDE'
        data[7][6] = declaracion.fecha_desde.strftime("%d/%m/%Y")
        data[8][4] = u'HASTA'
        data[8][6] = declaracion.fecha_hasta.strftime("%d/%m/%Y")
        data[7][8] = u'FECHA DE PRESENTACIÓN'
        data[8][8] = declaracion.fecha_presentacion.strftime("%d/%m/%Y")
        # C.- AUTOLIQUIDACIÓN DEL IMPUESTO
        data[9][0] = u'C.- AUTOLIQUIDACIÓN DEL IMPUESTO'
        data[10][0] = u'C.1.- ESTADO DEMOSTRATIVO DEL INGRESO'
        data[11][0] = u'FUENTE TERRITORIAL'
        data[12][0] = u'1'
        data[12][1] = u'Ventas Propias Internas no gravadas por la Ley del IVA'
        data[13][0] = u'2'
        data[13][1] = u'Ventas de Exportación'
        data[14][0] = u'3'
        data[14][1] = u'Ventas Internas Gravadas por Alícuota General'
        data[15][0] = u'4'
        data[15][1] = u'Ventas Internas Gravadas por Alícuota General más Alícuota Adicional'
        data[16][0] = u'5'
        data[16][1] = u'Ventas Internas Gravadas por Alícuota Reducida'
        data[17][0] = u'6'
        data[17][1] = u'Total Ventas de Fuente territorial (7+8+9+10+11)'
        data[12][7] = u'7'
        data[12][8] = pretty_number(declaracion.ventas_propias)
        data[13][7] = u'8'
        data[13][8] = pretty_number(declaracion.ventas_exportacion)
        data[14][7] = u'9'
        data[14][8] = pretty_number(declaracion.ventas_internas_general)
        data[15][7] = u'10'
        data[15][8] = pretty_number(declaracion.ventas_internas_adicional)
        data[16][7] = u'11'
        data[16][8] = pretty_number(declaracion.ventas_internas_reducida)
        data[17][7] = u'12'
        data[17][8] = pretty_number(declaracion.total_ventas_territorial)
        # ANTICIPO
        data[18][0] = u'ANTICIPO'
        data[19][0] = u'13'
        data[19][1] = u'Anticipo'
        data[20][0] = u'14'
        data[20][1] = u'Total Ventas Menos Anticipo (12-16)'
        data[21][0] = u'15'
        data[21][1] = u'Contribución Especial Determinada'
        data[19][7] = u'16'
        data[19][8] = pretty_number(declaracion.anticipo_declaracion)
        data[20][7] = u'17'
        data[20][8] = pretty_number(declaracion.total_ventas_menos_anticipo)
        data[21][7] = u'18'
        data[21][8] = pretty_number(declaracion.contribucion_especial_determinada)
        # D.- COMPENSACIÓN
        data[22][0] = u'D.- COMPENSACIÓN'
        data[23][0] = u'19'
        data[23][1] = u'Compensaciones con créditos propios'
        data[24][0] = u'20'
        data[24][1] = u'Número de Resolución'
        data[25][0] = u'21'
        #data[25][1] =
        data[26][0] = u'22'
        #data[26][1] =
        data[27][0] = u'23'
        #data[27][1] =
        data[24][3] = u'24'
        data[24][4] = u'FECHA'
        data[25][3] = u'25'
        #data[25][4] =
        data[26][3] = u'26'
        #data[26][4] =
        data[27][3] = u'27'
        #data[27][4] =
        data[24][6] = u'28'
        data[24][7] = u'Monto'
        data[25][6] = u'29'
        #data[25][7] =
        data[26][6] = u'30'
        #data[26][7] =
        data[27][6] = u'31'
        #data[27][7] =
        data[28][0] = u'32'
        data[28][1] = u'Compensaciones con Créditos Adquiridos (Cesión)'
        data[29][0] = u'33'
        data[29][1] = u'Número de Resolución'
        data[30][0] = u'34'
        #data[30[1] =
        data[29][3] = u'35'
        data[29][4] = u'FECHA'
        data[30][3] = u'36'
        #data[30][4] =
        data[29][6] = u'37'
        data[29][7] = u'RIF Cedente'
        data[30][6] = u'38'
        #data[30][7] =
        data[29][9] = u'39'
        data[29][10] = u'Monto'
        data[30][9] = u'40'
        #data[30][10] =
        data[31][0] = u'41'
        data[31][1] = u'Total Compensación (29+30+31+40)'
        data[32][0] = u'42'
        data[32][1] = u'TOTAL A PAGAR (18-43)'
        data[31][9] = u'43'
        data[31][10] = pretty_number(declaracion.total_compensacion)
        data[32][3] = u'44'
        data[32][4] = pretty_number(declaracion.total_pagar)
        data[33][0] = Paragraph(u'''JURO QUE LOS DATOS CONTENIDOS EN ESTA DECLARACION HAN SIDO DETERMINADOS
                                CON BASE A LAS DISPOSICIONES LEGALES Y EXAMINADOS POR MI PERSONA:<br/>
                                LUGAR:<br/>
                                FECHA:<br/>
                                REPRESENTANTE LEGAL Nº RIF:<br/>
                                FIRMA DEL CONTRIBUYENTE O REPRESENTANTE LEGAL:<br/>''',
                                styles['Justify'])
        data[33][5] = Paragraph(u'''YO &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                                &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                                CON CEDULA DE IDENTIDAD Nº &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                                &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                                DECLARO QUE LOS DATOS Y CIFRAS QUE APARECEN EN LA PRESENTE DECLARACION
                                SON UNA COPIA FIEL Y EXACTA DE LOS DATOS CONTENIDOS EN LOS REGISTROS DE
                                CONTABILIDAD Y CONTROL TRIBUTARIO QUE HAN SIDO LLEVADOS CONFORME A LA LEY
                                EN CARACAS A LOS &nbsp; &nbsp; &nbsp; &nbsp; DIAS DEL MES DE<br/>
                                FIRMA:''',
                                styles['Justify'])

        h = [16 for i in xrange(33)]
        h.append(70)
        w = [40,90,50,40,50,50,40,40,50,40,50]
        t = Table(data, rowHeights=h, colWidths=w)

        t.setStyle(TableStyle([('GRID',(0,0),(-1,-1), 0.25, colors.black),
                               ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                               ('ALIGN', (1,12), (1,17), 'LEFT'),
                               ('ALIGN', (1,19), (1,21), 'LEFT'),
                               ('ALIGN', (0,11), (0,11), 'LEFT'),
                               ('ALIGN', (0,18), (0,18), 'LEFT'),
                               ('ALIGN', (1,23), (1,23), 'LEFT'),
                               ('ALIGN', (1,28), (1,28), 'LEFT'),
                               ('ALIGN', (1,31), (1,32), 'LEFT'),
                               ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                               ('VALIGN',(0,33),(-1,33),'TOP'),
                               ('FONTSIZE', (0,0),(-1,-1),9),
                               ('FACE',(0,2),(-1,2), 'Helvetica-Bold'),
                               ('FACE',(0,7),(5,7), 'Helvetica-Bold'),
                               ('FACE',(8,7),(-1,7), 'Helvetica-Bold'),
                               ('FACE',(4,8),(5,8), 'Helvetica-Bold'),
                               ('FACE',(1,17),(1,17), 'Helvetica-Bold'),
                               ('FACE',(1,20),(1,21), 'Helvetica-Bold'),
                               ('FACE',(1,31),(1,32), 'Helvetica-Bold'),
                               ('SPAN',(0,0),(-1,0)),
                               ('BACKGROUND',(0,0),(-1,0), colors.grey),
                               ('FACE',(0,0),(-1,0), 'Helvetica-Bold'),
                               ('SPAN',(0,1),(-1,1)),
                               ('SPAN',(0,4),(-1,4)),
                               ('SPAN',(0,5),(-1,5)),
                               ('BACKGROUND',(0,5),(-1,5), colors.grey),
                               ('FACE',(0,5),(-1,5), 'Helvetica-Bold'),
                               ('SPAN',(0,6),(-1,6)),
                               ('SPAN',(0,9),(-1,9)),
                               ('SPAN',(0,10),(-1,10)),
                               ('SPAN',(0,11),(-1,11)),
                               ('BACKGROUND',(0,9),(-1,11), colors.grey),
                               ('FACE',(0,9),(-1,11), 'Helvetica-Bold'),
                               ('SPAN',(0,18),(-1,18)),
                               ('BACKGROUND',(0,18),(-1,18), colors.grey),
                               ('FACE',(0,18),(-1,18), 'Helvetica-Bold'),
                               ('SPAN',(0,22),(-1,22)),
                               ('BACKGROUND',(0,22),(-1,22), colors.grey),
                               ('FACE',(0,22),(-1,22), 'Helvetica-Bold'),
                               ('SPAN',(0,2),(1,2)),
                               ('SPAN',(2,2),(6,2)),
                               ('SPAN',(8,2),(10,2)),
                               ('SPAN',(0,3),(1,3)),
                               ('SPAN',(2,3),(6,3)),
                               ('SPAN',(8,3),(10,3)),
                               ('SPAN',(0,7),(1,7)),
                               ('SPAN',(2,7),(3,7)),
                               ('SPAN',(4,7),(5,7)),
                               ('SPAN',(6,7),(7,7)),
                               ('SPAN',(8,7),(10,7)),
                               ('SPAN',(0,8),(1,8)),
                               ('SPAN',(2,8),(3,8)),
                               ('SPAN',(4,8),(5,8)),
                               ('SPAN',(6,8),(7,8)),
                               ('SPAN',(8,8),(10,8)),
                               ('SPAN',(1,12),(6,12)),
                               ('SPAN',(8,12),(10,12)),
                               ('SPAN',(1,13),(6,13)),
                               ('SPAN',(8,13),(10,13)),
                               ('SPAN',(1,14),(6,14)),
                               ('SPAN',(8,14),(10,14)),
                               ('SPAN',(1,15),(6,15)),
                               ('SPAN',(8,15),(10,15)),
                               ('SPAN',(1,16),(6,16)),
                               ('SPAN',(8,16),(10,16)),
                               ('SPAN',(1,17),(6,17)),
                               ('SPAN',(8,17),(10,17)),
                               ('SPAN',(1,19),(6,19)),
                               ('SPAN',(8,19),(10,19)),
                               ('SPAN',(1,20),(6,20)),
                               ('SPAN',(8,20),(10,20)),
                               ('SPAN',(1,21),(6,21)),
                               ('SPAN',(8,21),(10,21)),
                               ('SPAN',(1,23),(10,23)),
                               ('SPAN',(1,24),(2,24)),
                               ('SPAN',(1,25),(2,25)),
                               ('SPAN',(1,26),(2,26)),
                               ('SPAN',(1,27),(2,27)),
                               ('SPAN',(4,24),(5,24)),
                               ('SPAN',(4,25),(5,25)),
                               ('SPAN',(4,26),(5,26)),
                               ('SPAN',(4,27),(5,27)),
                               ('SPAN',(7,24),(10,24)),
                               ('SPAN',(7,25),(10,25)),
                               ('SPAN',(7,26),(10,26)),
                               ('SPAN',(7,27),(10,27)),
                               ('SPAN',(1,28),(10,28)),
                               ('SPAN',(1,29),(2,29)),
                               ('SPAN',(1,30),(2,30)),
                               ('SPAN',(4,29),(5,29)),
                               ('SPAN',(4,30),(5,30)),
                               ('SPAN',(7,29),(8,29)),
                               ('SPAN',(7,30),(8,30)),
                               ('SPAN',(1,31),(8,31)),
                               ('SPAN',(1,32),(2,32)),
                               ('SPAN',(4,32),(5,32)),
                               ('SPAN',(4,32),(10,32)),
                               ('SPAN',(0,33),(4,33)),
                               ('SPAN',(5,33),(10,33)),
                               ]))

        t.wrapOn(pdf, 200, 300)
        t.drawOn(pdf, 35, 690 - t._height)

        pdf.save()

        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        page1 = input.getPage(0)

        page1.mergePage(watermark.getPage(0))

        # add processed pdf page
        output.addPage(page1)
        # finally, write "output" to the response
        output.write(response)
        return response


# Helpers (Funciones) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calc_contribucion_especial_determinada(data):
    return get_decimal(data['total_ventas_menos_anticipo']) * Decimal('0.01')


def calc_total_ventas_menos_anticipo(data):
    result = get_decimal(data['total_ventas_territorial'])
    result -= get_decimal(
        data['anticipo_declaracion'].total_ventas_menos_anticipo
        if data['anticipo_declaracion'] else None
    )
    return result


def calc_total_pagar(data):
    result = get_decimal(data['contribucion_especial_determinada'])
    result -= get_decimal(data['total_compensacion'])
    return result


def calc_total_ventas_territorial(data):
    result = get_decimal(data['ventas_propias'])
    result += get_decimal(data['ventas_exportacion'])
    result += get_decimal(data['ventas_internas_general'])
    result += get_decimal(data['ventas_internas_adicional'])
    result += get_decimal(data['ventas_internas_reducida'])
    return result


def get_decimal(value):
    return value if value is not None else Decimal('0')


def pretty_number(value):
    if not value:
        return u'0,00'

    value = (
        value if not isinstance(value, Declaracion)
        else value.total_ventas_menos_anticipo
    )

    return locale.currency(
        float(unicode(value)), symbol=False, grouping=True
    )


def pretty_string(value):
    value = unicode(value)
    if value == u'None':
        return u''
    else:
        return value


def pretty_tipo(value):
    value = unicode(value).split(' ')
    if len(value) == 2:
        return value[-1]
    else:
        return ' '.join(value[-2:])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
