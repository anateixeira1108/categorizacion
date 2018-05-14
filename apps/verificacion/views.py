# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse
from django.http import QueryDict
from django.conf import settings
from django.views.generic import View
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.shortcuts import redirect

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from apps.verificacion.textos import NumToWord
from apps.actas.models import ActaDocumentos, ActaRequisito
from registro.models import Direccion
from apps.verificacion.models import FuncionariosVerificacion
from apps.verificacion import models as verificacion_models
from apps.cuentas.models import MinturUser
from django.contrib.auth.models import Group
from apps.verificacion.textos import text_providencia, gaceta, notificacion, label, text_requerimiento_abierta, pasivo, \
    supervisor_firma, funcionario_firma, text_recepcion_abierta, text_constancia
from utils import views_helpers as helpers
from utils.email import MailMan
# class view~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Pdf(View):
    def get(self, request, pk):
        documento = ActaDocumentos.objects.get(id=pk)
        id_tipo = documento.tipo.id
        func = TIPO_ACTA_FUNCS[id_tipo]
        response = func(documento)
        if not isinstance(response, HttpResponse):
            return redirect('funcionario_detalle_verificacion', pk=documento.verificacion_id)
        return response


# Ajax ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def concluir_verificacion_json(request):
    if request.method != 'PUT':
        helpers.json_response({
            'error': -1, 'msg': 'HTTP method not allow.'
        })

    request.PUT = QueryDict(request.body)

    if 'acta_id' not in request.PUT:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar el ID de la verificación a concluir.'
        })

    try:
        verificacion = verificacion_models.Verificacion.objects.get(
            pk=request.PUT['acta_id']
        )

    except verificacion_models.Verificacion.DoesNotExist:
        return helpers.json_response({
            'error': -3,
            'msg': u'No existe verificación alguna con el ID indicado.'
        })

    else:
        if verificacion.estatus == verificacion_models.CONCLUIDA:
            return helpers.json_response({
                'error': 1,
                'msg': u'La verificación en cuestión ya está concluida.'
            })

        verificacion.estatus = verificacion_models.CONCLUIDA
        verificacion.save()

        return helpers.json_response({'error': 0, 'result': u''})


def registrar_observaciones_json(request):
    if request.method != 'PUT':
        helpers.json_response({
            'error': -1, 'msg': 'HTTP method not allow.'
        })

    request.PUT = QueryDict(request.body)

    if 'acta_id' not in request.PUT:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar el ID de la verificación.'
        })

    if 'observaciones' not in request.PUT:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar las observaciones a registrar.'
        })

    if 'conclusiones' not in request.PUT:
        return helpers.json_response({
            'error': -2,
            'msg': u'Debe indicar las conclusiones a registrar.'
        })

    try:
        verificacion = verificacion_models.Verificacion.objects.get(
            pk=request.PUT['acta_id']
        )

    except verificacion_models.Verificacion.DoesNotExist:
        return helpers.json_response({
            'error': -3,
            'msg': u'No existe verificación alguna con el ID indicado.'
        })

    else:
        MailMan.verificacion_concluida(
            data_dict={
                'razon_social': verificacion.pst.razon_social,
                'periodo_desde': verificacion.desde,
                'periodo_hasta': verificacion.hasta,
                'observaciones': request.PUT['observaciones'],
            },
            receptor_email=verificacion.pst.user.correo_electronico
        )

        verificacion.conclusiones = request.PUT['conclusiones']
        verificacion.observaciones = request.PUT['observaciones']
        verificacion.save()

        return helpers.json_response({'error': 0, 'result': u''})


# helpers~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def documento_info(documento):
    gerente = MinturUser.objects.get(groups=Group.objects.get(name='gerente_dggt'))
    try:
        domicilio = Direccion.objects.get(pst=documento.pst.id)
    except:
        domicilio = ''
    funcionarios_ids = FuncionariosVerificacion.objects.filter(verificacion=documento.verificacion.id)
    funcionarios = []
    apoyo = []
    for funcionario in funcionarios_ids:
        if funcionario.es_coordinador:
            supervisor = MinturUser.objects.get(id=funcionario.funcionario.id)
        elif funcionario.es_apoyo:
            apoyo.append(MinturUser.objects.get(id=funcionario.funcionario.id))
        else:
            funcionarios.append(MinturUser.objects.get(id=funcionario.funcionario.id))
    return domicilio, gerente, supervisor, funcionarios, apoyo


