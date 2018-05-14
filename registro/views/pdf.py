# -*- coding: utf-8 -*-
u''' Vistas para impresion de PDFs. '''

# Modulos --------------------------------------------------------
import os
import datetime
from datetime import date

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from PyPDF2 import PdfFileWriter, PdfFileReader


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from utils.report import BuildReport
from natural import Paso5View
from juridica import Paso9View

from registro import models
# ---------------------------------------------------------------------

PST_AGENTE = u'Agente Turístico'

PST_CONDUCTOR = u'Conductor Turístico'

PST_GUIA = u'Guía Turístico'

PAGINATOR = ['UNO (1)', 'DOS (2)', 'TRES (3)', 'CUATRO (4)', 'CINCO (5)', 'SEIS (6)', 'SIETE (7)', 'OCHO (8)',
             'NUEVE (9)', 'DIEZ (10)',
             'ONCE (11)', 'DOCE (12)', 'TRECE (13)', 'CATORCE (14)', 'QUINCE (15)',
             'DIEZ Y SEIS (16)', 'DIEZ Y SIETE (17)', 'DIEZ Y OCHO (18)', 'DIEZ Y NUEVE (19)', 'VEINTE (20)',
             'VEINTE Y UNO (21)', 'VEINTE Y DOS (22)', 'VEINTE Y TRES (23)', 'VEINTE Y CUATRO (24)',
             'VEINTE Y CINCO (25)',
             'VEINTE Y SEIS (26)', 'VEINTE Y SIETE (27)', 'VEINTE Y OCHO (28)', 'VEINTE Y NUEVE (29)', 'TREINTA (30)',
             'TREINTA Y UNO (31)', 'TREINTA Y DOS (32)', 'TREINTA Y TRES (33)', 'TREINTA Y CUATRO (35)',
             'TREINTA Y CINCO (35)',
             'TREINTA Y SEIS (36)', 'TREINTA Y SIETE (37)', 'TREINTA Y OCHO (38)', 'TREINTA Y NUEVE (39)',
             'CUARENTA (40)',
             'CUARENTA Y UNO (41)', 'CUARENTA Y DOS (42)', 'CUARENTA Y TRES (43)', 'CUARENTA Y CUATRO (44)',
             'CUARENTA Y CINCO (45)',
             'CUARENTA Y SEIS (46)', 'CUARENTA Y SIETE (47)', 'CUARENTA Y OCHO (48)', 'CUARENTA Y NUEVA (49)',
             'CINCUENTA (50)',
             'CINCUENTA Y UNO (51)', 'CINCUENTA Y DOS (52)', 'CINCUENTA Y TRES (53)', 'CINCUENTA Y CUATRO (54)',
             'CINCUENTA Y CINCO (55)',
             'CINCUENTA Y SEIS (56)', 'CINCUENTA Y SIETE (57)', 'CINCUENTA Y OCHO (58)', 'CINCUENTA Y NUEVE (59)',
             'SESENTA (60)',
             'SESENTA Y UNO (61)', 'SESENTA Y DOS (62)', 'SESENTA Y TRES (63)', 'SESENTA Y CUATRO (64)',
             'SESENTA Y CINCO (65)',
             'SESENTA Y SEIS (66)', 'SESENTA Y SIETE (67)', 'SESENTA Y OCHO (68)', 'SESENTA Y NUEVE (69)',
             'SETENTA (70)',
             'SETENTA Y UNO (71)', 'SETENTA Y DOS (72)', 'SETENTA Y TRES (73)', 'SETENTA Y CUATRO (74)',
             'SETENTA Y CINCO (75)',
             'SETENTA Y SEIS (76)', 'SETENTA Y SIETE (77)', 'SETENTA Y OCHO (78)', 'SETENTA Y NUEVE (79)',
             'OCHENTA (80)',
             'OCHENTA Y UNO (81)', 'OCHENTA Y DOS (82)', 'OCHENTA Y TRES (83)', 'OCHENTA Y CUATRO (84)',
             'OCHENTA Y CINCO (85)',
             'OCHENTA Y SEIS (86)', 'OCHENTA Y SIETE (87)', 'OCHENTA Y OCHO (88)', 'OCHENTA Y NUEVE (89)',
             'NOVENTA (90)',
             'NOVENTA Y UNO (91)', 'NOVENTA Y DOS (92)', 'NOVENTA Y TRES (93)', 'NOVENTA Y CUATRO (94)',
             'NOVENTA Y CINCO (95)',
             'NOVENTA Y SEIS (96)', 'NOVENTA Y SIETE (97)', 'NOVENTA Y OCHO (98)', 'NOVENTA Y NUEVE (99)', 'CIEN (100)']
