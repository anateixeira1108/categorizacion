# -*- coding: utf-8 -*-
"""
Vistas para los reportes
"""
import os
import json
import xlwt
import datetime
from collections import OrderedDict
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from registro.models import Pst, TipoPst, Direccion, DatoEspecifico
from registro.models import ORIGINAL, MODIFICACION, REPRESENTANTE, CONTACTO
from registro.views.pdf import TIPO_PST, response_juridica
from venezuela.models import Estado
from apps.reportes.serializers import PstSerializer
from utils import views_helpers as helpers
from PyPDF2 import PdfFileWriter, PdfFileReader
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PST_AGENTE = u'Agente Turístico'

PST_CONDUCTOR = u'Conductor Turístico'

PST_GUIA = u'Guía Turístico'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IndexReportes(TemplateView):
    """
    Clase para mostrar la vista principal para crear los reportes
    a los candidatos
    """
    template_name='reportes/funcionario_reportes.html'

    def get_context_data(self, **kwargs):
        context = super(IndexReportes, self).get_context_data()
        estados = [{"id": e.id, "nombre": e.estado} for e in Estado.objects.all()]
        actividad = [{"id": t.id, "nombre": t.nombre} for t in TipoPst.objects.all()]
        context['actividad_economica'] = json.dumps(actividad, ensure_ascii=True)
        context['estados'] = json.dumps(estados, ensure_ascii=True)
        return context

class IndexReportesEnMora(View):
    def get(self, request):
        context = dict()
        hoy = datetime.date.today()
        mora = hoy - datetime.timedelta(days=30)
        
        ListPsts = Pst.objects.filter(creado_el__lt=mora,
                                      ultima_verificacion=None)
        
        context['ids'] = ','.join([str(pst.id) for pst in ListPsts])
        context['psts'] = ListPsts
        return render(request, 'reportes/funcionario_reportes_en_mora.html', context)

class FiltrarReportes(View):
    def post(self, request):
        response = dict(success=False, message=u"No se encontaron Candidatos")
        post = request.POST.copy()
        ListPsts, data = [], []
        search, search_region = dict(), dict()
        region = ['estado', 'municipio', 'parroquia']
        rif = ''
        del post['csrfmiddlewaretoken']
        if post['busqueda'] == 'basica':
            try:
                rif = post['rif']
            except:
                pass

            if rif == '':
                ListPsts = Pst.objects.all()
            else:
                ListPsts = Pst.objects.filter(rif__exact=rif)

        if post['busqueda'] == 'avanzada':
            del post['busqueda']

            for key, value in post.iteritems():
                if key in region and value :
                    search_region[str(key)] = value.encode('utf-8')
                elif value:
                    search[str(key)] = value.encode('utf-8')

            if any(search_region):
                list_ids = []
                direcciones_pst = Direccion.objects.filter(**search_region)
                for direccion in direcciones_pst:
                    list_ids.append(direccion.pst.id)

                if any(list_ids):
                    search['pk__in'] = list_ids

            if any(search):
                ListPsts = Pst.objects.filter(**search)

            if not any(search) and not any(search_region):
                ListPsts = Pst.objects.all()
                

        serializer = PstSerializer(ListPsts, many=True)
        response = dict(success=True, data=serializer.data)

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')

class Expediente(View):
    def get(self, request, id=''):
        if id != '':
            pst_id = id
        else:
            pst_id = request.GET['id']
        pst = Pst.objects.get(id=pst_id)
        context = {'pst': pst}
        
        if pst.tipo_juridica:
            try:
                direccion = Direccion.objects.get(pst=pst)
                context['direccion'] = direccion
            except Exception as e:
                pass
            try:
                accionistas = Accionista.objects.filter(pst=pst)
                context['accionistas'] = accionistas
            except Exception as e:
                context['accionistas'] = []
            try:
                acta = Acta.objects.get(pst=pst, tipo_acta=ORIGINAL)
                context['acta'] = acta
            except Exception as e:
                pass
            try:
                modif_acta = Acta.objects.filter(pst=pst, tipo_acta=MODIFICACION)
                context['modificaciones'] = modif_acta
            except Exception as e:
                context['modificaciones'] = []
            try:
                contacto = RepresentanteContacto.objects.get(pst=pst, tipo=CONTACTO)
                context['contacto'] = contacto
            except Exception as e:
                pass
            try:
                representante = RepresentanteContacto.objects.get(pst=pst, tipo=REPRESENTANTE)
                context['representante'] = representante
            except Exception as e:
                pass
            if id != '':
                return context
            else:
                return render(request, 'reportes/juridica_expediente.html', context)
        else:
            listed_fields = {}
            if pst.tipo_pst.nombre == PST_AGENTE:
                listed_fields = (
                    ('anios_experiencia', u'Años de experiencia'),
                    ('archivo_curriculum', u'Currículum Vitae'),
                    ('titulo_universitario', u'Título universitario'),
                )
            elif pst.tipo_pst.nombre == PST_CONDUCTOR:
                listed_fields = (
                    ('archivo_certificado', u'Copia del certificado médico'),
                    ('archivo_licencia', u'Copia de la licencia de conducir'),
                    ('certificado_medico', u'No. del Certificado Médico'),
                    ('fecha_vencimiento_certificado', u'Vencimiento del certificado'),
                    ('fecha_vencimiento_licencia', u'Vencimiento de la licencia'),
                    ('get_grado_licencia_display', u'Grado de la licencia de conducir'),
                )
            elif pst.tipo_pst.nombre == PST_GUIA:
                listed_fields = (
                    ('guia_especializado', u'Nivel'),
                    ('egresado_instituto', u'Instituto del cual egresó'),
                    ('nombre_curso', u'Nombre del curso'),
                    ('fecha_curso', u'Fecha del curso'),
                    ('presta_servicio', u'Empresa donde presta servicio'),
                    ('primeros_auxilios', u'Primeros auxilios (Instituto)'),
                    ('ciudad_primeros_auxilios', u'Primeros auxilios (Ciudad)'),
                    ('fecha_primeros_auxilios', u'Primeros auxilios (Fecha)'),
                )
            dato_especifico = helpers.get_object_or_none(DatoEspecifico, pst=pst)
            if dato_especifico is not None:
                context['datos_especificos'] = OrderedDict()

                for field, alias in listed_fields:
                    context['datos_especificos'][alias] = (
                        helpers.process_field_value(getattr(dato_especifico, field))
                    )
            context['direccion'] = helpers.get_object_or_none(Direccion, pst=pst)
            if id != '':
                return context
            else:
                return render(request, 'reportes/natural_expediente.html', context)