# specific prints~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def providencia(documento):
    mes_letras = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }

    def text_to_bold(text):
        return u'''<b><font size=12>{}</font></b> <br/>'''.format(text)

    def print_text_bold(text, x, y, pdf):
        p = ParagraphStyle('test')
        p.textColor = 'black'
        p.alignment = TA_LEFT
        p.fontSize = 8
        p.leading = 9
        para = Paragraph(text_to_bold(unicode(text)), p)
        para.wrapOn(pdf, 300, 50)
        para.drawOn(pdf, x, y)

    def get_fecha():
        from datetime import date

        d = date.today()
        fecha = "Caracas, {dia_letra} ({dia}) de {mes} de {anyo}".format(
            dia_letra=NumToWord.get_month_words(d.day),
            dia=str(d.day),
            mes=mes_letras[d.month],
            anyo=str(d.year)
        )
        return fecha

    domicilio, gerente, supervisor, funcionarios, apoyo = documento_info(documento)

    texto = text_providencia(supervisor, funcionarios, apoyo)

    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_JUSTIFY
    p.fontSize = 10
    p.leading = 12
    para = Paragraph(text_to_bold(unicode(domicilio)), p)
    para_texto = Paragraph(unicode(texto), p)

    output = PdfFileWriter()
    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'PROVIDENCIA.pdf'), 'rb'))
    # create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Verificacion_Providencia.pdf'

    fecha = get_fecha()
    # get number of pages
    num_pages = input.getNumPages()

    for page in xrange(num_pages - 1):
        new_page = False
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        print_text_bold(unicode(documento.pst.razon_social), 220, 768 + 2, pdf)
        print_text_bold(unicode(documento.pst.rif), 220, 750 + 2, pdf)
        # pdf.drawString(220, 768, unicode(documento.pst.razon_social))
        # pdf.drawString(220, 750, unicode(documento.pst.rif))
        if documento.pst.rtn != None:
            rtn = unicode(documento.pst.rtn)
            # pdf.drawString(220, 735, unicode(documento.pst.rtn))
        else:
            rtn = u'S/RTN'
            # pdf.drawString(220, 735, u'S/RTN')

        print_text_bold(rtn, 220, 735 + 2, pdf)
        print_text_bold(unicode(documento.codigo), 80, 835, pdf)
        print_text_bold(fecha, 295, 835, pdf)
        # pdf.drawString(80, 835, unicode(documento.codigo))

        para.wrapOn(pdf, 300, 50)
        para.drawOn(pdf, 220, 695)

        para_texto.wrapOn(pdf, 450, 300)
        para_texto.drawOn(pdf, 80, 675 - para_texto.height)

        if 675 - para_texto.height > 230:
            gaceta_end = gaceta(pdf, 675 - para_texto.height, gerente)
            notificacion(pdf, gaceta_end)
            label(pdf, gaceta_end, page)
        else:
            new_page = True

        pdf.save()
        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        tmp = input.getPage(page)

        tmp.mergePage(watermark.getPage(0))
        buffer.seek(0)

        # add processed pdf page
        output.addPage(tmp)
        if new_page:
            buffer = StringIO()  # create string buffer for PDF
            pdf = canvas.Canvas(buffer, pagesize=letter)

            gaceta_end = gaceta(pdf, 800, gerente)
            notificacion(pdf, gaceta_end)
            label(pdf, gaceta_end, page)

            pdf.save()

            # put on watermark from buffer
            watermark = PdfFileReader(buffer)
            input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'PROVIDENCIA.pdf'), 'rb'))
            tmp = input.getPage(3)

            tmp.mergePage(watermark.getPage(0))
            buffer.seek(0)

            # add processed pdf page
            output.addPage(tmp)

    output.write(response)
    return response