# HELPERS ----------------------------------------------------------------------------------------------------------------

def pager(output, input, pagina_numero):
    buffer = StringIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.rotate(90)
    pdf.drawString(650, -580, PAGINATOR[pagina_numero])
    pdf.save()
    watermark = PdfFileReader(buffer)
    page = input
    page.mergePage(watermark.getPage(0))
    output.addPage(page)
    pagina_numero += 1
    return output, pagina_numero


def base(context, pdf_file, funcionario=False):
    output = PdfFileWriter()
    input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, pdf_file), 'rb'))
    pagina_numero = 0
    # create response object
    response = HttpResponse(content_type='application/pdf')
    if funcionario:
        response['Content-Disposition'] = 'attachment; filename=expediente_natural.pdf'
    else:
        response['Content-Disposition'] = 'attachment; filename=registro_natural.pdf'

    # get number of pages
    num_pages = input.getNumPages()

    if not funcionario:
        # fill first page
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.drawString(450, 659, date.today().strftime("%d/%m/%Y"))
        pdf.drawString(41, 559, u'{nombres} {apellidos}'.format(nombres=unicode(context['pst'].nombres),
                                                                apellidos=unicode(context['pst'].apellidos)))
        pdf.drawString(41, 525, u'{rif} / {ci}'.format(rif=unicode(context['pst'].rif),
                                                       ci=unicode(context['pst'].cedula)))
        pdf.save()
        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        page1 = input.getPage(0)

        page1.mergePage(watermark.getPage(0))
        buffer.seek(0)

        # add processed pdf page
        output.addPage(page1)

    # paginas Copia de la Cedula de Identidad
    output, pagina_numero = pager(output, input.getPage(1), pagina_numero)
    try:
        ci = PdfFileReader(file(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_cedula)), 'rb'))
        output, pagina_numero = pager(output, ci.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(2), pagina_numero)
    # paginas RIF
    output, pagina_numero = pager(output, input.getPage(3), pagina_numero)
    try:
        rif = PdfFileReader(file(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_rif)), 'rb'))
        output, pagina_numero = pager(output, rif.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(4), pagina_numero)
    # paginas Recibo de Servicio
    output, pagina_numero = pager(output, input.getPage(5), pagina_numero)
    servicio_file_format = unicode(context['pst'].archivo_servicio).split('.')[-1]
    try:
        if servicio_file_format in ['pdf', 'PDF']:
            servicio = PdfFileReader(
                file(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_servicio)), 'rb'))
            output, pagina_numero = pager(output, servicio.getPage(0), pagina_numero)
        else:
            buffer2 = StringIO()
            servicio = canvas.Canvas(buffer2, pagesize=letter)
            w = 500
            h = 700
            servicio.drawImage(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_servicio)),
                               letter[0] / 2 - w / 2, letter[1] / 2 - h / 2, width=w, height=h, mask='auto')
            servicio.save()
            watermark = PdfFileReader(buffer2)
            page6 = input.getPage(6)
            page6.mergePage(watermark.getPage(0))
            output, pagina_numero = pager(output, page6, pagina_numero)
            buffer2.seek(0)
    except:
        output, pagina_numero = pager(output, input.getPage(6), pagina_numero)
    # paginas Foto tipo Carnet
    output, pagina_numero = pager(output, input.getPage(7), pagina_numero)
    buffer3 = StringIO()
    foto = canvas.Canvas(buffer3, pagesize=letter)
    w = 120
    h = 160
    foto.drawImage(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_pasaporte)),
                   letter[0] / 2 - w / 2, letter[1] / 2 - h / 2, width=w, height=h, mask='auto')
    foto.save()
    watermark = PdfFileReader(buffer3)
    page8 = input.getPage(8)
    page8.mergePage(watermark.getPage(0))
    output, pagina_numero = pager(output, page8, pagina_numero)

    return response, input, output, pagina_numero


