# -*- coding: utf-8 -*-

import os
from cgi import escape

from django.conf import settings
from PyPDF2 import PdfFileWriter, PdfFileReader
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template

from django.template import Context
from django.http import HttpResponse


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code128
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT


class BuildReport(object):
    """
        Ejemplo:
        1)
            builder = BuildReport('archivo.pdf')
            builder.add_text(x=150, y=60, text='prueba de un texto')
            builder.add_paragraph(x=150, y=60, text='prueba de un parrafo')
            builder.add_bar_code(x=150, y=60, text='prueba de un codigo de barra')
            builder.add_qr_code(x=150, y=60, text='prueba de un codigo qr')
            return builder.build() # retorna una respuesta de tipo: application/pdf

        2)
            builder = BuildReport('archivo.pdf')
            builder \
            .add_text(x=150, y=60, text='prueba de un texto') \
            .add_paragraph(x=150, y=60, text='prueba de un parrafo') \
            .add_bar_code(x=150, y=60, text='prueba de un codigo de barra') \
            .add_qr_code(x=150, y=60, text='prueba de un codigo qr') \
            return builder.build() # retorna una respuesta de tipo: application/pdf

    """

    # Variables publicas para cambiar configuraciones en el pdf a generar
    # fuente por defecto: Helvetica
    FONT = 'Helvetica'
    # tamaño de fuente
    FONT_SIZE = 8
    # Objetos de inicialización que permiten manipular caracteristicas desde instancias de clase
    PDF_CANVAS = None
    INPUT = None
    OUTPUT = None
    RESPONSE = None
    BUFFER = None

    def __init__(self, dir_file_in=str(), file_name_input=None, file_name_output=None):
        """
            Constructor del builder.
                Recibe 3 parametros:
                    1) dir_file_in: El directorio dentro del cual se encuentra el archivo
                    2) file_name_input: El nombre del archivo o plantilla de entrada.
                                        El archivo o plantilla donde se van a escribir los cambios
                    3) file_name_output: El nombre del archivo de salida.
                                         El archivo que se va a generar.
        """
        # se obtiene el path del archivo
        file_path = os.path.join(settings.PDF_ROOT, dir_file_in, file_name_input)
        file_object = file(file_path)
        # se valida si el nombre del archivo existe en el path y se verifica si es un archivo
        self.__valid_file(file_path=file_path)

        self.OUTPUT = PdfFileWriter()
        self.INPUT = PdfFileReader(file_object, 'rb')

        # create response object
        self.RESPONSE = HttpResponse(content_type='application/pdf')
        name = file_name_output if file_name_output else file_name_input
        self.RESPONSE['Content-Disposition'] = 'attachment; filename=' + name

    def __valid_file(self, file_path):
        """
            Metodo privado que valida el path del archivo
        """
        import os

        valid = os.path.exists(file_path) and \
                os.path.isfile(file_path)
        if valid:
            return True
        else:
            raise NameError(
                'Error de Tipo. El archivo no existe o no posee permisos de lectura y escritura'
            )

    def __get_object_buffer(self, new_instance=False):
        """
            Metodo privado que retorna un objeto string buffer
        """
        if self.BUFFER == None or new_instance == True:
            self.BUFFER = StringIO()
        return self.BUFFER

    def __get_object_pdf_canvas(self):
        """
            Metodo privado que retorna un objeto canvas sobre el que se escriben los datos
        """
        if self.PDF_CANVAS == None:
            # fill first page
            buffer = self.__get_object_buffer(new_instance=True)  # create string buffer for PDF
            self.PDF_CANVAS = canvas.Canvas(buffer, pagesize=letter)
            self.PDF_CANVAS.setFont(self.FONT, self.FONT_SIZE)
        return self.PDF_CANVAS

    def __get_object_paragraph_style(self):
        """
            Metodo privado que retorna un estilo de parrafo
        """
        style = ParagraphStyle('test')
        style.textColor = 'black'
        style.alignment = TA_JUSTIFY
        style.fontSize = 8
        style.leading = 10
        return style

    def add_text(self, x, y, text):
        """
            Metodo que agrega un texto al canvas
        """
        # se obtiene el canvas donde trabajar
        pdf_canvas = self.__get_object_pdf_canvas()
        pdf_canvas.drawString(x, y, text)
        return self

    def add_text_bold(self, x, y, text, style=None):
        """
            Metodo que agrega un texto en negrita al canvas
        """
        if not style:
            style = ParagraphStyle('test')
            style.textColor = 'black'
            style.alignment = TA_LEFT
            style.fontSize = 8
            style.leading = 9

        # se obtiene el canvas donde trabajar
        pdf_canvas = self.__get_object_pdf_canvas()
        text = u'''<b><font size=12>{}</font></b> <br/>'''.format(text)
        paragraph = Paragraph(unicode(text), style)
        paragraph.wrapOn(pdf_canvas, 300, 50)
        paragraph.drawOn(pdf_canvas, x, y - paragraph.height)
        return self

    def add_paragraph(self, x, y, text, style=None, aW=250, aY=50):
        """
            Metodo que agrega un parrafo al canvas
        """
        # se obtiene el canvas donde trabajar
        pdf_canvas = self.__get_object_pdf_canvas()
        # se definen los estilos del parrafo
        if style == None:
            style = self.__get_object_paragraph_style()

        paragraph = Paragraph(unicode(text), style)
        paragraph.wrapOn(pdf_canvas, aW, aY)
        paragraph.drawOn(pdf_canvas, x, y - paragraph.height)
        return self

    def add_paragraph_bold(self, x, y, text, style=None, aW=250, aY=50):
        """
            Metodo que agrega un parrafo en negrita al canvas
        """
        # se obtiene el canvas donde trabajar
        pdf_canvas = self.__get_object_pdf_canvas()
        # se definen los estilos del parrafo
        if style == None:
            style = self.__get_object_paragraph_style()

        text = u'''<b><font size=12>{}</font></b> <br/>'''.format(text)
        paragraph = Paragraph(unicode(text), style)
        paragraph.wrapOn(pdf_canvas, aW, aY)
        paragraph.drawOn(pdf_canvas, x, y - paragraph.height)
        return self

    def add_qr_code(self, x, y, text):
        """
            Metodo utilizado para crear un codigo QR dentro del pdf
        """
        pdf_canvas = self.__get_object_pdf_canvas()
        # codigo QR
        qrw = QrCodeWidget(text)
        bounds = qrw.getBounds()
        w = bounds[2] - bounds[0]
        h = bounds[3] - bounds[1]

        d = Drawing(45, 45, transform=[140. / w, 0, 0, 140. / h, x, y])
        d.add(qrw)

        renderPDF.draw(d, pdf_canvas, 1, 1)
        return self

    def add_bar_code(self, x, y, text):
        """
            Metodo utilizado para crear un codigo de barra dentro del pdf
        """
        pdf_canvas = self.__get_object_pdf_canvas()
        barcode128 = code128.Code128(text)
        barcode128.drawOn(pdf_canvas, x, y)
        return self

    def add_watermark(self):
        """
            Metodo utilizado para agregar una marca de agua al archivo pdf
        """
        new_buffer = self.__get_object_buffer()
        watermark = PdfFileReader(new_buffer)
        tmp = self.INPUT.getPage(0)
        tmp.mergePage(watermark.getPage(0))
        self.BUFFER.seek(0)
        self.OUTPUT.addPage(tmp)
        return self

    def add_watermark_from_file(self, dir_file_in='', file_name_input=None):
        """
            Metodo utilizado para agregar una marca de agua al archivo pdf desde otro archivo
        """
        new_buffer = self.__get_object_buffer(new_instance=True)
        watermark = PdfFileReader(new_buffer)
        input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, dir_file_in, file_name_input), 'rb'))
        tmp = input.getPage(0)
        tmp.mergePage(watermark.getPage(0))
        self.BUFFER.seek(0)
        self.OUTPUT.addPage(tmp)
        return self

    def build(self):
        """
            Retorna la respuesta del pdf creado
        """
        # se guardan los cambios en el canvas
        self.PDF_CANVAS.save()
        # se aplica una marca de agua
        self.add_watermark()
        # se escribe la salida en la respuesta HTTP
        self.OUTPUT.write(self.RESPONSE)
        # se retorna la respuesta HTTP
        return self.RESPONSE


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    data = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("utf-8")), data)
    if not pdf.err:
        return HttpResponse(data.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

from xhtml2pdf import pisa
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def render_html_as_pdf(html_path, pdf_path):
    with open(html_path, 'r') as html_file:
        html_content = html_file.read()

    with open(pdf_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(
            html_content, dest=pdf_file
        )

    return pisa_status.err