def requerimiento_abierta(documento, cerrada=False):
    new_page = False
    domicilio, gerente, supervisor, funcionarios, apoyo = documento_info(documento)

    texto = text_requerimiento_abierta(documento, supervisor, funcionarios)

    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_JUSTIFY
    p.fontSize = 10
    p.leading = 12
    para = Paragraph(unicode(domicilio), p)
    para_texto = Paragraph(unicode(texto), p)

    output = PdfFileWriter()
    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'REQUERIMIENTO_ABIERTA.pdf'), 'rb'))
    # create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Verificacion_Acta_Requerimientos_abierta.pdf'

    # get number of pages
    num_pages = input.getNumPages()

    buffer = StringIO()  # create string buffer for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(220, 800, unicode(documento.pst.razon_social))
    pdf.drawString(220, 788, unicode(documento.pst.rif))
    if documento.pst.rtn != None:
        pdf.drawString(220, 775, unicode(documento.pst.rtn))
    else:
        pdf.drawString(220, 775, u'S/RTN')
    pdf.drawString(80, 855, unicode(documento.codigo))

    para.wrapOn(pdf, 300, 50)
    para.drawOn(pdf, 220, 770 - para.height)

    para_texto.wrapOn(pdf, 450, 300)
    para_texto.drawOn(pdf, 80, 730 - para_texto.height)

    pasivo(pdf, 730 - para_texto.height)
    supervisor_end = supervisor_firma(pdf, 730 - para_texto.height, supervisor)
    for funcionario in xrange(len(funcionarios)):
        supervisor_end = funcionario_firma(pdf, supervisor_end, funcionarios[funcionario])
        if supervisor_end <= 114 and funcionario != len(funcionarios) - 1:
            new_page = True
            start_funcionario = funcionario + 1
            break

    pdf.save()
    # put on watermark from buffer
    watermark = PdfFileReader(buffer)
    tmp = input.getPage(0)

    tmp.mergePage(watermark.getPage(0))
    buffer.seek(0)

    # add processed pdf page
    output.addPage(tmp)
    if new_page:
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        supervisor_end = 850
        for funcionario in xrange(start_funcionario, len(funcionarios)):
            supervisor_end = funcionario_firma(pdf, supervisor_end, funcionarios[funcionario])

        pdf.save()

        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'PROVIDENCIA.pdf'), 'rb'))
        tmp = input.getPage(3)

        tmp.mergePage(watermark.getPage(0))
        buffer.seek(0)

        # add processed pdf page
        output.addPage(tmp)

    if cerrada:
        return output, response

    output.write(response)
    return response


def requerimiento_cerrada(documento):
    output, response = requerimiento_abierta(documento, cerrada=True)

    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'CERRADA.pdf'), 'rb'))
    response['Content-Disposition'] = 'attachment; filename=Verificacion_Acta_Requerimientos_cerrada.pdf'

    buffer = StringIO()  # create string buffer for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)

    data = [['REQUISITO']]

    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_JUSTIFY
    p.fontSize = 10
    p.leading = 12

    requisitos = ActaRequisito.objects.filter(acta=documento.id)
    i = 1
    for requisito in requisitos:
        data.append([Paragraph(u'{}.- {}'.format(str(i), unicode(requisito.requisito)), p)])
        i += 1

    t = Table(data, colWidths=(450))
    t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BACKGROUND', (0, 0), (0, 0), colors.gray),
                           ('ALIGN', (0, 0), (0, 0), 'CENTER')
    ]))

    t.wrapOn(pdf, 200, 300)
    t.drawOn(pdf, 80, 870 - t._height)

    pdf.save()
    # put on watermark from buffer
    watermark = PdfFileReader(buffer)
    tmp = input.getPage(0)

    tmp.mergePage(watermark.getPage(0))
    buffer.seek(0)

    # add processed pdf page
    output.addPage(tmp)

    output.write(response)
    return response