def response_juridica(context, funcionario=False):
    output = PdfFileWriter()
    if len(context['modificaciones']) == 0:
        input = PdfFileReader(
            file(os.path.join(settings.PDF_ROOT, 'ACTA_CONSIGNACION_JURIDICA_SIN_MODIFICACIONES.pdf'), 'rb'))
    else:
        input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'ACTA_CONSIGNACION_JURIDICA.pdf'), 'rb'))
    pagina_numero = 0

    # create response object
    response = HttpResponse(content_type='application/pdf')
    if funcionario:
        response['Content-Disposition'] = 'attachment; filename=expediente_juridica.pdf'
    else:
        response['Content-Disposition'] = 'attachment; filename=registro_juridica.pdf'

    # get number of pages
    num_pages = input.getNumPages()

    if not funcionario:
        # fill first page
        buffer = StringIO()  # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)

        pdf.drawString(450, 659, date.today().strftime("%d/%m/%Y"))
        pdf.drawString(41, 559, u'{rs}'.format(rs=unicode(context['pst'].razon_social)))
        pdf.drawString(41, 525, unicode(context['pst'].rif))
        pdf.save()

        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        page1 = input.getPage(0)

        page1.mergePage(watermark.getPage(0))
        buffer.seek(0)

        # add processed pdf page
        output.addPage(page1)

    # Fotocopia de la cedula de identidad del representante legal de la empresa.
    output, pagina_numero = pager(output, input.getPage(1), pagina_numero)
    try:
        representante_ci = PdfFileReader(
            file(os.path.join(settings.MEDIA_ROOT, unicode(context['representante'].archivo_cedula)), 'rb'))
        output, pagina_numero = pager(output, representante_ci.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(2), pagina_numero)

    # Fotocopia de la cedula de identidad de todos los accionistas de la empresa.
    output, pagina_numero = pager(output, input.getPage(3), pagina_numero)
    try:
        for accionista in context['accionistas']:
            accionista_ci = PdfFileReader(
                file(os.path.join(settings.MEDIA_ROOT, unicode(accionista.archivo_cedula)), 'rb'))
            output, pagina_numero = pager(output, accionista_ci.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(4), pagina_numero)

    # Fotocopia de la cedula de identidad de todos los accionistas de la empresa.
    output, pagina_numero = pager(output, input.getPage(5), pagina_numero)
    try:
        for accionista in context['accionistas']:
            accionista_rif = PdfFileReader(
                file(os.path.join(settings.MEDIA_ROOT, unicode(accionista.archivo_rif)), 'rb'))
            output, pagina_numero = pager(output, accionista_rif.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(6), pagina_numero)

    # Listado de Accionistas.
    output, pagina_numero = pager(output, input.getPage(7), pagina_numero)
    buffer2 = StringIO()
    lista = canvas.Canvas(buffer2, pagesize=letter)
    n = 1
    if context['accionistas']:
        for accionista in context['accionistas']:
            lista.drawString(41, 600 - 10 * n,
                             u'{}.- {nombres} {apellidos}'.format(n, nombres=unicode(accionista.nombres),
                                                                  apellidos=unicode(accionista.apellidos)))
            n += 1
        lista.save()
        watermark = PdfFileReader(buffer2)
        page8 = input.getPage(8)
        page8.mergePage(watermark.getPage(0))
        output, pagina_numero = pager(output, page8, pagina_numero)
    else:
        output, pagina_numero = pager(output, input.getPage(8), pagina_numero)

    # Fotocopia del Acta Constitutiva y Estatutos Sociales.
    output, pagina_numero = pager(output, input.getPage(9), pagina_numero)
    try:
        acta = PdfFileReader(
            file(os.path.join(settings.MEDIA_ROOT, unicode(context['acta'].archivo_acta_constitutiva)), 'rb'))
        num_pages = acta.getNumPages()
        for pagina_acta in xrange(num_pages):
            output, pagina_numero = pager(output, acta.getPage(pagina_acta), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(10), pagina_numero)

    # Fotocopia de las Modificaciones del Acta Constitutiva y Estatutos Sociales.
    if len(context['modificaciones']) != 0:
        output, pagina_numero = pager(output, input.getPage(11), pagina_numero)
        for modificacion_acta in context['modificaciones']:
            acta = PdfFileReader(
                file(os.path.join(settings.MEDIA_ROOT, unicode(modificacion_acta.archivo_acta_constitutiva)), 'rb'))
            num_pages = acta.getNumPages()
            for pagina_acta in xrange(num_pages):
                output, pagina_numero = pager(output, acta.getPage(pagina_acta), pagina_numero)

    # Fotocopia del Registro Unico de Informacion Fiscal (RIF).
    output, pagina_numero = pager(output, input.getPage(13), pagina_numero)
    try:
        rif = PdfFileReader(file(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_rif)), 'rb'))
        output, pagina_numero = pager(output, rif.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(14), pagina_numero)

    # Acta de SUNACOOP
    # output, pagina_numero = pager(output, input.getPage(13), pagina_numero)
    # try:
    #     rif = PdfFileReader(file(os.path.join(settings.MEDIA_ROOT, unicode(context['pst'].archivo_rif)), 'rb'))
    #     output, pagina_numero = pager(output, rif.getPage(0), pagina_numero)
    # except:
    #     output, pagina_numero = pager(output, input.getPage(14), pagina_numero)

    # finally, write "output" to the response
    output.write(response)
    return response