class PdfExpediente(View):
    def get(self, request, id):
        context = Expediente.as_view()(self.request, id=id)
        if context['pst'].tipo_juridica:
            response = response_juridica(context, funcionario=True)
        else:
            response = TIPO_PST[unicode(context['pst'].tipo_pst)](context, funcionario=True)
        return response
    
class PdfReporteLista(View):
    def get(self, request):
        if 'filtros' in request.GET:
            filtros = dict()
            ystart = 530
            for i in request.GET['filtros'].split('&'):
                key_val = i.split('=')
                filtros[key_val[0]] = key_val[1]
        else:
            ystart = 620
        
        ids = [int(id) for id in request.GET['ids'].split(',')]
        search = dict()
        search['pk__in'] = ids
        ListPsts = Pst.objects.filter(**search)
        
        output = PdfFileWriter()
        if 'filtros' in request.GET:
            input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'reportes_lista_con_filtros.pdf'), 'rb'))
        else:
            input = PdfFileReader(file(os.path.join(settings.PDF_ROOT, 'reportes_lista_en_mora.pdf'), 'rb'))
        #create response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Reportes.pdf'

        # fill first page
        buffer = StringIO() # create string buffer for PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)

        if 'filtros' in request.GET:
            #impresion de filtros
            pdf.drawString(50, 633, unicode(filtros['riftur']))
            pdf.drawString(180, 633, unicode(filtros['rif']))
            pdf.drawString(310, 633, unicode(filtros['tipo_pst']))
            pdf.drawString(440, 633, unicode(filtros['razon_social']))
            pdf.drawString(70, 606, unicode(filtros['estado']))
            pdf.drawString(250, 606, unicode(filtros['municipio']))
            pdf.drawString(420, 606, unicode(filtros['parroquia']))
        
        #impresion de lista
        offset = 0
        for pst in ListPsts:
            pdf.drawString(50, ystart - offset, unicode(pst.rif))
            try:
                pdf.drawString(150, ystart - offset, unicode(pst.riftur))
            except:
                pass
            pdf.drawString(250, ystart - offset, unicode(pst.razon_social))
            pdf.drawString(400, ystart - offset, unicode(pst.tipo_pst))
            offset += 20


        pdf.save()
        # put on watermark from buffer
        watermark = PdfFileReader(buffer)
        page1 = input.getPage(0)

        page1.mergePage(watermark.getPage(0))

        # add processed pdf page
        output.addPage(page1)
        output.write(response)
        return response

class XlsReporteLista(View):
    def get(self, request):
        ids = [int(id) for id in request.GET['ids'].split(',')]
        search = dict()
        search['pk__in'] = ids
        ListPsts = Pst.objects.filter(**search)
        
        #create response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reportes.xls'

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Lista')
        
        ws.write(0, 0, 'RIF')
        ws.write(0, 1, 'RIFTUR')
        ws.write(0, 2, 'Razon Social')
        ws.write(0, 3, 'Actividad Economica')

        row = 1
        for pst in ListPsts:
            ws.write(row, 0, unicode(pst.rif))
            try:
                ws.write(row, 1, unicode(pst.riftur))
            except:
                pass
            ws.write(row, 2, unicode(pst.razon_social))
            ws.write(row, 3, unicode(pst.tipo_pst))
            row += 1


        wb.save(response)
        return response