def recepcion_abierta(documento, cerrada=False):
    new_page = False
    domicilio, gerente, supervisor, funcionarios, apoyo = documento_info(documento)

    texto = text_recepcion_abierta(documento, supervisor, funcionarios)

    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_JUSTIFY
    p.fontSize = 10
    p.leading = 12
    para = Paragraph(unicode(domicilio), p)
    para_texto = Paragraph(unicode(texto), p)

    output = PdfFileWriter()
    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'RECEPCION_ABIERTA.pdf'), 'rb'))
    # create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Verificacion_Acta_Recepcion_abierta.pdf'

    # get number of pages
    num_pages = input.getNumPages()

    buffer = StringIO()  # create string buffer for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(220, 793, unicode(documento.pst.razon_social))
    pdf.drawString(220, 777, unicode(documento.pst.rif))
    if documento.pst.rtn != None:
        pdf.drawString(220, 763, unicode(documento.pst.rtn))
    else:
        pdf.drawString(220, 763, u'S/RTN')
    pdf.drawString(80, 850, unicode(documento.codigo))

    para.wrapOn(pdf, 300, 50)
    para.drawOn(pdf, 220, 756 - para.height)

    para_texto.wrapOn(pdf, 450, 300)
    para_texto.drawOn(pdf, 80, 730 - para_texto.height)

    pasivo(pdf, 730 - para_texto.height)
    supervisor_end = supervisor_firma(pdf, 730 - para_texto.height, supervisor)
    for funcionario in xrange(len(funcionarios)):
        supervisor_end = funcionario_firma(pdf, supervisor_end, funcionarios[funcionario])
        if supervisor_end <= 114 and funcionario != len(funcionarios) - 1:
            new_page = True
            start_funcionario = funcionario + 1
            break

    pdf.save()
    # put on watermark from buffer
    watermark = PdfFileReader(buffer)
    tmp = input.getPage(0)

    tmp.mergePage(watermark.getPage(0))
    buffer.seek(0)

    # add processed pdf page
    output.addPage(tmp)
    if new_page:
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        supervisor_end = 850
        for funcionario in xrange(start_funcionario, len(funcionarios)):
            supervisor_end = funcionario_firma(pdf, supervisor_end, funcionarios[funcionario])

        pdf.save()

        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'PROVIDENCIA.pdf'), 'rb'))
        tmp = input.getPage(3)

        tmp.mergePage(watermark.getPage(0))
        buffer.seek(0)

        # add processed pdf page
        output.addPage(tmp)

    if cerrada:
        return output, response

    output.write(response)
    return response


def recepcion_cerrada(documento):
    output, response = recepcion_abierta(documento, cerrada=True)

    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'CERRADA.pdf'), 'rb'))
    response['Content-Disposition'] = 'attachment; filename=Verificacion_Acta_Recepcion_cerrada.pdf'

    buffer = StringIO()  # create string buffer for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)

    data = [['Entrego', 'REQUISITO']]

    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_JUSTIFY
    p.fontSize = 10
    p.leading = 12

    requisitos = ActaRequisito.objects.filter(acta=documento.id)
    i = 1
    for requisito in requisitos:
        if requisito.entrego:
            check = u'\u2713'
        else:
            check = u'\u2715'
        data.append([check, Paragraph(u'{}.- {}'.format(str(i), unicode(requisito.requisito)), p)])
        i += 1

    t = Table(data, colWidths=(None, 400))
    t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                           ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                           ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (0, -1), 'MIDDLE')
    ]))

    t.wrapOn(pdf, 200, 300)
    t.drawOn(pdf, 80, 870 - t._height)

    pdf.save()
    # put on watermark from buffer
    watermark = PdfFileReader(buffer)
    tmp = input.getPage(0)

    tmp.mergePage(watermark.getPage(0))
    buffer.seek(0)

    # add processed pdf page
    output.addPage(tmp)

    output.write(response)
    return response


def constancia(documento):
    new_page = False
    domicilio, gerente, supervisor, funcionarios, apoyo = documento_info(documento)

    texto = text_constancia(documento, supervisor, funcionarios)

    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_JUSTIFY
    p.fontSize = 10
    p.leading = 12
    if domicilio:
        para = Paragraph(unicode(domicilio), p)
    else:
        para = Paragraph(unicode("No tiene registro de domicilio"), p)
    para_texto = Paragraph(unicode(texto), p)

    output = PdfFileWriter()
    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'CONSTANCIA.pdf'), 'rb'))
    # create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Verificacion_Constancia.pdf'

    # get number of pages
    num_pages = input.getNumPages()

    buffer = StringIO()  # create string buffer for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(220, 793, unicode(documento.pst.razon_social))
    pdf.drawString(220, 779, unicode(documento.pst.rif))
    if documento.pst.rtn != None:
        pdf.drawString(220, 766, unicode(documento.pst.rtn))
    else:
        pdf.drawString(220, 766, u'S/RTN')
    pdf.drawString(80, 850, unicode(documento.codigo))

    para.wrapOn(pdf, 300, 50)
    para.drawOn(pdf, 220, 762 - para.height)

    para_texto.wrapOn(pdf, 450, 300)
    para_texto.drawOn(pdf, 80, 730 - para_texto.height)

    pasivo(pdf, 730 - para_texto.height)
    supervisor_end = supervisor_firma(pdf, 730 - para_texto.height, supervisor)
    for funcionario in xrange(len(funcionarios)):
        supervisor_end = funcionario_firma(pdf, supervisor_end, funcionarios[funcionario])
        if supervisor_end <= 114 and funcionario != len(funcionarios) - 1:
            new_page = True
            start_funcionario = funcionario + 1
            break

    pdf.save()
    # put on watermark from buffer
    watermark = PdfFileReader(buffer)
    tmp = input.getPage(0)

    tmp.mergePage(watermark.getPage(0))
    buffer.seek(0)

    # add processed pdf page
    output.addPage(tmp)
    if new_page:
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        supervisor_end = 850
        for funcionario in xrange(start_funcionario, len(funcionarios)):
            supervisor_end = funcionario_firma(pdf, supervisor_end, funcionarios[funcionario])

        pdf.save()

        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'verificacion', 'PROVIDENCIA.pdf'), 'rb'))
        tmp = input.getPage(3)

        tmp.mergePage(watermark.getPage(0))
        buffer.seek(0)

        # add processed pdf page
        output.addPage(tmp)

    output.write(response)
    return response