# Funciones por TIPO PST ------------------------------------------------------
def guia(context, funcionario=False):
    response, input, output, page_number = base(
        context, 'ACTA_CONSIGNACION_NATURAL_GUIA.pdf', funcionario=funcionario
    )

    # Certificado de guía especializado
    output, page_number = pager(output, input.getPage(9), page_number)

    try:
        pdf_reader = PdfFileReader(
            os.path.join(
                settings.MEDIA_ROOT,
                unicode(context['datos_especificos'].get(
                    u'Certificado de guía especializado'
                ))
            ),
            'rb'
        )

        for current_page in xrange(pdf_reader.getNumPages()):
            output, page_number = pager(
                output,
                pdf_reader.getPage(current_page),
                page_number
            )
    except:
        output, page_number = pager(output, input.getPage(10), page_number)


    # Constancia de primeros auxilios
    output, page_number = pager(output, input.getPage(11), page_number)

    try:
        pdf_reader = PdfFileReader(
            os.path.join(
                settings.MEDIA_ROOT,
                unicode(context['datos_especificos'].get(
                    u'Primeros auxilios (Constancia)'
                ))
            ),
            'rb'
        )

        for current_page in xrange(pdf_reader.getNumPages()):
            output, page_number = pager(
                output,
                pdf_reader.getPage(current_page),
                page_number
            )
    except:
        output, page_number = pager(output, input.getPage(12), page_number)

    # finally, write "output" to the response
    output.write(response)
    return response


def agente(context, funcionario=False):
    response, input, output, pagina_numero = base(context, 'ACTA_CONSIGNACION_NATURAL_AGENTE.pdf',
                                                  funcionario=funcionario)
    # paginas Curriculum Vitae
    output, pagina_numero = pager(output, input.getPage(9), pagina_numero)
    try:
        cv = PdfFileReader(
            file(os.path.join(settings.MEDIA_ROOT, unicode(context['datos_especificos'][u'Currículum Vitae'])), 'rb'))
        num_pages = cv.getNumPages()
        for pagina_cv in xrange(num_pages):
            output, pagina_numero = pager(output, cv.getPage(pagina_cv), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(10), pagina_numero)

    # finally, write "output" to the response
    output.write(response)
    return response


def conductor(context, funcionario=False):
    response, input, output, pagina_numero = base(context, 'ACTA_CONSIGNACION_NATURAL_CONDUCTOR.pdf',
                                                  funcionario=funcionario)
    # paginas Copia de la licencia de conducir
    output, pagina_numero = pager(output, input.getPage(9), pagina_numero)
    try:
        licencia = PdfFileReader(file(os.path.join(settings.MEDIA_ROOT, unicode(
            context['datos_especificos'][u'Copia de la licencia de conducir'])), 'rb'))
        output, pagina_numero = pager(output, licencia.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(10), pagina_numero)
    # paginas Copia del certificado médico
    output, pagina_numero = pager(output, input.getPage(11), pagina_numero)
    try:
        certificado_medico = PdfFileReader(file(
            os.path.join(settings.MEDIA_ROOT, unicode(context['datos_especificos'][u'Copia del certificado médico'])),
            'rb'))
        output, pagina_numero = pager(output, certificado_medico.getPage(0), pagina_numero)
    except:
        output, pagina_numero = pager(output, input.getPage(12), pagina_numero)

    # finally, write "output" to the response
    output.write(response)
    return response


TIPO_PST = {PST_GUIA: guia,
            PST_AGENTE: agente,
            PST_CONDUCTOR: conductor}
# Clases -----------------------------------------------------------------------------------------------------------
class Natural(View):
    def get(self, request):
        context = Paso5View.as_view()(self.request).context_data

        actividad_principal = models.ActividadComercial.objects.get(
            pst=context['pst'],
            tipo_actividad=models.ACTIVIDAD_PRINCIPAL,
            cached=True
        )

        return TIPO_PST[actividad_principal.actividad.nombre](context)


class Juridica(View):
    def get(self, request):
        context = Paso9View.as_view()(self.request).context_data
        response = response_juridica(context)
        return response


class RIFTUR(View):
    def get(self, request, **kwargs):
        pst = models.Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        rtn = models.CertificacionRIFTUR.objects.get(pst=pst)
        direccion = models.Direccion.objects.get(pst=pst)

        numero_comprobante = rtn.numero_comprobante
        fecha_registro = pst.creado_el.strftime('%x')
        fecha_certificacion = rtn.fecha_certificacion.strftime('%x')
        anio_vencimiento = (rtn.fecha_certificacion + datetime.timedelta(days=(3 * 365.24))).strftime('%x')
        rif = pst.rif
        numero_contribuyente = pst.numero_contribuyente
        nombre_o_razon = unicode(pst.nombre_o_razon())
        email = pst.correo_electronico
        url_texto_qr_code = 'http://www.inatur.com.ve'

        builder = BuildReport(file_name_input='RIFTUR.pdf')
        builder \
            .add_text(465, 655.5, numero_comprobante) \
            .add_text(500, 620, fecha_registro) \
            .add_text(500, 605, fecha_certificacion) \
            .add_text(500, 590, anio_vencimiento) \
            .add_text(100, 620, rif) \
            .add_text(100, 605, numero_contribuyente) \
            .add_text(100, 585, nombre_o_razon) \
            .add_paragraph(100, 565, direccion) \
            .add_text(100, 520, email) \
            .add_bar_code(420, 670, numero_comprobante) \
            .add_qr_code(420, 450, url_texto_qr_code)

        return builder.build()


class RTN(View):
    def get(self, request, **kwargs):
        pst = models.Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        rtn = models.CertificacionRTN.objects.get(pst=pst)
        direccion = models.Direccion.objects.get(pst=pst)
        numero_comprobante = rtn.numero_comprobante
        fecha_registro = pst.creado_el.strftime('%x')
        fecha_certificacion = rtn.fecha_certificacion.strftime('%x')
        anio_vencimiento = (rtn.fecha_certificacion + datetime.timedelta(days=(3 * 365.24))).strftime('%x')
        rif = pst.rif
        rtn = str(pst.rtn)
        nombre_o_razon = unicode(pst.nombre_o_razon())
        email = pst.correo_electronico
        url_texto_qr_code = 'http://www.inatur.com.ve'

        builder = BuildReport(file_name_input='RTN.pdf')
        builder \
            .add_text(465, 655.5, numero_comprobante) \
            .add_text(500, 620, fecha_registro) \
            .add_text(500, 605, fecha_certificacion) \
            .add_text(500, 590, anio_vencimiento) \
            .add_text(100, 620, rif) \
            .add_text(100, 605, rtn) \
            .add_text(100, 590, nombre_o_razon) \
            .add_paragraph(100, 575, direccion) \
            .add_text(100, 530, email) \
            .add_bar_code(420, 670, numero_comprobante) \
            .add_qr_code(420, 450, url_texto_qr_code)

        return builder.build()