def cedula_hallazgo(documento):
    domicilio, gerente, supervisor, funcionarios, apoyo = documento_info(documento)

    output = PdfFileWriter()
    # create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Cedula_de_Hallazgo.pdf'

    buffer = StringIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=50, bottomMargin=100)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=8))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=8))

    Story = []

    I = Image(os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png'))
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    data = [[I, '', '', '', '', ''],
            ['SUJETO PASIVO:', '', '', '', '', ''],
            ['MATERIA:', '', '', '', '', '']
    ]
    data[0][2] = Paragraph(u'''<b>CEDULA DE HALLAZGOS<br/>
                            Contribución Especial del 1% por la Presentación de<br/>
                            Servicios Turísticos</b>''', styles["Center"])
    data[0][4] = documento.codigo
    data[1][1] = documento.pst.nombre_o_razon()
    data[1][3] = 'RIF: ' + documento.pst.rif
    data[2][1] = documento.hallazgos_materia
    data[2][3] = 'PERIODO: ' + documento.fecha_notificacion.strftime("%d/%m/%Y")
    w = [80, 30, 90, 90, 80, 80]
    Story.append(Table(data, colWidths=w,
                       style=[('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                              ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                              ('FONTSIZE', (0, 0), (-1, -1), 8),
                              ('SPAN', (0, 0), (1, 0)),
                              ('SPAN', (2, 0), (3, 0)),
                              ('SPAN', (4, 0), (5, 0)),
                              ('SPAN', (1, 1), (2, 1)),
                              ('SPAN', (1, 2), (2, 2)),
                              ('SPAN', (3, 1), (5, 1)),
                              ('SPAN', (3, 2), (5, 2))]))
    Story.append(Spacer(1, 12))

    data = [['CONDICIÓN', 'CRITERIO', 'EFECTO', 'EVIDENCIA'],
            ['', '', '', ''],
            ['', '', '', '']
    ]
    try:
        data[2][0] = Paragraph(documento.hallazgos_condicion, styles["Justify"])
        data[2][1] = Paragraph(documento.hallazgos_criterio, styles["Justify"])
        data[2][2] = Paragraph(documento.hallazgos_efecto, styles["Justify"])
        data[2][3] = Paragraph(documento.hallazgos_evidencia, styles["Justify"])
    except:
        pass
    Story.append(Table(data, colWidths=[95, 170, 81, 105],
                       style=[('GRID', (0, 0), (-1, 0), 0.25, colors.black),
                              ('GRID', (0, 2), (-1, 2), 0.25, colors.black),
                              ('FONTSIZE', (0, 0), (-1, -1), 8),
                              ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                              ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('VALIGN', (0, 2), (-1, 2), 'TOP'), ]))
    Story.append(Spacer(1, 12))

    ptext = 'Observaciones: <u>%s</u>' % documento.observaciones
    Story.append(Paragraph(ptext, styles['Normal']))
    Story.append(Spacer(1, 12))

    Story.append(Paragraph('Fiscal Actuante: %s' % gerente.get_full_name(), styles['Normal']))
    Story.append(Paragraph('Supervisor: %s' % supervisor.get_full_name(), styles['Normal']))

    doc.build(Story)

    watermark = PdfFileReader(buffer)
    output.addPage(watermark.getPage(0))
    output.write(response)
    return response


def informe_fiscal(documento):
    pass


def conformidad(documento):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TIPO_ACTA_FUNCS = ['ACTAS',
                   providencia,
                   requerimiento_abierta,
                   requerimiento_cerrada,
                   recepcion_abierta,
                   recepcion_cerrada,
                   constancia,
                   cedula_hallazgo,
                   informe_fiscal,
                   conformidad
]
