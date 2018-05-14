#-*- encoding: utf-8 -*-
from __future__ import unicode_literals

"""
    models.py
    ~~~~~~~~~

    Conjunto de controladores orientados a dar soporte
    a los servicios del modulo de calidad turistica

"""
try:

    """
        Modulos utilizados por DevTeam CGTS
    """
    from apps.categorizacion.helpers import model_list, camel_case_converter, algoritmo_asignacion
    from apps.categorizacion.helpers import generar_formulario, constants, generar_pdf
    from apps.licencias.models import EstatusSolicitud,SolicitudLicencia,TipoLicencia
    from apps.categorizacion.helpers.aes_cipher import decode as secure_value_decode
    from apps.categorizacion.helpers.validations import validate_file_type as val
    from apps.categorizacion.helpers.aes_cipher import encode as secure_value
    from apps.categorizacion.helpers import obtener_tabulador_actual
    from apps.categorizacion.helpers.debug_printer import dprint
    from apps.categorizacion.helpers.evaluar_categoria import *
    from apps.cuentas.models import ROLE_PST, ROLE_FUNCIONARIO
    from apps.categorizacion.helpers.obtener_tipo_pst import *
    from apps.categorizacion.helpers.validar_flujo import *
    from apps.categorizacion.helpers.decorators import *
    ################# Imports de Firmas #######################
    from apps.categorizacion.helpers.firmas_scripts import copiar_antes_firma 
    from apps.categorizacion.helpers.firmas_scripts import eliminar_antes_firma
    from apps.categorizacion.helpers.firmas_scripts import eliminar_file
    from apps.categorizacion.helpers.firmas_scripts import cambio_nombre_doc
    from apps.categorizacion.helpers.firmas_scripts import obtener_hash_doc
    from apps.categorizacion.helpers.firmas_scripts import cambio_nombre_file
    from apps.categorizacion.helpers.firmas_scripts import mover_file
    from apps.categorizacion.helpers.firmas_scripts import copiar_file
    ############## Culmina Imports de Firmas ##################
    from apps.categorizacion.helpers import tree
    from apps.categorizacion.helpers import model_list
    from registro.models import PERSONA_NATURAL
    from apps.cuentas.models import MinturUser
    from apps.categorizacion.models import *
    from registro.models import Direccion as Registro_Direccion
    from apps.licencias.models import Notificacion as NotificacionLicencia
    from apps.licencias.models import SolicitudLicencia, EstatusSolicitud, TipoLicencia
    from apps.categorizacion import forms as fc
    from apps.categorizacion.fields import StarsField, StarsFieldRango, RangoField, StarsFieldLogical
    from apps.categorizacion.helpers.number_to_letter import *
    """
        Librerias standard
    """
    from django.core.exceptions import ValidationError, FieldError    
    from django.contrib.auth.decorators import login_required
    from django.core.files.uploadedfile import UploadedFile
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import cache_page
    from django.db.models import get_app, get_models, Q
    from django.template.loader import select_template
    from django.core.urlresolvers import reverse_lazy
    from django.template import TemplateDoesNotExist
    from django.core.urlresolvers import reverse
    from django.views.generic import View
    from mintur.settings import BASE_DIR
    from mintur.settings import *
    from django.http import HttpResponse
    from django.core.cache import cache
    from reportlab.pdfgen import canvas
    from collections import defaultdict
    from django.core import serializers
    from django.contrib import messages
    from django.db.models import Count
    from django.utils import timezone
    from django.core import paginator
    from django.db.models import Max, Min
    from django.http import Http404
    from django.shortcuts import *
    from django.core.mail import EmailMultiAlternatives
    from django.core.mail import EmailMessage
    from bs4 import BeautifulSoup
    from random import shuffle
    from struct import *
    from urllib import quote_plus
    import datetime
    import operator
    import calendar
    import random
    import json
    import math
    import sys
    import os
    import threading
    import smtplib
    import re
    import pickle

    """ 
        Easy PDF 
    """
    import copy
    import easy_pdf
    from xhtml2pdf import pisa
    import cStringIO as StringIO
    from django.template import Context
    from django.utils.six import BytesIO
    from utils.gluon.storage import Storage
    from easy_pdf.views import PDFTemplateView
    from django.template.loader import get_template
    from easy_pdf.rendering import render_to_pdf_response
    from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

except Exception, e:
    print "[!] Conjunto de dependencias no encontradas o erroneas! Imposible continuar!!!"
    raise e

# Definiendo aplicacion categorizacion
APP_NAME = 'categorizacion'
APP = get_app(APP_NAME)
CACHED_VIEW_TABULADOR_TIMEOUT = 60 * 60 * 12


def correo(
    title=u'[MINTUR] Resultados del proceso de categorización',
    content=None, 
    content_plain=None, 
    by='gccdev@cgtscorp.com', 
    to=None,
    attach_file=None, 
    images=None, 
    args=None):

    dprint("entro en correos")
    dprint(by=by,to=to,attach_file=attach_file, images=images)

    funciona=False
    i=0
    while i<3 and funciona==False:
        i+=1
        try:
            msg_plain = EmailMessage(title,content_plain,by,to)
            msg = EmailMultiAlternatives(title,content,by,to)

            msg.attach_alternative(content, "text/html")
            if attach_file:
                if attach_file.find('.pdf') >= 0 or attach_file.find('.PDF') >= 0:
                    content = open(attach_file, 'rb')
                    msg.attach('file',content.read(),'application/pdf')
                    content_plain = open(attach_file, 'rb')
                    msg_plain.attach('file',content_plain.read(),'application/pdf')
                    content.close()
                    content_plain.close()

            msg_plain.send()
            msg.send()
            funciona=True
        except smtplib.SMTPException:
            print "-----------------------Falla en el correo------------------------------"
            continue

class GeneradorPDF(View):
    default_text = ' Ejemplo Ejemplo Ejemplo '
    default_pdf_name = 'reporte'

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; \
        filename='+self.default_pdf_name+'.pdf'
        p = canvas.Canvas(response)
        p.drawCentredString(275, 500, self.default_text)
        p.showPage()
        p.save()
        return response


class VisorPDF(View):
    def get(self, request, *args, **kwargs):
        dprint( request.GET['file'] )
        if request.GET['file'] is not None:            
            return render(request, 'viewer.html', {})


#Vistas del panel administrativo

class PanelAdministrativo(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(PanelAdministrativo, self).dispatch(*args, **kwargs)

    @del_tabulador_session
    def get(self, request, *args, **kwargs):
        m = get_models(APP)        
        modelo = kwargs['modelo'] if kwargs['modelo'] is not None else None
        try:            
            context = {
                'modelo': modelo,
                'modelos': model_list.get_model_list_nuevo(m),
                'show_name': model_list.get_instance_model(APP_NAME,modelo).show_name if modelo is not None else None,
                'actor': 'administrador',
                'administrador': True           
            }
            return render(request, 'administrador/inicio.html', context)
        except Exception, e:
            raise Http404    


class PanelAdministrativoEditar(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(PanelAdministrativoEditar, self).dispatch(*args, **kwargs)
    
    def get(self, request,*args,**kwargs):        
        modelos = get_models(APP)
        m = kwargs['modelo']
        template_to_render = 'administrador/editar_form.html'
        ident = kwargs ['id']
        modelo = model_list.get_instance_model(APP_NAME,m)
        objeto = get_object_or_404(modelo,id=ident)
        form = generar_formulario.GenerarFormulario(APP_NAME,m,None)
        form_filled =form(instance=objeto)

        if m.lower() == 'funcionario':

            form_filled.fields['user'].queryset = MinturUser.objects.exclude(role=ROLE_PST)

        elif m.lower() == 'tabulador':

            if Tabulador.objects.filter(
                tipo_pst = objeto.tipo_pst,
                version_actual = True
            ).exists() and not objeto.version_actual:
                del form_filled.fields['version_actual']
        elif m.lower() == 'seccionconfig':
            """
                Con las siguientes modificaciones se evita que 
                el usuario seleccione como padre de subseccion/seccion
                a si mismo, generando ciclos e inconsistencias
            """            
            form_filled.fields[
                'seccion_padre_config'
            ].queryset = SeccionConfig.objects.filter(
                aspecto_config__tabulador = objeto.aspecto_config.tabulador,              
            ).exclude(id = objeto.id).exclude(
                seccion_padre_config_id = objeto.id
            )

        elif m.lower() == 'subseccionconfig':
            form_filled.fields[
                'subseccion_config_padre'
            ].queryset = SubseccionConfig.objects.filter(
                seccion_config__aspecto_config__tabulador = objeto.seccion_config.aspecto_config.tabulador                            
            ).exclude(id = objeto.id).exclude(
                subseccion_config_padre_id = objeto.id
            )

        context= {
            'id': ident,
            'm': m,
            'form': form_filled,
            'modelo': model_list.get_instance_model(APP_NAME,m).show_name,            
            'modelos': model_list.get_model_list_nuevo(modelos),
            'es_editable':False,
            'actor': 'administrador',
            'administrador':True
        }
        
        return render(request, template_to_render, context)
    
    def post(self,request,*args,**kwargs):
        m=kwargs['modelo']
        ident = kwargs['id']
        tabulador_sustituto = None
        formul = generar_formulario.GenerarFormulario(APP_NAME,m,None)
        modelo=model_list.get_instance_model(APP_NAME,m)
        objeto = get_object_or_404(modelo,id=ident)
        form = formul(request.POST, instance=objeto)
        list_models = get_models(APP)

        low = m.lower()
        if low == 'funcionario':
            """
                Se evita que dentro de los formularios de creacion
                de funcionarios se muestre un usuario que no posea
                roles de funcionario interno
            """
            form.fields['user'].queryset = MinturUser.objects.exclude(role=ROLE_PST)

        if form.is_valid():

            """
                Luego de registrado el cambio en el elemento
                se realiza un filtrado para determinar cuando es
                necesario realizar una actualizacion de memoria
                cache
            """
            if low in [
                'subseccionconfig',
                'seccionconfig',
                'aspectofundamentalconfig',
                'tabulador',
                'tipomedida',
                'respuestaconfig'
                ]:               

                form.save()

                """
                    Se realiza la edicion de elemento que conforma el tabulador,
                    genera la necesidad de realizar una actualizacion memoria cache 
                    de tabuladores generados
                """
                t = None
                if low == 'subseccionconfig':
                    t = objeto.seccion_config.aspecto_config.tabulador
                elif low == 'seccionconfig':
                    t = objeto.aspecto_config.tabulador
                elif low == 'aspectofundamentalconfig':
                    t = objeto.tabulador
                elif low == 'tabulador':
                    t = objeto            
                elif low == 'respuestaconfig' or low == 'tipomedida':
                    """
                        En caso de que la edicion se haga sobre alguna
                        de las posibles respuestas del tabulador se hace una
                        limpieza total de los tabuladores
                    """
                    cache.clear()

                if t is not None:
                    key = 'mintur-cachedtabulador_%d' % (t.id)
                    if cache.get(key) is not None:
                        cache.delete(key)

                """
                    En caso de cambio de version de un tabulador
                    se actualiza el tabulador sustituto para seleccionarlo
                    como tabulador actual
                """
                if request.POST.has_key('tabulador_sustituto'):                    
                    tabulador_sustituto = int(request.POST['tabulador_sustituto'])
                    Tabulador.objects.filter(id=tabulador_sustituto).update(version_actual = True)

            elif low == 'funcionario':
                funcionario = Funcionario.objects.filter(id= objeto.id).first()
                dprint(objeto=objeto.habilitado)
                if (funcionario.habilitado != objeto.habilitado and objeto.habilitado ==False) or funcionario.tiporol.nombre != objeto.tiporol.nombre:
                    if funcionario.tiporol.nombre == 'inspector':
                        print "Inspector"
                        asignacion1= Asignacion.objects.filter(
                            funcionario__tiporol__nombre=funcionario.tiporol.nombre,
                            asignacion_habilitada=True
                        ).values_list('solicitud').annotate(dcount=Count('funcionario'))

                        solicits_insp=[]
                            
                        for e in asignacion1:
                            if e[1] > 1:
                                solicits_insp.append(e[0])

                        asignacion_extra = Asignacion.objects.filter(
                            funcionario=funcionario,
                            asignacion_habilitada=True,
                            solicitud_id__in=solicits_insp
                        )

                        asignaciones = Asignacion.objects.filter(
                            funcionario=funcionario,
                            asignacion_habilitada=True
                        )
                        solicituds1 = [e.solicitud_id for e in asignaciones]

                        if asignacion_extra:
                            solicits_extra = [e.solicitud_id for e in asignacion_extra]
                            solicits= [e for e in solicituds1 if e not in solicits_extra]
                            """
                            solicitudes_extra = Solicitud.objects.filter(
                                (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                                | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                                | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                                | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits_extra)
                            )
                            """
                            solicitudes_extra = Solicitud.objects.filter(
                                id__in=solicits_extra
                            )

                            asignaciones_extras = Asignacion.objects.filter(
                                funcionario=funcionario,
                                asignacion_habilitada=True,
                                solicitud_id__in= solicitudes_extra
                            )
                        else:
                            solicits = solicituds1
                        """
                        solicitudes = Solicitud.objects.filter(
                            (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                            | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                            | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                            | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits)
                        )
                        """
                        solicitudes = Solicitud.objects.filter(
                            id__in=solicits
                        )

                        asignaciones_quedan = Asignacion.objects.filter(
                            funcionario=funcionario,
                            asignacion_habilitada=True,
                            solicitud_id__in=solicitudes
                        )

                    else:
                        asignaciones = Asignacion.objects.filter(
                            funcionario=funcionario,
                            funcionario__tiporol__nombre=funcionario.tiporol.nombre, 
                            asignacion_habilitada=True
                        )
                        solicitudes = [e.solicitud if e.solicitud else e.solicitud_libro for e in asignaciones ]

                    if len(solicitudes)>0:
                        dprint(solicitudes=solicitudes)    
                        solicits3 = [e.id for e in solicitudes]
                        funcionario_nuevo_id = algoritmo_asignacion.algoritmo_de_asignacion(funcionario.tiporol.nombre,funcionario.id)
                        if funcionario_nuevo_id:
                            funcionario_nuevo = Funcionario.objects.get(id = funcionario_nuevo_id)

                            notificacion_emisor_viejo = Notificacion.objects.filter(
                                emisor=funcionario.user, solicitud__in= solicitudes
                            )

                            notificacion_receptor_viejo = Notificacion.objects.filter(
                                receptor=funcionario.user, solicitud__in= solicitudes
                            )

                            for e in notificacion_emisor_viejo:
                                notificaciones_movidas_back=  NotificacionBackup(
                                    emisor=e.emisor, receptor=e.receptor, 
                                    solicitud=e.solicitud, asunto=e.asunto,
                                    observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                    estatus_actual=e.estatus_actual
                                )
                                notificaciones_movidas_back.save()
                                notif_emisor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                notificacion=e)
                                dprint(notif_emisor_doc=notif_emisor_doc)
                                for f in notif_emisor_doc:
                                    f.notificacion_backup_id = notificaciones_movidas_back.id
                                    f.notificacion_id = None
                                    f.save()

                                e.delete()

                            for e in notificacion_receptor_viejo:
                                notificaciones_movidas_back=  NotificacionBackup(
                                    emisor=e.emisor, receptor=e.receptor, 
                                    solicitud=e.solicitud, asunto=e.asunto,
                                    observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                    estatus_actual=e.estatus_actual
                                )
                                notificaciones_movidas_back.save()
                                dprint(receptor=notificaciones_movidas_back)
                                notif_receptor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                notificacion=e)
                                dprint(notif_receptor_doc=notif_receptor_doc)
                                for f in notif_receptor_doc:
                                    f.notificacion_backup_id = notificaciones_movidas_back.id
                                    f.notificacion_id = None
                                    f.save()

                                e.delete()

                            if funcionario.tiporol.nombre != 'inspector':
                                for n in asignaciones:
                                    asignacion_nueva = Asignacion(
                                        funcionario=funcionario_nuevo, 
                                        tipo_asignacion=n.tipo_asignacion,
                                        solicitud_id=n.solicitud_id,
                                        solicitud_libro=n.solicitud_libro,
                                        fecha_asignacion=datetime.datetime.now(),
                                        asignacion_habilitada=True)
                                    asignacion_nueva.save()
                                    n.asignacion_habilitada=False
                                    n.save()
                            else:
                                print "Inspector"
                                for n in asignaciones_quedan:
                                    asignacion_nueva = Asignacion(
                                        funcionario=funcionario_nuevo, 
                                        tipo_asignacion=n.tipo_asignacion,
                                        solicitud_id=n.solicitud_id, 
                                        fecha_asignacion=datetime.datetime.now(),
                                        asignacion_habilitada=True)
                                    asignacion_nueva.save()
                                    n.asignacion_habilitada=False
                                    n.save()


                            if funcionario.tiporol.nombre != 'inspector':
                                sol_funcionario = Solicitud.objects.filter(
                                    id__in=solicits3)
                                sol_lsr = SolicitudLibro.objects.filter(
                                    id__in=solicits3)
                            else:
                                print "Inspector"
                                sol_funcionario = solicitudes

                            for s in sol_funcionario:
                                if s.funcionario_id == funcionario.id:
                                    s.funcionario_id = funcionario_nuevo.id
                                    s.save()
                                if funcionario.tiporol.nombre == 'inspector':
                                    if s.funcionario_extra_id == funcionario.id:
                                        s.funcionario_extra_id = funcionario_nuevo.id
                                        s.save()
                            for s in sol_lsr:
                                if s.funcionario == funcionario:
                                    s.funcionario = funcionario_nuevo
                                    s.save()

                        else:
                            return HttpResponseRedirect(
                                reverse(
                                    'home_panel_administrativo',
                                    kwargs={'modelo': m}
                                )
                            )
                    if funcionario.tiporol.nombre == 'inspector':
                        if len(asignacion_extra)>0:
                            if len(solicitudes_extra)!= 0:
                                for n in asignaciones_extras:
                                    n.asignacion_habilitada=False
                                    n.save()

                    if funcionario.tiporol.nombre == 'inspector':
                        #fun with pdf time!
                        tipoInspector = TipoAsignacion.objects.get(abreviacion='I')
                        """
                        solicitudes = Solicitud.objects.filter(
                            (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                            | Q(estatus__abreviacion='EI')
                            | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                            | Q(estatus__abreviacion='EA') ) & Q(id__in=solicituds1)
                        )
                        """
                        solicitudes = Solicitud.objects.filter(
                            id__in=solicituds1
                        )

                        asignaciones = Asignacion.objects.filter(tipo_asignacion__abreviacion='I')

                        for s in solicitudes:
                            inspectores = asignaciones.filter(
                                solicitud=s,asignacion_habilitada=True,
                                tipo_asignacion=tipoInspector
                            )
                            coordinador_dif = Asignacion.objects.get(
                                solicitud=s,asignacion_habilitada=True,
                                funcionario__tiporol__nombre='coordinador_dif'
                            ).funcionario
                            plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/credencial.html")
                            tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                            path = model_list.get_file_path(coordinador_dif.user.rif,"",'credenciales')
                            locationPath ='documents/files/'+ path

                            if len(inspectores)==1:
                                notificacion= Notificacion(
                                    emisor=coordinador_dif.user, receptor=inspectores[0].funcionario.user, 
                                    solicitud=s, estatus_actual=s.estatus
                                )
                                notificacion.save()

                                try:
                                    #Creando el documento
                                    nombre_documento = "%s_credencial_%s_%s" % (
                                        coordinador_dif.user.rif,
                                        s.id,
                                        inspectores[0].funcionario.id
                                    )
                                    credencial = Documento.objects.filter(
                                        nombre=nombre_documento).first()
                                    if credencial:
                                        credencial.fecha_aprobacion=datetime.datetime.now()
                                        credencial.eliminado=False
                                    else:
                                        data = Storage(
                                            nombre=nombre_documento,
                                            fecha_aprobacion=datetime.datetime.now(),
                                            plantilla_documento=plantilla,
                                            ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                            extension = 'pdf',
                                            tipo_documento_compuesto=tipo_documento,
                                        )
                                        credencial = Documento.create(data)
                                    
                                    credencial.save()

                                    #La notificacion respectiva a uno de los inspectores
                                    ndc = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion,
                                        documento = credencial
                                    )
                                    ndc.save()

                                    try:
                                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                            +str(direc.codigo_postal)
                                        data = Storage(
                                            nombre_establecimiento=s.pst.denominacion_comercial,
                                            direccion=direccionPST,
                                            nombre_inspector1=inspectores[0].funcionario.nombre\
                                                + " "+inspectores[0].funcionario.apellido,
                                            cedula_inspector1=inspectores[0].funcionario.cedula,
                                            nombre_inspector2="",
                                            cedula_inspector2="",
                                            nombre_coordinador_dif=coordinador_dif.nombre\
                                                +" "+coordinador_dif.apellido,
                                        )

                                        generar_pdf.generar_pdf(
                                            context=data,
                                            ruta_template='documentos/oficios/credencial.html',
                                            ruta_documento=locationPath,
                                            nombre_documento=nombre_documento
                                        )
                                    except Exception, e:
                                        dprint("Hubo errores creando el documento")
                                        raise e
                                except Exception, e:
                                    dprint("Hubo errores haciendo las notificaciones")
                                    raise e
                            else:
                                notificacion= Notificacion(
                                    emisor=coordinador_dif.user, receptor=inspectores[0].funcionario, 
                                    solicitud=s, estatus_actual=s.estatus
                                )
                                notificacion1= Notificacion(
                                    emisor=coordinador_dif.user, receptor=inspectores[1].funcionario, 
                                    solicitud=s, estatus_actual=s.estatus
                                )
                                notificacion.save()
                                notificacion1.save()

                                try:
                                    #Creando el documento
                                    nombre_documento = "%s_credencial_%s_%s_%s" % (
                                        coordinador_dif.user.rif,
                                        s.id,
                                        inspectores[0].funcionario.id,
                                        inspectores[1].funcionario.id
                                    )
                                    credencial = Documento.objects.filter(
                                        nombre=nombre_documento).first()
                                    if credencial:
                                        credencial.fecha_aprobacion=datetime.datetime.now()
                                        credencial.eliminado=False
                                    else:
                                        data = Storage(
                                            nombre=nombre_documento,
                                            fecha_aprobacion=datetime.datetime.now(),
                                            plantilla_documento=plantilla,
                                            ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                            extension = 'pdf',
                                            tipo_documento_compuesto=tipo_documento,
                                        )
                                        credencial = Documento.create(data)
                                    credencial.save()

                                    #La notificacion respectiva a uno de los inspectores
                                    ndc = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion,
                                        documento = credencial
                                    )
                                    ndc.save()
                                    #La notificacion respectiva al otro inspector
                                    ndc1 = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion1,
                                        documento = credencial
                                    )
                                    ndc1.save()

                                    try:
                                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                        direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                            +str(direc.codigo_postal)
                                        data = Storage(
                                            pagesize='A4',
                                            nombre_establecimiento=s.pst.denominacion_comercial,
                                            direccion=direccionPST,
                                            nombre_inspector1=inspectores[0].funcionario.nombre\
                                                + " "+inspectores[0].funcionario.apellido,
                                            cedula_inspector1=inspectores[0].funcionario.cedula,
                                            nombre_inspector2=inspectores[1].funcionario.nombre\
                                                + " "+inspectores[1].funcionario.apellido,
                                            cedula_inspector2=inspectores[1].funcionario.cedula,
                                            nombre_coordinador_dif=coordinador_dif.nombre\
                                                +" "+coordinador_dif.apellido,
                                        )

                                        generar_pdf.generar_pdf(
                                            context=data,
                                            ruta_template='documentos/credencial.html',
                                            ruta_documento=locationPath,
                                            nombre_documento=nombre_documento
                                        )
                                    except Exception, e:
                                        dprint("Errores documento") 
                                        raise e
                                except Exception, e:
                                    dprint("Errores notificaciones")
                                    raise e
                form.save()

            else:
                form.save()

            return HttpResponseRedirect(
                reverse(
                    'home_panel_administrativo',
                    kwargs={'modelo': m}
                )
            )
        else:            
            context ={
                'id': ident,
                'form':form,
                'es_editable':True,
                'm': m,
                'modelo':m,
                'modelos':model_list.get_model_list_nuevo(list_models),
                'actor':'administrador',
                'administrador':True
            }
            return render(request, 'administrador/editar_form.html',context)


class EliminarRecurso(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(EliminarRecurso, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        m = kwargs['modelo']
        Modelo = model_list.get_instance_model(APP_NAME, m)
        id_obj = int(request.POST['id'])
        objeto = get_object_or_404(Modelo,id=id_obj)
        dprint(objeto)
        #objeto1= Modelo.objects.filter(id=id_obj)
        low = m.lower()
        try:
            if low == 'funcionario':
                funcionario = Funcionario.objects.filter(id= objeto.id).first()

                if funcionario.tiporol.nombre == 'inspector':
                    print "Inspector"
                    asignacion1= Asignacion.objects.filter(
                        funcionario__tiporol__nombre=funcionario.tiporol.nombre,
                        asignacion_habilitada=True
                    ).values_list('solicitud').annotate(dcount=Count('funcionario'))

                    solicits_insp=[]
                        
                    for e in asignacion1:
                        if e[1] > 1:
                            solicits_insp.append(e[0])

                    asignacion_extra = Asignacion.objects.filter(
                        funcionario=funcionario,
                        asignacion_habilitada=True,
                        solicitud_id__in=solicits_insp
                    )

                    asignaciones = Asignacion.objects.filter(
                        funcionario=funcionario,
                        asignacion_habilitada=True
                    )
                    solicituds1 = [e.solicitud_id for e in asignaciones]

                    if len(asignacion_extra)>0:
                        solicits_extra = [e.solicitud_id for e in asignacion_extra]
                        solicits= [e for e in solicituds1 if e not in solicits_extra]
                        """
                        solicitudes_extra = Solicitud.objects.filter(
                            (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                            | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                            | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                            | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits_extra)
                        )
                        """
                        solicitudes_extra = Solicitud.objects.filter(
                            id__in=solicits_extra
                        )

                        asignaciones_extras = Asignacion.objects.filter(
                            funcionario=funcionario,
                            asignacion_habilitada=True,
                            solicitud_id__in= solicitudes_extra
                        )
                        dprint(solicitudes_extra=solicitudes_extra)
                    else:
                        solicits = solicituds1

                    solicitudes = Solicitud.objects.filter(
                        (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                        | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                        | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                        | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits)
                    )

                    solicitudes = Solicitud.objects.filter(
                        id__in=solicits
                    )

                    asignaciones_quedan = Asignacion.objects.filter(
                        funcionario=funcionario,
                        asignacion_habilitada=True,
                        solicitud_id__in=solicitudes
                    )

                else:
                    asignaciones = Asignacion.objects.filter(
                        funcionario=funcionario,
                        funcionario__tiporol__nombre=funcionario.tiporol.nombre, 
                        asignacion_habilitada=True
                    )
                    solicitudes = [e.solicitud for e in asignaciones]

                if len(solicitudes) > 0:
                    funcionario_nuevo_id = algoritmo_asignacion.algoritmo_de_asignacion(funcionario.tiporol.nombre,funcionario.id)
                    if funcionario_nuevo_id:
                        funcionario_nuevo = Funcionario.objects.filter(
                            id = funcionario_nuevo_id).first()
                        notificacion_emisor_viejo = Notificacion.objects.filter(
                            emisor= funcionario.user, solicitud_id__in= solicitudes
                        )
                        notificacion_receptor_viejo = Notificacion.objects.filter(
                            receptor= funcionario.user, solicitud_id__in= solicitudes
                        )
                        dprint(notificacion_emisor_viejo)
                        for e in notificacion_emisor_viejo:
                            
                            notificaciones_movidas_back=  NotificacionBackup(
                                emisor=e.emisor, receptor=e.receptor, 
                                solicitud=e.solicitud, asunto=e.asunto,
                                observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                estatus_actual=e.estatus_actual
                            )
                            notificaciones_movidas_back.save()
                            dprint(emisor=notificaciones_movidas_back)
                            notif_emisor_doc = NotificacionDocumentoCompuesto.objects.filter(
                            notificacion=e)
                            dprint(notif_emisor_doc=notif_emisor_doc)
                            for f in notif_emisor_doc:
                                f.notificacion_backup_id = notificaciones_movidas_back.id
                                f.notificacion_id = None
                                f.save()

                            e.delete()

                        for e in notificacion_receptor_viejo:
                            notificaciones_movidas_back=  NotificacionBackup(
                                emisor=e.emisor, receptor=e.receptor, 
                                solicitud=e.solicitud, asunto=e.asunto,
                                observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                estatus_actual=e.estatus_actual
                            )
                            notificaciones_movidas_back.save()
                            dprint(receptor=notificaciones_movidas_back)
                            notif_receptor_doc = NotificacionDocumentoCompuesto.objects.filter(
                            notificacion=e)
                            dprint(notif_receptor_doc=notif_receptor_doc)
                            for f in notif_receptor_doc:
                                f.notificacion_backup_id = notificaciones_movidas_back.id
                                f.notificacion_id = None
                                f.save()

                            e.delete()

                        if funcionario.tiporol.nombre != 'inspector':
                            for n in asignaciones:
                                asignacion_nueva = Asignacion(
                                    funcionario=funcionario_nuevo, 
                                    tipo_asignacion=n.tipo_asignacion,
                                    solicitud_id=n.solicitud_id, 
                                    fecha_asignacion=datetime.datetime.now(),
                                    asignacion_habilitada=True)
                                asignacion_nueva.save()
                                n.asignacion_habilitada=False
                                n.save()
                        else:
                            print "Inspector"
                            for n in asignaciones_quedan:
                                asignacion_nueva = Asignacion(
                                    funcionario=funcionario_nuevo, 
                                    tipo_asignacion=n.tipo_asignacion,
                                    solicitud_id=n.solicitud_id, 
                                    fecha_asignacion=datetime.datetime.now(),
                                    asignacion_habilitada=True)
                                asignacion_nueva.save()
                                n.asignacion_habilitada=False
                                n.save()


                        if funcionario.tiporol.nombre != 'inspector':
                            sol_funcionario = Solicitud.objects.filter(
                                id__in=solicitudes)
                        else:
                            print "Inspector"
                            sol_funcionario = solicitudes

                        for s in sol_funcionario:
                            if s.funcionario_id == funcionario.id:
                                s.funcionario_id = funcionario_nuevo.id
                                s.save()
                            if funcionario.tiporol.nombre == 'inspector':
                                if s.funcionario_extra_id == funcionario.id:
                                    s.funcionario_extra_id = funcionario_nuevo.id
                                    s.save()
                    else:
                        jsontmp = {
                            "err_msg": "Parametros invalidos",
                            "success": "", 
                            "data": "funcionario"
                        }
                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False,
                                content_type="application/json",
                            )
                        )
                if funcionario.tiporol.nombre == 'inspector':
                    if len(asignacion_extra)>0:
                        if len(solicitudes_extra)!= 0:
                            for n in asignaciones_extras:
                                n.asignacion_habilitada=False
                                n.save()

                if funcionario.tiporol.nombre == 'inspector':
                    #fun with pdf time!
                    tipoInspector = TipoAsignacion.objects.get(abreviacion='I')
                    """
                    solicitudes = Solicitud.objects.filter(
                        (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                        | Q(estatus__abreviacion='EI')
                        | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                        | Q(estatus__abreviacion='EA') ) & Q(id__in=solicituds1)
                    )
                    """
                    solicitudes = Solicitud.objects.filter(
                        id__in=solicituds1
                    )

                    asignaciones = Asignacion.objects.filter(tipo_asignacion__abreviacion='I')
                    for s in solicitudes:
                        inspectores = asignaciones.filter(
                            solicitud=s,asignacion_habilitada=True,
                            tipo_asignacion=tipoInspector
                        )
                        coordinador_dif = Asignacion.objects.get(
                            solicitud=s,asignacion_habilitada=True,
                            funcionario__tiporol__nombre='coordinador_dif'
                        ).funcionario
                        plantilla = PlantillaDocumento.objects.get(formato="documentos/credencial.html")
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                        path = model_list.get_file_path(coordinador_dif.user.rif,"",'credenciales')
                        locationPath ='documents/files/'+ path

                        if len(inspectores)==1:
                            notificacion= Notificacion(
                                emisor=coordinador_dif.user, receptor=inspectores[0].funcionario.user, 
                                solicitud=s, estatus_actual=s.estatus
                            )
                            notificacion.save()

                            try:
                                #Creando el documento
                                nombre_documento = "%s_credencial_%s_%s" % (
                                    coordinador_dif.user.rif,
                                    s.id,
                                    inspectores[0].funcionario.id
                                )
                                credencial = Documento.objects.filter(
                                    nombre=nombre_documento).first()
                                if credencial:
                                    credencial.fecha_aprobacion=datetime.datetime.now()
                                    credencial.eliminado=False
                                else:
                                    data = Storage(
                                        nombre=nombre_documento,
                                        fecha_aprobacion=datetime.datetime.now(),
                                        plantilla_documento=plantilla,
                                        ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                        extension = 'pdf',
                                        tipo_documento_compuesto=tipo_documento,
                                    )
                                    credencial = Documento.create(data)
                                credencial.save()

                                #La notificacion respectiva a uno de los inspectores
                                ndc = NotificacionDocumentoCompuesto(
                                    notificacion = notificacion,
                                    documento = credencial
                                )
                                ndc.save()

                                try:
                                    #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                    direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                                    direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                        +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                        + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                        +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                        +str(direc.codigo_postal)
                                    data = Storage(
                                        pagesize='A4',
                                        nombre_establecimiento=s.pst.denominacion_comercial,
                                        direccion=direccionPST,
                                        nombre_inspector1=inspectores[0].funcionario.nombre\
                                            + " "+inspectores[0].funcionario.apellido,
                                        cedula_inspector1=inspectores[0].funcionario.cedula,
                                        nombre_inspector2="",
                                        cedula_inspector2="",
                                        nombre_coordinador_dif=coordinador_dif.nombre\
                                            +" "+coordinador_dif.apellido,
                                    )

                                    generar_pdf.generar_pdf(
                                        context=data,
                                        ruta_template='documentos/credencial.html',
                                        ruta_documento=locationPath,
                                        nombre_documento=nombre_documento
                                    )
                                except Exception, e:
                                    dprint("Hubo errores creando el documento")
                                    raise e
                            except Exception, e:
                                dprint("Hubo errores haciendo las notificaciones")
                                raise e
                        else:
                            notificacion= Notificacion(
                                emisor=coordinador_dif.user, receptor=inspectores[0].funcionario, 
                                solicitud=s, estatus_actual=s.estatus
                            )
                            notificacion1= Notificacion(
                                emisor=coordinador_dif.user, receptor=inspectores[1].funcionario, 
                                solicitud=s, estatus_actual=s.estatus
                            )
                            notificacion.save()
                            notificacion1.save()

                            try:
                                #Creando el documento
                                nombre_documento = "%s_credencial_%s_%s_%s" % (
                                    coordinador_dif.user.rif,
                                    s.id,
                                    inspectores[0].funcionario.id,
                                    inspectores[1].funcionario.id
                                )
                                credencial = Documento.objects.filter(
                                    nombre=nombre_documento).first()
                                if credencial:
                                    credencial.fecha_aprobacion=datetime.datetime.now()
                                    credencial.eliminado=False
                                else:
                                    data = Storage(
                                        nombre=nombre_documento,
                                        fecha_aprobacion=datetime.datetime.now(),
                                        plantilla_documento=plantilla,
                                        ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                        extension = 'pdf',
                                        tipo_documento_compuesto=tipo_documento,
                                    )
                                    credencial = Documento.create(data)
                                credencial.save()

                                #La notificacion respectiva a uno de los inspectores
                                ndc = NotificacionDocumentoCompuesto(
                                    notificacion = notificacion,
                                    documento = credencial
                                )
                                ndc.save()
                                #La notificacion respectiva al otro inspector
                                ndc1 = NotificacionDocumentoCompuesto(
                                    notificacion = notificacion1,
                                    documento = credencial
                                )
                                ndc1.save()

                                try:
                                    #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                    direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                                    direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                        +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                        + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                        +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                        +str(direc.codigo_postal)
                                    data = Storage(
                                        pagesize='A4',
                                        nombre_establecimiento=s.pst.denominacion_comercial,
                                        direccion=direccionPST,
                                        nombre_inspector1=inspectores[0].funcionario.nombre\
                                            + " "+inspectores[0].funcionario.apellido,
                                        cedula_inspector1=inspectores[0].funcionario.cedula,
                                        nombre_inspector2=inspectores[1].funcionario.nombre\
                                            + " "+inspectores[1].funcionario.apellido,
                                        cedula_inspector2=inspectores[1].funcionario.cedula,
                                        nombre_coordinador_dif=coordinador_dif.nombre\
                                            +" "+coordinador_dif.apellido,
                                    )

                                    generar_pdf.generar_pdf(
                                        context=data,
                                        ruta_template='documentos/credencial.html',
                                        ruta_documento=locationPath,
                                        nombre_documento=nombre_documento
                                    )
                                except Exception, e:
                                    dprint("Errores documento") 
                                    raise e
                            except Exception, e:
                                dprint("Errores notificaciones")
                                raise e

                
            objeto.delete()
            jsontmp = {
                "err_msg": "",
                "success": "Objeto eliminado",
                "data":{"elemento_id":id_obj},
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )
        except Exception, e:
            jsontmp = {
                "err_msg": e,
                "success": "",
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )


class AgregarRecurso(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(AgregarRecurso, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        m = get_models(APP)
        mod = kwargs['modelo']
        f = generar_formulario.GenerarFormulario(APP_NAME, mod)
        form = f()
        modelo = model_list.get_instance_model(APP_NAME,mod)

        if mod.lower() == 'funcionario':
            form.fields['user'].queryset = MinturUser.objects.exclude(role=ROLE_PST)
        elif mod.lower() == "tabulador":
            form.fields['tipo_pst'].queryset = TipoLicencia.objects.filter(
                padre = TipoLicencia.objects.get(codigo = "LIC_ALO_T")
                )

        context = {
            'modelos': model_list.get_model_list_nuevo(m),
            'modelo': kwargs['modelo'],
            'form': form,
            'show_name': modelo.show_name,
            'actor': 'administrador',
            'administrador': True,
        }
        return render(request, 'administrador/agregar.html', context)
    
    def post(self, request, *args, **kwargs):
        dprint(request.POST)
        m = get_models(APP)
        mod = kwargs['modelo']
        modelo = model_list.get_instance_model(APP_NAME,mod)
        f = generar_formulario.GenerarFormulario(APP_NAME, mod)
        form = f(request.POST)

        if mod.lower() == 'funcionario':
            form.fields['user'].queryset = MinturUser.objects.exclude(role=ROLE_PST)

        if mod.lower() in [
                'subseccionconfig',
                'seccionconfig',
                'aspectofundamentalconfig',
                'tabulador',
                'tipomedida',
                'respuestaconfig'
                ]:
            """
                Se esta registrando algun cambio que podria
                generar una actualizacion de la estructura 
                del tabulador, por ello se limpia la memoria
                cache para reflejar el cambio
            """
            cache.clear()
        try:
            form.is_valid()
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'home_panel_administrativo',
                    kwargs ={'modelo':mod}
                )
            )
        except Exception, e:            
            context = {
                'modelos': model_list.get_model_list_nuevo(m),
                'modelo': mod,
                'form': form,
                'show_name': modelo.show_name,
                'actor': 'administrador',
                'administrador': True,
            }
            return render(request, 'administrador/agregar.html', context)


class ObtenerTiposRespuesta(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))    
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(ObtenerTiposRespuesta, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        jsontmp = cache.get("mintur_tipos_respuesta")
        if jsontmp is None:
            try:
                s = serializers.serialize(
                    'json',
                    TipoRespuesta.objects.all().exclude(codigo__in= ['REP', 'E']),
                    fields = ('id','nombre','codigo')
                )
                jsontmp = {}
                jsontmp['data'] = s
                jsontmp['success_msg'] = "OK"
                cache.set(
                    "mintur_tipos_respuesta",
                    jsontmp
                )

                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 200
                )
            except Exception, e:            
                return HttpResponse(
                    json.dumps(
                        {
                            "err_msg": "Error obteniendo datos de tipos de elemento %s" % (str(e))
                        }
                        , sort_keys=False
                    ),
                    content_type="application/json",
                    status = 500
                )
        return HttpResponse(
            json.dumps(jsontmp, sort_keys=False),
            content_type="application/json",
            status = 200
        )


class ObtenerFormularioElemento(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))    
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(ObtenerFormularioElemento, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            code = request.GET["code"]
            tipopst = Tabulador.objects.get( id = int(request.GET['tabulador'])).tipo_pst
            currentTab = request.GET["current_tab"]
            
            try:
                iconografia = TipoIcono.objects.get(tipo_pst = tipopst)
            except TipoIcono.DoesNotExist:
                iconografia = Storage(representacion = "fa-star")

            categoria = Categoria.objects.filter(
                tipo_pst = tipopst
            ).count()

            if code == "E_ASPECTOF":
                
                form = fc.AspectoFundamentalForm(currentTab = currentTab)
                form.fields['nombre'].widget.attrs['rows'] = '5'

                if currentTab == "specific-req":
                    form.fields['peso_porcentual'] = RangoField()

                return  HttpResponse(
                    json.dumps(
                        {
                            "form": form.as_p()
                        }
                        , sort_keys=False
                    ),
                    content_type="application/json",
                    status = 200
                )
            elif code == "E_SECCION":
                f = generar_formulario.GenerarFormulario(APP_NAME, "seccionconfig")

                form=f()
                del form.fields['aspecto_config']
                del form.fields['seccion_padre_config']
                return  HttpResponse(
                    json.dumps(
                        {
                            "form": form.as_p()
                        }, sort_keys=False
                    ),
                    content_type="application/json",
                    status = 200
                )
            elif code == "D":
                form = fc.RespuestaDual()
                form.fields['relevancia_por_categoria'] = StarsField (
                    categorias =  categoria,
                    star_icon = iconografia.representacion
                    )
                form.fields['enunciado'].widget.attrs['rows'] = '5'
                
                return  HttpResponse(
                    json.dumps(
                        {
                            "form": form.as_p()
                        }
                        , sort_keys=False
                    ),
                    content_type="application/json",
                    status = 200
                )
            elif code == "E":
                form = fc.RespuestaEscala()
                form.fields['relevancia_por_categoria'] = StarsField (
                    categorias = categoria,
                    star_icon = iconografia.representacion
                    )
                form.fields['enunciado'].widget.attrs['rows'] = '5'

                return  HttpResponse(
                    json.dumps(
                        {
                            "form": form.as_p()
                        }
                        , sort_keys=False
                    ),
                    content_type="application/json",
                    status = 200
                )    
            elif code == "R":
                form = fc.RespuestaRango()
                form.fields['relevancia_por_categoria'] = StarsFieldRango(
                    categorias = categoria,
                    star_icon = iconografia.representacion
                    )
                form.fields['enunciado'].widget.attrs['rows'] = '5'

                return  HttpResponse(
                    json.dumps(
                        {
                            "form": form.as_p()
                        }
                        , sort_keys=False
                    ),
                    content_type="application/json",
                    status = 200
                )
            elif code == "REP":
                form = fc.RespuestaRepetitiva()
                form.fields['enunciado'].widget.attrs['rows'] = '5'

                form.fields['cantidad_por_categoria'] = StarsField (
                    categorias = categoria, 
                    flag="input",
                    star_icon = iconografia.representacion
                )
                return  HttpResponse(
                    json.dumps(
                        {
                            "form": str(form.as_p())
                        }
                        , sort_keys=False
                    ),
                    content_type="application/json",
                    status = 200
                )
            elif code == "C":
                tabulador = Tabulador.objects.get(id= int(request.GET['tabulador']))
                subseccion = SubseccionConfig.objects.filter(
                        seccion_config__aspecto_config__tabulador_id= 0
                    )
               
                form = fc.RespuestaCondicional()
                form.fields['enunciado'].widget.attrs['rows'] = '5'

                form.fields['conjunto_de_condiciones_positiva']=forms.ModelChoiceField(
                    widget=forms.Select(attrs={'class': 'select_form'}),
                    queryset= subseccion
                )
                form.fields['conjunto_de_condiciones_negativa']=forms.ModelChoiceField(
                    widget=forms.Select(attrs={'class': 'select_form1'}),
                    queryset= subseccion
                )                
            elif code == "F":
                form = fc.RespuestaFormula(tabulador = int(request.GET['tabulador']))
                form.fields['enunciado'].widget.attrs['rows'] = '5'
                
                lo = OperadorFormula.objects.filter(logico = True)
                t = ()
                for e in lo:
                    t += ((e.id, e.representacion),)

                form.fields['relacion'] = StarsFieldLogical (
                    lo = t,
                    categorias = categoria ,
                    star_icon = iconografia.representacion
                )
                form.fields['relacion'].label = u"Relación entre valores retornados y valores ingresados"
            return  HttpResponse(
                json.dumps(
                    {
                        "form": form.as_p()
                    }
                    , sort_keys=False
                ),
                content_type="application/json",
                status = 200
            )

        except Exception, e:
            raise e

########################
#                      #
# Agregar un tabulador #
#                      #
########################
class AgregarTabulador(View):
    """
        AgregarTabulador
        Metodo para agregar un tabulador para realizar la evaluacion
        de los establecimientos

        Maneja creacion dinamica y reconstruccion mediante el url recontruir y clonacion 
        mediante peticion al url clonar.
    """

    def __init__(self):
        self.template = "administrador/agregar_tabulador.html" 
        self.modelos = model_list.get_model_list_nuevo(get_models(APP))    

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(AgregarTabulador, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):

        id_tabulador = int(kwargs['tabulador']) if kwargs.has_key('tabulador') else None
        operacion_clonado = True if kwargs.has_key('flag') else False

        max_tab =Tabulador.objects.all().aggregate(Max('id'))['id__max']
        max_subseccion = SubseccionConfig.objects.all().aggregate(Max('id'))['id__max']
        max_seccion = SeccionConfig.objects.all().aggregate(Max('id'))['id__max']
        max_aspecto = AspectoFundamentalConfig.objects.all().aggregate(Max('id'))['id__max']
        max_indicador = Indicador.objects.all().aggregate(Max('id'))['id__max']

        append_ids =[]

        if id_tabulador is not None:        
            append_ids.append(id_tabulador-1)
        else:
            append_ids.append(max_tab if max_tab is not None else 1)

        append_ids.append(max_subseccion if max_subseccion is not None else 1)
        append_ids.append(max_seccion if max_seccion is not None else 1)        
        append_ids.append(max_aspecto if max_aspecto is not None else 1)
        append_ids.append(max_indicador if max_indicador is not None else 1)
        
        c = Categoria.objects.distinct("tipo_pst")
        q = []
        iconografia = None

        for e in c:
            try:
                iconografia = TipoIcono.objects.get(tipo_pst = e.tipo_pst)
            except TipoIcono.DoesNotExist:
                iconografia = Storage(representacion = "fa-star")

            q.append(          
                {
                    'tipo_pst':e.tipo_pst, 
                    'count':Categoria.objects.filter( tipo_pst = e.tipo_pst ).count(),
                    'icon': iconografia.representacion
                }               
            )

        t = [
                {'id':e.id, 'nombre':e.nombre, 'abreviacion':e.abreviacion} for e in TipoSubseccion.objects.filter(tipopadre__abreviacion="RD")
            ]

        w = {}
        for e in TipoAspectoFundamental.objects.all():
            w.update({e.abreviacion:e.id})

        return render(
            request,
            self.template,
            {
                'actor': 'administrador',
                'administrador': True,
                'modelos': self.modelos,
                'modelo': 'tabulador',
                'tiposprestador': q,
                'tiposdocumento': t,
                'tiposaspectofundamental':w,
                'maximos_ids': append_ids,
                'tabulador': Tabulador.objects.get(id=id_tabulador) if id_tabulador else id_tabulador,
                'clonado': operacion_clonado
            }
        )

    def post(self, request, *args, **kwargs):

        jsontmp = {
            "err_msg":"",
            "success_msg":"",
            "data": {}
        }
        flag_tab = False
        tabulador = None 
        tipo_pst = 0      
        try:
            tabulador = int(request.POST['tabulador'])

            jsontmp['data'].update({'tabulador': tabulador})

            if request.POST.has_key('main_cookie'):

                # Handles main configuration cookie
                cookie = json.loads(request.POST['main_cookie'])            
                e = cookie[0]
                
                jsontmp['data'].update({'version': len(Tabulador.objects.filter(tipo_pst=int(e['type']),version_actual=True))})
                try:
                    tab = Tabulador.objects.get(id=int(e['id']))
                    tipo_pst = int(e['type'])
                    if e['state'] == "edited":
                        tab.tipo_pst_id = int(e['type'])
                        tab.nombre = e['name']
                        tab.version_actual = e['version_actual']
                        tab.save()
                        flag_tab = True
                    tabulador = tab.id
                    tipo_pst = int(e['type'])
                    jsontmp['data'].update({'tabulador': tabulador})
                except Tabulador.DoesNotExist:
                    if e['state'] == "added" or e['state'] == "edited":
                        tipo_pst = int(e['type'])
                        tab = Tabulador(
                            tipo_pst_id = int(e['type']),
                            nombre = e['name'],
                            fecha_creacion=datetime.datetime.now(),
                            version_actual = e['version_actual']
                        )
                        tab.save()
                        tabulador = tab.id
                        jsontmp['data'].update({'tabulador': tabulador})
                        flag_tab = True

                if request.POST.has_key('tabulador_sustituto'):                    
                    tabulador_sustituto = int(request.POST['tabulador_sustituto'])
                    Tabulador.objects.filter(id=tabulador_sustituto).update(version_actual = True)
            
            if request.POST.has_key('documental_cookie'):
                
                cookie = json.loads(request.POST['documental_cookie'])           
                ids_dr = []
                onetime = True
                s = None
                a = None

                for e in cookie:
                    if e['state'] != "done" :                        
                        if onetime:
                            onetime = False
                            try:
                                s = SeccionConfig.objects.get(
                                    aspecto_config__tabulador_id = tabulador,
                                    aspecto_config__nombre = "RD",
                                    nombre = "RD"
                                )
                            except SeccionConfig.DoesNotExist:
                                try:
                                    a = AspectoFundamentalConfig.objects.get( 
                                        nombre = "RD",
                                        tabulador_id = tabulador,
                                        tipo_aspecto = TipoAspectoFundamental.objects.get(abreviacion = "RD")
                                    )
                                except AspectoFundamentalConfig.DoesNotExist:
                                    a = AspectoFundamentalConfig(
                                        nombre = "RD",
                                        tabulador_id = tabulador,
                                        peso_porcentual = 1,
                                        tipo_aspecto = TipoAspectoFundamental.objects.get(abreviacion = "RD")
                                    )
                                    a.save()

                                s = SeccionConfig(
                                    nombre = "RD",
                                    aspecto_config = a,
                                    seccion_padre_config =  None
                                )
                                s.save()

                        if e['state'] == 'added':                      
                            sb = SubseccionConfig(
                                    nombre = e['name'],
                                    seccion_config = s,
                                    tipo_subseccion_id = int(e['type']),
                                    respuesta_config = RespuestaConfig.objects.get(
                                        tipo_respuesta__codigo = "A"),
                                    subseccion_config_padre = None,
                                    subs_imagen = True
                                )                        
                            sb.save()
                            
                            ids_dr.append(
                                {
                                    'pid': e['id'], 'nid': sb.id
                                }
                            )
                        elif e['state'] == 'edited' or  e['state'] == 'deleted':
                            try:
                                sb = SubseccionConfig.objects.get( id = int(e['id']) )
                                idc = None

                                if e['state'] == 'edited':
                                    sb.nombre = e['name']
                                    sb.tipo_subseccion_id = int(e['type'])
                                    sb.save()
                                    idc = sb.id
                                elif e['state'] == 'deleted':                                    
                                    
                                    tl = len(
                                        SubseccionConfig.objects.filter(
                                            seccion_config__aspecto_config__tabulador_id = tabulador,
                                            tipo_subseccion__tipopadre__abreviacion = "RD"
                                            )
                                        )

                                    if tl == 1:
                                        AspectoFundamentalConfig.objects.get(nombre = "RD",tabulador_id = tabulador).delete()
                                    else:
                                        sb.delete()

                                    idc = 0
                                
                                ids_dr.append( 
                                    {
                                        'pid': e['id'], 'nid': idc                                    
                                    }
                                )
                            except SubseccionConfig.DoesNotExist:
                                if e['state'] == 'edited':
                                    sb = SubseccionConfig(
                                            nombre = e['name'],
                                            seccion_config = s,
                                            tipo_subseccion_id = int(e['type']),
                                            respuesta_config = RespuestaConfig.objects.get(
                                                tipo_respuesta__codigo = "A"
                                            ),
                                            subseccion_config_padre = None,
                                            subs_imagen = True
                                        )                        
                                    sb.save()

                                    ids_dr.append( 
                                        {
                                            'pid': e['id'], 'nid': sb.id
                                        } 
                                    )
                                else:
                                    ids_dr.append({e['id']: -1})
                        else:
                            raise Exception("Estado del elemento invalido")
                    
                    jsontmp['data'].update({'elementos_dr': ids_dr,})                    

            if request.POST.has_key('specific_values_cookie'):

                cookie = json.loads(request.POST['specific_values_cookie']) 
                tabuld = Tabulador.objects.get(id= tabulador)
                ids_ve = []                
                onetime = True
                s = None
                a = None
                
                for e in cookie:
                    if e['state'] != 'done':
                        try:
                            s = Indicador.objects.get(id = int(e['id']))
                            
                            if e['state'] == "edited":
                                s.nombre = e['name']
                                s.save()
                                
                                relacion = ValorCategoria.objects.filter( indicador = s ).order_by("categoria__valor")
                                if type(e['valor']) == list and str(e['valor']).lower().strip() not in ["n/a","-"]:
                                    cat = Categoria.objects.filter(
                                        tipo_pst = tipo_pst
                                    ).order_by('valor')

                                    if len(relacion) == len(cat):
                                        for re,val in zip(relacion, e['valor']):
                                            re.valor = val
                                            re.save()
                                    else:
                                        for val, cat in zip(e['valor'], cat):
                                            v = ValorCategoria(
                                                categoria = cat,
                                                indicador = s,
                                                operador = None,
                                                valor_comparacion = None,
                                                valor = float(val)
                                            )
                                            v.save()
                                else:
                                    if len(relacion):
                                        relacion.delete();

                                ids_ve.append(
                                    {
                                        'pid': e['id'], 'nid': s.id
                                    }
                                )  
                            elif e['state'] == 'deleted':
                                s.delete()
                                ids_ve.append({e['id']: -1})

                        except Indicador.DoesNotExist:
                            if e['state'] == "added" or e['state'] == "edited":
                                """
                                    En este caso entra porque se esta mandando algo
                                    nuevo pero de edicion remota pero que es considerado
                                    nuevo en su totalidad
                                """
                                s = Indicador(
                                    nombre = e['name'],
                                    tabulador_id = tabulador
                                )
                                s.save()

                                """
                                    Se crea la estructura completa del tabulador
                                    partiendo de que solo se utilizara una seccion 
                                    , subseccion y respuesta config del tipo VE para
                                    los requisitos especificos, lo que permite que se
                                    puedan visualizar en las funciones de vista previa
                                """
                                try:
                                    sec = SeccionConfig.objects.get(
                                        aspecto_config__tabulador_id = tabulador,
                                        aspecto_config__nombre = "VE",
                                        nombre = "Valores Especificos"
                                    )
                                except SeccionConfig.DoesNotExist:
                                    try:
                                        a = AspectoFundamentalConfig.objects.get( 
                                            nombre = "VE",
                                            tabulador_id = tabulador,
                                            tipo_aspecto = TipoAspectoFundamental.objects.get(abreviacion = "VE")
                                        )
                                    except AspectoFundamentalConfig.DoesNotExist:
                                        a = AspectoFundamentalConfig(
                                            nombre = "VE",
                                            tabulador_id = tabulador,
                                            peso_porcentual = 1,
                                            tipo_aspecto = TipoAspectoFundamental.objects.get(abreviacion = "VE")
                                        )
                                        a.save()

                                    sec = SeccionConfig(
                                        nombre = "VE",
                                        aspecto_config = a,
                                        seccion_padre_config =  None
                                    )
                                    sec.save()

                                try:
                                    rve = RespuestaConfig.objects.get(tipo_respuesta__codigo = "VE")
                                except RespuestaConfig.DoesNotExist:
                                    rve =  RespuestaConfig(
                                        nombre = "Valores Especificos",
                                        tipo_respuesta = TipoRespuesta.objects.get(codigo = 'VE')
                                    )
                                    rve.save()

                                sb = SubseccionConfig(
                                        nombre = e['name'],
                                        seccion_config = sec,
                                        tipo_subseccion = TipoSubseccion.objects.get(abreviacion = "VE"),
                                        respuesta_config = rve,
                                        subseccion_config_padre = None,
                                        subs_imagen = False,
                                        suministrado = True if e['suministrado'].lower().strip() == "si" else False
                                    )                      
                                sb.save()

                                vi = ValorIndicador(
                                    respuesta_config=rve,
                                    indicador= s,
                                    orden = 1,
                                    suministrado = True if e['suministrado'].lower().strip() == "si" else False
                                )
                                vi.save()

                                if str(e['valor']).lower().strip() not in ["n/a","-"]:
                                    cat = Categoria.objects.filter(
                                        tipo_pst = tipo_pst
                                    ).order_by('valor')

                                    for val, cat in zip(e['valor'], cat):
                                        v = ValorCategoria(
                                            categoria = cat,
                                            indicador = s,
                                            operador = None,
                                            valor_comparacion = None,
                                            valor = float(val)
                                        )
                                        v.save()
                                
                                ids_ve.append(
                                    {
                                        'pid': e['id'], 'nid': s.id
                                    }
                                )

                    jsontmp['data'].update({'elementos_ve': ids_ve })

            if request.POST.has_key('basic_req') or request.POST.has_key('specific_req'):
                
                if flag_tab == False:
                
                    if request.POST.has_key('basic_req'):
                        c = json.loads(request.POST['basic_req'])
                        if len(c) and len(c[0]['children'])>0:
                            ids_req_basic = []
                            ids_req_basic = tree.BuildingTree(c[0],None,ids_req_basic,None,tipo_pst,"RB",None)
                            jsontmp['data'].update({'elementos_req_basic': ids_req_basic})
                            
                    if request.POST.has_key('specific_req'):
                        c = json.loads(request.POST['specific_req'])
                        if len(c) and len(c[0]['children'])>0:
                            ids_req_specific = []
                            ids_req_specific = tree.BuildingTree(
                                c[0],
                                None,
                                ids_req_specific,
                                None,
                                tipo_pst,
                                "RE",
                                None
                            )

                            jsontmp['data'].update({'elementos_req_specific': ids_req_specific})

            return HttpResponse(
                json.dumps(jsontmp, sort_keys=False),
                content_type="application/json",
                status = 200
            )
        except Exception, e:
            raise e


#############################################
#                                           #
# Reconstruir un tabulador basado en su id  #
#                                           #
#############################################
class ReconstruirTabulador(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    @admin_only
    def dispatch(self, *args, **kwargs):
        return super(ReconstruirTabulador, self).dispatch(*args, **kwargs)

    def reconstruirRequisitos(self, tabulador, tipo_requisitos, user, clone):
        
        if tipo_requisitos in ["RB", "RE"]:

            bob = GenerarTabulador()
            tabulador_json = []
            secciones_empty = []
            aspectos_empy = []
            taf = ["B","M"] if tipo_requisitos == "RB" else ["E",]            

            s = SubseccionConfig.objects.filter(
                    seccion_config__aspecto_config__tabulador = tabulador,
                    creado_en__isnull = True,
                    tipo_subseccion__abreviacion = tipo_requisitos
                ).distinct(
                    'seccion_config'
                ).values('seccion_config')

            #
            # Estructura completa se subsecciones existentes
            #
            for e in s:

                temp = {}
                temp_acum = []

                sc = SeccionConfig.objects.get(id=e['seccion_config'])

                secciones_empty.append(sc.id)
                aspectos_empy = [sc.aspecto_config.id]

                sbsc = SubseccionConfig.objects.filter(
                    seccion_config = sc,
                    subseccion_config_padre__isnull = True
                ).order_by('tipo_subseccion')

                for e in sbsc :                        
                    temp_acum.append(bob.preorder({}, e, 0, 0, None, user, True, clone))

                inter = {
                    "name": sc.aspecto_config.nombre,
                    "children": [bob.to_root(temp_acum, sc, True, clone)],
                    "content": [],
                    "id": (-1 if clone else 1)*sc.aspecto_config.id,
                    "state": "done" if not clone else "added",
                    "type": "AF",
                    "extra": {
                        "tipo_aspecto": sc.aspecto_config.tipo_aspecto.id,
                        "tipo_aspecto_text": sc.aspecto_config.tipo_aspecto.abreviacion
                    }
                }

                if sc.aspecto_config.tipo_aspecto.abreviacion == "E":
                    inter['extra'].update({
                        "percent": str(sc.aspecto_config.peso_porcentual)
                    })

                tabulador_json.append(inter)            
            #
            # Secciones que no poseen elementos del tipo subseccion
            #
            for se in SeccionConfig.objects.filter(aspecto_config__tabulador = tabulador, aspecto_config__tipo_aspecto__abreviacion__in= taf).exclude(id__in=secciones_empty):
                aspectos_empy.append(se.aspecto_config.id)
                inter = {
                    "name": se.aspecto_config.nombre,
                    "children": [bob.to_root([], se, True, clone)],
                    "content": [],
                    "id": (-1 if clone else 1)*se.aspecto_config.id,
                    "state": "done" if not clone else "added",
                    "type": "AF",
                    "extra": {
                        "tipo_aspecto": se.aspecto_config.tipo_aspecto.id,
                        "tipo_aspecto_text": se.aspecto_config.tipo_aspecto.abreviacion
                    }
                }

                if se.aspecto_config.tipo_aspecto.abreviacion == "E":
                    inter['extra'].update({
                        "percent": str(se.aspecto_config.peso_porcentual)
                    })

                tabulador_json.append(inter)
            #
            # Aspectos que no poseen secciones
            #
            for ae in AspectoFundamentalConfig.objects.filter(tabulador = tabulador, tipo_aspecto__abreviacion__in= taf).exclude(id__in=aspectos_empy):
                inter = {
                    "name": ae.nombre,
                    "children": [],
                    "content": [],
                    "id": (-1 if clone else 1)*ae.id,
                    "state": "done" if not clone else "added",
                    "type": "AF",
                    "extra": {
                        "tipo_aspecto": ae.tipo_aspecto.id,
                        "tipo_aspecto_text": ae.tipo_aspecto.abreviacion
                    }
                }

                if ae.tipo_aspecto.abreviacion == "E":
                    inter['extra'].update({
                        "percent": str(ae.peso_porcentual)
                    })

                tabulador_json.append(inter)

            return tabulador_json

        else:
            raise Exception("El valor tipo_requisito debe ser un tipo de requisito valido dentro de las especificaciones del tabulador")        

    def get(self, request, *args, **kwargs):

        try:
            id_tabulador = int(kwargs["tabulador"])
            clone = request.GET["clonado"] == "true"
            jsontmp = {"success": "OK"}
            code = 200
            main_config_cookie = []
            documental_req_cookie = []
            specific_value_cookie = []
            user = request.user

            # Reconstruir información basica:
            tabulador = Tabulador.objects.get(id=id_tabulador)
            tabulador_id = tabulador.id

            if clone:
                tabulador_new = Tabulador(
                    tipo_pst_id = tabulador.tipo_pst.id,
                    nombre = tabulador.nombre +"_copia_"+datetime.datetime.now().strftime('%d%m%Y%H%M%S'),
                    fecha_creacion=datetime.datetime.now(),
                    version_actual = tabulador.version_actual
                )
                tabulador_new.save()
                tabulador = tabulador_new

            main_config_cookie.append(
                {
                    "id": tabulador.id, 
                    "name": tabulador.nombre, 
                    "type": tabulador.tipo_pst.id,
                    "state": "done",
                    "version_actual": tabulador.version_actual
                }
            )

            jsontmp.update({'version': len(Tabulador.objects.filter(tipo_pst=tabulador.tipo_pst,version_actual=True))})
            jsontmp.update({"main_config_cookie": main_config_cookie})

            # Reconstruir Requisitos Documentales:
            rd_list = SubseccionConfig.objects.filter(
                (Q(tipo_subseccion__abreviacion="RD")|Q(tipo_subseccion__tipopadre__abreviacion="RD")) ,
                Q(seccion_config__aspecto_config__tabulador_id = tabulador_id)
            )

            for rd in rd_list:
                documental_req_cookie.append({
                    "id": (-1 if clone else 1)*rd.id,
                    "state": "done" if not clone else "added",
                    "name": rd.nombre,
                    "type": rd.tipo_subseccion.id,
                    "extra": {
                        "texttype": rd.tipo_subseccion.nombre
                    }
                })
            jsontmp.update({"documental_req_cookie": documental_req_cookie})


            # Reconstruir Valores Especificos:
            ve_list = Indicador.objects.filter( 
                tabulador_id= tabulador_id
            )

            for ve in ve_list:
                specific_value_cookie.append({
                    "id": (-1 if clone else 1)*ve.id,
                    "state": "done" if not clone else "added",
                    "name": ve.nombre,
                    "suministrado": "Si" if ValorIndicador.objects.get(indicador = ve, respuesta_config__tipo_respuesta__codigo="VE").suministrado else "No",
                    "valor": ValorCategoria.getValoresCategoria(ve),
                })

            jsontmp.update({"specific_value_cookie": specific_value_cookie})

            # Reconstruccion de Requisitos Basico y Requisitos Especificos            
            bob = GenerarTabulador()
            basic_req = self.reconstruirRequisitos(Tabulador.objects.get(id=tabulador_id), "RB", user, clone)
            specific_req = self.reconstruirRequisitos(Tabulador.objects.get(id=tabulador_id), "RE", user, clone)

            jsontmp.update({"basic_req": basic_req})
            jsontmp.update({"specific_req": specific_req})

        except Exception, e:
            jsontmp = {"error": str(e)}
            code = 400

        return HttpResponse(
            json.dumps(jsontmp, sort_keys=True),
                content_type="application/json",
                status = code
            )

"""
    Definiciones de vistas para generacion y despliegue de instrumentos de evaluacion
"""
class VisorTabulador(View):

    def get(self, request, *args, **kwargs):        
        tipo = ''
        tabulador = ''
    
        if kwargs.has_key('tabulador'):
            tabulador = int(kwargs['tabulador'])
            
        if kwargs.has_key('tipo'):
            tipo = kwargs['tipo']
     
        m = get_models(APP)
        context = {
            'modelo': 'tabulador',
            'modelos': model_list.get_model_list_nuevo(m),
            'show_name': 'Tabulador',
            'actor': 'administrador',
            'administrador': True,
            'tabulador': tabulador,
            'tipo': tipo
        }

        return render(
            request,
            'administrador/ver_tabulador.html',
            context
        )

    def post(self, request, *args, **kwargs):
        #
        # Este metodo permite realizar el almacenamiento de datos de manera 
        # temporal en memoria cache para permitir la visualizacion del tabulador
        #
        try:
            if request.POST.has_key('main-config-cookie') and request.POST.has_key('documental-req-cookie') and request.POST.has_key('specific-values-cookie') and request.POST.has_key('basic-req') and request.POST.has_key('specific-req') and request.POST.has_key('cookies-ids'):
                data = {
                    'main-config-cookie': json.loads(request.POST['main-config-cookie']),
                    'documental-req-cookie': json.loads(request.POST['documental-req-cookie']),
                    'specific-values-cookie': json.loads(request.POST['specific-values-cookie']),
                    'basic-req': json.loads(request.POST['basic-req']),
                    'specific-req': json.loads(request.POST['specific-req']),
                    'cookies-ids': json.loads(request.POST['cookies-ids'])
                }

                request.session["data_tabulador_%s" % (request.user.rif)] = data
                
            jsontmp = {
                "success_msg":"LocalStorage saved with result [OK] - You can proceed now."
            }
        except Exception, e:
            jsontmp = {
                "error_msg":"LocalStorage saved with result [%s] - You can not proceed." % str(e)
            }

        return HttpResponse(
            json.dumps(jsontmp, sort_keys=False),
            content_type="application/json",
            status = 200
        )
        

class OperacionElemVal(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):        
        return super(OperacionElemVal, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        solicit_id = int(kwargs['solicitud'])
        solicitud=Solicitud.objects.get(id=solicit_id)
        res = RespuestaTabulador.objects.filter(solicitud_id =solicit_id).first()
        user = request.user
        edit = False

        try:
            func = Funcionario.objects.get(user=user)
            if func.tiporol.nombre == "inspector" and (solicitud.funcionario == func or solicitud.funcionario_extra == func):
                edit = True
        except Funcionario.DoesNotExist:
            pass
        dprint(kwargs['operacion'])
        if kwargs['operacion'] == 'observaciones' and kwargs.has_key('subseccion'):
            dprint(kwargs['operacion'])
            subsecc_id = int(kwargs['subseccion'])
            if res:
                try:
                    subsecc = Subseccion.objects.get(
                        subseccion_config_id=subsecc_id, respuesta_tabulador=res
                    )
                    if subsecc.observacion:
                        observ = subsecc.observacion
                    else:
                        observ=""

                    jsontmp={
                        "err_msg": "",
                        "success_msg": "OK",
                        'data':{
                            'observacion': observ
                        } 
                    }
                except Subseccion.DoesNotExist:
                    jsontmp={
                        "err_msg": "",
                        "success_msg": "",
                        'data':{
                            'observacion': u'No se han registrado observaciones'
                        }
                    }
                if edit:
                    jsontmp['data'].update({
                        'editar': True    
                    })
                else:
                    jsontmp['data'].update({
                        'editar': False    
                    })
            else:
                jsontmp={
                    "err_msg": "No existe un respuesta asociada a este tabulador",
                    "success_msg": "",
                }
            dprint(jsontmp["err_msg"])
            if jsontmp['err_msg']=="":
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 200
                )
            else:
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 400
                )
        elif kwargs['operacion'] == 'imagenes':
            if request.GET['info']:

                values = secure_value_decode(request.GET['info']).split("_")

                dprint(values = values)
                
                s = int(values[2])
                af = int(values[1])
                sbsc = int(values[3])
                valor_respuesta = int(values[4])
                """
                values = secure_value_decode(request.GET['info']).split("_")
                s = int(values[3])
                af = int(values[2])
                sbsc = int(values[4])
                puntaje = float(values[0])
                valor_respuesta = int(values[5])
                """
                no_tienen = []
                tienen = []
                subsec_conf = SubseccionConfig.objects.filter(
                    seccion_config__aspecto_config=af, 
                    seccion_config_id=s,
                )
                dprint(subsec_conf=subsec_conf)
                if len(subsec_conf)>0:
                    for e in subsec_conf:
                        if e.subs_imagen == True:
                            try:
                                subseccio = Subseccion.objects.get(
                                    respuesta_tabulador__solicitud__id= solicit_id,
                                    subseccion_config=e
                                )
                                dprint(subseccio=subseccio)
                                try:
                                    sub_archiv = SubseccionArchivoRequisito.objects.get(
                                        subseccion=subseccio
                                    )
                                    dprint(sub_archiv=sub_archiv)
                                    tienen.append((e.nombre, e.id, str(sub_archiv.requisito_digital.file_path.url), sub_archiv.requisito_digital.extension))
                                except SubseccionArchivoRequisito.DoesNotExist:
                                    no_tienen.append((e.nombre , e.id))

                            except Subseccion.DoesNotExist:
                                no_tienen.append((e.nombre , e.id))
                                continue                   
                    
                    if len(tienen)==0 and len(no_tienen)==0:
                        jsontmp ={
                            'err_msg':"",
                            'success_msg':"OK"
                        }
                    else:
                        jsontmp ={
                            'err_msg':"",
                            'success_msg':"OK",
                            'data': {
                                'tienen': tienen,
                                'no_tienen': no_tienen,
                            }
                        }
                        if edit:
                            jsontmp['data'].update({
                                'editar': True    
                            })
                        else:
                            jsontmp['data'].update({
                                'editar': False    
                            })
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json",
                        status = 200
                    )
            jsontmp = {
                "err_msg": "Parametros invalidos o subseccion invalida",
                "success_msg":""
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=False),
                content_type="application/json",
                status = 400
            )


    def post(self, request, *args, **kwargs):
        solicit_id = int(kwargs['solicitud'])
        if kwargs['operacion'] == 'observaciones' and kwargs.has_key('subseccion'):
            subsecc_id = int(kwargs['subseccion']);
            subsecc_config = SubseccionConfig.objects.filter(id=subsecc_id).first()
            if request.POST['observacion']:
                res = RespuestaTabulador.objects.filter(solicitud_id =solicit_id).first()
                if res:
                    try:
                        if subsecc_config:
                            subsecc = Subseccion.objects.get(
                                subseccion_config_id=subsecc_id, respuesta_tabulador=res
                            )
                            subsecc.observacion = request.POST['observacion']
                            subsecc.save()

                            jsontmp={
                                "err_msg": "",
                                "success_msg": "OK",
                            }
                        else:
                            jsontmp={
                                "err_msg": "La subseccion config seleccionada no existe",
                                "success_msg": "",
                            }
                    except Subseccion.DoesNotExist:
                        if subsecc_config:
                            subsecc = Subseccion(
                                nombre = "subseccion_%s_%s" % (
                                    request.user.rif,
                                    datetime.datetime.now().strftime('%d-%m-%Y')
                                ),
                                observacion= request.POST['observacion'],
                                tipo_subseccion = subsecc_config.tipo_subseccion,
                                subseccion_config = subsecc_config,
                                respuesta_tabulador = res
                            )
                            subsecc.save()
                            jsontmp={
                                "err_msg": "",
                                "success_msg": "OK",
                            }
                        else:
                            jsontmp={
                                "err_msg": "La subseccion config seleccionada no existe",
                                "success_msg": "",
                            }
                else:
                    jsontmp={
                        "err_msg": "No existe esa respuesta a este tabulador",
                        "success_msg": "",
                    }
            else:
                jsontmp={
                    "err_msg": "Parametros Incompletos",
                    "success_msg": "",
                }
            if jsontmp['err_msg'] == "":
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 200
                )
            else:
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 400
                )
        elif kwargs['operacion'] == 'imagenes':
            solicit_id= int(kwargs['solicitud'])
            dprint(files=request.FILES)
            error_formato=False
            error=False
            jsontmp={'data':[]}
            for e in request.FILES:
                aux =int(e)
                formato = val(
                    request.FILES, 
                    e,
                    ['image/jpeg', 'image/png'] ,
                    2621440
                )
                if formato:
                    try:
                        subsecc_config= SubseccionConfig.objects.get(id=aux)
                        rt = RespuestaTabulador.objects.get(
                            solicitud_id=solicit_id
                        )
                        try:
                            subsecc = Subseccion.objects.get(
                                subseccion_config_id = aux,
                                respuesta_tabulador__solicitud_id = solicit_id,
                            )
                            dprint(subsecc=subsecc)    
                        except Subseccion.DoesNotExist:
                            subsecc = Subseccion(
                                nombre = "subseccion_%s_%s" % (
                                    request.user.rif,
                                    datetime.datetime.now().strftime('%d-%m-%Y')
                                ),
                                tipo_subseccion = subsecc_config.tipo_subseccion,
                                subseccion_config = subsecc_config,
                                respuesta_tabulador = rt
                            )
                            dprint(subsecc_nueva=subsecc)
                            subsecc.save()
                        
                        data = Storage(
                            solicitud = Solicitud.objects.get(id=solicit_id),
                            file_path = request.FILES[e],
                            nombre = "%s_%s_%s_%s" % (str(rt.pst.user.rif), str(request.user.rif), str(aux), str(solicit_id)),
                            extension = formato.split("/")[1]
                        )
                        dprint("guardando imagen")
                        try:
                            rd = RequisitoDigital.objects.get(
                                nombre = data.nombre
                            )
                            rd.solicitud = data.solicitud
                            rd.file_path = data.file_path
                            rd.nombre = data.nombre
                            rd.extension = data.extension
                            rd.save()
                        except RequisitoDigital.DoesNotExist:
                            rd = RequisitoDigital.create(data)
                            rd.save()
                            rel = SubseccionArchivoRequisito(
                                subseccion = subsecc,
                                requisito_digital = rd
                            )
                            rel.save()
                        if error_formato == False or error == False:
                            jsontmp.update({
                                "err_msg":"",
                                "success_msg":"Imagenes subidas correctamente",

                            })
                    except SubseccionConfig.DoesNotExist:
                        error=True
                        jsontmp.update({
                            "err_msg":"Alguna de las subsecciones seleccionadas no se encuentra, introduzca nuevamente",
                            "success_msg":"",
                            "data":[]
                        })

                else:
                    if error == False:
                        error_formato=True
                        try:
                            subsecc_config= SubseccionConfig.objects.get(id=aux)
                            jsontmp.update({
                                "err_msg":"Las imagenes subidas son incorrectas",
                                "success_msg":"",
                            })
                            jsontmp['data'].append(subsecc_config.nombre)
                        except SubseccionConfig.DoesNotExist:
                            error=True
                            jsontmp.update({
                                "err_msg":"Alguna de las subsecciones seleccionadas no se encuentra, introduzca nuevamente",
                                "success_msg":"",
                                "data":[]
                            })
            if error_formato or error:
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 400
                )
            else:
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status = 200
                )         
            

class GenerarTabulador(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):        
        return super(GenerarTabulador, self).dispatch(*args, **kwargs)

    @classmethod    
    def to_root(
            self, 
            d, 
            it, 
            restoration_call=False,
            clone_call = False
        ):
        """
            Obtiene el cuerpo del tabulador partiendo
            de las una seccion it
        """
        toor = False
        while not it == None:
            if restoration_call:
                d = {
                    "name": it.nombre,
                    "children": d if type(d) == list else [d],
                    "content": [],
                    "id": (-1 if clone_call else 1) * it.id,
                    "state": "done" if not clone_call else "added",
                    "type": "S"
                }
            else:                
                d = {it.nombre: d}
                if it is not None and not toor:
                    d[it.nombre].update({'toor': True})
                    d[it.nombre].update({'nsec': it.nombre})
                    toor = True
            it = it.seccion_padre_config
        return d

    @classmethod
    def traducir_respuesta(
            self,
            user = None,
            sid=None, 
            rcfg=None, 
            t=None, 
            af=None, 
            s=None,
            gid = None,
            sbsc=None,
            desactivar = False,
            valores_asociados = False,            
            solicitud = None,
            valores_obligatorios = True
            ):
        """
            Parametros de entrada:
            ~~~~~~~~~~~~~~~~~~~~~
            - user: usuario que se encuentra actualmente en el sistema
            - sid: id de la subseccion config que estamos traduciendo
            - rcfg: Respuesta Config
            - t: Tabulador
            - af: Aspecto AspectoFundamental
            - s: Seccion
            - gid: identificador del grupo al que pertenece la respuesta
            - sbsc: SubseccionConfig
            - desactivar: Permite generar un tabulador con todos 
            - valores_obligatorios: Permite especificar si se desea que todos los campos sean obligatorios
            los inputs desactivados
                (
                    -1 en este atributo significa que no posee padre
                    dentro de las subsecciones
                )
            - valores_asociados: Permite retornar los valores asociados a
            la respuesta config si es el caso de que los tenga en el cuerpo
            del tabulador almacenado
            - solicitud: identificador de la seccion, permite saber a que 
            solicitud estan asociadas las respuestas a ser renderizadas
        """

        try:
            v  = None
            str_out = ''
            tiene_respuesta = False
            name = rcfg.tipo_respuesta.nombre.lower().replace(' ','_')
            value = None
            subseccion_object = SubseccionConfig.objects.get(id = sid)

            if rcfg.tipo_respuesta.input_type in ['file', 'radio', 'input']:

                itype = rcfg.tipo_respuesta.input_type

                # String format for representation
                # %[flags][width][.precision]type
                size_bootstrap = 4 if rcfg.tipo_respuesta.input_type in ['file', 'input'] else 3
                placeholder = ["Ingrese su respuesta aqui",]
                input_str = '<div class="col-lg-{d[size_bootstrap]} col-xs-{d[size_bootstrap]} col-md-{d[size_bootstrap]}" style="height: 0px;" group="{d[group]}"> <input type="{d[tipo]}" name="{d[nombre]}" id="{d[id]}" placeholder = "{d[placeholder]}" class="form-control generated-input"'
                input_str += ' disabled = "disabled"' if desactivar else ''
                input_str += ' value="{d[value]}" {d[checked]} ' +('required' if not subseccion_object.tipo_subseccion.abreviacion in ['RB', 'RE'] else '')+ '/> &nbsp;{d[label]}</div>'

                values = RespuestaValorRespuesta.objects.filter(
                        pregunta_config = rcfg
                    )

                #dprint(
                #    desactivar = desactivar,
                #    valores_asociados =valores_asociados,
                #    valores_obligatorios =valores_obligatorios,
                #    subseccion_id = sid,
                #    subseccion_config = sbsc,
                #    solicitud = solicitud,
                #    tipo_respuesta = rcfg.tipo_respuesta.nombre.lower().replace(' ','_'),
                #    values = values
                #)

                """
                    Normalizar aquellos posibles valores de respuesta que
                    puedan tener mas de un elemento de interfaz de entrada 
                    como valores de rango (flatten)
                """
                if rcfg.tipo_respuesta.nombre.lower() == 'rango':
                    values = [values.first()]

                if valores_asociados and solicitud is not None:                 
                    try:
                        subseccion = Subseccion.objects.get(
                            subseccion_config_id = sid,
                            respuesta_tabulador__solicitud_id = solicitud
                        )

                        if subseccion:

                            """
                                En caso de que se soliciten los valores asociados
                                y de que los mismos existan se coloca entonces 
                                se valor que se ha guardado
                            """

                            tiene_respuesta = ValorRespuesta.objects.get(
                                subseccion_id = subseccion.id
                            )

                    except Exception, e:
                        pass

                if not len(values) and name in ['formula', 'valor_especifico']:
                    values = []
                    values.append(rcfg)

                for v in values:

                    if itype == 'file':
                        str_out += '<i class="fa fa-upload"></i>'
                        continue
                    
                    inter = v if name in ['formula', 'valor_especifico'] else v.respuesta_config

                    if isinstance(v, RespuestaValorRespuesta):
                        inter = v.respuesta_config

                    datos = defaultdict(dict,
                        tipo = itype if itype != 'input' else 'number',
                        t= t.id,
                        id = sid,
                        placeholder = placeholder[0],
                        label = inter.nombre if itype not in ['input', 'file'] else '',
                        value = "",
                        checked = "",
                        size_bootstrap = size_bootstrap,
                        group = gid
                    )

                    val = secure_value(
                        "%d_%d_%d_%d_%d" % (
                            t.id,
                            af.id, s.id,
                            sid,
                            inter.id
                        )
                    )

                    if itype not in ['input', 'file']:
                        datos["nombre"] = sid
                        datos["value"] = val
                    else:
                        datos["nombre"] = val
                        del datos["value"]                        
                    
                    if valores_asociados and tiene_respuesta not in [None, False]:
                        if itype not in ['input', 'file'] and tiene_respuesta.valor_respuesta == inter:
                            datos["checked"] = 'checked'
                        elif itype in ['input', 'file']:
                            datos["value"] = tiene_respuesta.valor

                    str_out += input_str.format(str, d = datos).replace('value="{}"','')

                    if user.role == ROLE_FUNCIONARIO and rcfg.tipo_respuesta.input_type == 'input':
                        str_out +='<div class="col-lg-1 col-md-1 col-sm-1"> <i data-toggle="tooltip" title="Observaciones" id="%d" class="fa fa-list icono-accion observaciones"></i></div>' % (sid,)

                if  name == 'escala':
                    """
                        Respuesta del tipo Bueno-Malo-Deficiente o alguna 
                        evaluada con escala de valores definida
                        Tipo de input HTML : radio
                    """
                    str_out = '<div class="col-lg-6 col-md-6 col-sm-6 radio-item">'+str_out+'</div>'
                    if user.role == ROLE_FUNCIONARIO and solicitud is not None:
                        str_out += '<div class="col-lg-1 col-md-1 col-sm-1">\
                        <i data-toggle="tooltip" title="Observaciones"\
                        id="{d[id]}"\
                        class="fa fa-list icono-accion observaciones"></i>\
                        </div>'.format(
                            str, 
                            d = defaultdict(dict,
                                id = sid
                            )
                        )

                response_json = {
                    'content': str_out, 
                    'gr': gid,
                    'condicion': str(subseccion_object.condicion_posneg).lower()
                }

                return response_json
            else:
                raise e
        except Exception, e:
            raise e

    @classmethod
    def preorder(
            self, 
            d, 
            it, 
            desactivar=0, 
            valores_asociados=0, 
            solicitud = None, 
            user=None,
            restoration_call=False,
            clone_call = False
        ):
        """
            Se realiza recorrido en preorden para 
            obtener el formato de las subsecciones
        """
        if solicitud == None:
            s = SubseccionConfig.objects.filter(
                    subseccion_config_padre_id=it.pk,
                    creado_en__isnull= True
                ).order_by('grupo_repetitivo', 'respuesta_config__tipo_respuesta')
        else:
            s = SubseccionConfig.objects.filter(
                    Q(subseccion_config_padre_id=it.pk),
                    (Q(creado_en__isnull=True)|Q(creado_en__id= solicitud))
                ).order_by('grupo_repetitivo', 'respuesta_config__tipo_respuesta')

        dprint(ELEMENTOS = s)

        sx = s

        if len(s) or it.respuesta_config.tipo_respuesta.codigo.lower() in ['c','rep']:
            if restoration_call:
                if it.respuesta_config.tipo_respuesta.codigo.lower() == 'c':
                    val = RespuestaValorRespuesta.objects.filter(pregunta_config=it.respuesta_config)
                    options = []
                    options_val = []

                    for e in val:
                        options.append(str(e.respuesta_config.id))
                        options_val.append(str(e.respuesta_config.nombre))

                    d['id']=(-1 if clone_call else 1)*it.id 
                    d["name"] = it.nombre
                    d["state"] = "done" if not clone_call else "added"
                    d["content"] = {
                        "extra":[ 
                            SubseccionConfig.objects.filter(subseccion_config_padre_id=it.id, condicion_posneg=True).count(), 
                            SubseccionConfig.objects.filter(subseccion_config_padre_id=it.id, condicion_posneg=False).count()
                            ],
                        "options": options,
                        "options_val":options_val,
                        "condicion": it.condicion_posneg
                    }
                    d['condicion']= str(it.condicion_posneg).lower()
                    d["children"] = []
                    d['parent'] = {
                        "id": it.seccion_config.id,
                        "type": "S"
                    }
                    d["type"] = "SS"
                    d["extra"]={
                        "subtype": "C"
                    }
                elif it.respuesta_config.tipo_respuesta.codigo.lower() == 'rep':
                    d["id"] = (-1 if clone_call else 1)*it.id
                    d["name"] = it.nombre
                    d["state"] = "done" if not clone_call else "added"
                    d["content"] = {
                        "repetition":[str(e.repeticion) for e in Relevancia.objects.filter(subseccion_config=it)],
                        "condicion": it.condicion_posneg
                    }
                    d["children"] = []
                    d['parent'] = {
                        "id": it.seccion_config.id,
                        "type": "S"
                    }
                    d["type"] = "SS"
                    d["extra"]={
                        "subtype": "REP"
                    }
            else:
                d.update({it.nombre:{}})                
                if it.respuesta_config.tipo_respuesta.codigo.lower() == 'c':
                    d.update({it.nombre: {'condicion':  str(it.condicion_posneg).lower(), 'id': it.id}})
                elif it.respuesta_config.tipo_respuesta.codigo.lower() == 'rep':
                    d.update({'repetitive': 'repetitive'})

        elif not restoration_call:
            d.update(
                {
                    it.nombre: self.traducir_respuesta
                    (
                        user,
                        it.id,
                        it.respuesta_config,
                        it.seccion_config.aspecto_config.tabulador,
                        it.seccion_config.aspecto_config,
                        it.seccion_config,
                        it.grupo_repetitivo,
                        it.subseccion_config_padre,
                        valores_asociados = valores_asociados,
                        desactivar = desactivar,
                        solicitud = solicitud
                    )           
                }
            )
        else:
            d["id"]= (-1 if clone_call else 1)*it.id
            d['name'] = it.nombre
            d['state'] = "done" if not clone_call else "added"
            d['children'] = []
            d['parent'] = {
                "id": it.seccion_config.id,
                "type": "S"
            }
            d["type"] = "SS"

            # Caso respuesta a traducir del tipo escala y dual son equivalentes
            if it.respuesta_config.tipo_respuesta.codigo in ["E", "D"]:
                d["extra"] = {
                    "subtype": it.respuesta_config.tipo_respuesta.codigo
                }
                l = RespuestaValorRespuesta.objects.filter(pregunta_config = it.respuesta_config)
                r =  Relevancia.objects.filter(subseccion_config=it).order_by("categoria__valor")
                relevance = []
                
                mx = Categoria.objects.filter(
                    tipo_pst = it.seccion_config.aspecto_config.tabulador.tipo_pst
                ).order_by("valor")

                i = 0
                for e in mx:
                    if i < len(r):
                        relevance.append(e == r[i].categoria)

                        if e == r[i].categoria:
                            i+=1
                    else: 
                        relevance.append(False)
                
                d['content'] = {
                    'options':[str(e.respuesta_config.id) for e in l],
                    'options_val':[e.respuesta_config.nombre for e in l],
                    "relevance" : relevance,
                    "condicion": it.condicion_posneg
                }
            # Caso respuesta a traducir del tipo rango            
            elif it.respuesta_config.tipo_respuesta.codigo == "R":
                d["extra"] = {
                    "subtype": "R"
                }

                l = RespuestaValorRespuesta.objects.filter(
                    pregunta_config = it.respuesta_config
                ).order_by("respuesta_config__categoria__valor")
                relevance = []
                
                mx = Categoria.objects.filter(
                     tipo_pst = it.seccion_config.aspecto_config.tabulador.tipo_pst
                ).order_by("valor")

                i = 0
                for e in mx:
                    if i < len(l):
                        relevance.append({
                            "inf_aplica": l[i].respuesta_config.limite_inferior != None,
                            "inf_star": l[i].respuesta_config.limite_inferior if l[i].respuesta_config.limite_inferior != None else -1,
                            "sup_aplica": l[i].respuesta_config.limite_superior != None ,
                            "sup_star": l[i].respuesta_config.limite_superior if l[i].respuesta_config.limite_superior != None else -1
                        })

                        if l[i].respuesta_config.limite_inferior or l[i].respuesta_config.limite_superior:
                            i+=1
                    else: 
                        relevance.append({
                            "inf_aplica": False,
                            "inf_star": -1,
                            "sup_aplica": False,
                            "sup_star": -1
                        })

                d['content'] = {
                    'unit': it.respuesta_config.tipo_medida.id,
                    'unit_representation':it.respuesta_config.tipo_medida.nombre,
                    'relevance_value': relevance,
                    "condicion": it.condicion_posneg
                }
            # Caso respuesta a traducir del tipo formula
            elif it.respuesta_config.tipo_respuesta.codigo == "F":
                d["extra"] = {
                    "subtype": "F"
                }

                # Componentes de la formula en su orden de aparicion en la misma
                v = ValorIndicador.objects.filter(
                    respuesta_config = it.respuesta_config
                ).order_by("orden")
                r = Relevancia.objects.filter(subseccion_config=it).order_by("categoria__valor")
                formula_elements = []
                logical_per_category = []

                i = 0
                e = v[0]
                izq_stack = []
                der_stack = []

                while i<len(v):

                    if e.operador_izquierdo != None and ((e.operador_izquierdo!=None and len(der_stack) and der_stack[len(der_stack)-1] != e.operador_izquierdo.id)or not len(der_stack)):
                        izq_stack.append(e.operador_izquierdo.id)
                        formula_elements.append({
                            "type": "operador",
                            "id": e.operador_izquierdo.id,
                            "name": e.operador_izquierdo.representacion
                        })

                    formula_elements.append({
                        "type": "operando",
                        "id": e.indicador.id,
                        "name": e.indicador.nombre
                    })

                    if e.operador_derecho != None and ((e.operador_derecho!=None and len(izq_stack) and der_stack[len(izq_stack)-1] != e.operador_derecho.id)or not len(izq_stack)):
                        der_stack.append(e.operador_derecho.id)
                        formula_elements.append({
                            "type": "operador",
                            "id": e.operador_derecho.id,
                            "name": e.operador_derecho.representacion
                        })
                    i+=1
                    e = v[i] if i < len(v) else None

                for m in r:
                    logical_per_category.append(str(m.operador_logico.id))

                d['content'] = {
                    'formula-elements': formula_elements,
                    'logical_per_category': logical_per_category,
                    "condicion": it.condicion_posneg
                }

        for e in s:
            inter = {}
            if not restoration_call:
                d[it.nombre].update(
                    self.preorder(
                        d[it.nombre],
                        e,
                        desactivar = desactivar,
                        valores_asociados = valores_asociados,
                        solicitud = solicitud,
                        user = user,
                        restoration_call = restoration_call,
                        clone_call = clone_call
                    )
                )
            else:
                self.preorder(
                    inter,
                    e,
                    desactivar = desactivar,
                    valores_asociados = valores_asociados,
                    solicitud = solicitud,
                    user = user,
                    restoration_call = restoration_call,
                    clone_call = clone_call
                )
                d["children"].append(inter)

        return d

    def get(self, request, *args, **kwargs):
        try:
        
            #
            #> Comentar para: mejorar performance en tiempo
            #> Descomentar para: deshabilitar el mecanismo de memoria cache (debug)
            #
            cache.clear()

            data_set = {}
            user = request.user
            key = 'none'

            """
                Se toma el id del tabulador actual en cuanto a la sesion
                o al que se desee visualizar en ese momento por medio del
                panel administrativo
            """

            if kwargs.has_key('tabulador'):
                data_set.update({'tabulador': int(kwargs['tabulador'])})

            if kwargs.has_key('solicitud'):
                data_set.update({'solicitud': int(kwargs['solicitud'])})

            if kwargs.has_key('tipo'):
                data_set.update({'tipo': kwargs['tipo']} )

            if kwargs.has_key('desactivar'):
                data_set.update({'desactivar': int(kwargs['desactivar'])})

            if kwargs.has_key('valores_asociados'):
                data_set.update({'valores_asociados': int(kwargs['valores_asociados'])})

            if kwargs.has_key('operacion'):
                data_set.update({'operacion': int(kwargs['operacion'])})

            ## Carga de requisitos completada ahora se procede a determinar la clave
            ## para el uso de memoria cache           

            if not data_set.has_key('tipo') or (data_set.has_key('tipo') and data_set['tipo'] == "*"):
                dprint("uso memoria cache tabulador: %d" % (data_set['tabulador'],))
                key = 'mintur-cachedtabulador_%d_admin' % (data_set['tabulador'])
            
            elif data_set.has_key('solicitud') and data_set.has_key('tipo'):
                dprint("uso memoria cache tabulador: %d solicitud: %d" % (data_set['tabulador'], data_set['solicitud']))
                key = 'mintur-cachedtabulador_%d_%d' % (data_set['tabulador'], data_set['solicitud'])
            
            elif data_set.has_key('tipo') and data_set.has_key('solicitud'):
                dprint("uso memoria cache tabulador: %d tipo: %s solicitud: %d" % (data_set['tabulador'], data_set['tipo'], data_set['solicitud']))
                key = 'mintur-cachedtabulador_%d_%s_%d_%s' % (data_set['tabulador'], data_set['tipo'], data_set['solicitud'], request.user.rif)
                dprint(on_tabulador = key)
            
            if cache.get(key) is not None:                
                return HttpResponse(
                  cache.get(key),
                  content_type="application/json",
                  status = 200
                )
            else:
                t = Tabulador.objects.get(id=data_set['tabulador'])

                if not data_set.has_key('tipo') or data_set['tipo'] == '*':
                    # Es el administrador quien esta consultando los elementos
                    # por tanto solo se generara un tabulador para los requisitos
                    # configurados en el panel administrativo, excluyendo los que
                    # sean creados de manera dinamica por los prestadores

                    s = SubseccionConfig.objects.filter(
                            seccion_config__aspecto_config__tabulador = t,
                            creado_en__isnull = True
                        ).distinct(
                            'seccion_config'
                        ).values('seccion_config', 'respuesta_config__tipo_respuesta__codigo')
                else:
                    if data_set['tipo'].lower() == 've':
                        # Es un funcionario diferente consultando los valores especificos
                        # Dado que no esta permitida la creacion dinamica de VEs no se 
                        # emplea el filtro de VEs (creado_en)

                        s = SubseccionConfig.objects.filter(
                                seccion_config__aspecto_config__tabulador = t,
                                tipo_subseccion__abreviacion = data_set['tipo'],
                                suministrado = True,
                                creado_en__isnull = True
                            ).distinct(
                                'seccion_config'
                            ).values('seccion_config', 'respuesta_config__tipo_respuesta__codigo')
                    else:
                        # Es un funcionario diferente consultando RDs,RBs o REs
                        # En este caso los RDs,RBs y REs pueden ser creados de manera dinamica
                        # por lo que es necesario aplicar un filtro particular en caso de que se 
                        # suministre un ID de solicitud para tal fin

                        if data_set.has_key('solicitud'):
                            s = SubseccionConfig.objects.filter(
                                Q(seccion_config__aspecto_config__tabulador = t),
                                Q(tipo_subseccion__abreviacion = data_set['tipo']),
                                (Q(creado_en__id=data_set['solicitud'])|Q(creado_en__isnull=True))
                            ).distinct(
                                'seccion_config'
                            ).values('seccion_config', 'respuesta_config__tipo_respuesta__codigo')

                        else:
                            s = SubseccionConfig.objects.filter(
                                seccion_config__aspecto_config__tabulador = t,
                                tipo_subseccion__abreviacion = data_set['tipo'],
                                creado_en__isnull=True
                            ).distinct(
                                'seccion_config'
                            ).values('seccion_config', 'respuesta_config__tipo_respuesta__codigo')

                tabulador_json = {}
                sc_a = []
                sbsc_a = []
                temp = {}

                dprint(s)

                for e in s:

                    temp = {}
                    sc = SeccionConfig.objects.get(id=e['seccion_config'])
                    
                    filtro = {
                        "seccion_config": sc,
                        "subseccion_config_padre__isnull":True
                    }
                    
                    if not data_set.has_key("tipo") or data_set['tipo'].lower() in  ['*', 've']:
                        # Para los elementos vistos por el administrador o los 
                        # que sea VEs explicitamente

                        sbsc = SubseccionConfig.objects.filter(
                            seccion_config = sc, 
                            subseccion_config_padre__isnull = True,
                            creado_en__isnull = True
                        ).order_by('tipo_subseccion')

                    elif data_set.has_key("tipo") and data_set.has_key("solicitud"):
                        # Para los RDs, REs, RBs explicitamente

                        sbsc = SubseccionConfig.objects.filter(
                            Q(seccion_config = sc),
                            Q(subseccion_config_padre__isnull = True),
                            ( Q(creado_en__isnull = True) | Q(creado_en__id = data_set['solicitud']) )
                        ).order_by('tipo_subseccion')

                    for e in sbsc:
                        temp.update(
                            self.preorder(
                                temp,
                                e,
                                data_set['desactivar'] if data_set.has_key('desactivar') else None,
                                data_set['valores_asociados'] if data_set.has_key('valores_asociados') else None,
                                data_set['solicitud'] if data_set.has_key('solicitud') else None,
                                user
                            )
                        )

                    if not tabulador_json.has_key(sc.aspecto_config.nombre):
                        tabulador_json.update({sc.aspecto_config.nombre:[]})
                    
                    r = self.to_root(temp, sc)

                    tabulador_json[sc.aspecto_config.nombre].append(r)


                for k,v in tabulador_json.items():
                    v.sort()

                tabulador_json = {
                    t.nombre: tabulador_json
                }

                jsontmp = {
                    "success_msg": "OK",
                    "data": tabulador_json
                }

                cache.set(
                    key,
                    json.dumps(jsontmp, sort_keys=True)
                )

                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=True),
                    content_type="application/json",
                    status = 200
                )
        except Exception, e:
            jsontmp = {
                "err_msg": "Errores encontrados al momento de crear objeto del tabulador: "+str(e),
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=False),
                content_type="application/json",
                status = 400
            )


#####################################
#                                   #
# Carga de Requisitos Documentales  #
#                                   #
#####################################

class CargarReqDoc(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CargarReqDoc, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):   

        sid = None
        if kwargs.has_key('solicitud'):
            sid = kwargs['solicitud']
        else:
            raise Exception("Url no valido o mal configurado")

        # Requisitos documentales asociados a este prestador
        
        solicitud = Solicitud.objects.get(id = sid)

        rdp = SubseccionConfig.objects.filter(
            Q(seccion_config__aspecto_config__tabulador = solicitud.tabulador) &
            (
                Q(tipo_subseccion__abreviacion = constants.TIPO_SUBSECCIONES['req_doc']) | Q(tipo_subseccion__tipopadre__abreviacion = constants.TIPO_SUBSECCIONES['req_doc'])
            )&
            (Q(creado_en = solicitud)|Q(creado_en__isnull=True))
        ).order_by('tipo_subseccion__tipopadre__abreviacion')

        contratos_servicio = []
        others = []
        name_contratos_servicio = ''
        name_others = ''

        for e in rdp:  
            res = Subseccion.objects.filter(                    
                    Q(respuesta_tabulador__pst = solicitud.pst),
                    Q(tipo_subseccion__abreviacion = constants.TIPO_SUBSECCIONES['req_doc'])|Q(tipo_subseccion__tipopadre__abreviacion = constants.TIPO_SUBSECCIONES['req_doc']),
                    Q(subseccion_config = e),
                    Q(respuesta_tabulador__solicitud_id = sid)
                )
            
            loaded =  True if len(res) > 0 else False

            elem = (
                SubseccionArchivoRequisito.objects.filter(
                        subseccion = res[0]
                    ).first()
                ) if loaded else None

            name_contratos_servicio = TipoSubseccion.objects.get(abreviacion="CS").nombre
            name_others = TipoSubseccion.objects.get(abreviacion="O").nombre

            if e.tipo_subseccion.abreviacion == constants.TIPO_SUBSECCIONES['req_doc'] or (e.tipo_subseccion.tipopadre is not None and e.tipo_subseccion.tipopadre.abreviacion == constants.TIPO_SUBSECCIONES['req_doc']):
                if e.tipo_subseccion.abreviacion == constants.TIPO_SUBSECCIONES['cont_serv']:
                    
                    # En caso de poseer un subtipo se coloca en listas
                    # independientes
                    contratos_servicio.append({
                        'id':e.id,
                        'name': e.nombre,
                        'loaded': loaded,
                        'url': elem.requisito_digital.file_path.url if loaded else '',
                        'tipo': elem.requisito_digital.extension if loaded else ''
                    })

                elif e.tipo_subseccion.abreviacion == constants.TIPO_SUBSECCIONES['otrs']:
                    # En caso de no poseer un subtipo o que el mismo sea otros se coloca 
                    # siempre en la lista de otros

                    others.append( {
                        'id':e.id,
                        'name': e.nombre,
                        'loaded': loaded,
                        'url': elem.requisito_digital.file_path.url if loaded else '',
                        'tipo': elem.requisito_digital.extension if loaded else ''
                    })    

        l = len(contratos_servicio) + len(others)
        if request.session.has_key('error'):
            errors = request.session['error']
            del request.session['error']
        else:
            errors=""

        context = {
            'solicitud': solicitud,
            'sid': sid,
            'contratos_servicio': contratos_servicio,
            'others': others,
            'error': errors,
            'name_others': name_others,
            'name_contratos_servicio': name_contratos_servicio
        }

        if request.user.role == ROLE_PST:
            context.update({'pst' : solicitud.pst,'natural': True,})
        elif request.user.role == ROLE_FUNCIONARIO:            
            f = Funcionario.objects.get(user = request.user)
            context.update({f.tiporol.nombre: True})

        return render(request, 'pst/requisitos.html', context)

    def post(self, request, *args, **kwargs):
        sid = None
        if kwargs.has_key('solicitud'):
            sid = kwargs['solicitud']
        else:
            raise Exception("Url no valido o mal configurado")

        p = Pst.objects.get(user = request.user)
        t = a = sc = sbsc = rd = None
        solicitud = Solicitud.objects.get(id = int(sid))               
        array_error= []
        condition=False
        guardarycontinuar = 0
        now = datetime.datetime.now()
        
        dprint(primero=request.POST)
        if request.POST.has_key("guardar-continuar-flag"):
            guardarycontinuar = int(request.POST["guardar-continuar-flag"])

        if guardarycontinuar:
            for e in request.FILES:            
                formato = val(
                    request.FILES, 
                    e,
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440
                )

                if formato :
                    try:                    
                        subseccion_config = SubseccionConfig.objects.filter(pk = e).first()
                        pt = Solicitud.objects.get(id = sid).tabulador

                        try:
                            t = RespuestaTabulador.objects.get(pst=p, solicitud_id = sid)
                        except RespuestaTabulador.DoesNotExist:                   
                            t = RespuestaTabulador (
                                solicitud_id = sid,
                                pst = p,
                                tabulador = pt,
                                nombre = 'respuestas_solicitud_%d_%s_%s' % (
                                        int(sid),
                                        request.user.get_full_name(),
                                        now.strftime('%d-%m-%Y')
                                    )
                                )
                            t.save()
                        
                        try:                    
                            sbsc = Subseccion.objects.get(
                                respuesta_tabulador = t,
                                tipo_subseccion = subseccion_config.tipo_subseccion,
                                subseccion_config = subseccion_config
                                )
                        except Subseccion.DoesNotExist:
                            sbsc = Subseccion(
                                nombre = "Requisito Documental",                        
                                respuesta_tabulador = t,
                                tipo_subseccion = subseccion_config.tipo_subseccion,
                                subseccion_config = subseccion_config
                                )
                            sbsc.save()

                        try:
                            data = Storage(
                                solicitud = solicitud,
                                file_path = request.FILES[e],
                                nombre = "%s_%s_%s" % (request.user.rif, sid, e),
                                extension = formato.split("/")[1]
                            )
                        except Exception, e:
                            raise ValidationError(
                                "Errores encontrados al momento de guardar archivos"
                            )

                        try:
                            rd = RequisitoDigital.objects.get(nombre = data.nombre)
                            rd.solicitud = data.solicitud
                            rd.file_path = data.file_path
                            rd.nombre = data.nombre
                            rd.extension = data.extension
                            rd.save()
                        except RequisitoDigital.DoesNotExist:
                            rd = RequisitoDigital.create(data)
                            rd.save()
                            rel = SubseccionArchivoRequisito(
                                subseccion = sbsc,
                                requisito_digital = rd
                                )
                            rel.save()

                    except Exception, e:
                        raise e
                else:
                    condition=True
            
        if (guardarycontinuar == 2 and not validate_requisitos_documentales(solicitud)) or condition ==True:
            if condition:
                request.session['error'] = 'Error con el formato de archivo'
            else:
                request.session['error'] = "No se han registrado en su totalidad los requisitos documentales para esta solicitud"
            return HttpResponseRedirect(
                reverse(
                    'cargar_requisitos', kwargs={
                        'solicitud': sid
                    }
                )
            )
        else:
            if guardarycontinuar == 1:
                return HttpResponseRedirect(
                    reverse(
                        'cargar_requisitos', kwargs={
                            'solicitud': sid
                        }
                    )
                )
            elif guardarycontinuar == 2 or not guardarycontinuar:
                return HttpResponseRedirect(
                    reverse(
                        'valores_especificos', kwargs={
                            'solicitud': sid
                        }
                    )
                )


#####################################################
#                                                   #
# Registrar nuevos requisitos documentales del tipo #
# Contratos de servicio u otros de manera dinamica  #
#                                                   #
#####################################################

class RegistrarDocumentosPST(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(RegistrarDocumentosPST, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        dynamic_doc_data = None
        if request.POST.has_key('caller') and request.POST.has_key('name') :
            dynamic_doc_data = {
                'name': request.POST['name'],
                'caller': request.POST['caller'], 
                'tabulador': int(request.POST['tabulador']),
                'solicitud': int(request.POST['solicitud'])
            }

        try:
            s = SeccionConfig.objects.get(
                aspecto_config__tabulador_id = dynamic_doc_data['tabulador'],
                aspecto_config__nombre = "RD",
                aspecto_config__tipo_aspecto__abreviacion = "RD",
                nombre = "RD"
            )
        except SeccionConfig.DoesNotExist:
            try:
                a = AspectoFundamentalConfig.objects.get( 
                    nombre = "RD",
                    tipo_aspecto__abreviacion = "RD",
                    tabulador_id = dynamic_doc_data['tabulador'],
                )
            except AspectoFundamentalConfig.DoesNotExist:
                a = AspectoFundamentalConfig(
                    nombre = "RD",
                    peso_porcentual = 1,
                    tabulador_id = dynamic_doc_data['tabulador'],
                    tipo_aspecto = TipoAspectoFundamental.objects.get(abreviacion = "RD")
                )
                a.save()

            s = SeccionConfig(
                nombre = "RD",
                aspecto_config = a,
                seccion_padre_config =  None
            )
            s.save()
                
        sb = SubseccionConfig(
                nombre = dynamic_doc_data['name'],
                seccion_config = s,
                tipo_subseccion = TipoSubseccion.objects.get(abreviacion=('CS' if dynamic_doc_data['caller'] == 'cs' else 'O')),
                respuesta_config = RespuestaConfig.objects.get(
                    tipo_respuesta__codigo = "A"),
                subseccion_config_padre = None,
                subs_imagen = True,
                creado_en_id = dynamic_doc_data['solicitud']
            )                        
        sb.save()
    
        return HttpResponse(
            json.dumps({'iddoc': sb.pk}, sort_keys=False),
            content_type="application/json",
            status = 200
        )


################################
#                              #
# Carga de Valores Especificos #
#                              #
################################

class CargarValoresEspecificos(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CargarValoresEspecificos, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Realizar la carga de los requisitos Funcionales
            para las solicitudes de la sucursal seleccionada
        """
        sid = None
        if kwargs.has_key('solicitud'):
            sid = kwargs['solicitud']
        else:
            raise Exception("Url no valido o mal configurado")

        """
            Solicitud actual sobre la que se requieren 
            los requisitos funcionales
        """
        solicitud = Solicitud.objects.get(id = int(sid))       

        """
            Usuario actualmente en el sistema
        """
        user = request.user

        """
            Estado de desactivado y valores_asociados
        """
        t = edicion_autorizada(user, solicitud, typeentry = 'RF')
        desactivar = t[0]
        valores_asociados = t[1]

        """
            Tabulador asociado a la solicitud
        """
        tabulador = solicitud.tabulador
        natural = juridica = False
        context = {}

        if user.role == ROLE_PST:
            pst = Pst.objects.get(user = user)
            if pst.tipo_figura == PERSONA_NATURAL:
                natural = True
            else:
                juridica = True

            context.update({
                    'pst': pst,
                    'natural': natural,
                    'juridica': juridica
                })
        elif user.role == ROLE_FUNCIONARIO:            
            funcionario = Funcionario.objects.get(user = user)
            context.update({
                funcionario.tiporol.nombre: True                
            })
        
        url = reverse(
                    'generar_tabulador',
                    kwargs = {
                        'tabulador':tabulador.id,
                        'solicitud':solicitud.id,
                        'tipo':'VE',
                        'desactivar': desactivar,
                        'valores_asociados': valores_asociados
                    }
                )

        context.update({
            'solicitud': solicitud,
            'actor': user.get_full_name(),
            'tabulador': tabulador.id,
            'tipo': 'VE',
            'desactivar': desactivar,
            'valores_asociados': valores_asociados,
            'url': url
        })

        return render(
            request,
            'valores_especificos.html',
            context
        )

    def post(self, request, *args, **kwargs): 

        try:            
            user = request.user
            context = {}
            goahead = False

            sid = None
            if kwargs.has_key('solicitud'):
                sid = kwargs['solicitud']
                sol = Solicitud.objects.get(id = int(sid))
            else:
                raise Exception("Url no valido o mal configurado")

            if user.role == ROLE_PST:            
                
                pst = Pst.objects.get(user = user)
                
                """
                Se genera la respuesta de tabulador si no existe,
                caso contrario se realiza la carga en la variable
                << rt >>
                """               
                try:                    
                    rt = RespuestaTabulador.objects.get(solicitud_id = int(sid))                    
                except RespuestaTabulador.DoesNotExist:
                    rt = RespuestaTabulador(
                        pst = pst,
                        tabulador = sol.tabulador,
                        nombre = 'respuestas_solicitud_%d_%s_%s' % (
                            int(sid),
                            request.user.get_full_name(),
                            datetime.datetime.now().strftime('%d-%m-%Y')
                        ),
                        fecha_creacion = datetime.datetime.now(),
                        solicitud = sol
                    )
                    rt.save()

                for k,v in request.POST.items():
                    if k != 'csrfmiddlewaretoken' and k!= 'continue':
                        values = secure_value_decode(k).split("_")
                        s = int(values[2])
                        af = int(values[1])
                        sbsc = int(values[3])
                        valor_respuesta = int(values[4])

                        try:
                            nsbsc = Subseccion.objects.get(
                                subseccion_config_id = sbsc,
                                respuesta_tabulador = rt
                                )                            
                        except Subseccion.DoesNotExist:
                            sbscconfig = SubseccionConfig.objects.get(id=sbsc)
                            nsbsc = Subseccion(
                                nombre = "subseccion_%s_%s" % (
                                    user.rif,
                                    datetime.datetime.now().strftime('%d-%m-%Y')
                                ),                                
                                tipo_subseccion = sbscconfig.tipo_subseccion,
                                subseccion_config = sbscconfig,
                                respuesta_tabulador = rt
                            )
                            nsbsc.save()

                        key = 'mintur-cachedtabulador_%d_VE_%d_%s' %(
                                sol.tabulador.id,
                                sol.id,
                                user.rif
                            )
                        try:
                            val = ValorRespuesta.objects.get(subseccion = nsbsc)

                            if val.valor != float(v):
                                val.valor  = float(v)
                                val.save()                                

                                if cache.get(key) is not None:
                                    cache.delete(key)

                        except ValorRespuesta.DoesNotExist:
                            val = ValorRespuesta(
                                    subseccion=nsbsc,
                                    valor=float(v)
                                )
                            val.save()

                            """
                                En caso de estar registrando nuevas respuestas
                                se elimina la entrada generada de memoria cache
                                correspondiente a este tabulador
                            """

                            if cache.get(key) is not None:
                                cache.delete(key)
                    if k == 'continue':
                        goahead = True
            
            t = edicion_autorizada(user, sol, typeentry = 'RF')
            desactivar = t[0]
            valores_asociados = t[1]
            natural = juridica = False

            if user.role == ROLE_PST:
                pst = Pst.objects.get(user = user)
                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True

                context.update({
                        'pst': pst,
                        'natural': natural,
                        'juridica': juridica
                    })
            elif user.role == ROLE_FUNCIONARIO:
                funcionario = Funcionario.objects.get(user = user)
                context.update({
                    funcionario.tiporol.nombre: True,
                    'pst': None
                })              

            url = reverse(
                    'generar_tabulador',
                    kwargs = {
                        'tabulador':sol.tabulador.id,
                        'solicitud':sol.id,
                        'tipo':'VE',
                        'desactivar': desactivar,
                        'valores_asociados': valores_asociados
                    }
                )

            context.update({
                'solicitud': sol,
                'actor': user.get_full_name(),
                'tabulador': sol.tabulador.id,
                'tipo': 'VE',
                'desactivar': desactivar,
                'valores_asociados': valores_asociados,
                'url': url
            })

            if not goahead:
                return render(
                    request,
                    'valores_especificos.html',
                    context
                )
            else:
                return HttpResponseRedirect(
                    reverse(
                        'requisitos_principales',
                        kwargs = {
                            'tipo': 'RB',
                            'solicitud': sol.id
                        }
                    )
                )

        except Exception, e:
            raise e


class CargarElemValAg(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CargarElemValAg, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Realizar la carga de los requisitos Funcionales
            para las solicitudes de la sucursal seleccionada
        """
        sid = None
        if kwargs.has_key('solicitud'):
            sid = kwargs['solicitud']
        else:
            raise Exception("Url no valido o mal configurado")

        """
            Solicitud actual sobre la que se requieren 
            los requisitos funcionales
        """
        solicitud = Solicitud.objects.get(id = int(sid))       

        """
            Usuario actualmente en el sistema
        """
        user = request.user

        """
            Estado de desactivado y valores_asociados
        """
        t = edicion_autorizada(user, solicitud, typeentry='RE')
        desactivar = t[0]
        valores_asociados = t[1]

        """
            Tabulador asociado a la solicitud
        """
        tabulador = solicitud.tabulador
        natural = juridica = False
        context = {}

        if user.role == ROLE_PST:
            pst = Pst.objects.get(user = user)
            if pst.tipo_figura == PERSONA_NATURAL:
                natural = True
            else:
                juridica = True

            context.update({
                    'pst': pst,
                    'natural': natural,
                    'juridica': juridica
                })
        elif user.role == ROLE_FUNCIONARIO:            
            funcionario = Funcionario.objects.get(user = user)
            context.update({
                funcionario.tiporol.nombre: True,
                "pst": solicitud.pst
            })
        
        context.update({
            'solicitud': solicitud,
            'actor': user.get_full_name(),
            'tabulador': tabulador.id,
            'tipo': 'RE',
            'desactivar': desactivar,
            'valores_asociados': valores_asociados,
        })

        return render(
            request,
            'elementos_valor_agregado.html',
            context
        )

    def post(self, request, *args, **kwargs):
        """
            Tomamos el identificador de la sucursal asociada
            a las respuestas que estan siendo enviadas desde el
            cliente
        """        
        try:            
            user = request.user                      
            evaluacion = 0
            sid = None
            if kwargs.has_key('solicitud'):
                sid = kwargs['solicitud']
            else:
                raise Exception("Url no valido o mal configurado")            
            
            sol = Solicitud.objects.get(id = int(sid))
            """
            Se genera la respuesta de tabulador si no existe,
            caso contrario se realiza la carga en la variable
            << rt >>
            """                
            try:                    
                rt = RespuestaTabulador.objects.get(solicitud_id = int(sid))                    
            except RespuestaTabulador.DoesNotExist:
                rt = RespuestaTabulador(
                    pst = sol.pst,
                    tabulador = sol.tabulador,
                    nombre = 'respuestas_solicitud_%d_%s_%s' % (
                        int(sid),
                        request.user.get_full_name(),
                        datetime.datetime.now().strftime('%d-%m-%Y')
                    ),
                    fecha_creacion = datetime.datetime.now(),
                    solicitud = sol
                )
                rt.save()            
            
            for k,v in request.POST.items():
                valor_ingresado = False
                if k != 'csrfmiddlewaretoken':
                    try:
                        values = secure_value_decode(v).split("_")
                    except Exception, e:
                        values = secure_value_decode(k).split("_")
                        valor_ingresado = float(v)
                    
                    """
                        Validacion para los casos en los que el formulario sea
                        enviado vacio de manera accidental/intencional
                    """
                    if len(''.join(values).strip()) :
                        s = int(values[2])
                        af = int(values[1])
                        sbsc = int(values[3])
                        valor_respuesta = float(values[4])
                        """
                        s = int(values[3])
                        af = int(values[2])
                        sbsc = int(values[4])
                        puntaje = float(values[0])
                        valor_respuesta = float(values[5])
                        """

                        try:
                            sbscconfig = SubseccionConfig.objects.get(id = sbsc)
                            nsbsc = Subseccion.objects.get(
                                subseccion_config_id = sbsc,
                                respuesta_tabulador = rt
                                )                            
                        except Subseccion.DoesNotExist:
                            sbscconfig = SubseccionConfig.objects.get(id = sbsc)
                            nsbsc = Subseccion(
                                nombre = "subseccion_%s_%s" % (
                                    user.rif,
                                    datetime.datetime.now().strftime('%d-%m-%Y')
                                ),                                
                                tipo_subseccion = sbscconfig.tipo_subseccion,
                                subseccion_config = sbscconfig,
                                respuesta_tabulador = rt
                            )
                            nsbsc.save()

                        key = 'mintur-cachedtabulador_%d_EVA_%d_%s' %(
                                sol.tabulador.id,
                                sol.id,
                                user.rif
                            )
                        try:
                            val_res = ValorRespuesta.objects.get(subseccion = nsbsc)
                            
                            if val_res.valor_respuesta_id != valor_respuesta:
                                val_res.valor_respuesta_id = valor_respuesta                            

                            if valor_ingresado:
                                val_res.valor = valor_ingresado
                            
                            val_res.save()

                            if cache.get(key) is not None:
                                cache.delete(key)

                        except ValorRespuesta.DoesNotExist:
                            val_res = ValorRespuesta(
                                    subseccion = nsbsc,
                                    valor_respuesta_id = valor_respuesta
                                )
                            
                            if valor_ingresado:
                                val_res.valor = valor_ingresado
                            
                            val_res.save()
                            """
                                En caso de estar registrando nuevas respuestas
                                se elimina la entrada generada de memoria cache
                                correspondiente a este tabulador
                            """
                            if cache.get(key) is not None:
                                cache.delete(key)

                        #evaluacion += evaluar_respuesta(nsbsc, valor_respuesta)
            
            #categoria_obtenida = evaluar_categoria(evaluacion, sol.pst, sol.sucursal)
            categoria_obtenida = dt_categoria(sol)

            """
                Se otorga la categoria de manera temporal usando para ello 
                calificacion_definitiva = False, solo cuando un funcionario
                de rango superior como viceministro determine que la aprobacion
                de la categoria la misma se otorga y se cambia el valor del 
                campo antes mencionado.
            """            
            pstcatdoccomp = None
            if categoria_obtenida > 0:
                if sol.pst_categoria_doc is None:
                    pstcatdoccomp = PstCategoriaDocumentoCompuesto(
                        categoria = categoria_obtenida,                                
                        calificacion = evaluacion,
                        calificacion_definitiva = False
                    )
                else:
                    pstcatdoccomp = sol.pst_categoria_doc
                    pstcatdoccomp.categoria = categoria_obtenida
                    pstcatdoccomp.calificacion = evaluacion
                    pstcatdoccomp.calificacion_definitiva = True

                pstcatdoccomp.save()
            elif sol.pst_categoria_doc is not None:
                p = sol.pst_categoria_doc
                sol.pst_categoria_doc = None
                sol.save()                
                p.delete()
                return HttpResponseRedirect(
                    reverse(
                        'bandeja'
                    )
                )                
            """
                Se actualiza la relacion con la solicitud 
                de acuerdo a la calificacion obtenida
            """
            sol.pst_categoria_doc = pstcatdoccomp
            sol.save()

            return HttpResponseRedirect(
                    reverse(
                        'bandeja'
                    )
                )
        except Exception, e:
            raise e


############################################
#                                          #
# Carga de Requisitos Basico y Especificos #
#                                          #
############################################

class CargarRequisitosPrincipales(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CargarRequisitosPrincipales, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Realizar la carga de los requisitos basico y especificos dependiendo 
            del tipo enviado en la solicitud via el url para las solicitudes de la 
            sucursal seleccionada
        """        
        sid = None
        tipo = None
        if kwargs.has_key('solicitud'):
            sid = kwargs['solicitud']
        else:
            raise Exception("Url no valido o mal configurado")

        if kwargs.has_key('tipo'):
            tipo = kwargs['tipo']
        else:
            raise Exception("Url no valido o mal configurado")


        """
            Solicitud actual sobre la que se requieren 
            los requisitos funcionales
        """
        solicitud = Solicitud.objects.get(id = int(sid))       

        """
            Usuario actualmente en el sistema
        """
        user = request.user

        """
            Estado de desactivado y valores_asociados
        """
        t = edicion_autorizada(user, solicitud, typeentry='RE')
        desactivar = t[0]
        valores_asociados = t[1]

        """
            Tabulador asociado a la solicitud
        """
        tabulador = solicitud.tabulador
        natural = juridica = False
        context = {}

        if user.role == ROLE_PST:
            pst = Pst.objects.get(user = user)
            if pst.tipo_figura == PERSONA_NATURAL:
                natural = True
            else:
                juridica = True

            context.update({
                    'pst': pst,
                    'natural': natural,
                    'juridica': juridica
                })
        elif user.role == ROLE_FUNCIONARIO:            
            funcionario = Funcionario.objects.get(user = user)
            context.update({
                funcionario.tiporol.nombre: True,
            })
        
        context.update(
            {
            'solicitud': solicitud,
            'actor': user.get_full_name(),
            'tabulador': tabulador.id,
            'tipo': tipo,
            'desactivar': desactivar,
            'valores_asociados': valores_asociados,
            'url': reverse(
                    'generar_tabulador',
                    kwargs = {
                        'tabulador':tabulador.id,
                        'solicitud':solicitud.id,
                        'tipo':tipo,
                        'desactivar': desactivar,
                        'valores_asociados': valores_asociados
                    }
                ),
            'url_comeback': reverse(
                        'valores_especificos', 
                        kwargs={
                            'solicitud': sid
                        }
                ) if tipo == "RB" else reverse(
                        'requisitos_principales',
                        kwargs = {
                            'solicitud':solicitud.id,
                            'tipo': 'RB'
                        }
                    )
            }
        )

        return render(
            request,
            'requisitos_principales.html',
            context
        )

    def post(self, request, *args, **kwargs):
        """
            Tomamos el identificador de la sucursal asociada
            a las respuestas que estan siendo enviadas desde el
            cliente
        """        
        #try:            
        user = request.user                   
        evaluacion = 0.0
        sid = None
        tipo = None
        excluded_safe = ['formula']
        radio_repetitive = input_repetitive = False
        goahead = False

        # re para radios nuevos de repetitivas
        radio_re = re.compile("^newrep\d+$")
        # re para valores de inputs
        input_re = re.compile("^.+#new\d+#$")

        #####################################################
        #                                                   #
        # Temporalmente se coloca la calificacion minima    #
        # hasta tener completamente terminado el algoritmo  #
        # de evaluacion                                     #
        #                                                   #
        #####################################################

        categoria_obtenida = None

        if kwargs.has_key('solicitud'):
            sid = kwargs['solicitud']
        else:
            raise Exception("Url no valido o mal configurado")

        if kwargs.has_key('tipo'):
            tipo = kwargs['tipo']
        else:
            raise Exception("Url no valido o mal configurado")          
        
        sol = Solicitud.objects.get(id = int(sid))
        
        """
        Se genera la respuesta de tabulador si no existe,
        caso contrario se realiza la carga en la variable
        << rt >>
        """                
        
        try:                
            rt = RespuestaTabulador.objects.get(solicitud_id = int(sid))                    
        except RespuestaTabulador.DoesNotExist:
            rt = RespuestaTabulador(
                pst = sol.pst,
                tabulador = sol.tabulador,
                nombre = 'respuestas_solicitud_%d_%s_%s' % (
                    int(sid),
                    request.user.get_full_name(),
                    datetime.datetime.now().strftime('%d-%m-%Y')
                ),
                fecha_creacion = datetime.datetime.now(),
                solicitud = sol
            )
            rt.save()

        for k,v in request.POST.items():
            
            valor_ingresado = False
            radio_repetitive = False
            input_repetitive = False

            if k != 'csrfmiddlewaretoken' and k!="continue":
                try:
                    try:
                        
                        values = secure_value_decode(v).split("_")
                        radio_repetitive = radio_re.match(k) is not None

                    except Exception, e:
                        
                        if input_re.match(k) is None:
                            values = secure_value_decode(k).split("_")
                        else:
                            k = re.sub("#new\d+#","",k)
                            values = secure_value_decode(k).split("_")
                            input_repetitive = True

                        valor_ingresado = float(v)
                except Exception, e:
                    
                    # Casos en los que la respuesta ha sido configurada para
                    # aparecer dentro del tabulador pero no genera un valor 
                    # significativo dentro del cuerpo del tabulador ya que 
                    # solo es un elemento de interaccion (condicional)
                    continue
                
                # Validacion para los casos en los que el formulario sea
                # enviado vacio de manera accidental/intencional
                
                if len(''.join(values).strip()) :
                    s = int(values[2])
                    af = int(values[1])
                    sbsc = int(values[3])
                    valor_respuesta = float(values[4])

                    if input_repetitive or radio_repetitive:
                        # Se clona la subseccion de la seccion repetitiva de manera 
                        # que sea renderizada la proxima oportunidad

                        sbsc = SubseccionConfig.objects.get(id = sbsc)
                        brothers_counter = sbsc.grupo_repetitivo +1
                        sbsc.nombre = ("#%d%s#%s" % (brothers_counter, datetime.datetime.now().strftime('%d%m%Y%H%M%S'), sbsc.nombre))
                        sbsc.grupo_repetitivo = brothers_counter
                        sbsc.creado_en = sol

                        sbsc.pk = None
                        sbsc.save()
                        sbsc = sbsc.pk
                    
                    try:
                        nsbsc = Subseccion.objects.get(
                            subseccion_config_id = sbsc,
                            respuesta_tabulador = rt
                        )
                    except Subseccion.DoesNotExist:
                        sbscconfig = SubseccionConfig.objects.get(id = sbsc)
                        nsbsc = Subseccion(
                            nombre = "subseccion_%s_%s" % (
                                user.rif,
                                datetime.datetime.now().strftime('%d-%m-%Y')
                            ),                                
                            tipo_subseccion = sbscconfig.tipo_subseccion,
                            subseccion_config = sbscconfig,
                            respuesta_tabulador = rt
                        )
                        nsbsc.save()

                    key = 'mintur-cachedtabulador_%d_%s_%d_%s' %(
                            sol.tabulador.id,
                            tipo,
                            sol.id,
                            user.rif
                        )
                    try:
                        val_res = ValorRespuesta.objects.get(
                            subseccion = nsbsc
                            )


                        if cache.get(key) is not None:
                            cache.delete(key)

                    except ValorRespuesta.DoesNotExist:
                        val_res = ValorRespuesta(
                                subseccion = nsbsc,
                            )


                        if cache.get(key) is not None:
                            cache.delete(key)

                    
                    try:
                        # Se intenta actualizar la respuesta de subseccion
                        # en caso de que la misma sea respondida con un valor
                        # que se haya configurado en los valores de respuesta
                        # en caso contrario la misma es respondida con valores
                        # y la asignacion de la respuesta se lleva a cabo solamente
                        # con el uso de la variable <<valor_ingresado>>
                        if valor_ingresado:
                            val_res.valor = valor_ingresado

                        elif val_res.valor_respuesta_id != valor_respuesta:
                            val_res.valor_respuesta_id = valor_respuesta  
                        
                        val_res.save()


                    except Exception, e:
                    
                        pass
                    
                        
                    # En caso de estar registrando nuevas respuestas
                    # se elimina la entrada generada de memoria cache
                    # correspondiente a este tabulador
                        
                    if cache.get(key) is not None:
                        cache.delete(key)

                    #evaluacion += evaluar_respuesta(nsbsc, valor_respuesta)

                    evaluacion += 0.0
                    
            if k == 'continue':
                goahead = v

        #categoria_obtenida = evaluar_categoria(evaluacion, sol.pst, sol.sucursal)
        """
        categoria_obtenida = Categoria.objects.filter(
            tipo_pst = otp_prestador(sol.pst, sol.sucursal)
            ).order_by('tope_porcentual').first()
        """
        categoria_obtenida = dt_categoria(sol)

        
        # Se otorga la categoria de manera temporal usando para ello 
        # calificacion_definitiva = False, solo cuando un funcionario
        # de rango superior como viceministro determine que la aprobacion
        # de la categoria la misma se otorga y se cambia el valor del 
        # campo antes mencionado.
                   
        pstcatdoccomp = None
        if categoria_obtenida > 0:
            if sol.pst_categoria_doc is None:
                pstcatdoccomp = PstCategoriaDocumentoCompuesto(
                    categoria = categoria_obtenida,                                
                    calificacion = evaluacion,
                    calificacion_definitiva = False
                )
            else:
                pstcatdoccomp = sol.pst_categoria_doc
                pstcatdoccomp.categoria = categoria_obtenida
                pstcatdoccomp.calificacion = evaluacion
                pstcatdoccomp.calificacion_definitiva = True

            pstcatdoccomp.save()

        elif sol.pst_categoria_doc is not None:
            p = sol.pst_categoria_doc
            sol.pst_categoria_doc = None
            sol.save()                
            p.delete()
            return HttpResponseRedirect(
                reverse(
                    'bandeja'
                )
            )                
        
        # Se actualiza la relacion con la solicitud 
        # de acuerdo a la calificacion obtenida
        
        sol.pst_categoria_doc = pstcatdoccomp
        sol.save()
        
        if not goahead:

            return HttpResponseRedirect(
                    reverse(
                        'requisitos_principales',
                        kwargs = {
                            'solicitud':sol.id,
                            'tipo': 'RB'
                        }
                    )
                )

        else:
            if goahead == 'RB':
                return HttpResponseRedirect(
                        reverse(
                            'requisitos_principales',
                            kwargs = {
                                'solicitud':sol.id,
                                'tipo': 'RE'
                            }
                        )
                    )

            elif goahead == 'RE':             
                return HttpResponseRedirect(
                        reverse(
                            'bandeja'                            
                        )
                    )
        #except Exception, e:
        #    raise e


class CambioVersion(View):
    """
        Permite realizar cambios de versiones
        en tabuladores del mismo tipo de prestador
    """
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CambioVersion, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            #request.POST = {tabulador: id, estado: id, tipo_pst: id}
            tabulador = int(request.POST['tabulador'])
            estado = int(request.POST['estado'])
            tipo_pst = int(request.POST['tipo_pst'])
            opciones = Tabulador.objects.filter(tipo_pst_id = tipo_pst)
            code = 200
            
            jsontmp = {
                "err_msg": "",
                "success": "",
                "data": {}
            }
            
            if not estado:
                """
                    Se esta pasando desactivando una version actual del tabulador
                """
                if opciones.count() > 1:
                    """
                        Si hay mas de un tabulador para este tipo de 
                        prestador => se retornan las opciones para la
                        sustitucion de la vesion actual por alguna 
                        existente
                    """                    
                    t = Tabulador.objects.exclude(
                            id = tabulador
                        ).filter(
                                tipo_pst_id = tipo_pst
                            )
                    """
                        Tabuladores opcionales distintos al tabulador
                        actual que se esta desactivando como 
                        version_actual
                    """
                    s = serializers.serialize(
                        'json',
                        t,
                        fields = ('id','nombre','version','fecha_creacion')
                    )
                    jsontmp['data'] = s;
                    jsontmp['success_msg'] = "Debe seleccionar una version de tabulador existente en reemplazo";

                elif opciones.count() == 1:
                    jsontmp['err_msg'] = "La versi&oacute;n actual del tabulador es la &uacute;nica existente para este tipo de prestador de servicio tur&iacute;stico. Tenga en cuenta que en lo sucesivo nuevos procesos de categorizaci&oacute;n no pordr&aacute;n ser iniciados."
                    code = 400
                
            res = HttpResponse(
                json.dumps(
                    jsontmp,
                    sort_keys=False                   
                ),
                content_type="application/json",
            )
            res.status_code = code
            
            return res

        except Exception, e:
            raise Exception("Errores encontrados en los procesos \
                de cambios de versiones del tabulador: %s" % (str(e)))


class Paginador(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(Paginador, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST['s'] is not None and request.POST['p'] is not None:
            p = int(request.POST['p'])
            s = request.POST['s']
            m = kwargs['modelo']
            url_agregar = reverse('agregar_recurso', kwargs={'modelo': m})
            Modelo = model_list.get_instance_model(APP_NAME, m)
            nombre_modelo = Modelo.show_name
            m_all = Modelo.objects.all()
            num_pag = math.ceil(m_all.count() / float(constants.ELEMENTO_POR_PAGINA))

            if s == '-':
                p -= 1
            elif s == '+':
                p += 1

            m = m_all[constants.ELEMENTO_POR_PAGINA*p : (1+p)*constants.ELEMENTO_POR_PAGINA]            
            modelo = [ e.to_json() for e in m ]
            jsontmp = {
                "err_msg": "",
                "success": "Pagina encontrada",
                "data": {
                    "pagina": p, 
                    "modelo": modelo, 
                    "num_pag": num_pag, 
                    "url_agregar": url_agregar, 
                    "nombre_modelo": nombre_modelo
                },
                "no_editable": False,
                "no_insertar": True if (kwargs['modelo']).replace(' ','').lower() == 'parametroconfiguracion' else False,
                "no_eliminable": True if (kwargs['modelo']).replace(' ','').lower() == 'parametroconfiguracion' else False
            }           
            
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=False),
                content_type="application/json"
            )

        else:
            jsontmp = {
                "err_msg": "Parametros invalidos",
                "success": "", "data": ""
            }
            return HttpResponse(
                json.dumps(
                    jsontmp, sort_keys=False,
                    content_type="application/json",
                )
            )


class NuevaSolicitud(View):    
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(NuevaSolicitud, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # No se permite crear una solicitud si ya existe una creada
        if kwargs.has_key('sucursal'):
            if int(kwargs['sucursal'])>0:
                sucursal=int(kwargs['sucursal'])
            else:
                sucursal=None
        else:
            raise Exception("Url no valido o mal configurado")
        pst = Pst.objects.get(user = request.user)        
        try: 
            if not Solicitud.objects.filter(
                pst= pst,                 
                sucursal_id = sucursal,
                renovar=False).exists():

                """
                    Dado que es una nueva solicitud le colocamos 
                    el tabulador de version actual que tengan asociados
                    a estos tipo de prestador
                """
                sol = Solicitud(
                    pst = request.user.pst_set.get(),
                    estatus = Estatus.objects.get(abreviacion = 'SC'),
                    fecha_modificacion_estado = datetime.datetime.now(),
                    tabulador = obtener_tabulador_actual.version_actual(
                        otp_prestador(pst, sucursal)
                    ),
                    sucursal_id = sucursal
                ) 
                sol.save()

                soli=Solicitud.objects.filter(pst=pst, sucursal_id=sucursal, 
                    renovar=True
                ).order_by("-fecha_clausura").first()


                dprint("hello")

                if soli:
                    resp = RespuestaTabulador.objects.get(pst=pst, solicitud=soli)
                    res = RespuestaTabulador(pst = pst, tabulador = resp.tabulador,
                            nombre = resp.nombre,fecha_creacion = resp.fecha_creacion, 
                            solicitud = sol
                        )
                    res.save()

                    sub = Subseccion.objects.filter(respuesta_tabulador=resp)

                    for s in sub:
                        subs = Subseccion(
                            nombre =s.nombre ,
                            observacion =s.observacion ,
                            tipo_subseccion =s.tipo_subseccion,
                            subseccion_config = s.subseccion_config,
                            respuesta_tabulador = res
                            )
                        subs.save()
                        try:
                            val_res = ValorRespuesta.objects.filter(subseccion=s)
                            for v in val_res:
                                val_resp = ValorRespuesta(valor = v.valor,subseccion =subs,
                                    valor_respuesta = v.valor_respuesta
                                )
                                val_resp.save()

                        except ValorRespuesta.DoesNotExist:
                            print "Algunas subsecciones no requieren respuesta"

                        try:
                            sub_arch = SubseccionArchivoRequisito.objects.get(subseccion=s)

                            sub_archiv = SubseccionArchivoRequisito(subseccion = subs, 
                                requisito_digital=sub_arch.requisito_digital
                            )
                            sub_archiv.save()
                        except SubseccionArchivoRequisito.DoesNotExist:
                            print "Algunas subsecciones no requieren subida de archivos"     
                
                """        
                lic = LicenciaAsignada.objects.filter(usuario_pst=request.user, 
                    sucursal_id=sucursal
                ).first()
                if lic:
                    if sucursal:
                        licencia = lic.numero_licencia
                        suc= sol.pst.denominacion_comercial
                        direccion = "%s, %s, %s, %s" %(sol.sucursal.urbanizacion, sol.sucursal.avenida_calle, sol.sucursal.edificio, sol.sucursal.oficina_apartamento)
                    else:                        
                        licencia = lic.numero_licencia
                        suc= "Sede Principal"
                        direccs = Registro_Direccion.objects.filter(pst=pst).first()                      
                        direccion = "%s, %s,%s, %s, %s, %s" %(
                            direccs.estado.estado,
                            direccs.municipio.municipio,
                            direccs.urbanizacion,
                            direccs.avenida_calle,
                            direccs.edificio,
                            direccs.oficina_apartamento
                        )


                    htmly = get_template('correo/iniciar_categorizacion.html')
                    text_plain = get_template('correo/iniciar_categorizacion.txt')

                    context = Context({
                     'licencia': lic,
                     'nombre_pst': sol.pst.nombres+" "+sol.pst.apellidos,
                     'nombre_establecimiento': suc,
                     'direccion': direccion
                     })

                    html_content = htmly.render(context)
                    text_content = text_plain.render(context)

                   
                    #Busqueda de correo en parametros de configuracion
                    #try:
                    #    corr = ParametroConfiguracion.objects.get(
                    #        clave="correo_interno"
                    #        )
                    #except ParametroConfiguracion.DoesNotExist:
                    #    raise e
                    #corrs = str(corr.valor)

                    thread_correo = threading.Thread(
                        name='thread_correo', 
                        target=correo, 
                        args=(
                            u'[MINTUR] Nuevo Proceso de Categorización',  
                            html_content, 
                            text_content, 
                            'gccdev@cgtscorp.com', 
                            ['gccdev@cgtscorp.com'], 
                            None, 
                            'nuevasolicitud')
                        )
                    thread_correo.start()
                """
                return HttpResponseRedirect(
                    reverse(
                        'cargar_requisitos',
                        kwargs={'solicitud': sol.id}
                    )
                )

            else:
                raise Exception("Ya existe una solicitud creada para este prestador")
        except Exception,e:
            raise e
            return HttpResponseRedirect(
                reverse(
                    'bandeja'
                )
            )


class CredencialesPDFView(PDFTemplateView):
    template_name="viceministro/oficios/oficio-placa.html"


class Bandeja(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(Bandeja, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        id_sesion = user.id
        natural = juridica = False
        busqueda_datos={}
        key='busqueda_cache'

        if request.session.has_key('error'):
            error = request.session['error']
            request.session.__delitem__('error')
        else:
            error = None

        if user.role == ROLE_PST:

            pst = user.pst_set.get()            

            if pst.tipo_figura == PERSONA_NATURAL:
                natural = True
            else:
                juridica = True
            
            if es_prestador_valido(user): 
                mas =True
                paginars = False
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        solicitudes = Solicitud.objects.filter(**filter_dict).order_by(
                            '-fecha_modificacion_estado'
                        )
                    else:
                        solicitudes = Solicitud.objects.filter(pst = pst.pk).order_by(
                            '-fecha_modificacion_estado'
                        )
                    busqueda_datos.update({'solicitudes':solicitudes})
                else:
                    x=cache.get(key)
                    solicitudes=x['solicitudes']

                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    sol= solicitudes
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    sol= solicitudes
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                sol_abierta = False
                if solicitudes:
                    if solicitudes[0].fecha_clausura is None:
                        sol_abierta = True

                notificacion={}
                documentos={}
                clasificaciones=[]         

                for s in solicitudes:

                    mx = Categoria.objects.filter(
                        tipo_pst = otp_prestador(s.pst, s.sucursal)
                    ).count()

                    try:
                        icon = TipoIcono.objects.get(tipo_pst = otp_prestador(s.pst, s.sucursal)).representacion
                    except Exception, e:
                        icon = "fa-star"
                    
                    if s.pst_categoria_doc is not None:
                        clasificaciones.append(
                            (
                                s.pst_categoria_doc.categoria.valor, 
                                mx - s.pst_categoria_doc.categoria.valor,
                                icon
                            )
                        )
                    else:
                        clasificaciones.append(
                            (
                                0,
                                mx,
                                icon
                            )
                        )

                    n=Notificacion.objects.filter(
                        solicitud_id = s.id,
                        receptor_id = int(id_sesion)
                    ).order_by(
                        '-fecha_emision'
                    ).first()
                    
                    if n:
                        if not notificacion.has_key(s.id):
                            notificacion.update({s.id:[]})

                        try:
                            doc=NotificacionDocumentoCompuesto.objects.get(
                                notificacion=n, 
                                documento__tipo_documento_compuesto__abreviacion='N'
                            ).documento
                            src=doc.ruta_documento
                            extension=doc.extension
                        except:
                            src=None
                            extension=None
                        notificacion[s.id].append(
                            {
                                'observacion': n.observacion,
                                'src': src,
                                'extension': extension
                            }
                        )

                    #Documentos asociados
                    notificacion_doc= NotificacionDocumentoCompuesto.objects.filter(
                        notificacion__solicitud=s
                    ).distinct('documento').exclude(
                        Q(documento__tipo_documento_compuesto__abreviacion = 'C') |
                        Q(documento__tipo_documento_compuesto__abreviacion = 'IT')
                        )
                    if notificacion_doc:
                        if not documentos.has_key(s.id):
                            documentos.update({s.id:[]})
                        for doc in notificacion_doc:
                            documentos[s.id].append(
                                {
                                    'nombre': doc.documento.tipo_documento_compuesto.nombre,
                                    #'abreviacion': doc.documento.tipo_documento_compuesto.abreviacion,
                                    'ruta': doc.documento.ruta_documento
                                }
                        )

                    """
                    #Oficio de reparación asociado a la solicitud
                    notificacion_rep= NotificacionDocumentoCompuesto.objects.filter(
                        documento__tipo_documento_compuesto__abreviacion='OAR',
                        notificacion__solicitud=s
                    ).first()

                    if notificacion_rep:
                        oficio_reparacion.update({s.id:notificacion_rep.documento.ruta_documento})
                    """
                
                contrato= ParametroConfiguracion.objects.get(clave="contrato_nueva_solicitud").valor
                sol_cat= zip(solicitudes,clasificaciones)

                context={
                    'pst': pst,
                    'rtn': pst.rtn,
                    'natural':natural,
                    'juridica':juridica,
                    'actor': user.get_full_name(),
                    'sol_abierta': sol_abierta,
                    'solicitudes': sol_cat,
                    'notificacion': notificacion,
                    'contrato': contrato,
                    'documentos': documentos,      
                    'error': error,
                }
                if paginars == True: 
                    context.update({'p':p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})
                dprint(context=context)
                return render(request, 'pst/bandeja.html', context)
            else:            
                context={
                    'pst': pst,
                    'rtn': pst.rtn,
                    'natural':natural,
                    'juridica':juridica,
                    'actor': user.get_full_name(),                    
                    'error': "Lo sentimos, hemos detectado que usted no posee licencias que lo acrediten como prestador de servicios turisticos de alojamiento, lo cual impide que pueda iniciar algún proceso de categorización."
                }                
                return render(request, 'pst/bandeja.html', context)
            
        elif user.role == ROLE_FUNCIONARIO:
            funcionario = Funcionario.objects.get(user_id=int(id_sesion))
            minturuser = MinturUser.objects.get(id=int(id_sesion))
            if funcionario.tiporol.nombre == "administrador":
                raise Http404

            context={}
            # Uso de firma de digitales
            try:
                firmas = CredencialesOtorgadas.objects.get(user=user)
                context.update({'firmas': True})
                """
                if firmas:
                    context.update({'firmas': True})
                    form = fc.FormFirma(
                        initial ={
                            'user': settings.SSH_USER,
                            'password': settings.SSH_PASSWORD,
                            'width': '150',
                            'height': '400',
                            'server': settings.SSH_SERVER,
                            'puerto': '22',
                            'rutaOrigen': settings.DOC_ELECTRONICOS_SOLICITUDES_ROOT+'/',
                            'rutaDestino': settings.DOC_ELECTRONICOS_FIRMADOS_ROOT+'/',
                            'passwordPdf': '123456',
                            'razon': 'Firma',
                            'ubicacion': 'Caracas - Baruta',
                            'mailContacto': minturuser.correo_electronico,
                            # Es importante que los siguientes parametros varien ya que esto indicara
                            # donde quedara la firma
                            'pX': '200',
                            'pY': '500',
                            'pW': '300',
                            'pH': '600',
                            'pagina': '1', 
                            # hasta aqui
                            'tipoFirma': '2',
                            'cantidad':'0',
                            'metodo': 'insertar()',
                            'email': 'null',
                            'serial': 'null',
                            'clave_publica': 'null',
                            'resultado_firma': '0',
                            'mayscript': 'true'
                        }
                    )
                    context.update({"form": form.as_p()})
                    """
            except CredencialesOtorgadas.DoesNotExist:
                firmas = None
            

            asignaciones=Asignacion.objects.filter(
                funcionario=funcionario, 
                asignacion_habilitada=True
            ).values('solicitud')

            #Todas las solicitudes de ese funcionario
            if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                cache.delete(key)
                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    dprint(decode=request.GET['solicitudes'])
                    params = secure_value_decode(request.GET['solicitudes'])
                    dprint(params=params)
                    filter_dict=pickle.loads(params)
                    dprint(filter_dict=filter_dict)
                    if filter_dict.has_key('adicional'):
                        array_texto = filter_dict['adicional']
                        filter_dict.pop('adicional')
                        solicitudes = Solicitud.objects.filter(
                            reduce(operator.or_,array_texto),**filter_dict
                        )
                    else:
                       solicitudes = Solicitud.objects.filter(**filter_dict)
                else:
                    solicitudes = Solicitud.objects.filter(id__in=asignaciones)
                busqueda_datos.update({'solicitudes':solicitudes})
            else:
                x=cache.get(key)
                solicitudes=x['solicitudes']

            paginars = False
            mas = True
            if request.GET.has_key('p') and request.GET.has_key('s'): 
                paginars = True
                p= int(request.GET['p'])
                s= request.GET['s']
                if s == '-':
                    p -= 1
                elif s == '+':
                    dprint(s)
                    p += 1
                sol= solicitudes
                num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                if len(sol[num:num+1]) ==0:
                    mas = False

            if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                p= 0
                num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                paginars = True
                sol= solicitudes
                solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                if len(sol[num:num+1]) ==0:
                    mas = False

            opciones={}
            documentos={}
            notificacion={}
            analistax={}
            inspectorx={}
            coordinadorx={}
            directorx={}
            cantidad={}
            clasificaciones=[]
            sol_firmas = {}

            for s in solicitudes:

                #
                # Firmas
                #
                print "############################################################################################################"
                print "############################################################################################################"
                print "############################################################################################################"
                print "############################################################################################################"
                print "############################################################################################################"
                print "############################################################################################################"
                if firmas:
                    notif_firma = Notificacion.objects.filter(solicitud=s)
                    notif_compuesto = NotificacionDocumentoCompuesto.objects.filter(
                        notificacion__in=notif_firma
                    ).order_by('documento__fecha_emision')
                    dprint(notif_compuesto=notif_compuesto)
                    for e in notif_compuesto:
                        if e.documento.tipo_documento_compuesto.abreviacion in constants.OFICIOS_FIRMAS and e.documento.firmado == False:    
                            sol_firmas.update({s.id:[e.documento.nombre]})
                            break

                """
                    Se obtiene el maximo valor posible de esa categoria
                    en ese caso se emplea dicho valor para determinar
                    el numero de elementos a ser pintados en el indicador de
                    la bandeja
                """
                mx = Categoria.objects.filter(
                    tipo_pst = otp_prestador(s.pst, s.sucursal)
                ).count()

                try:
                    icon = TipoIcono.objects.get(tipo_pst = otp_prestador(s.pst, s.sucursal)).representacion
                except Exception, e:
                    icon = "fa-star"
                
                if s.pst_categoria_doc is not None:
                    clasificaciones.append(
                        (
                            s.pst_categoria_doc.categoria.valor, 
                            mx - s.pst_categoria_doc.categoria.valor,
                            icon
                        )
                    )
                else:
                    clasificaciones.append(
                        (
                            0,
                            mx,
                            icon
                        )
                    )

                #Las notificaciones por cada solicitud             
                n=Notificacion.objects.filter(
                    receptor_id=int(id_sesion), 
                    solicitud_id=s.id
                ).order_by('-fecha_emision').first()
                if n is not None:
                    if not notificacion.has_key(s.id):
                        notificacion.update({s.id:[]})
                    try:
                        doc=NotificacionDocumentoCompuesto.objects.get(
                            notificacion=n, 
                            documento__tipo_documento_compuesto__abreviacion='N'
                        ).documento
                        src=doc.ruta_documento
                        extension=doc.extension
                    except:
                        src=None
                        extension=None
                    notificacion[s.id].append(
                        {
                            'observacion': n.observacion,
                            'src': src,
                            'extension': extension
                        }
                    )
                    #notificacion.update({s.id:n.observacion})

                #Las opciones segun el estatus de la solicitud
                opciones.update({s.id:constants.OPCIONES[s.estatus.abreviacion]})
                
                #Documentos asociados
                notificacion_doc= NotificacionDocumentoCompuesto.objects.filter(
                    notificacion__solicitud=s
                ).distinct('documento').exclude(
                        Q(documento__tipo_documento_compuesto__abreviacion = 'N') 
                        )
                if notificacion_doc:
                    if not documentos.has_key(s.id):
                        documentos.update({s.id:[]})
                    for doc in notificacion_doc:
                        documentos[s.id].append(
                            {
                                'nombre': doc.documento.tipo_documento_compuesto.nombre,
                                'abreviacion': doc.documento.tipo_documento_compuesto.abreviacion,
                                'ruta': doc.documento.ruta_documento,
                                'firmado': doc.documento.firmado
                            }
                    )
                """
                #Oficio de reparación asociado a la solicitud
                notificacion_rep= NotificacionDocumentoCompuesto.objects.filter(
                    documento__tipo_documento_compuesto__abreviacion='OAR',
                    notificacion__solicitud=s
                ).first()

                if notificacion_rep:
                    oficio_reparacion.update({s.id:notificacion_rep.documento.ruta_documento})

                #Informe técnico asociado a la solicitud
                notificacion_doc= NotificacionDocumentoCompuesto.objects.filter(
                    documento__tipo_documento_compuesto__abreviacion='IT',
                    notificacion__solicitud=s
                ).first()
                if notificacion_doc:
                    informe_tecnico.update({s.id:notificacion_doc.documento.ruta_documento})

                """
                f = Asignacion.objects.filter(
                    solicitud_id=s, 
                    asignacion_habilitada=True
                ).values('funcionario')
                
                #Los funcionarios asignados a esa solicitud
                funcionarios= Funcionario.objects.filter(id__in=f)
                i=0
                
                for e in funcionarios:
                    #USA DIRECCIONFUNCIONARIOTIPOROL
                    #x=DireccionFuncionarioTiporol.objects.filter(funcionario=e)
                    if e.tiporol.nombre=='analista':
                        analistax.update({s.id:[(e.id, e.nombre+" "+e.apellido)]})
                    elif e.tiporol.nombre=='inspector':
                        if i == 0:
                            inspectorx.update({s.id:[(e.id, e.nombre+" "+e.apellido)]})
                            cantidad.update({s.id:1})
                            i+=1
                        else:
                            inspectorx[s.id].append((e.id,e.nombre+" "+e.apellido))
                            cantidad.update({s.id:2})                            
                    elif e.tiporol.nombre=='coordinador_ct':
                        coordinadorx.update({s.id:e.nombre+" "+e.apellido})
                    elif e.tiporol.nombre=='director_ct':
                        directorx.update({s.id:e.nombre+" "+e.apellido})

            dprint(sol_firmas=sol_firmas)
            sol_cat= zip(solicitudes,clasificaciones)
            context.update({
                'actor': user.get_full_name(),
                'natural': natural,
                'juridica':juridica,
                'solicitudes': sol_cat,
                'opciones': opciones,
                'funcionario_id': funcionario.id,
                'analistax': analistax,
                'inspectorx': inspectorx,
                'coordinadorx': coordinadorx,
                'directorx': directorx,
                'tiporol': funcionario.tiporol.nombre,
                'cantidad':cantidad,
                'notificacion':notificacion,
                'documentos': documentos,
            })

            if bool(sol_firmas) == True:
                context.update({'sol_firmas': sol_firmas})

            if paginars == True:
                context.update({'p':p, 'mas':mas})

            if request.GET.has_key('busqueda'):
                cache.set(
                    key,
                    busqueda_datos
                )

            if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})
            
            user = funcionario.tiporol.nombre
            context.update({user: True})

            return render(request, 'bandeja.html', context)           
        else:
            return Http404     


class Empleados(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(Empleados, self).dispatch(*args, **kwargs)

    def get(self,request,*args,**kwargs):
        user = request.user
        id_sesion = user.id
        funcionario = Funcionario.objects.get(user_id=int(id_sesion))

        if funcionario.tiporol.nombre == 'coordinador_ct':
            funcionarios = Funcionario.objects.filter(tiporol__nombre='analista');
        else:
            funcionarios = Funcionario.objects.filter(tiporol__nombre='inspector');  

        paginars = False
        mas = True
        if request.GET.has_key('p') and request.GET.has_key('s'): 
            paginars = True
            p= int(request.GET['p'])
            s= request.GET['s']
            dprint(s)
            if s == '-':
                p -= 1
            elif s == '+':
                dprint(s=s)
                p += 1
            func= funcionarios   
            num=((p+1)*constants.ELEMENTO_POR_PAGINA)
            funcionarios = funcionarios[(p*constants.ELEMENTO_POR_PAGINA):num]
            if len(func[num:num+1]) ==0:
                mas = False

        if not request.GET.has_key('p') or not request.GET.has_key('s'):
            p= 0
            num=((p+1)*constants.ELEMENTO_POR_PAGINA)
            paginars = True
            func= funcionarios
            funcionarios = funcionarios[(p*constants.ELEMENTO_POR_PAGINA):num]
            if len(func[num:num+1]) ==0:
                mas = False

        context={
            'actor': user.get_full_name(),
            'funcionario': funcionario,
            'funcionarios':funcionarios,
            'tiporol': funcionario.tiporol.nombre
        }
        if paginars == True:
            context.update({'p': p, 'mas': mas})

        user = funcionario.tiporol.nombre
        context.update({user: True})
        
        return render(request,'empleados.html',context)


class AdminEmpleados(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(AdminEmpleados, self).dispatch(*args, **kwargs)

    def get(self,request,*args,**kwargs):
        func_id= int(request.user.pk)
        tiporol = kwargs['tiporol']
        funcionario_coord = Funcionario.objects.filter(Q(user_id= func_id) 
            & (Q(tiporol__nombre='coordinador_ct') 
                | Q(tiporol__nombre='coordinador_dif'))).first()
        if funcionario_coord:
            if request.GET['funcionario_id']:
                funcionario_id = int(request.GET['funcionario_id'])

                if tiporol == 'coordinador_ct':
                    analistas = Funcionario.objects.filter(id= funcionario_id, 
                        tiporol__nombre='analista').first()
                    if analistas:
                        verif_modal = Asignacion.objects.filter(funcionario=analistas, 
                            asignacion_habilitada=True)
                        if len(verif_modal)>0:
                            asigs= [e.solicitud_id for e in verif_modal]
                            """                            
                            solicitudes = Solicitud.objects.filter(
                                (Q(estatus__abreviacion='SAR') | Q(estatus__abreviacion='EC') 
                                | Q(estatus__abreviacion='SEAR')
                                | Q(estatus__abreviacion='EANP')) | Q(estatus__abreviacion='SAI')
                                & Q(id__in=asigs))
                            """
                            solicitudes = Solicitud.objects.filter(id__in=asigs)

                            if len(solicitudes)>0:
                                analista_list = algoritmo_asignacion.asignacion_analista_inspector('analista')

                                for e in analista_list:
                                    if e[0] == funcionario_id:
                                        analista_list.remove(e)
                                        break
                                jsontmp = {
                                    "err_msg": "",
                                    "success": "Pagina encontrada",
                                    "data": {"analistas":analista_list}
                                }
                                return HttpResponse(
                                    json.dumps(jsontmp, sort_keys=False),
                                    content_type="application/json"
                                )
                        jsontmp = {
                            "err_msg": "No necesario asignar nuevo analista",
                            "success": ""
                        }
                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                        )

                elif tiporol == 'coordinador_dif':
                    inspectores = Funcionario.objects.filter(id= funcionario_id, 
                        tiporol__nombre='inspector').first()

                    if inspectores:

                        asignacion1 = Asignacion.objects.filter(
                            funcionario__tiporol__nombre='inspector',
                            asignacion_habilitada=True
                            ).values_list('solicitud').annotate(dcount=Count('funcionario'))

                        solicits_insp=[]
                        
                        for e in asignacion1:
                            if e[1] == 1:
                                solicits_insp.append(e[0])

                        asignacion_extra = Asignacion.objects.filter(
                            funcionario=inspectores,
                            asignacion_habilitada=True,
                            solicitud_id__in=solicits_insp
                        )
                        solicituds = [e.solicitud_id for e in asignacion_extra]
                        """
                        solicitudes = Solicitud.objects.filter(
                            (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                            | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                            | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                            | Q(estatus__abreviacion='EA') ) & Q(id__in=solicituds))
                        """
                        solicitudes = Solicitud.objects.filter(id__in=solicituds)

                        if len(solicitudes)>0:

                            inspector_list=algoritmo_asignacion.asignacion_analista_inspector('inspector')

                            for e in inspector_list:
                                if e[0] == funcionario_id:
                                    inspector_list.remove(e)
                                    break
                            jsontmp = {
                                "err_msg": "",
                                "success": "Pagina encontrada",
                                "data": {"inspectores":inspector_list}
                            }
                            
                        else:
                            jsontmp = {
                                "err_msg": "No necesario asignar nuevo inspector",
                                "success": "",
                            }
                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                        )


        jsontmp = {
            "err_msg": "Parametros invalidos",
            "success": "", 
            "data": ""
        }
        return HttpResponse(
            json.dumps(jsontmp, sort_keys=False),
                content_type="application/json",
                status=400
        )

    def post(self, request, *args, **kwargs):
        tiporol = kwargs['tiporol']
        if request.POST['funcionario_id']: 
            esta = False
            if request.POST.has_key('funcionario_nuevo'):
                if request.POST['funcionario_nuevo']:
                    esta = True
            funcionario_id = int(request.POST['funcionario_id'])
            if esta==True:
                funcionario_nuevo = int(request.POST['funcionario_nuevo'])

                if tiporol == 'coordinador_ct':
                    func_nuevo = Funcionario.objects.filter(
                        id= funcionario_nuevo, tiporol__nombre='analista').first()
                    if func_nuevo:
                        analista = Funcionario.objects.filter(id=funcionario_id, 
                            tiporol__nombre='analista', habilitado=True).first()
                        dprint(analista)
                        if analista:      
                            #tomando todas las solicitudes asignadas del analista viejo
                            #TODO Revisar si son algunos estados o todos
                            asignaciones = Asignacion.objects.filter(
                                funcionario=analista,
                                asignacion_habilitada=True)
                            solicits = [e.solicitud_id for e in asignaciones]
                            """
                            solicitudes = Solicitud.objects.filter(
                                (Q(estatus__abreviacion='SAR') | Q(estatus__abreviacion='EC') 
                                | Q(estatus__abreviacion='SEAR')
                                | Q(estatus__abreviacion='EANP')) | Q(estatus__abreviacion='SAI') 
                                & Q(id__in=solicits))
                            """
                            solicitudes = Solicitud.objects.filter(id__in=solicits)

                            if solicitudes:
                                solicitudes_analista = [e.id for e in solicitudes]
                                asignaciones_nueva = Asignacion.objects.filter(
                                    funcionario=analista, solicitud_id__in=solicitudes_analista)
                                #tomando todas las notificaciones del analista viejo
                                notificaciones_emisor_viejo = Notificacion.objects.filter(
                                    emisor=analista.user, solicitud_id__in=solicitudes_analista)
                                notificaciones_receptor_viejo = Notificacion.objects.filter(
                                    receptor = analista.user, solicitud_id__in=solicitudes_analista)

                                #pasando notificaciones a backup
                                for e in notificaciones_emisor_viejo:
                                    notificaciones_movidas_back=  NotificacionBackup(
                                        emisor=e.emisor, receptor=e.receptor, 
                                        solicitud=e.solicitud, asunto=e.asunto,
                                        observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                        estatus_actual=e.estatus_actual
                                    )
                                    notificaciones_movidas_back.save()
                                    notif_emisor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                    notificacion=e)
                                    dprint(notif_emisor_doc=notif_emisor_doc)
                                    for f in notif_emisor_doc:
                                        f.notificacion_backup_id = notificaciones_movidas_back.id
                                        f.notificacion_id = None
                                        f.save()

                                    e.delete()

                                for e in notificaciones_receptor_viejo:
                                    notificaciones_movidas_back=  NotificacionBackup(
                                        emisor=e.emisor, receptor=e.receptor, 
                                        solicitud=e.solicitud, asunto=e.asunto,
                                        observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                        estatus_actual=e.estatus_actual
                                    )
                                    notificaciones_movidas_back.save()
                                    dprint(receptor=notificaciones_movidas_back)
                                    notif_receptor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                    notificacion=e)
                                    dprint(notif_receptor_doc=notif_receptor_doc)
                                    for f in notif_receptor_doc:
                                        f.notificacion_backup_id = notificaciones_movidas_back.id
                                        f.notificacion_id = None
                                        f.save()

                                    e.delete()

                                #moviendo asignaciones del analista viejo al nuevo

                                if asignaciones:
                                    tipoasig = TipoAsignacion.objects.get(abreviacion='A')
                                    for n in asignaciones_nueva:
                                        asignacion_nueva = Asignacion(
                                            funcionario=func_nuevo, tipo_asignacion=tipoasig,
                                            solicitud_id=n.solicitud_id, 
                                            fecha_asignacion=datetime.datetime.now(),
                                            asignacion_habilitada=True)
                                        asignacion_nueva.save()
                                        n.asignacion_habilitada=False
                                        n.save()

                                for s in solicitudes:
                                    if s.funcionario_id == analista.id:
                                        s.funcionario_id = func_nuevo.id
                                        s.save()



                            analista.habilitado = False
                            analista.save()

                            jsontmp = {
                                "err_msg": "",
                                "success": "Analista Deshabilitado",
                                "data":"",
                            }
                            return HttpResponse(
                                json.dumps(jsontmp, sort_keys=False),
                                    content_type="application/json"
                            )
                elif tiporol == 'coordinador_dif':
                    func_nuevo = Funcionario.objects.filter(
                        id= funcionario_nuevo, tiporol__nombre='inspector').first()
                    if func_nuevo:
                        inspector = Funcionario.objects.filter(id=funcionario_id,
                            tiporol__nombre='inspector', habilitado=True).first()
                        if inspector:      
                            asignacion1 = Asignacion.objects.filter(
                                funcionario__tiporol__nombre='inspector',
                                asignacion_habilitada=True
                                ).values_list('solicitud').annotate(dcount=Count('funcionario'))

                            solicits_insp=[]
                            
                            for e in asignacion1:
                                if e[1] > 1:
                                    solicits_insp.append(e[0])

                            asignacion_extra = Asignacion.objects.filter(
                                funcionario=inspector,
                                asignacion_habilitada=True,
                                solicitud_id__in=solicits_insp
                            )
                            asignaciones = Asignacion.objects.filter(
                                funcionario=inspector,
                                asignacion_habilitada=True
                            )
                            solicituds1 = [e.solicitud_id for e in asignaciones]
                            if asignacion_extra:
                                solicits_extra = [e.solicitud_id for e in asignacion_extra]
                                solicits= [e for e in solicituds1 if e not in solicits_extra]
                                """
                                solicitudes_extra = Solicitud.objects.filter(
                                    (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                                    | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                                    | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                                    | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits_extra))
                                """

                                solicitudes_extra = Solicitud.objects.filter(id__in=solicits_extra)

                                asignaciones_extra = Asignacion.objects.filter(
                                    funcionario=inspector,
                                    asignacion_habilitada=True,
                                    solicitud_id__in = solicitudes_extra
                                )
                            else:
                                solicits = solicituds1
                            """    
                            solicitudes = Solicitud.objects.filter(
                                (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                                | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                                | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                                | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits))
                            """
                            solicitudes= Solicitud.objects.filter(id__in=solicits)

                            dprint(solicitudes=solicitudes)

                            asignaciones_quedan = Asignacion.objects.filter(
                                funcionario=inspector,
                                asignacion_habilitada=True,
                                solicitud_id__in = solicitudes
                            )
                            
                            if len(solicitudes)!=0:
                                #tomando todas las notificaciones del inspector viejo
                                notificaciones_emisor_viejo = Notificacion.objects.filter(
                                    emisor=inspector.user, solicitud__in=solicitudes
                                )
                                notificaciones_receptor_viejo = Notificacion.objects.filter(
                                    receptor = inspector.user, solicitud__in=solicitudes
                                )

                                #moviendo notificaciones del inspector viejo al nuevo
                                for e in notificaciones_emisor_viejo:
                                    notificaciones_movidas_back=  NotificacionBackup(
                                        emisor=e.emisor, receptor=e.receptor, 
                                        solicitud=e.solicitud, asunto=e.asunto,
                                        observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                        estatus_actual=e.estatus_actual
                                    )
                                    notificaciones_movidas_back.save()
                                    notif_emisor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                    notificacion=e)
                                    dprint(notif_emisor_doc=notif_emisor_doc)
                                    for f in notif_emisor_doc:
                                        f.notificacion_backup_id = notificaciones_movidas_back.id
                                        f.notificacion_id = None
                                        f.save()

                                    e.delete()

                                for e in notificaciones_receptor_viejo:
                                    notificaciones_movidas_back=  NotificacionBackup(
                                        emisor=e.emisor, receptor=e.receptor, 
                                        solicitud=e.solicitud, asunto=e.asunto,
                                        observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                        estatus_actual=e.estatus_actual
                                    )
                                    notificaciones_movidas_back.save()
                                    dprint(receptor=notificaciones_movidas_back)
                                    notif_receptor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                    notificacion=e)
                                    dprint(notif_receptor_doc=notif_receptor_doc)
                                    for f in notif_receptor_doc:
                                        f.notificacion_backup_id = notificaciones_movidas_back.id
                                        f.notificacion_id = None
                                        f.save()

                                    e.delete()
                                #moviendo asignaciones del inspector viejo al nuevo
                                if len(asignaciones_quedan)!=0:
                                    tipoasig = TipoAsignacion.objects.get(abreviacion='I')
                                    for n in asignaciones_quedan:
                                        asignacion_nueva = Asignacion(
                                            funcionario=func_nuevo, tipo_asignacion=tipoasig,
                                            solicitud_id=n.solicitud_id, 
                                            fecha_asignacion=datetime.datetime.now(),
                                            asignacion_habilitada=True)
                                        asignacion_nueva.save()
                                        n.asignacion_habilitada=False
                                        n.save()

                                for s in solicitudes:
                                    if s.funcionario_id == inspector.id:
                                        s.funcionario_id = func_nuevo.id
                                        s.save()
                                    elif s.funcionario_extra_id == inspector.id:
                                        s.funcionario_extra_id = func_nuevo.id
                                        s.save()

                            if len(asignacion_extra)!=0:
                                for n in asignaciones_extra:
                                    n.asignacion_habilitada=False
                                    n.save()

                            inspector.habilitado = False
                            inspector.save()
                            #fun with pdf time!
                            tipoInspector = TipoAsignacion.objects.get(abreviacion='I')
                            """
                            solicitudes = Solicitud.objects.filter(
                                (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                                | Q(estatus__abreviacion='EI')
                                | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                                | Q(estatus__abreviacion='EA') ) & Q(id__in=solicituds1)
                            )
                            """
                            solicitudes = Solicitud.objects.filter(id__in=solicituds1)

                            asignaciones = Asignacion.objects.filter(tipo_asignacion__abreviacion='I')
                            for s in solicitudes:
                                inspectores = asignaciones.filter(
                                    solicitud=s,asignacion_habilitada=True,
                                    tipo_asignacion=tipoInspector
                                )
                                coordinador_dif = Asignacion.objects.get(
                                    solicitud=s,asignacion_habilitada=True,
                                    funcionario__tiporol__nombre='coordinador_dif'
                                ).funcionario
                                plantilla = PlantillaDocumento.objects.get(formato="documentos/credencial.html")
                                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                                path = model_list.get_file_path(coordinador_dif.user.rif,"",'credenciales')
                                locationPath ='documents/files/'+ path

                                if len(inspectores)==1:
                                    notificacion= Notificacion(
                                        emisor=coordinador_dif.user, receptor=inspectores[0].funcionario.user, 
                                        solicitud=s, estatus_actual=s.estatus
                                    )
                                    notificacion.save()
                                    dprint(notificacion.id)
                                    try:
                                        #Creando el documento
                                        nombre_documento = "%s_credencial_%s_%s" % (
                                            coordinador_dif.user.rif,
                                            s.id,
                                            inspectores[0].funcionario.id
                                        )
                                        credencial = Documento.objects.filter(
                                            nombre=nombre_documento).first()
                                        if credencial:
                                            credencial.fecha_aprobacion=datetime.datetime.now()
                                            credencial.eliminado=False
                                        else:
                                            data = Storage(
                                                nombre=nombre_documento,
                                                fecha_aprobacion=datetime.datetime.now(),
                                                plantilla_documento=plantilla,
                                                ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                                extension = 'pdf',
                                                tipo_documento_compuesto=tipo_documento,
                                            )
                                            credencial = Documento.create(data)
                                        credencial.save()

                                        #La notificacion respectiva a uno de los inspectores
                                        ndc = NotificacionDocumentoCompuesto(
                                            notificacion = notificacion,
                                            documento = credencial
                                        )
                                        ndc.save()

                                        try:
                                            #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                            direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                                            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                                +str(direc.codigo_postal)
                                            data = Storage(
                                                pagesize='A4',
                                                nombre_establecimiento=s.pst.denominacion_comercial,
                                                direccion=direccionPST,
                                                nombre_inspector1=inspectores[0].funcionario.nombre\
                                                    + " "+inspectores[0].funcionario.apellido,
                                                cedula_inspector1=inspectores[0].funcionario.cedula,
                                                nombre_inspector2="",
                                                cedula_inspector2="",
                                                nombre_coordinador_dif=coordinador_dif.nombre\
                                                    +" "+coordinador_dif.apellido,
                                            )

                                            generar_pdf.generar_pdf(
                                                context=data,
                                                ruta_template='documentos/credencial.html',
                                                ruta_documento=locationPath,
                                                nombre_documento=nombre_documento
                                            )
                                        except Exception, e:
                                            dprint("Hubo errores creando el documento")
                                            raise e
                                    except Exception, e:
                                        dprint("Hubo errores haciendo las notificaciones")
                                        raise e
                                else:
                                    notificacion= Notificacion(
                                        emisor=coordinador_dif.user, receptor=inspectores[0].funcionario, 
                                        solicitud=s, estatus_actual=s.estatus
                                    )
                                    notificacion1= Notificacion(
                                        emisor=coordinador_dif.user, receptor=inspectores[1].funcionario, 
                                        solicitud=s, estatus_actual=s.estatus
                                    )
                                    notificacion.save()
                                    notificacion1.save()
                                    try:
                                        #Creando el documento
                                        nombre_documento = "%s_credencial_%s_%s_%s" % (
                                            coordinador_dif.user.rif,
                                            s.id,
                                            inspectores[0].funcionario.id,
                                            inspectores[1].funcionario.id
                                        )
                                        credencial = Documento.objects.filter(
                                            nombre=nombre_documento).first()
                                        if credencial:
                                            credencial.fecha_aprobacion=datetime.datetime.now()
                                            credencial.eliminado=False
                                        else:
                                            data = Storage(
                                                nombre=nombre_documento,
                                                fecha_aprobacion=datetime.datetime.now(),
                                                plantilla_documento=plantilla,
                                                ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                                extension = 'pdf',
                                                tipo_documento_compuesto=tipo_documento,
                                            )
                                            credencial = Documento.create(data)
                                        credencial.save()

                                        #La notificacion respectiva a uno de los inspectores
                                        ndc = NotificacionDocumentoCompuesto(
                                            notificacion = notificacion,
                                            documento = credencial
                                        )
                                        ndc.save()
                                        #La notificacion respectiva al otro inspector
                                        ndc1 = NotificacionDocumentoCompuesto(
                                            notificacion = notificacion1,
                                            documento = credencial
                                        )
                                        ndc1.save()

                                        try:
                                            #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                            direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                                            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                                +str(direc.codigo_postal)
                                            data = Storage(
                                                pagesize='A4',
                                                nombre_establecimiento=s.pst.denominacion_comercial,
                                                direccion=direccionPST,
                                                nombre_inspector1=inspectores[0].funcionario.nombre\
                                                    + " "+inspectores[0].funcionario.apellido,
                                                cedula_inspector1=inspectores[0].funcionario.cedula,
                                                nombre_inspector2=inspectores[1].funcionario.nombre\
                                                    + " "+inspectores[1].funcionario.apellido,
                                                cedula_inspector2=inspectores[1].funcionario.cedula,
                                                nombre_coordinador_dif=coordinador_dif.nombre\
                                                    +" "+coordinador_dif.apellido,
                                            )

                                            generar_pdf.generar_pdf(
                                                context=data,
                                                ruta_template='documentos/credencial.html',
                                                ruta_documento=locationPath,
                                                nombre_documento=nombre_documento
                                            )
                                        except Exception, e:
                                            dprint("Errores documento") 
                                            raise e
                                    except Exception, e:
                                        dprint("Errores notificaciones")
                                        raise e
                            jsontmp = {
                                "err_msg": "",
                                "success": "Inspector Deshabilitado",
                                "data":"",
                            }

                            return HttpResponse(
                                json.dumps(jsontmp, sort_keys=False),
                                    content_type="application/json"
                            )
                jsontmp = {
                    "err_msg": "Parametros invalidos",
                    "success": "", 
                    "data": ""
                }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json",
                        status=400
                )


            else:
                if tiporol == 'coordinador_ct':
                    analista = Funcionario.objects.filter(id=funcionario_id, 
                        habilitado=False).first()
                    if analista:
                        analista.habilitado = True
                        analista.save()

                        jsontmp = {
                            "err_msg": "",
                            "success": "Analista Habilitado",
                            "data":"",
                        }

                    elif request.POST.has_key('funcionario'):
                        analistes = Funcionario.objects.filter(id=funcionario_id, 
                            tiporol__nombre='analista', habilitado=True).first()
                        if analistes:
                            analistes.habilitado = False
                            analistes.save()
                            jsontmp = {
                                "err_msg": "",
                                "success": "Analista Deshabilitado",
                                "data":"",
                            }
                        else:
                            jsontmp = {
                                "err_msg": "Parametros invalidos",
                                "success": ""
                            }
                    else:
                        jsontmp = {
                            "err_msg": "Error: No se puede dejar sin reemplazar un funcionario",
                            "success": "", 
                        }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                    )   

                elif tiporol == 'coordinador_dif':
                    dprint("esta == false")
                    inspector = Funcionario.objects.filter(id=funcionario_id, 
                        habilitado=False).first()
                    if inspector:
                        inspector.habilitado = True
                        inspector.save()
                        jsontmp = {
                            "err_msg": "",
                            "success": "Inspector Habilitado",
                            "data":"",
                        }
                    elif request.POST.has_key('funcionario'):
                        insps = Funcionario.objects.filter(id=funcionario_id, 
                            tiporol__nombre='inspector', habilitado=True).first()
                        dprint(insps)
                        if insps:
                            asignacion1 = Asignacion.objects.filter(
                                funcionario__tiporol__nombre='inspector',
                                asignacion_habilitada=True
                            ).values_list('solicitud').annotate(dcount=Count('funcionario'))
                            solicits_insp=[]
                            
                            for e in asignacion1:
                                if e[1] > 1:
                                    solicits_insp.append(e[0])
                            """
                            solicitudes_extra = Solicitud.objects.filter(
                                (Q(estatus__abreviacion='VI') | Q(estatus__abreviacion='RI') 
                                | Q(estatus__abreviacion='PAI') | Q(estatus__abreviacion='EI')
                                | Q(estatus__abreviacion='CI') | Q(estatus__abreviacion='EANP') 
                                | Q(estatus__abreviacion='EA') ) & Q(id__in=solicits_insp))
                            """
                            solicitudes_extra = Solicitud.objects.filter(id__in=solicits_insp)

                            solicitusp = [e.id for e in solicitudes_extra]

                            asignacion_extra = Asignacion.objects.filter(
                                funcionario=insps,
                                asignacion_habilitada=True,
                                solicitud_id__in=solicitusp
                            )
                            dprint(asignacion_extra)

                            for e in asignacion_extra:
                                e.asignacion_habilitada=False
                                e.save()

                            for s in solicitudes_extra:
                                dprint(solicitudes_extra=solicitudes_extra)
                                if s.funcionario_id == insps.id:
                                    print "funcionario_id"
                                    s.funcionario_id = None
                                    s.save()
                                elif s.funcionario_extra_id == insps.id:
                                    print "funcionario_extra_id"
                                    s.funcionario_extra_id = None
                                    s.save()
                                    
                            insps.habilitado = False
                            insps.save()

                            inspector_restante = Asignacion.objects.filter(
                                funcionario__tiporol__nombre='inspector',
                                asignacion_habilitada=True,
                                solicitud_id__in=solicitusp
                            ).first()

                            plantilla = PlantillaDocumento.objects.get(formato="documentos/credencial.html")
                            tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                            for s in solicitudes_extra:
                                coordinador_dif = Asignacion.objects.get(
                                    solicitud=s,asignacion_habilitada=True,
                                    funcionario__tiporol__nombre='coordinador_dif'
                                ).funcionario
                                path = model_list.get_file_path(coordinador_dif.user.rif,"",'credenciales')
                                locationPath ='documents/files/'+ path
                                notificacion= Notificacion(
                                    emisor=coordinador_dif.user, receptor=inspector_restante.funcionario.user, 
                                    solicitud=s, estatus_actual=s.estatus
                                )
                                notificacion.save()
                                dprint(notificacion)
                                try:
                                    #Creando el documento
                                    nombre_documento = "%s_credencial_%s_%s" % (
                                        coordinador_dif.user.rif,
                                        s.id,
                                        inspector_restante.funcionario.id
                                    )
                                    credencial = Documento.objects.filter(
                                        nombre=nombre_documento).first()
                                    if credencial:
                                        credencial.fecha_aprobacion=datetime.datetime.now()
                                        credencial.eliminado=False
                                    else:
                                        data = Storage(
                                            nombre=nombre_documento,
                                            fecha_aprobacion=datetime.datetime.now(),
                                            plantilla_documento=plantilla,
                                            ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                            extension = 'pdf',
                                            tipo_documento_compuesto=tipo_documento,
                                        )
                                        credencial = Documento.create(data)

                                    credencial.save()

                                    #La notificacion respectiva a uno de los inspectores
                                    ndc = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion,
                                        documento = credencial
                                    )
                                    ndc.save()

                                    try:
                                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                        direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                            +str(direc.codigo_postal)
                                        data = Storage(
                                            pagesize='A4',
                                            nombre_establecimiento=s.pst.denominacion_comercial,
                                            direccion=direccionPST,
                                            nombre_inspector1=inspector_restante.funcionario.nombre\
                                                + " "+inspector_restante.funcionario.apellido,
                                            cedula_inspector1=inspector_restante.funcionario.cedula,
                                            nombre_inspector2="",
                                            cedula_inspector2="",
                                            nombre_coordinador_dif=coordinador_dif.nombre\
                                                +" "+coordinador_dif.apellido,
                                        )

                                        generar_pdf.generar_pdf(
                                            context=data,
                                            ruta_template='documentos/credencial.html',
                                            ruta_documento=locationPath,
                                            nombre_documento=nombre_documento
                                        )
                                    except Exception, e:
                                        dprint("Hubo errores creando el documento")
                                        raise e
                                except Exception, e:
                                    dprint("Hubo errores creando la credencial")
                                    raise e
                            jsontmp = {
                                "err_msg": "",
                                "success": "Inspector Deshabilitado",
                                "data":"",
                            }
                        else:
                            jsontmp = {
                                "err_msg": "Parametros invalidos",
                                "success": ""
                            }
                    else:
                        jsontmp = {
                            "err_msg": "Error: No se puede dejar sin reemplazar un funcionario",
                            "success": "",
                        }

                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                    )

        jsontmp = {
            "err_msg": "Parametros invalidos",
            "success": "", 
            "data": ""
        }
        return HttpResponse(
            json.dumps(jsontmp, sort_keys=False),
                content_type="application/json",
                status=400
        )

class IncumplimientoReparacion(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(IncumplimientoReparacion, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        emisor_id= int(request.user.pk)
        try:
            id_s = request.POST['solicitud']
            if len (request.POST['comentario-incumplimiento'])==0:
                observacion="No se han registrado observaciones"
            else:
                observacion=request.POST['comentario-incumplimiento']
            emisor=Funcionario.objects.filter(user_id=int(emisor_id)).first()
            tiporol_emisor=emisor.tiporol.nombre
            estatus= Estatus.objects.filter(abreviacion='EN').first()
            """
            if tiporol_emisor == 'analista':
                tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='C')
                estatus= Estatus.objects.filter(abreviacion='EAN').first()
            """
            if tiporol_emisor == 'coordinador_ct':
                tiporol= TipoRol.objects.filter(nombre='director_ct').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='D')
            elif tiporol_emisor == 'director_ct':
                tiporol= TipoRol.objects.filter(nombre='viceministro').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='V')
            elif tiporol_emisor == 'viceministro':
                tiporol= TipoRol.objects.filter(nombre='ministro').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='V')
            solicitud= Solicitud.objects.filter(id=int(id_s)).first()

            #Verificamos los fucionarios involucrados en esa solicitud
            asig=Asignacion.objects.filter(solicitud_id=solicitud.id, funcionario__tiporol__id=tiporol.id, asignacion_habilitada=True).order_by('-fecha_asignacion').first()
            
            if not asig:
                funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion(tiporol.nombre)
                asignacion = Asignacion(
                    funcionario_id=funcionario_id,
                    tipo_asignacion=tipoasig, 
                    solicitud_id=solicitud.id,
                    fecha_asignacion=datetime.datetime.now(),
                    asignacion_habilitada=True
                    )
                asignacion.save()
                asig=Asignacion.objects.filter(solicitud_id=solicitud.id, funcionario__tiporol__id=tiporol.id, asignacion_habilitada=True).order_by('-fecha_asignacion').first()
            receptor = Funcionario.objects.filter(id=asig.funcionario.id).first()
            notificacion= Notificacion(
                emisor_id=emisor_id,
                receptor_id=receptor.user_id, 
                solicitud_id=solicitud.id,
                estatus_actual=estatus
                )
            notificacion.save()
            solicitud.estatus_id=estatus.id
            solicitud.funcionario_id= receptor.id
            solicitud.fecha_modificacion_estado=datetime.datetime.now()
            solicitud.save()
            jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}

            return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
        except Exception, e:
            raise e


class ProponerAprobacion(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(ProponerAprobacion, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        emisor_id= int(request.user.pk)
        try:
            id_s = request.POST['solicitud']
            ultima_notificacion=Notificacion.objects.filter(
                solicitud__id=id_s
                ).order_by('-fecha_emision').first()

            validacion = val(
                request.FILES,
                'archivo',
                ['application/pdf', 'image/jpeg', 'image/png'] ,
                2621440) if request.FILES.has_key('archivo') else False

            if len (request.POST['comentario-proponeraprob'])==0:
                observacion=ultima_notificacion.observacion
            else:
                observacion=request.POST['comentario-proponeraprob']

            emisor=Funcionario.objects.filter(user_id=int(emisor_id)).first()
            tiporol_emisor=emisor.tiporol.nombre
            estatus= Estatus.objects.filter(abreviacion='EA').first()
            if tiporol_emisor == 'analista':
                tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='C')
                estatus= Estatus.objects.filter(abreviacion='SEAR').first()
            if tiporol_emisor == 'coordinador_ct':
                tiporol= TipoRol.objects.filter(nombre='director_ct').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='D')
            elif tiporol_emisor == 'director_ct':
                tiporol= TipoRol.objects.filter(nombre='viceministro').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='V')
            elif tiporol_emisor == 'viceministro':
                tiporol= TipoRol.objects.filter(nombre='ministro').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='V')
            solicitud= Solicitud.objects.filter(id=int(id_s)).first()
            #Verificamos los fucionarios involucrados en esa solicitud
            asig=Asignacion.objects.filter(solicitud_id=solicitud.id, funcionario__tiporol__id=tiporol.id, asignacion_habilitada=True).order_by('-fecha_asignacion').first()
            #funcionarios = Funcionario.objects.filter(tiporol_id=tiporol.id).values_list('id')
            #ids= [e[0] for e in funcionarios]
            #asig = Asignacion.objects.filter(funcionario_id__in=ids, solicitud_id=solicitud.id).first()
            if not asig:
                funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion(tiporol.nombre)
                asignacion = Asignacion(
                    funcionario_id=funcionario_id,
                    tipo_asignacion=tipoasig, 
                    solicitud_id=solicitud.id,
                    fecha_asignacion=datetime.datetime.now(),
                    asignacion_habilitada=True
                    )
                asignacion.save()
                asig=Asignacion.objects.filter(solicitud_id=solicitud.id, funcionario__tiporol__id=tiporol.id, asignacion_habilitada=True).order_by('-fecha_asignacion').first()
            receptor = Funcionario.objects.filter(id=asig.funcionario.id).first()
            notificacion= Notificacion(
                emisor_id=emisor_id,
                receptor_id=receptor.user_id, 
                solicitud_id=solicitud.id,
                estatus_actual=estatus,
                observacion=observacion
                #archivo=request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
            notificacion.save()
            if validacion:
                #TODO: volver plantilla documento nulo
                nombre_documento = "archivo_notificacion_%s_%s" % (
                    notificacion.id,
                    solicitud.id
                )
                documento = Documento(
                    nombre = nombre_documento,
                    ruta_documento=request.FILES['archivo'],
                    tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                    extension = str(request.FILES['archivo']).split(".")[1]
                )
                documento.save()

                notificaciondoc= NotificacionDocumentoCompuesto(
                    notificacion=notificacion,
                    documento=documento
                )
                notificaciondoc.save()
            solicitud.estatus_id=estatus.id
            solicitud.funcionario_id= receptor.id
            solicitud.fecha_modificacion_estado=datetime.datetime.now()
            solicitud.save()
            jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
            return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
        except Exception, error:
            return  HttpResponse(error, content_type="application/json", status=400)


class ProponerNoProcedencia(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(ProponerNoProcedencia, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        emisor_id = int(request.user.pk)

        try:
            id_s = request.POST['solicitud']

            ultima_notificacion=Notificacion.objects.filter(
                solicitud__id=id_s
                ).order_by('-fecha_emision').first()

            validacion = val(
                request.FILES,
                'archivo',
                ['application/pdf', 'image/jpeg', 'image/png'] ,
                2621440) if request.FILES.has_key('archivo') else False

            if len (request.POST['comentario-noproc'])==0:
                observacion=ultima_notificacion.observacion
            else:
                observacion=request.POST['comentario-noproc']
            emisor=Funcionario.objects.filter(user_id=int(emisor_id)).first()
            tiporol_emisor=emisor.tiporol.nombre
            estatus= Estatus.objects.filter(abreviacion='EANP').first()
            if tiporol_emisor == 'analista':
                tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='C')
            elif tiporol_emisor == 'coordinador_ct':
                tiporol= TipoRol.objects.filter(nombre='director_ct').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='D')
            elif tiporol_emisor == 'director_ct':
                tiporol= TipoRol.objects.filter(nombre='viceministro').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='V')
            elif tiporol_emisor == 'viceministro':
                tiporol= TipoRol.objects.filter(nombre='ministro').first()
                tipoasig=TipoAsignacion.objects.get(abreviacion='M')
            solicitud= Solicitud.objects.filter(id=int(id_s)).first()
            #Verificamos los fucionarios involucrados en esa solicitud
            asig=Asignacion.objects.filter(solicitud_id=solicitud.id, funcionario__tiporol__id=tiporol.id, asignacion_habilitada=True).order_by('-fecha_asignacion').first()
            #funcionarios = Funcionario.objects.filter(tiporol_id=tiporol.id).values_list('id')
            #ids= [e[0] for e in funcionarios]
            #asig = Asignacion.objects.filter(funcionario_id__in=ids, solicitud_id=solicitud.id).first()
            if not asig:
                funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion(tiporol.nombre)
                asignacion = Asignacion(
                    funcionario_id=funcionario_id,
                    tipo_asignacion=tipoasig, 
                    solicitud_id=solicitud.id,
                    fecha_asignacion=datetime.datetime.now(),
                    asignacion_habilitada=True
                )
                asignacion.save()
                asig = Asignacion.objects.filter(solicitud_id=solicitud.id, funcionario__tiporol__id=tiporol.id, asignacion_habilitada=True).order_by('-fecha_asignacion').first()
            receptor = Funcionario.objects.filter(id=asig.funcionario.id).first()
            notificacion = Notificacion(
                emisor_id=emisor_id,
                receptor=receptor.user,
                solicitud_id=solicitud.id,
                observacion=observacion,
                estatus_actual=estatus
                #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
            )
            notificacion.save()
            if validacion:
                #TODO: volver plantilla documento nulo
                nombre_documento = "archivo_notificacion_%s_%s" % (
                    notificacion.id,
                    solicitud.id
                )
                documento = Documento(
                    nombre = nombre_documento,
                    ruta_documento=request.FILES['archivo'],
                    tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                    extension = str(request.FILES['archivo']).split(".")[1]
                )
                documento.save()

                notificaciondoc= NotificacionDocumentoCompuesto(
                    notificacion=notificacion,
                    documento=documento
                )
                notificaciondoc.save()
            solicitud.estatus_id=estatus.id
            solicitud.funcionario_id= receptor.id
            solicitud.fecha_modificacion_estado=datetime.datetime.now()
            solicitud.save()
            jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
            return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
            #return HttpResponse(status=200)
        except Exception, e:
            raise e

            
class AnalistaOperacion(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(AnalistaOperacion, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        analista_ident = int(request.user.pk)
        try:
            id_s = request.POST['solicitud']
            op=kwargs['operacion']
            solicitud = Solicitud.objects.get(id=int(id_s))

            ultima_notificacion=Notificacion.objects.filter(
                solicitud__id=id_s
                ).order_by('-fecha_emision').first()

            if op == 'solicitaredicion':

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-observacion-edicion'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-observacion-edicion']
                estatus = Estatus.objects.get(abreviacion='EC')

                notificacion = Notificacion(
                    emisor_id=analista_ident,
                    receptor=solicitud.pst.user,
                    solicitud=solicitud,
                    observacion=observacion,
                    estatus_actual= estatus
                    #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )

                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.estatus = estatus
                solicitud.funcionario=None
                solicitud.fecha_modificacion_estado = datetime.datetime.now()
                solicitud.save()

                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                    +str(direc.codigo_postal)
                #licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

                #<--- Envio de Correo --->
                htmly = get_template('correo/correccion_requisitos_docs.html')
                text_plain = get_template('correo/correccion_requisitos_docs.txt')

                context = Context({
                    'razon_social': solicitud.pst.razon_social,
                    'direccion': direccionPST,
                    'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first()
                 })

                html_content = htmly.render(context)
                text_content = text_plain.render(context)
                """
                lic = LicenciaAsignada.objects.filter(usuario_pst=solicitud.pst, 
                    sucursal_id=solicitud.sucursal_id
                ).first()
                if lic:
                    if solicitud.sucursal_id:
                        licencia = lic.numero_licencia
                        suc= solicitud.pst.denominacion_comercial
                        direccion = "%s, %s, %s, %s" %(solicitud.sucursal.urbanizacion, solicitud.sucursal.avenida_calle, solicitud.sucursal.edificio, solicitud.sucursal.oficina_apartamento)
                    else:
                        licencia = lic.numero_licencia
                        suc= "Sede Principal"
                        direccs = Registro_Direccion.objects.get(pst=receptor)
                        direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)

                #<---- Envio de Correo ----->                        
                htmly = get_template('correo/correccion_requisitos_docs.html')
                text_plain = get_template('correo/correccion_requisitos_docs.txt')

                context = Context({
                 'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                 'nombre_establecimiento': suc,
                 'direccion': direccion,
                 'notificacion': notificacion.observacion
                })

                notif1 = re.sub('<br\s*?>', '\n', notificacion.observacion)

                notif = BeautifulSoup(notif1)
                
                #notif1 = re.sub("(?P<piso>(\_)?)(?P<ast>(\*\*)?)(?P<word>[a-zA-Z0-9]+)(?P=ast)(?P=piso)", "\g<word>",notif)
                
                context1 = Context({
                 'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                 'nombre_establecimiento': suc,
                 'direccion': direccion,
                 'notificacion': notif.get_text()
                })

                html_content = htmly.render(context)
                text_content = text_plain.render(context1)
                
                Busqueda de correo en parametros de configuracion
                try:
                    corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
                except ParametroConfiguracion.DoesNotExist:
                    raise e
                corrs = str(corr.valor)
                """

                thread_correo = threading.Thread(
                    name='thread_correo', 
                    target=correo, 
                    args=(
                        u'[MINTUR] Correcciones del Proceso de Categorización', 
                        html_content, 
                        text_content, 
                        'gccdev@cgtscorp.com', 
                        ['gccdev@cgtscorp.com'], 
                        None, 
                        None)
                    )                
                thread_correo.start()

                #return HttpResponse(status=200)
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'aprobarinspeccion':
                """
                it=NotificacionDocumentoCompuesto.objects.filter(
                    (Q(notificacion__solicitud=solicitud)
                    | Q(notificacion_backup__solicitud=solicitud))
                    & Q(documento__tipo_documento_compuesto__abreviacion='IT'))
                itr=NotificacionDocumentoCompuesto.objects.filter(
                    (Q(notificacion__solicitud=solicitud)
                    | Q(notificacion_backup__solicitud=solicitud))
                    & Q(documento__tipo_documento_compuesto__abreviacion='ITR'))
                if  solicitud.fecha_clausura and itr or not solicitud.fecha_clausura and it:
                    estatus = Estatus.objects.get(abreviacion='ITG')
                elif solicitud.fecha_clausura and not itr or not solicitud.fecha_clausura and not it:
                    estatus = Estatus.objects.get(abreviacion='VI')
                """
                estatus = Estatus.objects.get(abreviacion='VI')
                asig=Asignacion.objects.filter(
                    solicitud=solicitud,
                    funcionario__tiporol__nombre='coordinador_ct',
                    asignacion_habilitada=True
                ).order_by('-fecha_asignacion').first()
                
                coordinador=asig.funcionario

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-observacionaprobarins'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-observacionaprobarins']

                notificacion = Notificacion(
                    emisor_id=analista_ident,
                    receptor=coordinador.user,
                    solicitud=solicitud,
                    estatus_actual=estatus,
                    observacion=observacion
                    #archivo= request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.funcionario = coordinador
                solicitud.estatus = estatus
                solicitud.fecha_modificacion_estado = datetime.datetime.now()
                solicitud.save()

                #return HttpResponse(status=200)
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            """
            elif op == 'proponerreparacion':
                if len (request.POST['comentario-reparacion'])==0:
                    observacion="No se han registrado observaciones"
                else:
                    observacion=request.POST['comentario-reparacion']
                estatus = Estatus.objects.get(abreviacion='EAR')

                notificacion = Notificacion(
                    emisor_id=analista_ident,
                    receptor=coordinador.user,
                    solicitud=solicitud,
                    observacion=observacion,
                    estatus_actual=estatus
                )
                solicitud.funcionario = coordinador
            """


        except Exception, e:
            raise e


class CoordinadorCTOperacion(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CoordinadorCTOperacion, self).dispatch(*args, **kwargs)

    def get(self,request,*args,**kwargs):
        op =kwargs ['operacion']
        ident = kwargs ['id']
        coordinador_ct_ident= int(request.user.pk)
        coordinador_ct_funcionario = Funcionario.objects.filter(
            user_id=coordinador_ct_ident).first()
        
        if op == 'asignaranalista':
            analista_list = algoritmo_asignacion.asignacion_analista_inspector('analista')

            if request.GET['analista_id']:
                if request.GET['libro']=='SI':
                    id_analista = Asignacion.objects.get(
                        funcionario__tiporol__nombre='analista', 
                        solicitud_libro_id=ident, asignacion_habilitada=True)
                else:
                    id_analista = Asignacion.objects.get(
                        funcionario__tiporol__nombre='analista', 
                        solicitud_id=ident, asignacion_habilitada=True)

                for e in analista_list:
                    if e[0] == id_analista.funcionario_id:
                        analista_list.remove(e)
                        break

            jsontmp = {
                "err_msg": "",
                "success": "Pagina encontrada",
                "data": {"analistas":analista_list}
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=False),
                content_type="application/json"
            )

    def post(self,request,*args,**kwargs):
        op =kwargs ['operacion']
        ident = kwargs ['id']
        coordinador_ct_ident= int(request.user.pk)
        solicitud = Solicitud.objects.get(id= int(ident)) if op != 'asignaranalistalibro' else SolicitudLibro.objects.get(id=int(ident))
        coordinador_ct_funcionario = Funcionario.objects.get(user_id=coordinador_ct_ident)
        ultima_notificacion=Notificacion.objects.filter(
            solicitud__id=ident
            ).order_by('-fecha_emision').first()

        try:            
            if op == 'negarprorroga':

                dprint(permitir=request.POST['permitirprorroga'])

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-negarprorroga'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-negarprorroga']

                estatus = Estatus.objects.get(abreviacion= 'ER')
                solicitud.estatus=estatus
                if request.POST['permitirprorroga']=='true':
                    solicitud.permitir_prorroga=True
                else:
                    solicitud.permitir_prorroga=False
                notificacion= Notificacion(
                    emisor_id=coordinador_ct_ident,
                    receptor=solicitud.pst.user,
                    solicitud_id=ident,
                    observacion=observacion,
                    estatus_actual=estatus
                    #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.funcionario_id = None
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()
                #return HttpResponse(status=200)
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'aprobarprorroga':
                
                estatus = Estatus.objects.get(abreviacion= 'RPG')

                #TODO Cambiar Asignacion a firmas delegadas y no cableado a Viceministro
                asig=Asignacion.objects.filter(
                    solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='viceministro', 
                    asignacion_habilitada=True).order_by('-fecha_asignacion').first()

                if not asig:
                    funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion('viceministro')
                    asig = Asignacion(
                        funcionario_id=funcionario_id,
                        tipo_asignacion__abreviacion='V', 
                        solicitud_id=solicitud.id,
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                        )
                    asig.save()

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if not request.POST['diasprorroga']:
                    error="Debe indicar los días que se le otorgarán al PST para cumplir con Disposiciones de Mejora"
                    return  HttpResponse(error, content_type="application/json", status=400)
                elif int(request.POST['diasprorroga']) > 0:
                    solicitud.dias_prorroga=int(request.POST['diasprorroga'])
                else:
                    error="Los días asignados deben ser números positivos"
                    return  HttpResponse(error, content_type="application/json", status=400)

                if len (request.POST['comentario-aprobarprorroga'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-aprobarprorroga']

                if request.POST['permitirprorroga']=='true':
                    solicitud.permitir_prorroga=True
                else:
                    solicitud.permitir_prorroga=False
                notificacion= Notificacion(
                    emisor_id=coordinador_ct_ident,
                    receptor=asig.funcionario.user,
                    solicitud=solicitud,
                    observacion=observacion,
                    estatus_actual=estatus
                    #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                
                solicitud.estatus=estatus
                solicitud.funcionario = asig.funcionario
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()
                

                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_respuesta_solicitud_de_prorroga.html")
                

                try:
                    #Creando el documento
                    tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='ORSP')
                    nombre_documento = "%s_oficio_respuesta_solicitud_de_prorroga_%s_%s" % (
                        solicitud.pst.user.rif,
                        solicitud.id,
                        solicitud.fecha_modificacion_estado.year
                    )

                    path = model_list.get_file_path(
                        solicitud.pst.user.rif,
                        'oficios',
                        "",
                    )

                    locationPath = os.path.join(
                        BASE_DIR,
                        'documents',
                        'files', 
                        path
                    )

                    oficio = Documento.objects.filter(nombre=nombre_documento).first()
                    if oficio:
                        oficio.fecha_emision=datetime.datetime.now()
                        oficio.eliminado=False
                    else:
                        data = Storage(
                            nombre=nombre_documento,
                            fecha_emision=datetime.datetime.now(),
                            plantilla_documento=plantilla,
                            ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                            extension = 'pdf',
                            tipo_documento_compuesto=tipo_documento,
                        )
                        oficio = Documento.create(data)
                    oficio.save()

                    #La notificacion respectiva a uno de los inspectores
                    ndc = NotificacionDocumentoCompuesto(
                        notificacion = notificacion,
                        documento = oficio
                    )
                    ndc.save()

                    try:
                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        data = Storage(
                            nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                            oficio=oficio,
                            fecha=datetime.date.today(),
                            razon_social=solicitud.pst.razon_social,
                            direccion=direccionPST,
                            telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                            contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                            dias=("%s(%d) días" % (to_word(solicitud.dias_prorroga), solicitud.dias_prorroga)).lower()
                        )

                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficios/oficio_respuesta_solicitud_de_prorroga.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )

                        locationAttach = os.path.join(
                            locationPath,
                            nombre_documento + '.pdf'
                        )
                    except Exception, e:
                        raise e
                    
                except Exception, e:
                    raise e
                
                #return HttpResponse(status=200)
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}

                dprint(jsontmp=jsontmp)
                
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            #TODO: Borrar esta op completa 
            elif op == 'proponerincumplimiento':
                if len (request.POST['comentario-oficio'])==0:
                    observacion="No se han registrado observaciones"
                else:
                    observacion=request.POST['comentario-oficio']
                estatus = Estatus.objects.get(abreviacion='EN')
                asig=Asignacion.objects.filter(
                    solicitud=solicitud, 
                    funcionario__tiporol__nombre='director_ct', 
                    asignacion_habilitada=True
                ).order_by('-fecha_asignacion').first()
                
                if not asig:
                    funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion('director_ct')
                    asig = Asignacion(
                        funcionario_id=funcionario_id,
                        tipo_asignacion=TipoAsignacion.objects.filter(abreviacion='D').first(), 
                        solicitud=solicitud,
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                        )
                    asig.save()
                notificacion= Notificacion(
                    emisor_id=coordinador_ct_ident, 
                    receptor_id=asig.funcionario.user.id,
                    solicitud=solicitud, 
                    observacion=observacion,
                    estatus_actual=estatus
                )
                notificacion.save()
                solicitud.estatus=estatus
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.funcionario_id = None
                Solicitud.fecha_clausura=datetime.datetime.now()
                solicitud.save()  

          
                #tabulador=RespuestaTabulador.objects.filter(pst_id=solicitud.pst_id)
                #tabulador.delete()
                '''
                lic = LicenciaAsignada.objects.filter(usuario_pst=solicitud.pst.user, 
                    sucursal_id=solicitud.sucursal_id
                ).first()
                if lic:
                    dprint(lic=lic)
                    if solicitud.sucursal_id:
                        licencia = lic.numero_licencia
                        suc= solicitud.pst.denominacion_comercial
                        direccion = "%s, %s, %s, %s" %(solicitud.sucursal.urbanizacion, solicitud.sucursal.avenida_calle, solicitud.sucursal.edificio, solicitud.sucursal.oficina_apartamento)
                    else:
                        licencia = lic.numero_licencia
                        suc= "Sede Principal"
                        direccs = Registro_Direccion.objects.get(pst=solicitud.pst)
                        direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)

                #<---- Envio de Correo ----->                        
                htmly = get_template('correo/acepta_niega_categorizacion.html')
                text_plain = get_template('correo/acepta_niega_categorizacion.txt')

                context = Context({
                 'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                 'nombre_establecimiento': solicitud.pst.denominacion_comercial,
                 'direccion': direccion
                })

                html_content = htmly.render(context)
                text_content = text_plain.render(context)

                try:
                    corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
                except ParametroConfiguracion.DoesNotExist:
                    raise e
                corrs = str(corr.valor)

                thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Resultados del proceso de categorización', html_content, text_content, corrs, ['gccdev@cgtscorp.com'], None, None))                
                thread_correo.start()

                asignaciones = Asignacion.objects.filter(
                    solicitud_id=solicitud.id, asignacion_habilitada=True)
                if asignaciones:
                    for n in asignaciones:
                        n.asignacion_habilitada=False
                        n.save()
                solicitud.fecha_clausura=datetime.datetime.now()
                solicitud.funcionario=None
                '''
                
                #return HttpResponseRedirect(reverse('bandeja'))
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}

                dprint(jsontmp=jsontmp)
                
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)            
            
            elif op == 'asignaranalistapost':
                asig = Asignacion.objects.filter(solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='analista', asignacion_habilitada=True)
                

                if request.POST['analista_id'] and len(asig) == 0:
                    analista_id = request.POST['analista_id']
                    dprint(analista_id)
                    analista = Funcionario.objects.filter(
                        id=analista_id, tiporol__nombre='analista').first()
                    #estatus_id = Estatus.objects.filter(abreviacion= 'SAR').first()
                    tipoasig = TipoAsignacion.objects.filter(abreviacion='A').first()
                    asignacion = Asignacion(
                        funcionario_id=analista.id, tipo_asignacion_id=tipoasig.id, 
                        solicitud_id=solicitud.id, fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True)
                    asignacion.save()
                    """
                    notificacion= Notificacion(
                        emisor_id=coordinador_ct_ident, receptor_id=analista.user_id, 
                        estatus_actual=estatus_id,
                        solicitud_id=solicitud.id)
                    notificacion.save()
                    solicitud.estatus_id=estatus_id.id
                    solicitud.funcionario_id = analista.id
                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                    solicitud.save()
                    """
                    jsontmp = {                    
                        "err_msg": "",
                        "success": "Pagina encontrada",
                        "data":{"analista": (analista.id, "%s %s"%(analista.nombre, analista.apellido))}
                    }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json"
                    )
                else:
                    jsontmp = {
                        "err_msg": "Parametros invalidos",
                        "success": "", 
                        "data": ""
                    }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json",
                            status=400
                    )
            
            elif op == 'asignaranalistalibro':
                dprint(request.POST['analista_id'])
                asig = Asignacion.objects.filter(
                    solicitud_libro_id=solicitud.id, 
                    funcionario__tiporol__nombre='analista', 
                    asignacion_habilitada=True,
                    tipo_asignacion__abreviacion='LSR'
                )
                

                if request.POST['analista_id'] and len(asig) == 1:
                    dprint("Opcion1")
                    asig=asig.first()
                    asig.asignacion_habilitada=False
                    asig.save()

                    analista_id = request.POST['analista_id']
                    dprint(analista_id)
                    analista = Funcionario.objects.filter(
                        id=analista_id, tiporol__nombre='analista').first()
                    #estatus_id = Estatus.objects.filter(abreviacion= 'SAR').first()
                    tipoasig = TipoAsignacion.objects.filter(abreviacion='A').first()
                    asignacion = Asignacion(
                        funcionario_id=analista.id, tipo_asignacion_id=tipoasig.id, 
                        solicitud_libro_id=solicitud.id, fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True)
                    asignacion.save()

                    jsontmp = {                    
                        "err_msg": "",
                        "success": "Pagina encontrada",
                        "data":{"analista": (analista.id, "%s %s"%(analista.nombre, analista.apellido))}
                    }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json"
                    )


                elif request.POST['analista_id'] and len(asig) == 0:
                    dprint("Opcion2")
                    analista_id = request.POST['analista_id']
                    dprint(analista_id)
                    analista = Funcionario.objects.filter(
                        id=analista_id, tiporol__nombre='analista').first()
                    #estatus_id = Estatus.objects.filter(abreviacion= 'SAR').first()
                    tipoasig = TipoAsignacion.objects.filter(abreviacion='LSR').first()
                    asignacion = Asignacion(
                        funcionario_id=analista.id, 
                        tipo_asignacion=tipoasig, 
                        solicitud_libro_id=solicitud.id, 
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                    )
                    asignacion.save()
                    """
                    notificacion= Notificacion(
                        emisor_id=coordinador_ct_ident, receptor_id=analista.user_id, 
                        estatus_actual=estatus_id,
                        solicitud_id=solicitud.id)
                    notificacion.save()
                    solicitud.estatus_id=estatus_id.id
                    solicitud.funcionario_id = analista.id
                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                    solicitud.save()
                    """
                    jsontmp = {                    
                        "err_msg": "",
                        "success": "Pagina encontrada",
                        "data":{"analista": (analista.id, "%s %s"%(analista.nombre, analista.apellido))}
                    }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json"
                    )
                else:
                    jsontmp = {
                        "err_msg": "Parametros invalidos",
                        "success": "", 
                        "data": ""
                    }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json",
                            status=400
                    )
            

            elif op == 'solicitaranalisis':

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-solicitarana'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-solicitarana']

                asig=Asignacion.objects.filter(
                    solicitud=solicitud, 
                    funcionario__tiporol__nombre='analista', 
                    asignacion_habilitada=True
                    ).order_by('-fecha_asignacion').first()

                estatus = Estatus.objects.filter(abreviacion='SAR').first()
                
                notificacion= Notificacion(
                    emisor_id=coordinador_ct_ident, 
                    receptor_id=asig.funcionario.user.id, 
                    solicitud_id=solicitud.id,
                    observacion=observacion,
                    estatus_actual=estatus
                    #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.estatus_id = estatus.id
                solicitud.funcionario= asig.funcionario
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()

                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'solicitarinspeccion':

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-solicitarins'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-solicitarins']

                asig=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='coordinador_dif', asignacion_habilitada=True
                    ).order_by('-fecha_asignacion').first()
                if asig:
                    coord = asig.funcionario
                else:
                    coordinador_id = algoritmo_asignacion.algoritmo_de_asignacion('coordinador_dif')
                    coord = Funcionario.objects.filter(id= coordinador_id).first()
                    tipoasig = TipoAsignacion.objects.filter(abreviacion='C').first()
                    asignacion = Asignacion(funcionario_id=coordinador_id, tipo_asignacion_id=tipoasig.id, 
                        solicitud_id=solicitud.id, fecha_asignacion=datetime.datetime.now(), 
                        asignacion_habilitada=True)
                    asignacion.save()

                estatus = Estatus.objects.filter(abreviacion='PAI').first()
                
                notificacion= Notificacion(
                    emisor_id=coordinador_ct_ident, 
                    receptor_id=coord.user_id, 
                    solicitud_id=solicitud.id,
                    observacion=observacion,
                    estatus_actual=estatus
                    #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.estatus_id = estatus.id
                solicitud.funcionario= coord
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()

                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                #return HttpResponseRedirect(reverse('bandeja'))

            elif op == 'eliminaranalistapost':

                if request.POST['analista_id'] and request.POST['analista_eliminado']:
                    dprint(solicitud=solicitud.estatus.abreviacion)
                    # La Asignacion que tiene el analista viejo
                    asig = Asignacion.objects.filter(
                        solicitud=solicitud, 
                        funcionario__tiporol__nombre='analista', 
                        asignacion_habilitada=True,
                        funcionario_id=request.POST['analista_eliminado']
                    ).first()
                    
                    # Analista nuevo
                    analista_agregar=Funcionario.objects.get(
                        id=request.POST['analista_id'])

                    # Analista viejo
                    analista_eliminar=Funcionario.objects.get(
                        id=request.POST['analista_eliminado'])
                    """
                    solicituds = Solicitud.objects.filter((Q(estatus__abreviacion='SEAR') 
                        | Q(estatus__abreviacion='VI')
                        | Q(estatus__abreviacion='EAP')
                        | Q(estatus__abreviacion='PAA'))
                        & Q(id=solicitud.id) 
                        & Q(funcionario = coordinador_ct_funcionario) 
                        ).first()
                    """
                    estatus_comprobacion=Estatus.objects.get(abreviacion='PAA')

                    if asig and solicitud.estatus == estatus_comprobacion :
                        """
                        notificacion_emisor= Notificacion.objects.filter(
                            emisor = analista_eliminar.user,
                            solicitud = solicitud
                        )
                        notificacion_receptor = Notificacion.objects.filter(
                            receptor = analista_eliminar.user,
                            solicitud = solicitud
                        )
                        for e in notificacion_emisor_viejo:
                            notificaciones_movidas_back=  NotificacionBackup(
                                emisor=e.emisor, receptor=e.receptor, 
                                solicitud=e.solicitud, asunto=e.asunto,
                                observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                estatus_actual=e.estatus_actual
                            )
                            notificaciones_movidas_back.save()
                            notif_emisor_doc = NotificacionDocumentoCompuesto.objects.filter(
                            notificacion=e)
                            dprint(notif_emisor_doc=notif_emisor_doc)
                            for f in notif_emisor_doc:
                                f.notificacion_backup_id = notificaciones_movidas_back.id
                                f.notificacion_id = None
                                f.save()

                            e.delete()

                        for e in notificacion_receptor_viejo:
                            notificaciones_movidas_back=  NotificacionBackup(
                                emisor=e.emisor, receptor=e.receptor, 
                                solicitud=e.solicitud, asunto=e.asunto,
                                observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                estatus_actual=e.estatus_actual
                            )
                            notificaciones_movidas_back.save()
                            dprint(receptor=notificaciones_movidas_back)
                            notif_receptor_doc = NotificacionDocumentoCompuesto.objects.filter(
                            notificacion=e)
                            dprint(notif_receptor_doc=notif_receptor_doc)
                            for f in notif_receptor_doc:
                                f.notificacion_backup_id = notificaciones_movidas_back.id
                                f.notificacion_id = None
                                f.save()

                            e.delete()

                        """

                        # TODO Agregar migracion en la tabla asignacion
                        # para el campo de eliminacion perezosa
                        asig.asignacion_habilitada=False
                        asig.save()
                        asignacion_nueva= Asignacion(
                            funcionario = analista_agregar, 
                            tipo_asignacion = TipoAsignacion.objects.get(abreviacion='A'),
                            solicitud = solicitud, 
                            asignacion_habilitada=True
                        )
                        #solicitud.fecha_modificacion_estado=datetime.datetime.now()
                        asignacion_nueva.save()
                        #solicitud.save()
                        jsontmp = {                    
                            "err_msg": "",
                            "success": "Analista eliminado",
                            "data":{'analista':(analista_agregar.id, "%s %s"%(analista_agregar.nombre, analista_agregar.apellido))},
                        }
                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                        )
                dprint("AQUI NOOO!!")
                jsontmp = {
                    "err_msg": "Parametros invalidos",
                    "success": "", 
                    "data": "",
                }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json",
                )

            elif op == 'solicitarreparaciones':
                dprint(request.POST)

                dprint('***********************flag')

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if not request.POST['diasprorroga']:
                    error="Debe indicar los días que se le otorgarán al PST para cumplir con Disposiciones de Mejora"
                    return  HttpResponse(error, content_type="application/json", status=400)
                elif int(request.POST['diasprorroga']) > 0:
                    solicitud.dias_prorroga=int(request.POST['diasprorroga'])
                else:
                    error="Los días asignados deben ser números positivos"
                    return  HttpResponse(error, content_type="application/json", status=400)

                if len (request.POST['comentario-solicitarrep']) == 0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-solicitarrep']
                #TODO Cambiar Asignacion a firmas delegadas y no cableado a Viceministro
                asig=Asignacion.objects.filter(
                    solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='viceministro', 
                    asignacion_habilitada=True
                ).order_by('-fecha_asignacion').first()

                if not asig:
                    funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion('viceministro')
                    asig = Asignacion(
                        funcionario_id=funcionario_id,
                        tipo_asignacion__abreviacion='V', 
                        solicitud_id=solicitud.id,
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                    )
                    asig.save()

                estatus = Estatus.objects.get(abreviacion= 'DMG')
                
                notificacion= Notificacion(
                    emisor_id=coordinador_ct_ident,
                    receptor=asig.funcionario.user,
                    solicitud=solicitud,
                    estatus_actual=estatus,
                    observacion=observacion
                )
                notificacion.save()
                
                solicitud.estatus=estatus
                solicitud.funcionario = asig.funcionario
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()

                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()

                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_de_disposiciones_de_mejora.html")
                tablas=dt_tablas_it(solicitud)
                try:
                    #Creando el documento
                    tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='ODM')
                    nombre_documento = "%s_oficio_de_disposiciones_de_mejora_%s_%s" % (
                        solicitud.pst.user.rif,
                        solicitud.id,
                        datetime.datetime.now().year
                    )

                    path = model_list.get_file_path(
                        solicitud.pst.user.rif,
                        'oficios',
                        "",
                    )

                    locationPath = os.path.join(
                        BASE_DIR,
                        'documents',
                        'files', 
                        path
                    )

                    oficio = Documento.objects.filter(nombre=nombre_documento).first()
                    if oficio:
                        oficio.fecha_emision=datetime.datetime.now()
                        oficio.eliminado=False
                    else:
                        data = Storage(
                            nombre=nombre_documento,
                            fecha_emision=datetime.datetime.now(),
                            plantilla_documento=plantilla,
                            ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                            extension = 'pdf',
                            tipo_documento_compuesto=tipo_documento,
                        )
                        oficio = Documento.create(data)
                    oficio.save()

                    #La notificacion respectiva a uno de los inspectores
                    ndc = NotificacionDocumentoCompuesto(
                        notificacion = notificacion,
                        documento = oficio
                    )
                    ndc.save()
                    
                    try:
                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO

                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)

                        licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
                        
                        
                        data = Storage(
                            nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                            oficio=oficio,
                            fecha=datetime.date.today(),
                            razon_social=solicitud.pst.razon_social,
                            direccion=direccionPST,
                            telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                            contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                            fecha_inspeccion=Notificacion.objects.filter(
                                estatus_actual__abreviacion='RI',
                                solicitud=solicitud).order_by('-fecha_emision').first().fecha_emision,
                            rtn=solicitud.pst.rtn,
                            dias= ("%s(%d) días" % (to_word(solicitud.dias_prorroga), solicitud.dias_prorroga)).lower(),
                            licencia=licencia.numero_licencia,
                            resolucion=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='R', 
                                documento_asociado__abreviacion='IT', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            gaceta=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='GO', 
                                documento_asociado__abreviacion='IT', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            tipo_pst=licencia.tipo_licenciaid,
                            cuadro_incumplimiento=tablas[1],
                            cuadro_incumplimiento_mya=tablas[2],
                            cuadro_porcentajes=tablas[0],
                            categorias=Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor')
                        )

                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template=plantilla.formato,
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )

                        locationAttach = os.path.join(
                            locationPath,
                            nombre_documento + '.pdf'
                        )
                    except Exception, error:
                        return  HttpResponse(error, content_type="application/json", status=400)
                    
                except Exception, error:
                    return  HttpResponse(error, content_type="application/json", status=400)
                
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'generarinformetecnico':
                licencia=otp_solicitud(solicitud=solicitud)
                dprint("##################################333SI!!")
                """asig=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='director_ct', asignacion_habilitada=True
                    ).order_by('-fecha_asignacion').first()
                estatus=Estatus.objects.get(abreviacion='EA')
                if asig:
                    dprint("Esta asignacion ya se encuentra")
                    director=asig.funcionario
                else:
                    dprint("Se genera una asignacion nueva")
                    director_id = algoritmo_asignacion.algoritmo_de_asignacion('director_ct')
                    dprint(director=director_id)
                    director = Funcionario.objects.get(id=director_id)
                    dprint(solicitud=solicitud)
                    asignac = Asignacion(funcionario_id=director.id, 
                        tipo_asignacion_id= TipoAsignacion.objects.get(abreviacion='D').id, 
                        solicitud=solicitud, fecha_asignacion=datetime.datetime.now(), 
                        asignacion_habilitada=True
                    )
                    asignac.save()
                    dprint(asignacion_nueva1=director_id)
                """            
                estatus = Estatus.objects.get(abreviacion='ITG')

                notificacion = Notificacion(
                    emisor_id=request.user.id,
                    receptor_id=request.user.id,
                    solicitud=solicitud,
                    estatus_actual=estatus
                )
                notificacion.save()
                

                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/informe_tecnico.html")
                tablas=dt_tablas_it(solicitud)
                
                try:
                    #Creando el documento
                    if solicitud.fecha_clausura:
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='ITR')
                        nombre_documento = "%s_informe_tecnico_reconsideracion_%s_%s" % (
                            solicitud.pst.user.rif,
                            solicitud.id,
                            solicitud.funcionario.id                        
                        )
                    else:
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='IT')
                        nombre_documento = "%s_informe_tecnico_%s_%s" % (
                            solicitud.pst.user.rif,
                            solicitud.id,
                            solicitud.funcionario.id                        
                        )

                    path = model_list.get_file_path(
                        solicitud.pst.user.rif,
                        'informe_tecnico',
                        "",
                    )

                    locationPath = os.path.join(
                        BASE_DIR,
                        'documents',
                        'files', 
                        path
                    )
                                            
                    try:
                        informe = Documento.objects.get(
                            nombre=nombre_documento
                        )
                        informe.fecha_aprobacion=datetime.datetime.now()
                        informe.eliminado=False
                    except:
                        data = Storage(
                            nombre=nombre_documento,
                            fecha_aprobacion=datetime.datetime.now(),
                            plantilla_documento=plantilla,
                            ruta_documento = '/documents/' + path +'/'+ nombre_documento + '.pdf',
                            extension = 'pdf',
                            tipo_documento_compuesto=tipo_documento,
                        )

                        informe = Documento.create(data)

                    informe.save()

                    #La notificacion 
                    ndi = NotificacionDocumentoCompuesto(
                        notificacion = notificacion,
                        documento = informe
                    )
                    ndi.save()

                    asig_inspectores=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='inspector', asignacion_habilitada=True
                    ).order_by('-fecha_asignacion')
                    #PARAMETROS PARA EL INFORME
                    data = Storage(
                        fecha=datetime.date.today(),
                        razon_social=solicitud.pst.razon_social,
                        tipo_pst=licencia.nombre,
                        inspector1=asig_inspectores[0].funcionario.nombre + ' ' + asig_inspectores[0].funcionario.apellido,
                        inspector2='y ' + asig_inspectores[1].funcionario.nombre + ' ' + asig_inspectores[1].funcionario.apellido if len(asig_inspectores)>1 else "",
                        resolucion=EspecificacionLegal.objects.filter(
                            tipo_especificacion__abreviacion='R', 
                            documento_asociado__abreviacion='IT', 
                            tipo_pst=licencia
                        ).first(),
                        gaceta=EspecificacionLegal.objects.filter(
                            tipo_especificacion__abreviacion='GO', 
                            documento_asociado__abreviacion='IT', 
                            tipo_pst=licencia
                        ).first(),
                        #articulo=EspecificacionLegal.objects.filter(
                        #    tipo_especificacion__abreviacion='A', 
                        #    documento_asociado__abreviacion='IT', 
                        #    tipo_pst=licencia
                        #),
                        funcionario=solicitud.funcionario,
                        cuadro_incumplimiento=tablas[1],
                        cuadro_incumplimiento_mya=tablas[2],
                        cuadro_porcentajes=tablas[0],
                        categorias=Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor')
                    )

                    generar_pdf.generar_pdf(
                        context=data,
                        ruta_template=plantilla.formato,
                        ruta_documento=locationPath,
                        nombre_documento=nombre_documento
                    )
                        
                except Exception, e:
                    return  HttpResponse(e, content_type="application/json", status=400)
                    #return e
                solicitud.estatus=estatus
                #solicitud.funcionario= director
                #solicitud.funcionario_extra_id=None
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()

                return  HttpResponse(status=200)

        except Exception, error:
            return  HttpResponse(error, content_type="application/json", status=400)
            """
            jsontmp = {
                "err_msg": "Problemas encontrados "+str(e),
                "success":'', 
                "data": "",
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=False),
                content_type="application/json",
                estatus=500
            )
            """


class CoordinadorDIFOperacion(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(CoordinadorDIFOperacion, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        op =kwargs ['operacion']
        ident = kwargs ['id']
        coordinador_dif_ident= int(request.user.pk)
        solicitud = Solicitud.objects.filter(id= int(ident)).first()
        coordinador_dif_funcionario = Funcionario.objects.filter(
            user_id=coordinador_dif_ident).first()

        if op == 'asignarinspector':
            try: 
                inspector_list=algoritmo_asignacion.asignacion_analista_inspector('inspector')
                dprint(inspector_list)
                cantidad_inspectores = Asignacion.objects.filter(
                    funcionario__tiporol__nombre='inspector', 
                    solicitud_id=ident, asignacion_habilitada=True
                ).values_list('funcionario')

                if len(cantidad_inspectores) == 1:
                    inspector_asignado = cantidad_inspectores[0]

                    for e in inspector_list:
                        if e[0] == inspector_asignado[0]:
                            inspector_list.remove(e)
                cantidad = len(cantidad_inspectores)
                jsontmp = {
                    "err_msg": "",
                    "success": "Pagina encontrada",
                    "data": {"inspectores":inspector_list},
                    "cantidad": cantidad
                }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json"
                )
            except Exception, e:
                raise e

        elif op == 'vercredencial':
            inspector = Asignacion.objects.filter(
                solicitud_id=ident, 
                funcionario__tiporol__nombre='inspector', asignacion_habilitada=True
                ).last().funcionario.user
            """
            notificaciones = Notificacion.objects.filter(
                emisor_id = coordinador_dif_ident,
                receptor_id = inspector.id,
                solicitud_id = ident
                )
            dprint(notificacion.id)
            """

            try:
                tipo = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                credencial = NotificacionDocumentoCompuesto.objects.filter(
                    documento__tipo_documento_compuesto=tipo,
                    notificacion__solicitud_id=ident
                    ).last().documento
                dprint(credencial_ruta_documento=credencial.ruta_documento)
                jsontmp = {
                    "err_msg": "",
                    "success": "Pagina encontrada",
                    "ruta_documento": str(credencial.ruta_documento)
                }

                return  HttpResponse(json.dumps(
                        jsontmp,sort_keys=True),
                        content_type="application/json",
                        status=200
                    )
            except Exception, e:
                jsontmp = {
                    "err_msg": "Documento inexistente",
                    "success": ""
                }

                return  HttpResponse(json.dumps(
                        jsontmp,sort_keys=True),
                        content_type="application/json",
                        status=200
                   )
            

    def post(self,request,*args,**kwargs):
        op =kwargs ['operacion']
        ident = kwargs ['id']
        coordinador_dif_ident= int(request.user.pk)
        solicitud = Solicitud.objects.filter(id= int(ident)).first()
        coordinador_dif_funcionario = Funcionario.objects.get(user_id=coordinador_dif_ident)
        ultima_notificacion=Notificacion.objects.filter(
            solicitud=solicitud
            ).order_by('-fecha_emision').first()

        try:
            if op == 'asignarinspectorpost':
                ins = {}
                t = {}
                asignacion = None
                if request.POST.has_key('inspectores'):
                    ins = request.POST['inspectores']
                    json_acceptable_string = ins.replace("'", "\"")
                    ins = json.loads(json_acceptable_string)
                
                    if ins:

                        tipoasig = TipoAsignacion.objects.filter(abreviacion='I').first()

                        estado = Solicitud.objects.filter(id=solicitud.id, 
                            estatus__abreviacion='RI'
                        ).first()

                        asigs = Asignacion.objects.filter(
                            funcionario__tiporol__nombre='inspector',
                            solicitud=solicitud, asignacion_habilitada=True
                            )

                        if estado and len(asigs) == 1:
                            inspector_queda = Funcionario.objects.get(
                                id=asigs.first().funcionario_id)
                            notificaciones_emisor= Notificacion.objects.filter(
                                solicitud= solicitud.id, emisor= inspector_queda.user)
                            notificaciones_receptor= Notificacion.objects.filter(
                                solicitud= solicitud.id, receptor= inspector_queda.user)
                            if notificaciones_emisor:
                                for k,v in ins.items():
                                    f = Funcionario.objects.get(id=int(v))
                                    for e in notificaciones_emisor:
                                        notificaciones_movidas= Notificacion(
                                            emisor = f.user,
                                            receptor = e.receptor,
                                            solicitud =e.solicitud,
                                            asunto = e.asunto,
                                            observacion = e.observacion,
                                            fecha_emision = e.fecha_emision,
                                            estatus_actual= e.estatus_actual
                                        )
                                        notificaciones_movidas.save()
                                       
                            if notificaciones_receptor:
                                for k,v in ins.items():
                                    f = Funcionario.objects.get(id=int(v))
                                    for e in notificaciones_receptor:
                                        notificaciones_movidas = Notificacion(
                                            emisor =e.emisor,
                                            receptor = f.user,
                                            solicitud =e.solicitud,
                                            asunto = e.asunto,
                                            observacion = e.observacion,
                                            fecha_emision=e.fecha_emision,
                                            estatus_actual = e.estatus_actual
                                        )
                                        notificaciones_movidas.save()

                            #A partir de aqui se crea la credencial nueva con un solo inspector
                            plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/credencial.html")
                            try:
                                notificacion= Notificacion(
                                    emisor_id=coordinador_dif_ident, receptor_id=f.user_id,
                                    solicitud_id=solicitud.id, 
                                    estatus_actual=solicitud.estatus
                                )
                                notificacion1= Notificacion(
                                    emisor_id=coordinador_dif_ident, receptor_id=inspector_queda.user_id,
                                    solicitud_id=solicitud.id,  
                                    estatus_actual=solicitud.estatus
                                )
                                notificacion.save()
                                notificacion1.save()
                                #Creando el documento
                                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                                nombre_documento = "%s_credencial_%s_%s_%s" % (
                                    coordinador_dif_funcionario.user.rif,
                                    solicitud.id,
                                    f.id,
                                    inspector_queda.id
                                )
                                path = model_list.get_file_path(coordinador_dif_funcionario.user.rif,"",'credenciales')
                                locationPath ='documents/files/'+ path
                                credencial = Documento.objects.filter(nombre=nombre_documento).first()
                               
                                if credencial:
                                    credencial.fecha_aprobacion=datetime.datetime.now()
                                    credencial.eliminado=False
                                    credencial.save()
                                    #La notificacion respectiva al inspector
                                    ndc = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion,
                                        documento = credencial
                                    )
                                    ndc.save()
                                    ndc1 = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion1,
                                        documento = credencial
                                    )
                                    ndc1.save()
                                else:                                        
                                    data = Storage(
                                        nombre=nombre_documento,
                                        fecha_aprobacion=datetime.datetime.now(),
                                        plantilla_documento=plantilla,
                                        ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                        extension = 'pdf',
                                        tipo_documento_compuesto=tipo_documento,
                                    )

                                    credencial = Documento.create(data)
                                    credencial.save()
                                    #Las notificaciones respectivas a los inspectores
                                    ndc = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion,
                                        documento = credencial
                                    )
                                    ndc.save()
                                    ndc1 = NotificacionDocumentoCompuesto(
                                        notificacion = notificacion1,
                                        documento = credencial
                                    )
                                    ndc1.save()
                                try:
                                    #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                    direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                    direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                        +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                        + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                        +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                        +str(direc.codigo_postal)
                                    data = Storage(
                                        nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                                        oficio=oficio,
                                        fecha=datetime.date.today(),
                                        razon_social=solicitud.pst.razon_social,
                                        direccion=direccionPST,
                                        telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                                        inspector1=f,
                                        inspector2=inspector_queda
                                    )
                                    generar_pdf.generar_pdf(
                                        context=data,
                                        ruta_template=plantilla,
                                        ruta_documento=locationPath,
                                        nombre_documento=nombre_documento
                                    )
                                    
                                except Exception, e:
                                    raise e

                            except Exception, e:
                                dprint("Algo paso creando el documento")
                                raise e
                        for k,v in ins.items():
                            f = Funcionario.objects.get(id=int(v))
                            asignacion = Asignacion(
                                funcionario = f,
                                tipo_asignacion = tipoasig,
                                solicitud = solicitud,
                                fecha_asignacion = datetime.datetime.now(),
                                asignacion_habilitada=True
                            )
                            asignacion.save()
                            dprint(asigs)                           

                            t.update(
                                {
                                    f.pk: "%s %s" % (
                                        f.nombre,
                                        f.apellido
                                    )
                                }
                            )
                        cantidad = Asignacion.objects.filter(solicitud=solicitud,
                            funcionario__tiporol__nombre= 'inspector')                
                        jsontmp = {                    
                            "err_msg": "",
                            "success": "Inspectores agregados",
                            "data":{
                                "inspectores": t,
                                "cantidad": len(cantidad),
                            }
                        }
                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"                    
                        )
                jsontmp = {
                    "err_msg": "Registro de inspectores no encontrado",
                    "success": "",
                    "data": ""
                }
                return HttpResponse(
                    json.dumps(
                        jsontmp, sort_keys=False),
                        content_type="application/json",
                )

            elif op == 'generarcredenciales':

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len(request.POST['comentario-otorgarcred'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-otorgarcred']
                
                #TODO Cambiar Asignacion a firmas delegadas y no cableado a Viceministro
                asig=Asignacion.objects.filter(
                    solicitud_id=solicitud.id, 
                    funcionario__tiporol__nombre='viceministro', 
                    asignacion_habilitada=True).order_by('-fecha_asignacion').first()

                if not asig:
                    funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion('viceministro')
                    asig = Asignacion(
                        funcionario_id=funcionario_id,
                        tipo_asignacion=TipoAsignacion.objects.get(abreviacion='V'), 
                        solicitud=solicitud,
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                    )
                    asig.save()
                
                estatus = Estatus.objects.get(abreviacion= 'CG')
                notificacion= Notificacion(
                    emisor_id=coordinador_dif_ident, 
                    receptor=asig.funcionario.user, 
                    solicitud_id=solicitud.id, 
                    estatus_actual=estatus,
                    observacion=observacion,
                    #archivo=request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()

                solicitud.estatus_id=estatus.id
                solicitud.funcionario_id = asig.funcionario.id
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()

                inspect= Asignacion.objects.filter(
                    solicitud=solicitud, 
                    asignacion_habilitada=True, 
                    funcionario__tiporol__nombre='inspector'
                ).values_list('funcionario')
                ins = [e[0] for e in inspect]
                inspectores= Funcionario.objects.filter(id__in=ins)

                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/credencial.html")
                try:
                    #Creando el documento
                    tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                    nombre_documento = "%s_credencial_%s_%s_%s" % (
                        coordinador_dif_funcionario.user.rif,
                        solicitud.id,
                        inspectores[0].id,
                        inspectores[1].id
                    )

                    path = model_list.get_file_path(
                        coordinador_dif_funcionario.user.rif,
                        'credenciales',
                        "",
                    )

                    locationPath = os.path.join(
                        BASE_DIR,
                        'documents',
                        'files', 
                        path
                    )

                    credencial = Documento.objects.filter(
                        nombre=nombre_documento).first()

                    if credencial:
                        credencial.fecha_aprobacion=datetime.datetime.now()
                        credencial.eliminado=False
                    else:
                        data = Storage(
                            nombre=nombre_documento,
                            fecha_aprobacion=datetime.datetime.now(),
                            plantilla_documento=plantilla,
                            ruta_documento = '/documents/' + path +'/'+ nombre_documento + '.pdf',
                            extension = 'pdf',
                            tipo_documento_compuesto=tipo_documento,
                        )
                        credencial = Documento.create(data)
                        
                    credencial.save()
                    dprint("credencial creada")
                    #La notificacion respectiva al viceministro
                    ndc = NotificacionDocumentoCompuesto(
                        notificacion = notificacion,
                        documento = credencial
                    )
                    ndc.save()

                    try:
                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        data = Storage(
                            nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                            oficio=credencial,
                            fecha=datetime.date.today(),
                            razon_social=solicitud.pst.razon_social,
                            direccion=direccionPST,
                            telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                            inspector1=inspectores[0],
                            inspector2=inspectores[1]
                        )
                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template=plantilla.formato,
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                    except Exception, e:
                        raise e                    
                except Exception, e:
                    raise e

                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'eliminarinspector':
                
                print "FLAG---------------------------------1"

                if request.POST['inspector_id']:
                    print "FLAG---------------------------------2"
                    asig = Asignacion.objects.filter(
                        solicitud_id=solicitud.id, 
                        funcionario__tiporol__nombre='inspector', 
                        funcionario_id=request.POST['inspector_id'], 
                        asignacion_habilitada=True
                    ).first()

                    inspector=Funcionario.objects.filter(id=request.POST['inspector_id']).first()

                    solicituds = Solicitud.objects.filter(Q(id=solicitud.id) 
                        & Q(funcionario_id=coordinador_dif_funcionario.id) 
                        & (Q(estatus__abreviacion='RI') | Q(estatus__abreviacion='PAI'))
                    ).first()
                    
                    estado_actual = solicitud.estatus.abreviacion

                    if asig and solicituds:
                        """
                        asig.asignacion_habilitada=False
                        asig.save()
                        jsontmp = {                    
                            "err_msg": "",
                            "success": "Eliminacion de inspector exitosa"
                        }

                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                        )
                        """
                        estado = Solicitud.objects.filter(
                            id=solicitud.id, estatus__abreviacion='RI').first()

                        print "FLAG---------------------------------", estado

                        if estado:
                            #ESTE CONDICIONAL SOLO DEBE ESTAR EN CASO DE QUE ESTATUS SEA RI
                            if request.POST['inspector_nuevo']:
                                cantidad_asignaciones = Asignacion.objects.filter(
                                    solicitud_id=solicitud.id, 
                                    funcionario__tiporol__nombre='inspector', 
                                    asignacion_habilitada=True)
                                #Entra aqui cuando se elimina el segundo inspector en RI
                                inspector_nuevo = Funcionario.objects.get(
                                        id=request.POST['inspector_nuevo'])
                                if len(cantidad_asignaciones) > 1:
                                    asig.asignacion_habilitada = False
                                    asig.save()
                                else:
                                    inspector_nuevo = Funcionario.objects.get(
                                        id=request.POST['inspector_nuevo'])
                                    if inspector_nuevo:
                                        notificaciones_emisor_viejo= Notificacion.objects.filter(
                                            emisor = inspector.user,
                                            solicitud = solicituds
                                        )
                                        
                                        notificaciones_receptor_viejo = Notificacion.objects.filter(
                                            receptor = inspector.user,
                                            solicitud = solicituds
                                        )

                                        for e in notificaciones_emisor_viejo:
                                            notificaciones_movidas_back=  NotificacionBackup(
                                                emisor=e.emisor, receptor=e.receptor, 
                                                solicitud=e.solicitud, asunto=e.asunto,
                                                observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                                estatus_actual=e.estatus_actual
                                            )
                                            notificaciones_movidas_back.save()
                                            notif_emisor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                            notificacion=e)
                                            dprint(notif_emisor_doc=notif_emisor_doc)
                                            for f in notif_emisor_doc:
                                                f.notificacion_backup_id = notificaciones_movidas_back.id
                                                f.notificacion_id = None
                                                f.save()

                                            e.delete()

                                        for e in notificaciones_receptor_viejo:
                                            notificaciones_movidas_back=  NotificacionBackup(
                                                emisor=e.emisor, receptor=e.receptor, 
                                                solicitud=e.solicitud, asunto=e.asunto,
                                                observacion=e.observacion, fecha_emision=e.fecha_emision, 
                                                estatus_actual=e.estatus_actual
                                            )
                                            notificaciones_movidas_back.save()
                                            dprint(receptor=notificaciones_movidas_back)
                                            notif_receptor_doc = NotificacionDocumentoCompuesto.objects.filter(
                                            notificacion=e)
                                            dprint(notif_receptor_doc=notif_receptor_doc)
                                            for f in notif_receptor_doc:
                                                f.notificacion_backup_id = notificaciones_movidas_back.id
                                                f.notificacion_id = None
                                                f.save()

                                            e.delete()

                                        asig.asignacion_habilitada=False
                                        asig.save()

                                        asignacion_nueva= Asignacion(
                                            funcionario = inspector_nuevo, 
                                            tipo_asignacion = TipoAsignacion.objects.get(abreviacion='I'),
                                            solicitud = solicituds, asignacion_habilitada=True
                                        )
                                        solicitud.fecha_modificacion_estado=datetime.datetime.now()
                                        asignacion_nueva.save()
                                        solicitud.save()

                                        quedan = Asignacion.objects.filter(solicitud_id=solicitud.id, 
                                            funcionario__tiporol__nombre='inspector', 
                                            asignacion_habilitada=True).values_list('funcionario')
                                        quedan1 = [e[0] for e in quedan]
                                        #A partir de aqui se crea la credencial nueva con un solo inspector
                                        plantilla = PlantillaDocumento.objects.get(formato="documentos/credencial.html")
                                        try:
                                            notificacion= Notificacion(
                                                emisor_id=coordinador_dif_ident, receptor_id=inspector_nuevo.user_id, 
                                                solicitud_id=solicitud.id, estatus_actual=solicitud.estatus
                                            )
                                            notificacion.save()
                                            #Creando el documento
                                            tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                                            nombre_documento = "%s_credencial_%s_%s" % (
                                                coordinador_dif_funcionario.user.rif,
                                                solicitud.id,
                                                inspector_nuevo.id
                                            )
                                            path = model_list.get_file_path(coordinador_dif_funcionario.user.rif,"",'credenciales')
                                            locationPath ='documents/files/'+ path
                                            credencial = Documento.objects.filter(nombre=nombre_documento).first()
                                            
                                            if credencial:
                                                credencial.fecha_aprobacion=datetime.datetime.now()
                                                credencial.eliminado=False
                                                credencial.save()
                                                #La notificacion respectiva al inspector
                                                ndc = NotificacionDocumentoCompuesto(
                                                    notificacion = notificacion,
                                                    documento = credencial
                                                )
                                                ndc.save()
                                            else:                                        
                                                data = Storage(
                                                    nombre=nombre_documento,
                                                    fecha_aprobacion=datetime.datetime.now(),
                                                    plantilla_documento=plantilla,
                                                    ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                                    extension = 'pdf',
                                                    tipo_documento_compuesto=tipo_documento,
                                                )

                                                credencial = Documento.create(data)
                                                credencial.save()
                                                #La notificacion respectiva al inspector
                                                ndc = NotificacionDocumentoCompuesto(
                                                    notificacion = notificacion,
                                                    documento = credencial
                                                )
                                                ndc.save()
                                            try:
                                                #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                                    +str(direc.codigo_postal)
                                                data = Storage(
                                                    pagesize='A4',
                                                    nombre_establecimiento=solicitud.pst.denominacion_comercial,
                                                    direccion=direccionPST,
                                                    nombre_inspector1=inspector_nuevo.nombre\
                                                        + " "+inspector_nuevo.apellido,
                                                    cedula_inspector1=inspector_nuevo.cedula,
                                                    nombre_inspector2="",
                                                    cedula_inspector2="",
                                                    nombre_coordinador_dif=coordinador_dif_funcionario.nombre\
                                                        +" "+coordinador_dif_funcionario.apellido,
                                                )

                                                generar_pdf.generar_pdf(
                                                    context=data,
                                                    ruta_template='documentos/credencial.html',
                                                    ruta_documento=locationPath,
                                                    nombre_documento=nombre_documento
                                                )

                                            except Exception, e:
                                                raise e

                                        except Exception, e:
                                            dprint("Algo paso creando el documento")
                                            raise e
                                        jsontmp = {                    
                                            "err_msg": "",
                                            "success": "Eliminacion de inspector exitosa",
                                            "data": {
                                                "inspector":quedan1,
                                                "inspector_nuevo":(inspector_nuevo.id, 
                                                    "%s %s"%(inspector_nuevo.nombre, inspector_nuevo.apellido)),
                                                "estado": estado_actual,
                                            },
                                        }
                                        return HttpResponse(
                                            json.dumps(jsontmp, sort_keys=False),
                                            content_type="application/json"
                                        )
                            else:
                                #Entra aqui si solo se elimina un inspector
                                plantilla = PlantillaDocumento.objects.get(formato="documentos/credencial.html")
                                try:
                                    inspect= Asignacion.objects.filter(solicitud_id=ident, asignacion_habilitada=True, 
                                        funcionario__tiporol__nombre='inspector').values_list('funcionario')
                                    #Se obtienen los 2 inspectores y se utiliza el que no este
                                    ins = [e[0] for e in inspect]
                                    inspectores= Funcionario.objects.filter(id__in=ins)
                                    ins = inspectores[1] if inspector.id == inspectores[0].id else inspectores[0]

                                    notificacion= Notificacion(
                                        emisor_id=coordinador_dif_ident, receptor_id=ins.user_id, 
                                        solicitud_id=solicitud.id, estatus_actual=solicitud.estatus
                                    )
                                    notificacion.save()
                                    #Creando el documento
                                    tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                                    nombre_documento = "%s_credencial_%s_%s" % (
                                        coordinador_dif_funcionario.user.rif,
                                        solicitud.id,
                                        ins.id
                                    )
                                    path = model_list.get_file_path(coordinador_dif_funcionario.user.rif,"",'credenciales')
                                    locationPath ='documents/files/'+ path
                                    credencial = Documento.objects.filter(nombre=nombre_documento).first()
                                    
                                    if credencial:
                                        credencial.fecha_aprobacion=datetime.datetime.now()
                                        credencial.eliminado=False
                                        credencial.save()
                                        #La notificacion respectiva al inspector
                                        ndc = NotificacionDocumentoCompuesto(
                                            notificacion = notificacion,
                                            documento = credencial
                                        )
                                        ndc.save()
                                    else:                                        
                                        data = Storage(
                                            nombre=nombre_documento,
                                            fecha_aprobacion=datetime.datetime.now(),
                                            plantilla_documento=plantilla,
                                            ruta_documento = '/documents/' + path + nombre_documento + '.pdf',
                                            extension = 'pdf',
                                            tipo_documento_compuesto=tipo_documento,
                                        )

                                        credencial = Documento.create(data)
                                        credencial.save()
                                        #La notificacion respectiva al inspector
                                        ndc = NotificacionDocumentoCompuesto(
                                            notificacion = notificacion,
                                            documento = credencial
                                        )
                                        ndc.save()
                                    try:
                                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                            +str(direc.codigo_postal)
                                        data = Storage(
                                            pagesize='A4',
                                            nombre_establecimiento=solicitud.pst.denominacion_comercial,
                                            direccion=direccionPST,
                                            nombre_inspector1=ins.nombre\
                                                + " "+ins.apellido,
                                            cedula_inspector1=ins.cedula,
                                            nombre_inspector2="",
                                            cedula_inspector2="",
                                            nombre_coordinador_dif=coordinador_dif_funcionario.nombre\
                                                +" "+coordinador_dif_funcionario.apellido,
                                        )
                                        generar_pdf.generar_pdf(
                                            context=data,
                                            ruta_template='documentos/credencial.html',
                                            ruta_documento=locationPath,
                                            nombre_documento=nombre_documento
                                        )

                                    except Exception, e:
                                        raise e

                                except Exception, e:
                                    dprint("Algo paso creando el documento")
                                    raise e
                                asig.asignacion_habilitada = False
                                asig.save()
                                notificaciones= Notificacion.objects.filter(Q(solicitud_id=solicitud.id) 
                                    & (Q(emisor= inspector.user) | Q(receptor=inspector.user)))
                                notificaciones.delete()

                        else:
                            asig.asignacion_habilitada = False
                            asig.save()
                            dprint(asig)
                            notificaciones= Notificacion.objects.filter(Q(solicitud_id=solicitud.id) 
                                & (Q(emisor= inspector.user) | Q(receptor=inspector.user)))
                            dprint(notificaciones=notificaciones)
                            for e in notificaciones:
                                print "===========================1"
                                notif_backup = NotificacionBackup(
                                    emisor = e.emisor,
                                    receptor = e.receptor,
                                    solicitud = e.solicitud,
                                    asunto = e.asunto,
                                    observacion = e.observacion,
                                    fecha_emision = e.fecha_emision,
                                    estatus_actual = e.estatus_actual
                                )

                                print "===========================2"
                                notif_backup.save()
                                print "===========================3"

                            notificaciones.delete()

                        quedan = Asignacion.objects.filter(solicitud_id=solicitud.id, 
                            funcionario__tiporol__nombre='inspector', asignacion_habilitada=True).values_list('funcionario')
                        dprint(quedan=quedan)
                        quedan1 = [e[0] for e in quedan]
                        dprint(quedan1)
                        jsontmp = {                    
                            "err_msg": "",
                            "success": "Eliminacion de inspector exitosa",
                            "data":{
                                "inspector": quedan1,
                                "estado": estado_actual,
                            },
                        }

                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=False),
                            content_type="application/json"
                        )
                        
                jsontmp = {
                    "err_msg": "Parametros invalidos",
                    "success": "", 
                    "data": "",
                }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                        content_type="application/json",
                )

            elif op == 'aprobarinspeccion':
                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-observacionaprobarins'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-observacionaprobarins']

                asig=Asignacion.objects.filter(solicitud_id=solicitud.id, asignacion_habilitada=True,
                 funcionario__tiporol__nombre='analista').order_by('-fecha_asignacion').first()
                analista=asig.funcionario
                estatus=Estatus.objects.get(abreviacion='SAI')
                notificacion = Notificacion(
                    emisor_id=coordinador_dif_ident,
                    receptor_id=analista.user_id,
                    solicitud=solicitud,
                    estatus_actual=estatus,
                    observacion=observacion,
                    #archivo= request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.estatus_id=estatus.id
                solicitud.funcionario_id= analista.id
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'cancelarinspeccion':

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-observacioncan'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-observacioncan']
                asig=Asignacion.objects.filter(solicitud_id=solicitud.id, asignacion_habilitada=True,
                 funcionario__tiporol__nombre='coordinador_ct').order_by('-fecha_asignacion').first()
                coordinador_ct=asig.funcionario
                estatus=Estatus.objects.get(abreviacion='SEAR')
                notificacion = Notificacion(
                    emisor_id=coordinador_dif_ident,
                    receptor_id=coordinador_ct.user_id,
                    solicitud=solicitud,
                    estatus_actual=estatus,
                    observacion=observacion,
                    #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                )
                asig_inspectores=Asignacion.objects.filter(solicitud_id=solicitud.id, asignacion_habilitada=True,
                 funcionario__tiporol__nombre='inspector').order_by('-fecha_asignacion')
                for a in asig_inspectores:
                    a.asignacion_habilitada=False
                    a.save()
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        solicitud.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()
                solicitud.estatus_id=estatus.id
                solicitud.funcionario_id= coordinador_ct.id
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()
                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                #return HttpResponse(status=200)

            elif op == 'aprobarformulario':
                asig=Asignacion.objects.filter(solicitud_id=solicitud.id, asignacion_habilitada=True,
                 funcionario__tiporol__nombre='coordinador_ct').order_by('-fecha_asignacion').first()
                coordinador_ct=asig.funcionario
                estatus=Estatus.objects.get(abreviacion='RS')
                notificacion = Notificacion(
                    emisor_id=coordinador_dif_ident,
                    receptor_id=coordinador_ct.user_id,
                    solicitud=solicitud,
                    estatus_actual=estatus
                )
                notificacion.save()
                solicitud.estatus_id=estatus.id
                solicitud.funcionario_id= coordinador_ct.id
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()
                return HttpResponse(status=200)

        except Exception, error:
            return  HttpResponse(error, content_type="application/json", status=400)
            # raise e


class SolicitarProrroga(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(SolicitarProrroga, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:

            solicitud_id = request.POST['solicitud']
            pst_id= int(request.user.pk)
            solicitud = Solicitud.objects.get(id= int(solicitud_id))
            estatus=Estatus.objects.get(abreviacion='EAP')
            asig=Asignacion.objects.filter(solicitud_id=solicitud.id, asignacion_habilitada=True,
                funcionario__tiporol__nombre='coordinador_ct').order_by('-fecha_asignacion').first()
            coordinador_ct=asig.funcionario
            notificacion = Notificacion(
                emisor_id=pst_id,
                receptor_id=coordinador_ct.user_id,
                solicitud=solicitud,
                estatus_actual=estatus
            )
            notificacion.save()
            solicitud.estatus_id=estatus.id
            solicitud.funcionario_id= coordinador_ct.id
            solicitud.fecha_modificacion_estado=datetime.datetime.now()
            solicitud.save()
            return  HttpResponse(status=200)
        except Exception, e:
            raise e


class EnviarSolicitud(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(EnviarSolicitud, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            solicitud_id = kwargs ['id']
            pst_id= int(request.user.pk)
            solicitud = Solicitud.objects.get(id= int(solicitud_id))
            error = None

            if solicitud.estatus.abreviacion == 'SC':
                if validate_requisitos_documentales(solicitud):
                    if validate_requisitos_principales(solicitud, 'RB'): 
                        #if validate_valores_especificos(solicitud):             
                        coordinador_id = algoritmo_asignacion.algoritmo_de_asignacion('coordinador_ct')
                        coord = Funcionario.objects.filter(id= coordinador_id).first()
                        tipoasig = TipoAsignacion.objects.filter(abreviacion='C').first()
                        asignacion = Asignacion(
                            funcionario_id=coordinador_id,
                            tipo_asignacion_id=tipoasig.id,
                            solicitud_id=solicitud.id,
                            fecha_asignacion=datetime.datetime.now()                    
                        )
                        asignacion.save()

                        asig=Asignacion.objects.filter(
                            solicitud_id=solicitud.id,
                            asignacion_habilitada=True,
                            funcionario__tiporol__nombre='coordinador_ct'
                        ).order_by('-fecha_asignacion').first()

                        estatus=Estatus.objects.get(abreviacion='PAA')
                        #else:
                            #request.session['error'] = "No se han registrado en su totalidad los valores especificos para esta solicitud"
                    else:
                        request.session['error'] = "No se han registrado en su totalidad los requisitos funcionales para esta solicitud"
                else:
                    request.session['error'] =  "No se han registrado en su totalidad los requisitos documentales para esta solicitud"
            else:                
                asig=Asignacion.objects.filter(
                    solicitud_id=solicitud.id, 
                    asignacion_habilitada=True,
                    funcionario__tiporol__nombre='analista'
                ).order_by('-fecha_asignacion').first()

                if validate_elementos_valor(solicitud):
                    estatus=Estatus.objects.get(abreviacion='SAI')
                else:
                    estatus=Estatus.objects.get(abreviacion='SAR')

            if not request.session.has_key('error'):
                receptor=asig.funcionario
                notificacion = Notificacion(
                    emisor_id=pst_id,
                    receptor_id=receptor.user_id,
                    solicitud=solicitud,
                    estatus_actual=estatus
                )
                
                notificacion.save()
                solicitud.estatus_id=estatus.id
                solicitud.funcionario_id= receptor.id
                solicitud.fecha_modificacion_estado=datetime.datetime.now()
                solicitud.save()

            return HttpResponseRedirect(
                reverse(
                    'bandeja'
                )                
            )
        except Exception, e:
            raise e            
        

class DevolverConObservaciones(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(DevolverConObservaciones, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):        
        emisor_id = int(request.user.pk)

        try:
            id_s = request.POST['solicitud']

            ultima_notificacion=Notificacion.objects.filter(
                solicitud__id=id_s
                ).order_by('-fecha_emision').first()

            validacion = val(
                request.FILES,
                'archivo',
                ['application/pdf', 'image/jpeg', 'image/png'] ,
                2621440) if request.FILES.has_key('archivo') else False

            dprint(id_s = id_s, validacion = val)
                    
            if len (request.POST['comentario-observaciondev'])==0:
                observacion=ultima_notificacion.observacion
            else:
                observacion=request.POST['comentario-observaciondev']
            
            emisor=Funcionario.objects.get(user_id=int(emisor_id))
            tiporol_emisor=emisor.tiporol.nombre
            solicitud = Solicitud.objects.get(id=int(id_s))
            estatus_solicitud=solicitud.estatus.abreviacion
            if estatus_solicitud == 'SAR':
                receptor = solicitud.pst
                solicitud.funcionario_id= None
                estatus= Estatus.objects.get(abreviacion='EC')
            else:
                if estatus_solicitud == 'RI':
                    tiporol= TipoRol.objects.get(nombre='inspector')
                    estatus= Estatus.objects.get(abreviacion='CI')
                    #funcionarios = Funcionario.objects.filter(tiporol_id=tiporol.id).values_list('id')
                    #ids= [e[0] for e in funcionarios]
                    asig=Asignacion.objects.filter(solicitud__id=solicitud.id, 
                        funcionario__tiporol__nombre='inspector',
                        asignacion_habilitada=True).order_by('-fecha_asignacion')
                    #asig = Asignacion.objects.filter(funcionario_id__in=ids, solicitud_id=solicitud.id)
                    if len(asig)>1:
                        receptor = asig[0].funcionario
                        receptor_extra = asig[1].funcionario
                        notificacion_extra = Notificacion(
                            emisor_id=emisor_id,
                            receptor_id=receptor_extra.user_id,
                            solicitud=solicitud,
                            observacion=observacion,
                            estatus_actual=estatus
                            #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                        )
                        notificacion_extra.save()
                        if validacion:
                            #TODO: volver plantilla documento nulo
                            nombre_documento = "archivo_notificacion_%s_%s" % (
                                notificacion_extra.id,
                                solicitud.id
                            )
                            documento = Documento(
                                nombre = nombre_documento,
                                ruta_documento=request.FILES['archivo'],
                                tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                                extension = str(request.FILES['archivo']).split(".")[1]
                            )
                            documento.save()

                            notificaciondoc= NotificacionDocumentoCompuesto(
                                notificacion=notificacion_extra,
                                documento=documento
                            )
                            notificaciondoc.save()
                        solicitud.funcionario_extra_id=receptor_extra.id
                    else:
                        receptor = asig[0].funcionario
                elif estatus_solicitud == 'ECI':
                    tiporol= TipoRol.objects.get(nombre='inspector')
                    estatus= Estatus.objects.get(abreviacion='EI')
                    #funcionarios = Funcionario.objects.filter(tiporol_id=tiporol.id).values_list('id')
                    #ids= [e[0] for e in funcionarios]
                    asig=Asignacion.objects.filter(solicitud__id=solicitud.id, 
                        funcionario__tiporol__nombre='inspector',
                        asignacion_habilitada=True).order_by('-fecha_asignacion')
                    #asig = Asignacion.objects.filter(funcionario_id__in=ids, solicitud_id=solicitud.id)
                    if len(asig)>1:
                        receptor = asig[0].funcionario
                        receptor_extra = asig[1].funcionario
                        notificacion_extra = Notificacion(
                            emisor_id=emisor_id,
                            receptor_id=receptor_extra.user_id,
                            solicitud=solicitud,
                            observacion=observacion,
                            estatus_actual=estatus
                            #archivo=request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                        )
                        notificacion_extra.save()
                        if validacion:
                            #TODO: volver plantilla documento nulo
                            nombre_documento = "archivo_notificacion_%s_%s" % (
                                notificacion_extra.id,
                                solicitud.id
                            )
                            documento = Documento(
                                nombre = nombre_documento,
                                ruta_documento=request.FILES['archivo'],
                                tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                                extension = str(request.FILES['archivo']).split(".")[1]
                            )
                            documento.save()

                            notificaciondoc= NotificacionDocumentoCompuesto(
                                notificacion=notificacion_extra,
                                documento=documento
                            )
                            notificaciondoc.save()
                        solicitud.funcionario_extra_id=receptor_extra.id
                    else:
                        receptor = asig[0].funcionario
                elif estatus_solicitud == 'EANP':
                        notificacion=Notificacion.objects.filter(solicitud_id=solicitud.id, receptor_id=emisor.user_id).order_by('-fecha_emision').first()
                        dprint(notificacion.estatus_actual)
                        while (solicitud.estatus.id == notificacion.estatus_actual.id):
                            #emisor_noti=Funcionario.objects.filter(user_id=notificacion.emisor.id).first()
                            notificacion=Notificacion.objects.filter(solicitud_id=solicitud.id, receptor_id=notificacion.emisor.id).order_by('-fecha_emision').first()
                        
                        receptor= Funcionario.objects.filter(user_id=notificacion.receptor.id).first()
                        estatus=notificacion.estatus_actual   
                else:
                    if estatus_solicitud == 'SAI':
                        tiporol= TipoRol.objects.filter(nombre='coordinador_dif').first()
                        estatus= Estatus.objects.filter(abreviacion='RI').first()            
                    elif estatus_solicitud == 'EA' or estatus_solicitud == 'EN':
                        tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                        estatus= Estatus.objects.filter(abreviacion='ITG').first()
                    elif estatus_solicitud == 'SEAR':
                        tiporol= TipoRol.objects.filter(nombre='analista').first()
                        estatus= Estatus.objects.filter(abreviacion='SAR').first()
                    elif estatus_solicitud == 'DMG' or estatus_solicitud == 'RPG':
                        tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                        if estatus_solicitud == 'DMG':
                            #tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                            estatus= Estatus.objects.filter(abreviacion='ITG').first()
                        elif estatus_solicitud == 'RPG':
                            #tiporol= TipoRol.objects.filter(nombre='coordinador_ct').first()
                            estatus= Estatus.objects.filter(abreviacion='EAP').first()
                        documento=NotificacionDocumentoCompuesto.objects.get(notificacion=ultima_notificacion).documento
                        documento.eliminado=True
                        documento.save()
                    elif estatus_solicitud == 'CG':
                        tiporol= TipoRol.objects.filter(nombre='coordinador_dif').first()
                        estatus= Estatus.objects.filter(abreviacion='PAI').first()
                        documento=NotificacionDocumentoCompuesto.objects.get(notificacion=ultima_notificacion).documento
                        documento.eliminado=True
                        documento.save()
                    elif estatus_solicitud == 'EI':
                        tiporol= TipoRol.objects.filter(nombre='coordinador_dif').first()
                        estatus= Estatus.objects.filter(abreviacion='ECI').first()
                        solicitud.funcionario_extra=None
                    elif tiporol_emisor == 'coordinador_ct':
                        tiporol= TipoRol.objects.filter(nombre='analista').first()
                        estatus= Estatus.objects.filter(abreviacion='SAI').first()
                    #funcionarios = Funcionario.objects.filter(tiporol_id=tiporol.id).values_list('id')
                    #ids= [e[0] for e in funcionarios]
                    #asig = Asignacion.objects.filter(funcionario_id__in=ids, solicitud_id=solicitud.id).first()
                    asig=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                        funcionario__tiporol__nombre=tiporol.nombre, asignacion_habilitada=True
                        ).order_by('-fecha_asignacion').first() 
                    receptor = Funcionario.objects.filter(id=asig.funcionario.id).first()
                solicitud.funcionario= receptor
            
            notificacion = Notificacion(
                emisor = emisor.user,
                receptor = receptor.user,
                solicitud = solicitud,
                observacion = observacion,
                estatus_actual = estatus
                #archivo = request.FILES['archivo'] if validacion else ultima_notificacion.archivo
            )
            #notificacion = Notificacion.create(obj)
            notificacion.save()
            if validacion:
                #TODO: volver plantilla documento nulo
                nombre_documento = "archivo_notificacion_%s_%s" % (
                    notificacion.id,
                    solicitud.id
                )
                documento = Documento(
                    nombre = nombre_documento,
                    ruta_documento=request.FILES['archivo'],
                    tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                    extension = str(request.FILES['archivo']).split(".")[1]
                )
                documento.save()

                notificaciondoc= NotificacionDocumentoCompuesto(
                    notificacion=notificacion,
                    documento=documento
                )
                notificaciondoc.save()

            if estatus_solicitud == 'SAR':
                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                    +str(direc.codigo_postal)
                #licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

                #<--- Envio de Correo --->
                htmly = get_template('correo/correccion_requisitos_docs.html')
                text_plain = get_template('correo/correccion_requisitos_docs.txt')

                context = Context({
                    'razon_social': solicitud.pst.razon_social,
                    'direccion': direccionPST,
                    'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first()
                 })

                html_content = htmly.render(context)
                text_content = text_plain.render(context)

                thread_correo = threading.Thread(
                    name='thread_correo', 
                    target=correo, 
                    args=(
                        u'[MINTUR] Correcciones del Proceso de Categorización', 
                        html_content, 
                        text_content, 
                        'gccdev@cgtscorp.com', 
                        ['gccdev@cgtscorp.com'], 
                        None, 
                        None)
                    )                
                thread_correo.start()

            solicitud.estatus=estatus
            solicitud.fecha_modificacion_estado=datetime.datetime.now()
            solicitud.save()

            jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
            return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
        except Exception, error:
            return  HttpResponse(error, content_type="application/json", status=400)


class InspectorOperacion(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(InspectorOperacion, self).dispatch(*args, **kwargs)

    def get(self,request,*args,**kwargs):
        op =kwargs ['operacion']
        ident = kwargs ['id']
        inspector_id= int(request.user.pk)
        solicitud = Solicitud.objects.get(id= int(ident))
        if op == 'vercredencial':
            coord = Asignacion.objects.get(
                solicitud_id=ident, 
                funcionario__tiporol__nombre='coordinador_dif',
                asignacion_habilitada=True
                ).funcionario.user

            try:
                tipo = TipoDocumentoCompuesto.objects.get(abreviacion='C')
                credencial = NotificacionDocumentoCompuesto.objects.filter(
                    documento__tipo_documento_compuesto=tipo,
                    notificacion__solicitud_id=ident
                    ).last().documento
                dprint(credencial_ruta_documento=credencial.ruta_documento)
                jsontmp = {
                    "err_msg": "",
                    "success": "Pagina encontrada",
                    "ruta_documento": str(credencial.ruta_documento)
                }

                return  HttpResponse(json.dumps(
                        jsontmp,sort_keys=True),
                        content_type="application/json",
                        status=200
                    )
            except Exception, e:
                jsontmp = {
                    "err_msg": "Documento inexistente",
                    "success": ""
                }

                return  HttpResponse(
                    json.dumps(jsontmp,sort_keys=True),
                    content_type="application/json",
                    status=200
                )

    def post(self,request,*args,**kwargs):
        op =kwargs ['operacion']
        ident = kwargs ['id']
        inspector_id= int(request.user.pk)
        solicitud = Solicitud.objects.get(id= int(ident))
        licencia=otp_solicitud(solicitud=solicitud)
        ultima_notificacion=Notificacion.objects.filter(
            solicitud=solicitud
            ).order_by('-fecha_emision').first()

        try:

            if op == 'enviarinspeccion':

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-enviarins'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-enviarins']

                if validate_requisitos_principales (solicitud, 'RE'):
                    if validate_fotografias_inspeccion(solicitud):
                        asig=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                            funcionario__tiporol__nombre='coordinador_dif', asignacion_habilitada=True
                            ).order_by('-fecha_asignacion').first()
                        coordinador_dif=asig.funcionario
                        estatus=Estatus.objects.get(abreviacion='RI')
                        notificacion = Notificacion(
                            emisor_id=inspector_id,
                            receptor_id=coordinador_dif.user_id,
                            solicitud=solicitud,
                            estatus_actual=estatus,
                            observacion=observacion
                            #archivo=request.FILES['archivo'] if validacion else ultima_notificacion.archivo
                        )
                        notificacion.save()
                        if validacion:
                            #TODO: volver plantilla documento nulo
                            nombre_documento = "archivo_notificacion_%s_%s" % (
                                notificacion.id,
                                solicitud.id
                            )
                            documento = Documento(
                                nombre = nombre_documento,
                                ruta_documento=request.FILES['archivo'],
                                tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                                extension = str(request.FILES['archivo']).split(".")[1]
                            )
                            documento.save()

                            notificaciondoc= NotificacionDocumentoCompuesto(
                                notificacion=notificacion,
                                documento=documento
                            )
                            notificaciondoc.save()

                        solicitud.estatus=estatus
                        solicitud.funcionario= coordinador_dif
                        solicitud.funcionario_extra_id=None
                        solicitud.fecha_modificacion_estado=datetime.datetime.now()
                        solicitud.save()

                        #return  HttpResponse(status=200)
                        jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                        return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                    else:
                        error="No se han registrado en su totalidad todas las imágenes de la Inspección."
                        return  HttpResponse(error, content_type="application/json", status=400)
                else:
                    error="No se ha registrado en su totalidad la Inspección."
                    return  HttpResponse(error, content_type="application/json", status=400)
            """
            elif op == 'enviarinforme':
                if validate_elementos_valor(solicitud):
                    asig=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                        funcionario__tiporol__nombre='coordinador_dif', asignacion_habilitada=True
                        ).order_by('-fecha_asignacion').first()
                    coordinador_dif=asig.funcionario
                    estatus=Estatus.objects.get(abreviacion='RI')
                    notificacion = Notificacion(
                        emisor_id=inspector_id,
                        receptor_id=coordinador_dif.user_id,
                        solicitud=solicitud,
                        estatus_actual=estatus
                    )
                    notificacion.save()

                    plantilla = PlantillaDocumento.objects.get(formato="pdf/informe_tecnico.html")
                    
                    try:
                        #Creando el documento
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='IT')
                        nombre_documento = "%s_informe_tecnico_%s_%s" % (
                            solicitud.pst.user.rif,
                            solicitud.id,
                            solicitud.funcionario.id                        
                        )
                        if solicitud.funcionario_extra:
                            nombre_documento+='_'+str(solicitud.funcionario_extra.id)

                        path = model_list.get_file_path(
                            solicitud.pst.user.rif,
                            'informe_tecnico',
                            "",
                        )

                        locationPath = os.path.join(
                            BASE_DIR,
                            'documents',
                            'files', 
                            path
                        )
                                                
                        try:
                            informe = Documento.objects.get(
                                nombre=nombre_documento)
                            informe.fecha_aprobacion=datetime.datetime.now()
                        except:
                            data = Storage(
                                nombre=nombre_documento,
                                fecha_aprobacion=datetime.datetime.now(),
                                plantilla_documento=plantilla,
                                ruta_documento = '/documents/' + path +'/'+ nombre_documento + '.pdf',
                                extension = 'pdf',
                                tipo_documento_compuesto=tipo_documento,
                            )

                            informe = Documento.create(data)

                        informe.save()

                        #La notificacion 
                        ndi = NotificacionDocumentoCompuesto(
                            notificacion = notificacion,
                            documento = informe
                        )
                        ndi.save()

                        #PARAMETROS PARA EL INFORME
                        data = Storage(
                            pagesize='A4',
                            tipo=licencia,
                            nombre_establecimiento=solicitud.pst.denominacion_comercial,
                            inspector1=solicitud.funcionario.nombre + ' ' + solicitud.funcionario.apellido,
                            inspector2=solicitud.funcionario_extra.nombre + ' ' + solicitud.funcionario_extra.apellido if solicitud.funcionario_extra is not None else "",
                            resolucion=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='R', 
                                documento_asociado__abreviacion='IT', 
                                tipo_pst=licencia
                            ).first(),
                            gaceta=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='GO', 
                                documento_asociado__abreviacion='IT', 
                                tipo_pst=licencia
                            ).first(),
                            articulo=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='A', 
                                documento_asociado__abreviacion='IT', 
                                tipo_pst=licencia
                            ),
                            funcionario=coordinador_dif
                        )

                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='pdf/informe_tecnico.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                            
                    except Exception, e:
                        return  HttpResponse(e, content_type="application/json", status=400)

                    solicitud.estatus=estatus
                    solicitud.funcionario= coordinador_dif
                    solicitud.funcionario_extra_id=None
                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                    solicitud.save()

                    return  HttpResponse(status=200)
                else:
                    error="No se ha registrado en su totalidad el Informe Técnico."
                    return  HttpResponse(error, content_type="application/json", status=400)
            """
        except Exception, e:
            raise e


class FinReparaciones(View):

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(FinReparaciones, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            solicitud_id = kwargs ['id']
            pst_id= int(request.user.pk)
            solicitud = Solicitud.objects.get(id= int(solicitud_id))
            estatus=Estatus.objects.get(abreviacion='SEAR')
            asig=Asignacion.objects.filter(solicitud_id=solicitud.id, 
                funcionario__tiporol__nombre='coordinador_ct', asignacion_habilitada=True
                ).order_by('-fecha_asignacion').first()
            coordinador_ct=asig.funcionario
            notificacion = Notificacion(
                emisor_id=pst_id,
                receptor_id=coordinador_ct.user_id,
                solicitud=solicitud,
                estatus_actual=estatus
            )
            notificacion.save()
            solicitud.estatus_id=estatus.id
            solicitud.funcionario_id= coordinador_ct.id
            solicitud.fecha_modificacion_estado=datetime.datetime.now()
            solicitud.save()

            return  HttpResponse(status=200)
        except Exception, e:
            raise e


class BandejaLibro(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(BandejaLibro, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):   
        
        try:
            user = request.user
            id_sesion = user.id
            natural = juridica = False
            libros={}
            busqueda_datos={}
            key='busqueda_cache'

            if user.role == ROLE_PST:
                pst = user.pst_set.get()            
                activar_libro = True

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True

                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        solicitudes = SolicitudLibro.objects.filter(**filter_dict).order_by(
                            '-fecha_realizacion'
                        )                    
                    else:
                        solicitudes = SolicitudLibro.objects.filter(pst = pst.pk).order_by('-fecha_realizacion')
                    busqueda_datos.update({'solicitudes':solicitudes})
                else:
                    x=cache.get(key)
                    solicitudes=x['solicitudes']
               
                paginars=False
                mas=True
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    sol= solicitudes
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    sol= solicitudes
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                for s in solicitudes:
                    l=LsrFisico.objects.filter(solicitud_libro=s).first()
                    if l:
                        libros.update({s.id:l.identificador})

                sucursales = sucursales_licencia(user)
                estados= Estado.objects.all()
                if request.session.has_key('error'):
                    errors = request.session['error']
                    del request.session['error']
                else:
                    errors=""
                context={
                    'activar_libro': activar_libro,
                    'pst': pst,
                    'error': errors,
                    'natural':natural,
                    'juridica':juridica,
                    'actor': user.get_full_name(),
                    'solicitudes': solicitudes,
                    'sucursales': sucursales,
                    'estados': estados,
                    'libros':libros
                }
                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})

                return render(request, 'pst/bandejaLSR.html', context)
            elif user.role == ROLE_FUNCIONARIO:
                funcionario = Funcionario.objects.get(user_id=int(id_sesion))
                """
                if funcionario.tiporol.nombre == "analista":
                    
                    numero_comprobante={}
                    archivo={}
                    funcionario=Funcionario.objects.get(user_id=id_sesion)

                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        if filter_dict.has_key('adicional'):
                            array_texto = filter_dict['adicional']
                            filter_dict.pop('adicional')
                            solicitudes = SolicitudLibro.objects.filter(
                                reduce(operator.or_,array_texto), funcionario=funcionario, **filter_dict
                            ).order_by('-fecha_realizacion')
                        else:    
                            solicitudes = SolicitudLibro.objects.filter(
                                funcionario=funcionario, **filter_dict).order_by(
                                '-fecha_realizacion'
                            )                    
                    else:
                        solicitudes = SolicitudLibro.objects.filter(funcionario = funcionario).order_by('-fecha_realizacion')
                    
                    paginars=False
                    mas=True
                    if request.GET.has_key('p') and request.GET.has_key('s'): 
                        paginars = True
                        p= int(request.GET['p'])
                        s= request.GET['s']
                        dprint(s)
                        if s == '-':
                            p -= 1
                        elif s == '+':
                            dprint(s)
                            p += 1
                        sol= solicitudes
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(sol[num:num+1]) ==0:
                            mas = False

                    if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                        p= 0
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        paginars = True
                        sol= solicitudes
                        solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(sol[num:num+1]) ==0:
                            mas = False

                    for s in solicitudes:
                        l=LsrFisico.objects.filter(solicitud_libro=s).first()
                        if l:
                            libros.update({s.id:l.identificador})
                    context={}
                    context.update({
                        'actor': user.get_full_name(),
                        'solicitudes': solicitudes,
                        'libros':libros,
                        'tiporol': funcionario.tiporol.nombre,
                    })
                    if paginars == True:
                        context.update({'p': p, 'mas': mas})

                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        solicit = quote_plus(request.GET['solicitudes'])
                        context.update({'sol_buscar': solicit, 'busqueda':True})                    

                    user = funcionario.tiporol.nombre
                    context.update({user: True})

                    return render(request, 'analista/bandejaLSR.html', context)
    
                """
                if funcionario.tiporol.nombre == "coordinador_ct" or funcionario.tiporol.nombre == 'analista':
                    funcionario=Funcionario.objects.get(user_id=id_sesion)
                    analistax={}
                    asignaciones=Asignacion.objects.filter(
                        funcionario=funcionario, 
                        #tipo_asignacion__abreviacion='LSR',
                        asignacion_habilitada=True
                    ).values('solicitud_libro')

                    if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                        cache.delete(key)
                        if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                            dprint(decode=request.GET['solicitudes'])
                            params = secure_value_decode(request.GET['solicitudes'])
                            dprint(params=params)
                            filter_dict=pickle.loads(params)
                            dprint(filter_dict=filter_dict)
                            if filter_dict.has_key('adicional'):
                                array_texto = filter_dict['adicional']
                                filter_dict.pop('adicional')
                                solicitudes = SolicitudLibro.objects.filter(
                                    reduce(operator.or_,array_texto),id__in=asignaciones, **filter_dict
                                ).order_by('-fecha_realizacion')
                            else:    
                                solicitudes = SolicitudLibro.objects.filter(
                                    id__in=asignaciones,**filter_dict).order_by(
                                    '-fecha_realizacion'
                                )                    
                        else:
                            solicitudes = SolicitudLibro.objects.filter(id__in=asignaciones
                                ).order_by('-fecha_realizacion'
                            )
                        busqueda_datos.update({'solicitudes':solicitudes})
                    else:
                        x=cache.get(key)
                        solicitudes=x['solicitudes']
                    
                    paginars=False
                    mas=True
                    if request.GET.has_key('p') and request.GET.has_key('s'):
                        paginars = True
                        p= int(request.GET['p'])
                        s= request.GET['s']
                        dprint(s)
                        if s == '-':
                            p -= 1
                        elif s == '+':
                            dprint(s)
                            p += 1
                        sol= solicitudes
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(sol[num:num+1]) ==0:
                            mas = False

                    if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                        p= 0
                        dprint(p=p)
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        paginars = True
                        sol= solicitudes
                        solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(sol[num:num+1]) ==0:
                            mas = False

                    for s in solicitudes:
                        asig=Asignacion.objects.filter(
                            solicitud_libro=s,
                            asignacion_habilitada=True,
                            funcionario__tiporol__nombre='analista'
                        ).first()
                        if asig:
                            analistax.update({s.id:[(asig.funcionario.id, asig.funcionario.nombre+" "+asig.funcionario.apellido)]})
    
                        l=LsrFisico.objects.filter(solicitud_libro=s).first()
                        if l:
                            libros.update({s.id:l.identificador})
                        pst=Pst.objects.get(id=s.pst.id)

                    context={
                        'actor': user.get_full_name(),
                        'solicitudes': solicitudes,
                        'libros':libros,
                        'tiporol': funcionario.tiporol.nombre,
                        'analistax': analistax,
                        'funcionario_id': funcionario.id
                    }

                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        solicit = quote_plus(request.GET['solicitudes'])
                        context.update({'sol_buscar': solicit, 'busqueda':True})

                    if paginars == True:
                        context.update({'p': p, 'mas': mas})
                    
                    if request.GET.has_key('busqueda'):
                        cache.set(
                            key,
                            busqueda_datos
                        )
                    user = funcionario.tiporol.nombre
                    context.update({user: True})

                    return render(request, 'coordinador_ct/bandejaLSR.html', context)

        except Exception, e:
            raise e


class PorEntregar(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(PorEntregar, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        user = request.user
        id_sesion = user.id
        numero_comprobante={}
        archivo={}
        libros={}
        busqueda_datos={}
        key='busqueda_cache'

        funcionario=Funcionario.objects.get(user_id=id_sesion)

        if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
            cache.delete(key)
            if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                dprint(decode=request.GET['solicitudes'])
                params = secure_value_decode(request.GET['solicitudes'])
                dprint(params=params)
                filter_dict=pickle.loads(params)
                dprint(filter_dict=filter_dict)
                if filter_dict.has_key('adicional'):
                    array_texto = filter_dict['adicional']
                    filter_dict.pop('adicional')
                    solicitudes = SolicitudLibro.objects.filter(
                        reduce(operator.or_,array_texto), estatus__abreviacion__in= ['CP', 'PC', 'O'], **filter_dict
                    ).order_by('-fecha_realizacion')
                else:    
                    solicitudes = SolicitudLibro.objects.filter(
                        estatus__abreviacion__in= ['CP', 'PC', 'O'], **filter_dict).order_by(
                        '-fecha_realizacion'
                    )                    
            else:
                solicitudes = SolicitudLibro.objects.filter(estatus__abreviacion__in= ['CP', 'PC', 'O']).order_by('-fecha_realizacion')
            busqueda_datos.update({'solicitudes':solicitudes})
        else:
            x=cache.get(key)
            solicitudes=x['solicitudes']
        
        paginars=False
        mas=True
        if request.GET.has_key('p') and request.GET.has_key('s'): 
            paginars = True
            p= int(request.GET['p'])
            s= request.GET['s']
            dprint(s)
            if s == '-':
                p -= 1
            elif s == '+':
                dprint(s)
                p += 1
            sol= solicitudes
            num=((p+1)*constants.ELEMENTO_POR_PAGINA)
            solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
            if len(sol[num:num+1]) ==0:
                mas = False

        if  not request.GET.has_key('p') or not request.GET.has_key('s'):
            p= 0
            num=((p+1)*constants.ELEMENTO_POR_PAGINA)
            paginars = True
            sol= solicitudes
            solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
            if len(sol[num:num+1]) ==0:
                mas = False

        for s in solicitudes:
            l=LsrFisico.objects.filter(solicitud_libro=s).first()
            if l:
                libros.update({s.id:l.identificador})
        context={}
        context.update({
            'actor': user.get_full_name(),
            'solicitudes': solicitudes,
            'libros':libros,
            'tiporol': funcionario.tiporol.nombre,
        })
        if paginars == True:
            context.update({'p': p, 'mas': mas})

        if request.GET.has_key('busqueda'):
            cache.set(
                key,
                busqueda_datos
            )

        if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
            solicit = quote_plus(request.GET['solicitudes'])
            context.update({'sol_buscar': solicit, 'busqueda':True})                    

        user = funcionario.tiporol.nombre
        context.update({user: True})

        return render(request, 'analista/porentregar.html', context)

class Respuesta(View):
    #firma no completado
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(Respuesta, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):   
        try:
            user = request.user
            id_sesion = user.id
            jsontmp = {}
            #natural = juridica = False
            funcionario= Funcionario.objects.get(user_id=int(id_sesion))    
            op = kwargs['operacion']
            #solicitud_id = request.POST['solicitud']
            solicitud= Solicitud.objects.get(id=int(request.POST['solicitud'])) if request.POST.has_key('solicitud') else None

            if op=='firmar':
                if request.POST.has_key('licencia'):
                    placa=Placa.objects.get(licencia_asignada__numero_licencia=int(request.POST['licencia']))
                    dprint(placa=placa)
                    doc=Documento.objects.get(id=placa.documento.id)
                    dprint(doc=doc)
                    doc.firmado=True
                    doc.save()
                    return HttpResponse(status=200)

                elif solicitud.estatus.abreviacion == 'CG':
                    estatus= Estatus.objects.get(abreviacion='EI')
                    inspect= Asignacion.objects.filter(
                        solicitud=solicitud, 
                        asignacion_habilitada=True, 
                        funcionario__tiporol__nombre='inspector'
                    ).values_list('funcionario')
                    ins = [e[0] for e in inspect]
                    inspectores= Funcionario.objects.filter(id__in=ins)

                    notificacion= Notificacion(
                        emisor_id=id_sesion, 
                        receptor_id=inspectores[0].user_id, 
                        solicitud_id=solicitud.id, 
                        estatus_actual=estatus
                    )
                    notificacion1= Notificacion(
                        emisor_id=id_sesion, 
                        receptor_id=inspectores[1].user_id, 
                        solicitud_id=solicitud.id, 
                        estatus_actual=estatus
                    )
                    notificacion.save()
                    notificacion1.save()

                    solicitud.estatus=estatus
                    solicitud.funcionario_id = inspectores[0].id
                    solicitud.funcionario_extra_id = inspectores[1].id
                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                    solicitud.save()

                    jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                else:
                    if solicitud.estatus.abreviacion == 'RPG':
                        estatus=Estatus.objects.get(abreviacion='EP')

                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

                        #<--- Envio de Correo --->
                        htmly = get_template('correo/aprobar_prorroga.html')
                        text_plain = get_template('correo/aprobar_prorroga.txt')

                        context = Context({
                            'razon_social': solicitud.pst.razon_social,
                            'direccion': direccionPST,
                            'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first()
                         })

                        html_content = htmly.render(context)
                        text_content = text_plain.render(context)

                        thread_correo = threading.Thread(
                            name='thread_correo', 
                            target=correo, 
                            args=(
                                u'[MINTUR] Respuesta de solicitud de Prórroga', 
                                html_content, 
                                text_content, 
                                'gccdev@cgtscorp.com', 
                                ['gccdev@cgtscorp.com'], 
                                None, 
                                None
                            )
                        )
                        thread_correo.start()

                    elif solicitud.estatus.abreviacion == 'DMG':
                        estatus=Estatus.objects.get(abreviacion='ER')

                        direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

                        #<--- Envio de Correo --->
                        htmly = get_template('correo/aprobar_reparacion_prorroga.html')
                        text_plain = get_template('correo/aprobar_reparacion_prorroga.txt')

                        context = Context({
                            'razon_social': solicitud.pst.razon_social,
                            'direccion': direccionPST,
                            'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                            'tipo_pst': licencia.tipo_licenciaid,
                            'resolucion': EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='R', 
                                documento_asociado__abreviacion='CDM', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            'gaceta': EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='G', 
                                documento_asociado__abreviacion='CDM', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            'dias': ("%s(%d)" % (to_word(solicitud.dias_prorroga), solicitud.dias_prorroga)).lower()
                         })

                        html_content = htmly.render(context)
                        text_content = text_plain.render(context)

                        thread_correo = threading.Thread(
                            name='thread_correo', 
                            target=correo, 
                            args=(
                                u'[MINTUR] Disposiciones de Mejora', 
                                html_content, 
                                text_content, 
                                'gccdev@cgtscorp.com', 
                                ['gccdev@cgtscorp.com'], 
                                None, 
                                None
                            )
                        )
                        thread_correo.start()
                    else:
                        error="Error inesperado"
                        return  HttpResponse(error, content_type="application/json", status=400)

                    notificacion = Notificacion(
                        emisor_id=id_sesion,
                        receptor=solicitud.pst.user,
                        solicitud=solicitud,
                        estatus_actual=estatus
                    )
                    notificacion.save()

                    solicitud.estatus=estatus
                    solicitud.funcionario=None
                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                    solicitud.save()
                    jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'aprobar' or op == 'aprobarcumplimiento' or op == 'negarincumplimiento' or op == 'negar':

                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                    +str(direc.codigo_postal)
                licencia = dt_licencia(solicitud.pst, solicitud.sucursal)


                if op == 'aprobar' or op == 'aprobarcumplimiento':

                    placa = Placa(
                        pst=solicitud.pst,
                        licencia_asignada=licencia,
                    )
                    placa.save()

                    estatus=Estatus.objects.get(abreviacion='A')
                    
                    notificacion = Notificacion(
                        emisor_id = int(id_sesion),
                        receptor_id = solicitud.pst.id,
                        solicitud = solicitud,
                        estatus_actual = estatus
                    )
                    notificacion.save()
                    solicitud.estatus=estatus
                    solicitud.funcionario=None
                    solicitud.save()

                    if op == 'aprobar':

                        categorizacion={}
                        try:
                            LsrDigital.objects.get(sucursal=solicitud.sucursal, pst=solicitud.pst)
                        except:
                            lsr = LsrDigital(
                                pst=solicitud.pst,
                                sucursal=solicitud.sucursal
                                )
                            lsr.save()
                        """
                        lic = LicenciaAsignada.objects.filter(usuario_pst=solicitud.pst.user, 
                            sucursal_id=solicitud.sucursal_id
                        ).first()
                        if lic:
                            dprint(lic=lic)
                            if solicitud.sucursal_id:
                                licencia = lic.numero_licencia
                                suc= solicitud.pst.denominacion_comercial
                                direccion = "%s, %s, %s, %s" %(solicitud.sucursal.urbanizacion, solicitud.sucursal.avenida_calle, solicitud.sucursal.edificio, solicitud.sucursal.oficina_apartamento)
                            else:
                                licencia = lic.numero_licencia
                                suc= "Sede Principal"
                                direccs = Registro_Direccion.objects.get(pst=solicitud.pst)
                                direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
                        """
                        # Creacion de pdf
                        plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_de_otorgamiento_de_categoria_1_vez.html")

                        try:
                            #Creando el documento
                            tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OOC1V')
                            nombre_documento = "%s_oficio_otorgamiento_de_categoria_1_vez_%s_%s" % (
                                solicitud.pst.user.rif,
                                solicitud.id,
                                solicitud.fecha_modificacion_estado.year
                            )

                            path = model_list.get_file_path(
                                solicitud.pst.user.rif,
                                'oficios',
                                "",
                            )

                            locationPath = os.path.join(
                                BASE_DIR,
                                'documents',
                                'files', 
                                path
                            )


                            oficio = Documento.objects.filter(nombre=nombre_documento).first()
                            
                            if oficio:
                                oficio.fecha_emision=datetime.datetime.now()
                                oficio.eliminado=False
                            else:
                                data = Storage(
                                    nombre=nombre_documento,
                                    fecha_aprobacion=datetime.datetime.now(),
                                    plantilla_documento=plantilla,
                                    ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                                    extension = 'pdf',
                                    tipo_documento_compuesto=tipo_documento,
                                )

                                oficio = Documento.create(data)
                            oficio.save()

                            #La notificacion respectiva a uno de los inspectores
                            ndc = NotificacionDocumentoCompuesto(
                                notificacion = notificacion,
                                documento = oficio
                            )
                            ndc.save()

                            try:
                                #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                '''
                                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                    +str(direc.codigo_postal)
                                licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
                                '''
                                data = Storage(
                                    nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                                    oficio=oficio,
                                    fecha=datetime.date.today(),
                                    razon_social=solicitud.pst.razon_social,
                                    direccion=direccionPST,
                                    telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                                    contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                                    rtn=solicitud.pst.rtn,
                                    fecha_apertura_solicitud=solicitud.fecha_apertura,
                                    licencia=licencia.numero_licencia,
                                    categoria=solicitud.pst_categoria_doc.categoria.nomnbre,
                                    denominacion_comercial=solicitud.pst.denominacion_comercial
                                )

                                generar_pdf.generar_pdf(
                                    context=data,
                                    ruta_template='documentos/oficios/oficio_de_otorgamiento_de_categoria_1_vez.html',
                                    ruta_documento=locationPath,
                                    nombre_documento=nombre_documento
                                )

                                locationAttach = os.path.join(
                                    locationPath,
                                    nombre_documento + '.pdf'
                                )
                                attach_file = locationAttach
                            except Exception, e:
                                raise e
                            
                        except Exception, e:
                            raise e
                        """
                        #<------ Envio de correo ------>
                        htmly = get_template('correo/acepta_niega_categorizacion.html')
                        text_plain = get_template('correo/acepta_niega_categorizacion.txt')

                        context = Context({
                         'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                         'nombre_establecimiento': solicitud.pst.razon_social,
                         'direccion': direccionPST
                         })
                        attach_file = locationAttach

                        html_content = htmly.render(context)
                        text_content = text_plain.render(context)
                        
                        Busqueda de correo en parametros de configuracion
                        try:
                            corr = ParametroConfiguracion.objects.get(
                                clave="correo_interno"
                                )
                        except ParametroConfiguracion.DoesNotExist:
                            raise e
                        corrs = str(corr.valor)
                        
                        thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Resultados del proceso de categorización', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], attach_file, None))                
                        thread_correo.start()


                        jsontmp = {"categorizacion":categorizacion}
                        """
                        #return  HttpResponse(json.dumps(jsontmp,sort_keys=True), 
                        #    content_type="application/json", status=200
                        #)

                    elif op == 'aprobarcumplimiento':
                        """
                        estatus=Estatus.objects.get(abreviacion='A')

                        notificacion = Notificacion(
                            emisor_id = int(id_sesion),
                            receptor_id = solicitud.pst.id,
                            solicitud = solicitud,
                            estatus_actual=estatus
                        )
                        notificacion.save()

                        solicitud.estatus=estatus
                        solicitud.funcionario=None
                        solicitud.save()
                        """
                        # Creacion de pdf
                        tablas=dt_tablas_it(solicitud)
                        plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_de_otorgamiento_de_categoria_por_cumplimiento_de_las_disposiciones_de_mejora.html")
                        try:
                            #Creando el documento
                            tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OCPPI')
                            nombre_documento = "%s_oficio_otorgamiento_de_categoria_por_cumplimiento_de_disposiciones_de_mejora_%s_%s" % (
                                solicitud.pst.user.rif,
                                solicitud.id,
                                datetime.datetime.now().year
                            )

                            path = model_list.get_file_path(
                                solicitud.pst.user.rif,
                                'oficios',
                                "",
                            )

                            locationPath = os.path.join(
                                BASE_DIR,
                                'documents',
                                'files', 
                                path
                            )

                            oficio = Documento.objects.filter(nombre=nombre_documento).first()

                            if oficio:
                                oficio.fecha_emision=datetime.datetime.now()
                                oficio.eliminado=False
                            else:
                                data = Storage(
                                    nombre=nombre_documento,
                                    fecha_emision=datetime.datetime.now(),
                                    plantilla_documento=plantilla,
                                    ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                                    extension = 'pdf',
                                    tipo_documento_compuesto=tipo_documento,
                                )
                                oficio = Documento.create(data)
                            oficio.save()

                            #La notificacion respectiva a uno de los inspectores
                            ndc = NotificacionDocumentoCompuesto(
                                notificacion = notificacion,
                                documento = oficio
                            )
                            ndc.save()
                            try:
                                #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                                '''
                                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                    +str(direc.codigo_postal)
                                licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
                                '''
                                data = Storage(
                                    nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                                    oficio=oficio,
                                    fecha=datetime.date.today(),
                                    razon_social=solicitud.pst.razon_social,
                                    direccion=direccionPST,
                                    telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                                    contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                                    fecha_inspeccion=Notificacion.objects.filter(
                                        estatus_actual__abreviacion='RI',
                                        solicitud=solicitud).order_by('-fecha_emision').first().fecha_emision,
                                    rtn=solicitud.pst.rtn,
                                    fecha_apertura_solicitud=solicitud.fecha_apertura,
                                    licencia=licencia.numero_licencia,
                                    resolucion=EspecificacionLegal.objects.filter(
                                        tipo_especificacion__abreviacion='R', 
                                        documento_asociado__abreviacion='IT', 
                                        tipo_pst=licencia.tipo_licenciaid 
                                    ).first(),
                                    gaceta=EspecificacionLegal.objects.filter(
                                        tipo_especificacion__abreviacion='GO', 
                                        documento_asociado__abreviacion='IT', 
                                        tipo_pst=licencia.tipo_licenciaid 
                                    ).first(),
                                    tipo_pst=licencia.tipo_licenciaid,
                                    cuadro_incumplimiento=tablas[1],
                                    cuadro_incumplimiento_mya=tablas[2],
                                    cuadro_porcentajes=tablas[0],
                                    categorias=Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor'),
                                    disposiciones=NotificacionDocumentoCompuesto.objects.filter(
                                        notificacion__solicitud=solicitud, 
                                        documento__tipo_documento_compuesto__abreviacion='ODM'
                                    ).first().documento,
                                    categoria=solicitud.pst_categoria_doc.categoria.nomnbre
                                )
                                generar_pdf.generar_pdf(
                                    context=data,
                                    ruta_template='documentos/oficios/oficio_de_otorgamiento_de_categoria_por_cumplimiento_de_las_disposiciones_de_mejora',
                                    ruta_documento=locationPath,
                                    nombre_documento=nombre_documento
                                )

                                locationAttach = os.path.join(
                                    locationPath,
                                    nombre_documento + '.pdf'
                                )
                                attach_file = locationAttach
                            except Exception, e:
                                raise e
                            
                        except Exception, e:
                            raise e
                        
                        #<!---- Envio de Correo ---->    
                        """
                        htmly = get_template('correo/acepta_niega_categorizacion.html')
                        text_plain = get_template('correo/acepta_niega_categorizacion.txt')

                        context = Context({
                         'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                         'nombre_establecimiento': solicitud.pst.razon_social,
                         'direccion': direccionPST
                        })

                        attach_file = locationAttach
                        html_content = htmly.render(context)
                        text_content = text_plain.render(context)

                        thread_correo = threading.Thread(
                            name='thread_correo', 
                            target=correo, 
                            args=(
                                u'[MINTUR] Resultados del proceso de categorización', 
                                html_content, 
                                text_content, 'gccdev@cgtscorp.com', 
                                ['gccdev@cgtscorp.com'], 
                                attach_file, 
                                None
                            )
                        )                
                        thread_correo.start()
                        """

                        #return  HttpResponse(status=200)
                    #solicitud placa
                    
                elif op == 'negarincumplimiento':
                    estatus=Estatus.objects.get(abreviacion='NPI')

                    notificacion = Notificacion(
                        emisor_id = int(id_sesion),
                        receptor_id = solicitud.pst.id,
                        solicitud = solicitud,
                        estatus_actual=estatus
                    )
                    notificacion.save()

                    solicitud.estatus=estatus
                    solicitud.funcionario=None
                    solicitud.save()
                    # Creacion de pdf
                    """plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_cierre_por_incumplimiento.html")
                    
                    lic = LicenciaAsignada.objects.filter(usuario_pst=solicitud.pst.user, 
                        sucursal_id=solicitud.sucursal_id
                    ).first()
                    if lic:
                        dprint(lic=lic)
                        if solicitud.sucursal_id:
                            licencia = lic.numero_licencia
                            suc= solicitud.pst.denominacion_comercial
                            direccion = '%s, %s, %s, %s' %(solicitud.sucursal.urbanizacion, solicitud.sucursal.avenida_calle, solicitud.sucursal.edificio, solicitud.sucursal.oficina_apartamento)
                        else:
                            licencia = lic.numero_licencia
                            suc= 'Sede Principal'
                            direccs = Registro_Direccion.objects.get(pst=solicitud.pst)
                            direccion = '%s, %s, %s, %s, %s, %s' %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)

                    """
                    plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_cierre_por_incumplimiento.html")
                    tablas=dt_tablas_it(solicitud)
                    try:
                        #Creando el documento
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OCPPI')
                        nombre_documento = "%s_oficio_cierre_por_incumplimiento_%s_%s" % (
                            solicitud.pst.user.rif,
                            solicitud.id,
                            datetime.datetime.now().year
                        )

                        path = model_list.get_file_path(
                            solicitud.pst.user.rif,
                            'oficios',
                            "",
                        )

                        locationPath = os.path.join(
                            BASE_DIR,
                            'documents',
                            'files', 
                            path
                        )

                        oficio = Documento.objects.filter(nombre=nombre_documento).first()
                        if oficio:
                            oficio.fecha_emision=datetime.datetime.now()
                            oficio.eliminado=False
                        else:
                            data = Storage(
                                nombre=nombre_documento,
                                fecha_emision=datetime.datetime.now(),
                                plantilla_documento=plantilla,
                                ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                                extension = 'pdf',
                                tipo_documento_compuesto=tipo_documento,
                            )
                            oficio = Documento.create(data)
                        oficio.save()

                        #La notificacion respectiva a uno de los inspectores
                        ndc = NotificacionDocumentoCompuesto(
                            notificacion = notificacion,
                            documento = oficio
                        )
                        ndc.save()
                        try:
                            #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                            '''
                            direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                +str(direc.codigo_postal)
                            licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
                            '''
                            data = Storage(
                                nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                                oficio=oficio,
                                fecha=datetime.date.today(),
                                razon_social=solicitud.pst.razon_social,
                                direccion=direccionPST,
                                telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                                contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                                fecha_inspeccion=Notificacion.objects.filter(
                                    estatus_actual__abreviacion='RI',
                                    solicitud=solicitud).order_by('-fecha_emision').first().fecha_emision,
                                rtn=solicitud.pst.rtn,
                                fecha_apertura_solicitud=solicitud.fecha_apertura,
                                licencia=licencia.numero_licencia,
                                resolucion=EspecificacionLegal.objects.filter(
                                    tipo_especificacion__abreviacion='R', 
                                    documento_asociado__abreviacion='IT', 
                                    tipo_pst=licencia.tipo_licenciaid 
                                ).first(),
                                gaceta=EspecificacionLegal.objects.filter(
                                    tipo_especificacion__abreviacion='GO', 
                                    documento_asociado__abreviacion='IT', 
                                    tipo_pst=licencia.tipo_licenciaid 
                                ).first(),
                                tipo_pst=licencia.tipo_licenciaid,
                                cuadro_incumplimiento=tablas[1],
                                cuadro_incumplimiento_mya=tablas[2],
                                cuadro_porcentajes=tablas[0],
                                categorias=Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor'),
                                disposiciones=NotificacionDocumentoCompuesto.objects.filter(
                                    notificacion__solicitud=solicitud, 
                                    documento__tipo_documento_compuesto__abreviacion='ODM'
                                ).first().documento
                            )
                            generar_pdf.generar_pdf(
                                context=data,
                                ruta_template='documentos/oficios/oficio_cierre_por_incumplimiento.html',
                                ruta_documento=locationPath,
                                nombre_documento=nombre_documento
                            )

                            locationAttach = os.path.join(
                                locationPath,
                                nombre_documento + '.pdf'
                            )
                            attach_file = locationAttach
                        except Exception, e:
                            raise e
                        
                    except Exception, e:
                        raise e
                    

                        #try:
                        #    jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}

                    #dprint(jsontmp=jsontmp)
                    
                    #return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

                    
                    #<!---- Envio de Correo ---->    
                    """
                    htmly = get_template('correo/acepta_niega_categorizacion.html')
                    text_plain = get_template('correo/acepta_niega_categorizacion.txt')

                    context = Context({
                     'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                     'nombre_establecimiento': solicitud.pst.razon_social,
                     'direccion': direccionPST
                    })

                    attach_file = locationAttach
                    html_content = htmly.render(context)
                    text_content = text_plain.render(context)
                    
                    Busqueda de correo en parametros de configuracion
                    try:
                        corr = ParametroConfiguracion.objects.get(
                            clave="correo_interno"
                            )
                    except ParametroConfiguracion.DoesNotExist:
                        raise e
                    corrs = str(corr.valor)
                    

                    thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Resultados del proceso de categorización', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], attach_file, None))                
                    thread_correo.start()
                    """

                    #return  HttpResponse(status=200)

                elif op == 'negar':
                    estatus = Estatus.objects.get(abreviacion='SN')
                    notificacion= Notificacion(
                        emisor_id=int(id_sesion), 
                        receptor_id=solicitud.pst.user_id,
                        solicitud=solicitud,
                        estatus_actual=estatus,
                        observacion=request.POST['comentario-negarnoproc'] if request.POST['comentario-negarnoproc'] else ""
                    )
                    notificacion.save()
                    solicitud.estatus=estatus
                    solicitud.fecha_modificacion_estado=datetime.datetime.now()

                    texto = notificacion.observacion
                    r = re.sub('<br\s*?>', '\n',texto)
                    r = BeautifulSoup(r)

                    plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_no_procedente.html")
                    try:
                        #Creando el documento
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='ONP')
                        nombre_documento = "%s_oficio_no_procedente_%s_%s" % (
                            solicitud.pst.user.rif,
                            solicitud.id,
                            datetime.datetime.now().year
                        )

                        path = model_list.get_file_path(
                            solicitud.pst.user.rif,
                            'oficios',
                            "",
                        )

                        locationPath = os.path.join(
                            BASE_DIR,
                            'documents',
                            'files', 
                            path
                        )

                        oficio = Documento.objects.filter(nombre=nombre_documento).first()

                        if oficio:
                            oficio.fecha_emision=datetime.datetime.now()
                            oficio.eliminado=False
                        else:
                            data = Storage(
                                nombre=nombre_documento,
                                fecha_emision=datetime.datetime.now(),
                                plantilla_documento=plantilla,
                                ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                                extension = 'pdf',
                                tipo_documento_compuesto=tipo_documento,
                            )
                            oficio = Documento.create(data)
                        oficio.save()

                        #La notificacion respectiva a uno de los inspectores
                        ndc = NotificacionDocumentoCompuesto(
                            notificacion = notificacion,
                            documento = oficio
                        )
                        ndc.save()
                        try:
                            #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                            '''
                            direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                +str(direc.codigo_postal)
                            licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
                            '''
                            data = Storage(
                                nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                                oficio=oficio,
                                fecha=datetime.date.today(),
                                razon_social=solicitud.pst.razon_social,
                                direccion=direccionPST,
                                telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                                contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                                rtn=solicitud.pst.rtn,
                                fecha_apertura_solicitud=solicitud.fecha_apertura,
                                licencia=licencia.numero_licencia,
                                resolucion=EspecificacionLegal.objects.filter(
                                    tipo_especificacion__abreviacion='R', 
                                    documento_asociado__abreviacion='OP', 
                                    tipo_pst=licencia.tipo_licenciaid 
                                ).first(),
                                gaceta=EspecificacionLegal.objects.filter(
                                    tipo_especificacion__abreviacion='GO', 
                                    documento_asociado__abreviacion='OP', 
                                    tipo_pst=licencia.tipo_licenciaid 
                                ).first(),
                                observacion=r.get_text()
                            )
                            generar_pdf.generar_pdf(
                                context=data,
                                ruta_template=plantilla,
                                ruta_documento=locationPath,
                                nombre_documento=nombre_documento
                            )

                            locationAttach = os.path.join(
                                locationPath,
                                nombre_documento + '.pdf'
                            )
                            attach_file = locationAttach
                        except Exception, e:
                    
                            raise e
                        
                    except Exception, e:
                        raise e

                    jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                
                    #tabulador=RespuestaTabulador.objects.filter(pst_id=solicitud.pst_id)
                    #tabulador.delete()
                    '''
                    lic = LicenciaAsignada.objects.filter(usuario_pst=solicitud.pst.user, 
                        sucursal_id=solicitud.sucursal_id
                    ).first()
                    if lic:
                        dprint(lic=lic)
                        if solicitud.sucursal_id:
                            licencia = lic.numero_licencia
                            suc= solicitud.pst.denominacion_comercial
                            direccion = "%s, %s, %s, %s" %(solicitud.sucursal.urbanizacion, solicitud.sucursal.avenida_calle, solicitud.sucursal.edificio, solicitud.sucursal.oficina_apartamento)
                        else:
                            licencia = lic.numero_licencia
                            suc= "Sede Principal"
                            direccs = Registro_Direccion.objects.get(pst=solicitud.pst)
                            direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
                    '''
                    #TODO generar oficio de No procedencia
                    """
                    direccs = Registro_Direccion.objects.filter(pst=solicitud.pst).first()           
                    htmly = get_template('correo/acepta_niega_categorizacion.html')
                    text_plain = get_template('correo/acepta_niega_categorizacion.txt')

                    context = Context({
                     'nombre_pst': solicitud.pst.nombres+" "+solicitud.pst.apellidos,
                     'nombre_establecimiento': solicitud.pst.razon_social,
                     'direccion': "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
                    })

                    html_content = htmly.render(context)
                    text_content = text_plain.render(context)
                    
                    Busqueda de correo en parametros de configuracion
                    try:
                        corr = ParametroConfiguracion.objects.get(
                            clave="correo_interno"
                            )
                    except ParametroConfiguracion.DoesNotExist:
                        raise e
                    corrs = str(corr.valor)
                    

                    thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Resultados del proceso de categorización', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], None, None))                
                    thread_correo.start()


                    asignaciones = Asignacion.objects.filter(
                        solicitud_id=solicitud.id, asignacion_habilitada=True)
                    if asignaciones:
                        for n in asignaciones:
                            n.asignacion_habilitada=False
                            n.save()
                    solicitud.fecha_clausura=datetime.datetime.now()
                    solicitud.funcionario=None
                    """
                    
                    #return  HttpResponse(status=200)

                asignaciones = Asignacion.objects.filter(
                    solicitud_id=solicitud.id, asignacion_habilitada=True)
                if asignaciones:
                    for n in asignaciones:
                        n.asignacion_habilitada=False
                        n.save()

                solicitud.fecha_clausura=datetime.datetime.now()
                solicitud.funcionario=None
                solicitud.save()

                #<--- Envio de Correo --->
                htmly = get_template('correo/acepta_niega_categorizacion.html')
                text_plain = get_template('correo/acepta_niega_categorizacion.txt')

                context = Context({
                    'razon_social': solicitud.pst.razon_social,
                    'direccion': direccionPST,
                    'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                    'solicitud': solicitud
                 })

                html_content = htmly.render(context)
                text_content = text_plain.render(context)

                thread_correo = threading.Thread(
                    name='thread_correo', 
                    target=correo, 
                    args=(
                        u'[MINTUR] Resultados del proceso de categorización', 
                        html_content, 
                        text_content, 
                        'gccdev@cgtscorp.com', 
                        ['gccdev@cgtscorp.com'], 
                        attach_file, 
                        None
                    )
                )
                thread_correo.start()
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                """
                if op == 'negar':
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                else:
                    return  HttpResponse(status=200)
                """

        except Exception, e:
            raise e


class PstLibro(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(PstLibro, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):        
        try:
            user = request.user
            id_sesion = user.id
            if user.role == ROLE_PST:
                pst = user.pst_set.get()
            elif user.role == ROLE_FUNCIONARIO:
                funcionario = Funcionario.objects.get(user_id=int(id_sesion))           
            op = kwargs ['operacion']

            if op == 'municipios':
                if request.POST['estado']:
                    estado_id=request.POST['estado']
                    municipios={}
                    m= Municipio.objects.filter(estado_id=int(estado_id))
                    for x in m:
                        municipios.update({x.id:x.municipio})

                    jsontmp = {"municipios":municipios}
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'oficinas':
                municipio_id=request.POST['municipio']

                oficinas={}
                numero=0
                o= OficinaRegional.objects.filter(municipio_id=int(municipio_id))
                for x in o:
                    oficinas.update({x.id:x.nombre})
                    numero=numero+1

                jsontmp = {"oficinas":oficinas, "numero": numero}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'nuevasolicitud':
                sucursal_id=request.POST['sucursal']
                oficina_id=request.POST['oficina']
                if sucursal_id==0:
                    sucursal = None
                else:
                    sucursal = Sucursales.objects.get(id=int(sucursal_id))
                    
                oficina = OficinaRegional.objects.get(id=int(oficina_id)) 

                solicitud = SolicitudLibro(
                    estatus = Estatus.objects.get(abreviacion='PP'),
                    pst = pst,
                    sucursal = sucursal,
                    oficina = oficina,
                    fecha_realizacion = datetime.datetime.now(), 
                ) 

                solicitud.save()    
                return HttpResponseRedirect(reverse('bandeja_libro'))

            elif op == 'subircomprobante':
                try:
                    validacion = val(
                        request.FILES,
                        'comprobante-file',
                        ['application/pdf', 'image/jpeg', 'image/png'] ,
                        2621440
                    )
                    if validacion:
                        comprobante=int(request.POST['numero'])
                        solicitud_id=int(request.POST['solicitud'])
                        """
                        funcionario=algoritmo_asignacion.algoritmo_de_asignacion('analista')

                        asignacion = Asignacion(
                            funcionario_id = funcionario,
                            tipo_asignacion = TipoAsignacion.objects.get(abreviacion='LSR'), 
                            solicitud_libro_id = solicitud_id,
                            fecha_asignacion = datetime.datetime.now(),
                            asignacion_habilitada = True
                        )
                        asignacion.save()
                        """
                        
                        s = SolicitudLibro.objects.get(id = solicitud_id)

                        s.numero_comprobante = comprobante
                        s.estatus = Estatus.objects.get(abreviacion='CP')
                        #s.funcionario_id = int(funcionario)
                        s.archivo_comprobante = request.FILES['comprobante-file']
                        s.save()                       

                    else:
                        request.session['error'] = 'error'

                    return HttpResponseRedirect(reverse('bandeja_libro'))
                except Exception, e:
                   raise e

            elif op == 'comprobarfolio':

                try:
                    libro_id=int(request.POST['libro'])
                    try:
                        f= Folio.objects.filter(lsr_fisico__identificador=libro_id).order_by('-numero').first()  
                        folio= 1+int(f.numero)                 
                    except:
                        folio=1
                    jsontmp = {"folio":folio}
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

                except Exception, e:
                    raise e

            elif op == 'verfolios':
                if request.POST['libro']:
                    libro=request.POST['libro']
                    folios={}
                    f= Folio.objects.filter(lsr_fisico__identificador=int(libro))
                    for x in f:
                        if x.consignacion:
                            edicion="NO"
                        else:
                            edicion="SI"
                        folios.update({x.numero:[x.file_path.url, edicion]})

                    jsontmp = {"folios":folios}
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'subirfolio':
                try:
                    validacion = val(request.FILES,'folio-file',['application/pdf', 'image/jpeg', 'image/png'] ,2621440)
                    if validacion:
                        numero_folio=int(request.POST['folio'])
                        libro_id=int(request.POST['libro'])
                        libro= LsrFisico.objects.get(identificador=int(libro_id))

                        data = Storage(
                            file_path = request.FILES['folio-file'],
                            lsr_fisico = libro,
                            numero= numero_folio,
                            fecha_carga = datetime.datetime.now(),  
                            extension = str(request.FILES['folio-file']).split(".")[1],         
                        ) 
                        try:
                            f = Folio.objects.get(
                                numero = numero_folio, 
                                lsr_fisico= libro
                            )                 
                            f.lsr_fisico = data.lsr_fisico
                            f.file_path = data.file_path
                            f.fecha_carga = data.fecha_carga
                            f.extension = data.extension
                            f.numero = data.numero
                            f.save()

                        except Folio.DoesNotExist:
                            folio = Folio.create(data)
                            folio.save()
                    else:
                        request.session['error'] = 'error'

                    return HttpResponseRedirect(reverse('bandeja_libro'))
                except Exception, e:
                    raise e

            elif op == 'comprobar':
                try:
                    numero_comprobante=int(request.POST['comprobante'])

                    if SolicitudLibro.objects.filter(numero_comprobante=numero_comprobante).first():
                        error="Este número de comprobante ya esta registrado. Por favor, ingrese otro."
                        return  HttpResponse(error, content_type="application/json", status=400)
                    return HttpResponseRedirect(reverse('bandeja_libro'))
                except:
                    error="Este número de comprobante es inválido. Por favor, ingrese otro."
                    return  HttpResponse(error, content_type="application/json", status=400)

        except Exception, e:
            raise e


class MostrarSucursales(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(MostrarSucursales, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            user = request.user
            #id_sesion = user.id
            #natural = juridica = False
            #pst = user.pst_set.get() 

            sucursales={}
            su=sucursales_licencia(user)
            hay_sucursal= False
            for s in su:
                try:
                    Solicitud.objects.get(sucursal=s.sucursal, renovar=False)
                except:
                    try:
                        sucursales.update({s.sucursal.id:s.sucursal.nombre})
                    except:
                        sucursales.update({0:'Sede Principal'})
                    hay_sucursal =True
            if hay_sucursal:
                jsontmp = {
                    "err_msg":"",
                    "success":"Mostrando Sucursales",
                    "data":{
                        "sucursales":sucursales
                    }
                }
            else:
                jsontmp = {
                    "err_msg":"No hay sucursales sin solicitudes pendientes",
                    "success":""
                }
            return HttpResponse(
                json.dumps(jsontmp,sort_keys=True), 
                content_type="application/json", 
                status=200
            )

        except Exception, e:
            raise e


class FuncionarioLibro(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(FuncionarioLibro, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):   
        
        try:
            user = request.user
            id_sesion = user.id
            funcionario=Funcionario.objects.get(user_id=int(id_sesion))          
            op = kwargs ['operacion']
            
            if op == 'verfolios':
                if request.POST['libro']:
                    libro=request.POST['libro']
                    folios={}
                    f= Folio.objects.filter(lsr_fisico__identificador=int(libro))
                    for x in f:
                        folios.update({x.numero:x.file_path.url})

                    jsontmp = {"folios":folios}
                    return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif funcionario.tiporol.nombre == 'analista':

                if op == 'confirmarpago':
                    solicitud_id=request.POST['solicitud']

                    solicitud=SolicitudLibro.objects.get(id=int(solicitud_id))
                    solicitud.estatus=Estatus.objects.get(abreviacion='PC')
                    solicitud.save()
                    notificacion = Notificacion(
                        emisor_id=solicitud.pst.user.id,
                        receptor_id=funcionario.user.id,
                        solicitud_libro=solicitud,
                        fecha_emision=datetime.datetime.now(),
                        estatus_actual=solicitud.estatus
                    )
                    notificacion.save()

                    return HttpResponseRedirect(reverse('bandeja_libro'))

                elif op == 'confirmarentrega':
                    solicitud_id=request.POST['solicitud']
                    """
                    asig=Asignacion.objects.filter(
                        funcionario=funcionario, 
                        tipo_asignacion=TipoAsignacion.objects.get(abreviacion='LSR'), 
                        solicitud_libro_id=solicitud_id
                    ).first()
                    asig.asignacion_habilitada=False
                    asig.save()
                    """
                    funcionario2=algoritmo_asignacion.algoritmo_de_asignacion('coordinador_ct')
                    asignacion = Asignacion(
                        funcionario_id=funcionario2,
                        tipo_asignacion=TipoAsignacion.objects.get(abreviacion='LSR'), 
                        solicitud_libro_id=solicitud_id,
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                    )
                    asignacion.save()
                    solicitud=SolicitudLibro.objects.get(id=int(solicitud_id))
                    solicitud.estatus= Estatus.objects.get(abreviacion='E')
                    solicitud.funcionario_id=funcionario2
                    #Para indicar la fecha de culminacion de la solicitud para el uso del cron de folio
                    solicitud.fecha_culminacion= datetime.datetime.now() 
                    solicitud.save()

                    notificacion = Notificacion(
                        emisor_id=solicitud.pst.user.id,
                        receptor_id=funcionario.user.id,
                        solicitud_libro=solicitud,
                        fecha_emision=datetime.datetime.now(),
                        estatus_actual=solicitud.estatus
                    )
                    notificacion.save()
                    return HttpResponseRedirect(reverse('bandeja_libro'))

                elif op == 'asignarlibro':
                    try:
                        libro_id=request.POST['libro']
                        solicitud_id=request.POST['solicitud']

                        solicitud=SolicitudLibro.objects.get(id=int(solicitud_id))

                        if LsrFisico.objects.filter(identificador=int(libro_id)).first():
                            error="Este identificador de Libro ya esta registrado. Por favor, ingrese otro."
                            return  HttpResponse(error, content_type="application/json", status=400)
                        
                        libro = LsrFisico(
                            pst = solicitud.pst,
                            sucursal = solicitud.sucursal,
                            solicitud_libro = solicitud,
                            identificador= int(libro_id),         
                        ) 
                        libro.save()
                        solicitud.estatus=Estatus.objects.get(abreviacion='O')
                        solicitud.save()

                        notificacion = Notificacion(
                            emisor_id=solicitud.pst.user.id,
                            receptor_id=funcionario.user.id,
                            solicitud_libro=solicitud,
                            fecha_emision=datetime.datetime.now(),
                            estatus_actual=solicitud.estatus
                        )
                        notificacion.save()

                        jsontmp = {
                            "err_msg":"",
                            "success":"",
                            "data":{
                                "libro": libro.identificador
                            }
                        }

                        return  HttpResponse(
                            json.dumps(jsontmp,sort_keys=True), 
                            content_type="application/json", 
                        )
                        #return HttpResponseRedirect(reverse('bandeja_libro'))

                    except:
                    #except Exception, e:
                        #raise e
                        error="Este identificador de Libro es inválido. Por favor, ingrese otro."
                        return  HttpResponse(error, content_type="application/json", status=400)

                        
            elif funcionario.tiporol.nombre == 'coordinador_ct':

                if op == 'asignaranalista':
                    try:
                        dprint(request.POST['analista'])
                        solicitud_id=request.POST['solicitud']
                        dprint(solicitud_id)
                        solicitud=SolicitudLibro.objects.get(id=int(solicitud_id))
                        solicitud.funcionario_id=request.POST['analista']
                        solicitud.save()

                        notificacion = Notificacion(
                            emisor_id=funcionario.user.id,
                            receptor_id=solicitud.funcionario.user.id,
                            solicitud_libro=solicitud,
                            fecha_emision=datetime.datetime.now(),
                            estatus_actual=solicitud.estatus
                        )
                        notificacion.save()

                        jsontmp = {
                            "err_msg":"",
                            "success":"analista asignado"
                        }
                        return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                    except:
                        jsontmp = {
                            "err_msg":"Error asignando analista",
                            "success":""
                        }
                        return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=400)


        except Exception, e:
            raise e

#
############## DESARROLLO DE FIRMAS ELECTRONICAS ##################
#

class FirmaCompleta(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(FirmaCompleta, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST:
            json_firmar = json.loads(request.POST['json_firmar'])
            user = request.user
            id_sesion = user.id
            funcionario= Funcionario.objects.get(user_id=int(id_sesion))
            estats = {}    
            for k in json_firmar:
                try:
                    solicitud = Solicitud.objects.get(id=int(k))
                    notif_firma = Notificacion.objects.filter(solicitud=solicitud)
                    notif_compuesto = NotificacionDocumentoCompuesto.objects.filter(
                        notificacion__in=notif_firma
                    ).order_by('documento__fecha_emision')
                    for e in notif_compuesto:
                        condic = False
                        if e.documento.tipo_documento_compuesto.abreviacion in constants.OFICIOS_FIRMAS and e.documento.firmado == False:    
                            doc = e.documento
                            condicion = self.firmado_file(doc,json_firmar,k)
                            if condicion:
                                if solicitud.estatus.abreviacion == 'CG':
                                    asignacion = Asignacion.objects.get(
                                        funcionario__tiporol__nombre = 'coordinador_dif',
                                        solicitud = solicitud 
                                    )
                                    estatus= Estatus.objects.get(abreviacion='EI')
                                    inspect= Asignacion.objects.filter(
                                        solicitud=solicitud, 
                                        asignacion_habilitada=True, 
                                        funcionario__tiporol__nombre='inspector'
                                    ).values_list('funcionario')
                                    ins = [e[0] for e in inspect]
                                    inspectores= Funcionario.objects.filter(id__in=ins)

                                    notificacion= Notificacion(
                                        emisor_id=asignacion.funcionario.user.id, 
                                        receptor_id=inspectores[0].user_id, 
                                        solicitud_id=solicitud.id, 
                                        estatus_actual=estatus
                                    )

                                    notificacion1= Notificacion(
                                        emisor_id=asignacion.funcionario.user.id, 
                                        receptor_id=inspectores[1].user_id, 
                                        solicitud_id=solicitud.id, 
                                        estatus_actual=estatus
                                    )

                                    notificacion.save()
                                    notificacion1.save()

                                    doc.firmado = True
                                    doc.firmado_por = user
                                    doc.firmado_el = datetime.datetime.now()
                                    doc.coletillado = True
                                    doc.coletillado_el = datetime.datetime.now()
                                    doc.save()

                                    solicitud.estatus=estatus
                                    solicitud.funcionario_id = inspectores[0].id
                                    solicitud.funcionario_extra_id = inspectores[1].id
                                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                                    solicitud.save()
                                    estats.update({k:[estatus.nombre,estatus.descripcion]})

                                elif solicitud.estatus.abreviacion == 'DMG':
                                    asignacion = Asignacion.objects.get(
                                        funcionario__tiporol__nombre = 'coordinador_ct',
                                        solicitud = solicitud 
                                    )
                                    estatus=Estatus.objects.get(abreviacion='ER')

                                    #<--- Envio de Correo --->
                                    htmly = get_template('correo/aprobar_reparacion_prorroga.html')
                                    text_plain = get_template('correo/aprobar_reparacion_prorroga.txt')

                                    direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                    direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                    +str(direc.codigo_postal)
                                    licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

                                    context = Context({
                                        'razon_social': solicitud.pst.razon_social,
                                        'direccion': direccionPST,
                                        'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                                        'tipo_pst': licencia.tipo_licenciaid,
                                        'resolucion': EspecificacionLegal.objects.filter(
                                            tipo_especificacion__abreviacion='R', 
                                            documento_asociado__abreviacion='CDM', 
                                            tipo_pst=licencia.tipo_licenciaid 
                                        ).first(),
                                        'gaceta': EspecificacionLegal.objects.filter(
                                            tipo_especificacion__abreviacion='G', 
                                            documento_asociado__abreviacion='CDM', 
                                            tipo_pst=licencia.tipo_licenciaid 
                                        ).first(),
                                        'dias': ("%s(%d)" % (to_word(solicitud.dias_prorroga), solicitud.dias_prorroga)).lower()
                                    })

                                    html_content = htmly.render(context)
                                    text_content = text_plain.render(context)

                                    thread_correo = threading.Thread(
                                        name='thread_correo', 
                                        target=correo, 
                                        args=(
                                            u'[MINTUR] Disposiciones de Mejora', 
                                            html_content, 
                                            text_content, 
                                            'gccdev@cgtscorp.com', 
                                            ['gccdev@cgtscorp.com'], 
                                            None, 
                                            None
                                        )
                                    )
                                    thread_correo.start()

                                    notificacion = Notificacion(
                                        emisor_id=asignacion.funcionario.user.id,
                                        receptor=solicitud.pst.user,
                                        solicitud=solicitud,
                                        estatus_actual=estatus
                                    )
                                    notificacion.save()

                                    doc.firmado = True
                                    doc.firmado_por = user
                                    doc.firmado_el = datetime.datetime.now()
                                    doc.coletillado = True
                                    doc.coletillado_el = datetime.datetime.now()
                                    doc.save()

                                    solicitud.estatus=estatus
                                    solicitud.funcionario=None
                                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                                    solicitud.save()
                                    estats.update({k:[estatus.nombre,estatus.descripcion]})
                                elif solicitud.estatus.abreviacion == "RPG":
                                    asignacion = Asignacion.objects.get(
                                        funcionario__tiporol__nombre = 'coordinador_ct',
                                        solicitud = solicitud 
                                    )
                                    estatus=Estatus.objects.get(abreviacion='EP')
                                    
                                    direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                                    direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                    +str(direc.codigo_postal)

                                    #<--- Envio de Correo --->
                                    htmly = get_template('correo/aprobar_prorroga.html')
                                    text_plain = get_template('correo/aprobar_prorroga.txt')

                                    context = Context({
                                        'razon_social': solicitud.pst.razon_social,
                                        'direccion': direccionPST,
                                        'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first()
                                    })

                                    html_content = htmly.render(context)
                                    text_content = text_plain.render(context)

                                    thread_correo = threading.Thread(
                                        name='thread_correo', 
                                        target=correo, 
                                        args=(
                                            u'[MINTUR] Respuesta de solicitud de Prórroga', 
                                            html_content, 
                                            text_content, 
                                            'gccdev@cgtscorp.com', 
                                            ['gccdev@cgtscorp.com'], 
                                            None, 
                                            None
                                        )
                                    )
                                    thread_correo.start()

                                    notificacion = Notificacion(
                                        emisor_id=asignacion.funcionario.user.id,
                                        receptor=solicitud.pst.user,
                                        solicitud=solicitud,
                                        estatus_actual=estatus
                                    )
                                    notificacion.save()

                                    doc.firmado = True
                                    doc.firmado_por = user
                                    doc.firmado_el = datetime.datetime.now()
                                    doc.coletillado = True
                                    doc.coletillado_el = datetime.datetime.now()
                                    doc.save()


                                    solicitud.estatus=estatus
                                    solicitud.funcionario=None
                                    solicitud.fecha_modificacion_estado=datetime.datetime.now()
                                    solicitud.save()
                                    
                                    estats.update({k:[estatus.nombre,estatus.descripcion]})
                except Solicitud.DoesNotExist:
                    pass
            jsontmp = {
                "success": "Documento firmado correctamente",
                "data": {
                    "estados":estats 
                }
            }
            return  HttpResponse(json.dumps(
                jsontmp,sort_keys=True),
                content_type="application/json",
                status=200
            )

    def firmado_file(self, doc, json_firmar, k):
        src_file = settings.DOC_ELECTRONICOS_FIRMADOS_ROOT+'/'+json_firmar[k]
        dest_file = settings.DOC_ELECTRONICOS_FIRMADOS_ROOT+'/'+str(doc.nombre)+'.'+str(doc.extension)
        cond = cambio_nombre_file(src_file,dest_file)
        if cond:
            cond = eliminar_file(settings.DOC_ELECTRONICOS_SOLICITUDES_ROOT+'/'+json_firmar[k])
            hash_doc = obtener_hash_doc(json_firmar[k])
            aux_hash = ''
            i=0
            for i in range(0,len(hash_doc),4):
                aux_hash = aux_hash+'/'+hash_doc[i:i+4]

            aux_hash = settings.MEDIA_ROOT+aux_hash

            aux_ruta = str(doc.ruta_documento).split('/')
            aux_ruta.pop()
            aux_ruta = aux_ruta.pop()
            aux_hash = aux_hash+'/'+aux_ruta
            copied = copiar_file(dest_file,aux_hash)
            if copied:
                return eliminar_file(dest_file)
        return False

class FirmaScript(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(FirmaScript, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET:
            idd = int(request.GET['id'])
        try:
            solicitud = Solicitud.objects.get(id=idd)
            notif_firma = Notificacion.objects.filter(solicitud_id=idd)
            if notif_firma:
                notif_compuesto = NotificacionDocumentoCompuesto.objects.filter(
                    notificacion__in=notif_firma
                ).order_by('documento__fecha_emision')
                condicional = False
                for e in notif_compuesto:
                    if e.documento.tipo_documento_compuesto.abreviacion in constants.OFICIOS_FIRMAS and e.documento.firmado == False:    
                        condicional = True
                        funcionario = Funcionario.objects.get(id=solicitud.funcionario.id)
                        credencial = CredencialesOtorgadas.objects.get(user=funcionario.user)
                        asignacion = Asignacion.objects.filter(
                            solicitud=solicitud,
                            funcionario__tiporol__nombre='inspector',
                            asignacion_habilitada=True
                        )
                        if str(kwargs['tipo']) =='agregar':
                            dprint(doc=e.documento.id)
                            """
                            aux_doc = str(e.documento.ruta_documento)
                            aux_ruta = aux_doc.replace('/documents/',settings.MEDIA_ROOT+'/') 
                            cond = copiar_antes_firma(aux_ruta,settings.DOC_ELECTRONICOS_SOLICITUDES_ROOT, e.documento)
                            if cond:

                            cond = cond+'.'+str(e.documento.extension)
                            """
                            nombre_doc = cambio_nombre_doc(e.documento)
                            self.crear_documento(asignacion,solicitud,funcionario,credencial,nombre_doc,e.documento)

                            hay_oficio = False 
                            if solicitud.estatus.abreviacion == 'CG':
                                oficio = "oficio_credencial"
                                modulo = "categorizacion"
                                hay_oficio = True
                            elif solicitud.estatus.abreviacion == "DMG":
                                oficio = "oficio_disposicion_mejora"
                                modulo = "categorizacion"
                                hay_oficio= True
                            elif solicitud.estatus.abreviacion == "RPG":
                                oficio = "oficio_aprobacion_prorroga"
                                modulo = "categorizacion"
                                hay_oficio= True
                            if hay_oficio == True:
                                coords = constants.COORDENADAS_DOCUMENTOS[modulo][oficio]
                                jsontmp = {
                                    "success": "Documento copiado correctamente en carpeta solicitud de firma",
                                    "data":{
                                        "nombre_documento": nombre_doc+'.'+str(e.documento.extension),
                                        "oficio": solicitud.estatus.abreviacion,
                                        "coordenadas": coords["firma_electronica"]
                                    }
                                }
                                return  HttpResponse(json.dumps(
                                    jsontmp,sort_keys=True),
                                    content_type="application/json",
                                    status=200
                                )

                            jsontmp = {
                                "err_msg": "Imposible continuar con la firma del documento",
                            }
                            return  HttpResponse(json.dumps(
                                jsontmp,sort_keys=True),
                                content_type="application/json",
                                status=400
                            )
                        elif str(kwargs['tipo']) =='eliminar':
                            aux_ruta = settings.DOC_ELECTRONICOS_SOLICITUDES_ROOT
                            cond = eliminar_antes_firma(aux_ruta,e.documento)
                            if cond:
                                jsontmp = {
                                    "success": "Documento eliminado correctamente en carpeta temporal de firma",
                                    "nombre_documento": e.documento.nombre,
                                }
                                return  HttpResponse(json.dumps(
                                    jsontmp,sort_keys=True),
                                    content_type="application/json",
                                    status=200
                                )
                            else:
                                jsontmp = {
                                    "err_msg": "Imposible continuar con la firma del documento",
                                }
                                return  HttpResponse(json.dumps(
                                    jsontmp,sort_keys=True),
                                    content_type="application/json",
                                    status=400
                                )

                        break
                if condicional == False:
                    jsontmp = {
                        "err_msg": "No se encontraron documentos que requieran ser firmados",
                    }
                    return  HttpResponse(json.dumps(
                        jsontmp,sort_keys=True),
                        content_type="application/json",
                        status=400
                    )

        except Solicitud.DoesNotExist:
            pass   

    def crear_documento(self,asignacion,solicitud,funcionario,credencial,nombre_documento,documento):

        #plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_de_disposiciones_de_mejora.html")

        plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_respuesta_solicitud_de_prorroga.html")

        if solicitud.estatus.abreviacion == "CG":
            tipoInspector = TipoAsignacion.objects.get(abreviacion='I')    
            inspectores = Asignacion.objects.filter(
                solicitud=solicitud,asignacion_habilitada=True,
                tipo_asignacion=tipoInspector
            )
            coordinador_dif = Asignacion.objects.get(
                solicitud=solicitud,asignacion_habilitada=True,
                funcionario__tiporol__nombre='coordinador_dif'
            ).funcionario
        elif solicitud.estatus.abreviacion == "DMG":
            licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
        try:
            #Creando el documento
            try:
                #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO

                direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                    +str(direc.codigo_postal)
                if solicitud.estatus.abreviacion == "CG":
                    ruta_temp = 'documentos/oficios/credencial.html'
                    data = Storage(
                        nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                        oficio=credencial,
                        fecha=datetime.date.today(),
                        razon_social=solicitud.pst.razon_social,
                        direccion=direccionPST,
                        telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                        inspector1=inspectores[0].funcionario,
                        inspector2=inspectores[1].funcionario if len(inspectores)>1 else "",
                        coletilla=credencial.coletilla
                    )
                elif solicitud.estatus.abreviacion == "DMG":
                    tablas=dt_tablas_it(solicitud)
                    ruta_temp = 'documentos/oficios/oficio_de_disposiciones_de_mejora.html'
                    data = Storage(
                        nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                        oficio=documento,
                        fecha=datetime.date.today(),
                        razon_social=solicitud.pst.razon_social,
                        direccion=direccionPST,
                        telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                        contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                        fecha_inspeccion=Notificacion.objects.filter(
                            estatus_actual__abreviacion='RI',
                            solicitud=solicitud).order_by('-fecha_emision').first().fecha_emision,
                        rtn=solicitud.pst.rtn,
                        dias= ("%s(%d) días" % (to_word(solicitud.dias_prorroga), solicitud.dias_prorroga)).lower(),
                        licencia=licencia.numero_licencia,
                        resolucion=EspecificacionLegal.objects.filter(
                            tipo_especificacion__abreviacion='R', 
                            documento_asociado__abreviacion='IT', 
                            tipo_pst=licencia.tipo_licenciaid 
                        ).first(),
                        gaceta=EspecificacionLegal.objects.filter(
                            tipo_especificacion__abreviacion='GO', 
                            documento_asociado__abreviacion='IT', 
                            tipo_pst=licencia.tipo_licenciaid 
                        ).first(),
                        tipo_pst=licencia.tipo_licenciaid,
                        cuadro_incumplimiento=tablas[1],
                        cuadro_incumplimiento_mya=tablas[2],
                        cuadro_porcentajes=tablas[0],
                        categorias=Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor'),
                        coletilla=credencial.coletilla
                    )
                elif solicitud.estatus.abreviacion == "RPG":
                    ruta_temp = 'documentos/oficios/oficio_respuesta_solicitud_de_prorroga.html'                   
                    data = Storage(
                        nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                        oficio=documento,
                        fecha=datetime.date.today(),
                        razon_social=solicitud.pst.razon_social,
                        direccion=direccionPST,
                        telefono=solicitud.pst.telefono_fijo if solicitud.pst.telefono_fijo else "" + " / " + solicitud.pst.telefono_celular if solicitud.pst.telefono_celular else "",
                        contacto=RepresentanteContacto.objects.filter(pst=solicitud.pst).first(),
                        dias=("%s(%d) días" % (to_word(solicitud.dias_prorroga), solicitud.dias_prorroga)).lower(),
                        coletilla=credencial.coletilla
                    )

                generar_pdf.generar_pdf(
                    context=data,
                    ruta_template=ruta_temp,
                    ruta_documento=settings.DOC_ELECTRONICOS_SOLICITUDES_ROOT,
                    nombre_documento=nombre_documento
                )
            except Exception, e:
                dprint("Hubo errores creando el documento")
                raise e
        except Exception, e:
            dprint("Hubo errores haciendo las notificaciones")
            raise e

            

#
#################  HASTA AQUI LLEGA FIRMAS ###################
#

class OficioPlaca(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(OficioPlaca, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            licencia=LicenciaAsignada.objects.get(numero_licencia=int(request.GET['licencia']))
            pst=Pst.objects.get(user=licencia.usuario_pst)
            viceministro=Funcionario.objects.filter(tiporol__nombre='viceministro').first()

            if licencia.tipo_licenciaid.codigo == 'LIC_TRANS_T' or licencia.tipo_licenciaid.padre.codigo == 'LIC_TRANS_T':
                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/placa_sin_diseño.html")
                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OPSD')
                nombre_documento = "%s_oficio_placa_sin_diseno_%s_%s" % (
                    pst.rif,
                    licencia.sucursal.id,
                    licencia.numero_licencia
                )
                path = model_list.get_file_path(
                    pst.user.rif,
                    "",
                    'placas',
                )

                locationPath = os.path.join(
                    BASE_DIR,
                    'documents',
                    'files', 
                    path
                )

                try: 
                    oficio = Documento.objects.get(nombre=nombre_documento)
                    oficio.fecha_aprobacion=datetime.datetime.now()
                    oficio.eliminado=False
                    oficio.save()
                    
                except:                                        
                    data = Storage(
                        nombre=nombre_documento,
                        fecha_aprobacion=licencia.fecha_renovacion if licencia.fecha_renovacion else licencia.fecha_emision,
                        plantilla_documento=plantilla,
                        ruta_documento = '/documents/' + path + nombre_documento +'.pdf',
                        extension = 'pdf',
                        tipo_documento_compuesto=tipo_documento,
                    )

                    oficio = Documento.create(data)
                    oficio.save()

                    try:

                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        
                        data = Storage(
                            nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                            oficio=oficio,
                            fecha=datetime.date.today(),
                            razon_social=pst.razon_social,
                            direccion=direccionPST,
                            telefono=pst.telefono_fijo if pst.telefono_fijo else "" + " / " + pst.telefono_celular if pst.telefono_celular else "",
                            contacto=RepresentanteContacto.objects.filter(pst=pst).first(),
                            rtn=pst.rtn,
                            licencia=licencia.numero_licencia,
                            resolucion=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='R', 
                                documento_asociado__abreviacion='OPSD', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            gaceta=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='GO', 
                                documento_asociado__abreviacion='OPSD', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            tipo_pst=licencia.tipo_licenciaid
                        )
                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficio_placa_para_transporte.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                    except Exception, e:
                        raise e
            elif licencia.tipo_licenciaid.padre.codigo == 'LIC_ALO_T':
                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/placa_autorizacion.html")
                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OPA')
                nombre_documento = "%s_oficio_placa_autorizacion_%s_%s" % (
                    pst.rif,
                    licencia.sucursal.id,
                    licencia.numero_licencia
                )
                path = model_list.get_file_path(
                    pst.user.rif,
                    "",
                    'placas',
                )

                locationPath = os.path.join(
                    BASE_DIR,
                    'documents',
                    'files', 
                    path
                )

                try: 
                    oficio = Documento.objects.get(nombre=nombre_documento)
                    oficio.fecha_aprobacion=datetime.datetime.now()
                    oficio.eliminado=False
                    oficio.save()
                    
                except:                                        
                    data = Storage(
                        nombre=nombre_documento,
                        fecha_aprobacion=licencia.fecha_renovacion if licencia.fecha_renovacion else licencia.fecha_emision,
                        plantilla_documento=plantilla,
                        ruta_documento = '/documents/' + path + nombre_documento +'.pdf',
                        extension = 'pdf',
                        tipo_documento_compuesto=tipo_documento,
                    )

                    oficio = Documento.create(data)
                    oficio.save()

                    try:

                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        
                        data = Storage(
                            nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                            oficio=oficio,
                            fecha=datetime.date.today(),
                            razon_social=pst.razon_social,
                            direccion=direccionPST,
                            telefono=pst.telefono_fijo if pst.telefono_fijo else "" + " / " + pst.telefono_celular if pst.telefono_celular else "",
                            contacto=RepresentanteContacto.objects.filter(pst=pst).first(),
                            rtn=pst.rtn,
                            licencia=licencia.numero_licencia,
                            resolucion=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='R', 
                                documento_asociado__abreviacion='OPA', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first(),
                            gaceta=EspecificacionLegal.objects.filter(
                                tipo_especificacion__abreviacion='GO', 
                                documento_asociado__abreviacion='OPA', 
                                tipo_pst=licencia.tipo_licenciaid 
                            ).first()
                        )
                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficio_placa_para_transporte.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                    except Exception, e:
                        raise e
            """
            elif licencia.solicitud_licenciaid.estatus_solicitudid.codigo == 'EST_APROB' and licencia.estatus == 1:

                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficio_placa.html")
                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OP')
                nombre_documento = "%s_oficio_placa_%s_%s" % (
                    pst.rif,
                    licencia.sucursal.id,
                    licencia.numero_licencia
                )
                path = model_list.get_file_path(
                    pst.user.rif,
                    "",
                    'placas',
                )

                locationPath = os.path.join(
                    BASE_DIR,
                    'documents',
                    'files', 
                    path
                )

                try: 
                    oficio = Documento.objects.get(nombre=nombre_documento)
                    oficio.fecha_aprobacion=datetime.datetime.now()
                    oficio.eliminado=False
                    oficio.save()
                    
                except:                                        
                    data = Storage(
                        nombre=nombre_documento,
                        fecha_aprobacion=licencia.fecha_renovacion if licencia.fecha_renovacion else licencia.fecha_emision,
                        plantilla_documento=plantilla,
                        ruta_documento = '/documents/' + path + nombre_documento +'.pdf',
                        extension = 'pdf',
                        tipo_documento_compuesto=tipo_documento,
                    )

                    oficio = Documento.create(data)
                    oficio.save()
                    

                    if licencia.tipo_licenciaid.padre.codigo == 'LIC_ALO_T':
                        notificacion=Notificacion.objects.filter(
                            solicitud__sucursal=licencia.sucursal, 
                            solicitud__pst=pst,
                            estatus_actual__abreviacion='A').order_by('-fecha_emision').first()
                        if notificacion:
                            ndc = NotificacionDocumentoCompuesto(
                                notificacion = notificacion,
                                documento = oficio
                            )
                            ndc.save()
                        else:
                            notificacion_backup=NotificacionBackup.objects.filter(
                                solicitud__sucursal=licencia.sucursal,
                                solicitud__pst=pst,
                                estatus_actual__abreviacion='A').order_by('-fecha_emision').first()
                            if notificacion_backup:
                                ndc = NotificacionDocumentoCompuesto(
                                    notificacion_backup = notificacion_backup,
                                    documento = oficio
                                )
                                ndc.save()
                    
                    try:

                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        #TODO: actualizar las imagenes cuando las envie Mintur y validar por cod no por nombre
                        especificaciones=""
                        if licencia.tipo_licenciaid.nombre =="Hotel de Turismo":
                            especificaciones="static/img/placas/tipoHotel.jpg"
                        elif licencia.tipo_licenciaid.nombre =="Posada de Turismo":
                            especificaciones="static/img/placas/tipoPosada.jpg"
                        elif licencia.tipo_licenciaid.nombre =="Campamento de Turismo":
                            especificaciones="static/img/placas/tipoCampamento.jpg"
                        elif licencia.tipo_licenciaid.nombre =="Hotel Turismo Internacional":
                            especificaciones="static/img/placas/tipoHotel.jpg"
                        
                        data = Storage(
                            nombre_establecimiento=pst.razon_social,
                            direccion=direccionPST,
                            nombre_pst=pst.nombres + " " + pst.apellidos,
                            tipo_pst=licencia.tipo_licenciaid.nombre,
                            rtn = pst.rtn,
                            especificaciones=especificaciones,
                            licencia = licencia.numero_licencia,
                            telefonos = str(pst.telefono_celular) + " / "\
                                +str(pst.telefono_fijo),
                            viceministro=viceministro.nombre + " " + viceministro.apellido,
                            fecha=oficio.fecha_aprobacion
                        )
                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficio_placa.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                    except Exception, e:
                        raise e
            elif licencia.solicitud_licenciaid.estatus_solicitudid.codigo == 'EST_APROB' and licencia.estatus == 3:
                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficio_placa_licencia_vencida.html")
                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OPLV')
                nombre_documento = '%s_oficio_placa_licencia_vencida_%s_%s' % (
                    pst.rif,
                    licencia.sucursal.id,
                    licencia.numero_licencia
                )
                path = model_list.get_file_path(
                    pst.user.rif,
                    "",
                    'placas',
                )

                locationPath = os.path.join(
                    BASE_DIR,
                    'documents',
                    'files', 
                    path
                )

                try: 
                    oficio = Documento.objects.get(nombre=nombre_documento)
                    oficio.fecha_aprobacion=datetime.datetime.now()
                    oficio.eliminado=False
                    oficio.save()
                    
                except:                                        
                    data = Storage(
                        nombre=nombre_documento,
                        fecha_aprobacion=licencia.fecha_vencimiento,
                        plantilla_documento=plantilla,
                        ruta_documento = '/documents/' + path + nombre_documento +'.pdf',
                        extension = 'pdf',
                        tipo_documento_compuesto=tipo_documento,
                    )

                    oficio = Documento.create(data)
                    oficio.save()
                    

                    if licencia.tipo_licenciaid.padre.codigo == 'LIC_ALO_T':
                        notificacion=Notificacion.objects.filter(
                            solicitud__sucursal=licencia.sucursal, 
                            solicitud__pst=pst,
                            estatus_actual__abreviacion='A').order_by('-fecha_emision').first()
                        if notificacion:
                            ndc = NotificacionDocumentoCompuesto(
                                notificacion = notificacion,
                                documento = oficio
                            )
                            ndc.save()
                        else:
                            notificacion_backup=NotificacionBackup.objects.filter(
                                solicitud__sucursal=licencia.sucursal,
                                solicitud__pst=pst,
                                estatus_actual__abreviacion='A').order_by('-fecha_emision').first()
                            if notificacion_backup:
                                ndc = NotificacionDocumentoCompuesto(
                                    notificacion_backup = notificacion_backup,
                                    documento = oficio
                                )
                                ndc.save()
                    

                    try:

                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        
                        data = Storage(
                            nombre_establecimiento=pst.razon_social,
                            direccion=direccionPST,
                            nombre_pst=pst.nombres + " " + pst.apellidos,
                            rtn = pst.rtn,
                            tipo_pst = licencia.tipo_licenciaid.nombre,
                            licencia = licencia.numero_licencia,
                            telefonos = str(pst.telefono_celular) + " / "\
                                +str(pst.telefono_fijo),
                            viceministro=viceministro.nombre + " " + viceministro.apellido,
                            fecha=oficio.fecha_aprobacion
                        )
                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficio_placa_licencia_vencida.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                    except Exception, e:
                        raise e
            else:
                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficio_placa_sin_licencia.html")
                tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OPSL')
                nombre_documento = "%s_oficio_placa_sin_licencia_%s_%s" % (
                    pst.rif,
                    licencia.sucursal.id,
                    licencia.numero_licencia
                )
                path = model_list.get_file_path(
                    pst.user.rif,
                    "",
                    'placas',
                )

                locationPath = os.path.join(
                    BASE_DIR,
                    'documents',
                    'files', 
                    path
                )

                try: 
                    oficio = Documento.objects.get(nombre=nombre_documento)
                    oficio.fecha_aprobacion=datetime.datetime.now()
                    oficio.eliminado=False
                    oficio.save()
                    
                except:                                        
                    data = Storage(
                        nombre=nombre_documento,
                        fecha_aprobacion=datetime.datetime.now(),
                        plantilla_documento=plantilla,
                        ruta_documento = '/documents/' + path + nombre_documento +'.pdf',
                        extension = 'pdf',
                        tipo_documento_compuesto=tipo_documento,
                    )

                    oficio = Documento.create(data)
                    oficio.save()
                    

                    if licencia.tipo_licenciaid.padre.codigo == 'LIC_ALO_T':
                        notificacion=Notificacion.objects.filter(
                            solicitud__sucursal=licencia.sucursal, 
                            solicitud__pst=pst,
                            estatus_actual__abreviacion='A').order_by('-fecha_emision').first()
                        if notificacion:
                            ndc = NotificacionDocumentoCompuesto(
                                notificacion = notificacion,
                                documento = oficio
                            )
                            ndc.save()
                        else:
                            notificacion_backup=NotificacionBackup.objects.filter(
                                solicitud__sucursal=licencia.sucursal,
                                solicitud__pst=pst,
                                estatus_actual__abreviacion='A').order_by('-fecha_emision').first()
                            if notificacion_backup:
                                ndc = NotificacionDocumentoCompuesto(
                                    notificacion_backup = notificacion_backup,
                                    documento = oficio
                                )
                                ndc.save()
                    
                    try:

                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        
                        data = Storage(
                            nombre_establecimiento=pst.razon_social,
                            direccion=direccionPST,
                            nombre_pst=pst.nombres + " " + pst.apellidos,
                            rtn = pst.rtn,
                            tipo_pst=licencia.tipo_licenciaid.nombre,
                            licencia = licencia.numero_licencia,
                            telefonos = str(pst.telefono_celular) + " / "\
                                +str(pst.telefono_fijo),
                            viceministro=viceministro.nombre + " " + viceministro.apellido,
                            fecha=oficio.fecha_aprobacion
                        )
                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficio_placa_sin_licencia.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )
                    except Exception, e:
                        raise e
            """
            placa=Placa.objects.get(licencia_asignada=licencia)
            placa.documento=oficio
            placa.save()

            jsontmp = {
                "success": "Pagina encontrada",
                "ruta": str(oficio.ruta_documento),
                "firmado": oficio.firmado
            }
            return  HttpResponse(json.dumps(
                jsontmp,sort_keys=True),
                content_type="application/json",
                status=200
            )
        except Exception, e:
            jsontmp = {
                "err_msg": e,
                "success": "",
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )
"""
    def get(self, request, *args, **kwargs):
        solicitud_id = kwargs ['id']
        pst_id = int(request.user.pk)
        solicitud = Solicitud.objects.get(id= int(solicitud_id))
        #estado = Estatus.objects.filter(abreviacion='A')
        #notificacion = Notificacion.objects.get(solicitud=solicitud,estatus_anterior=estado)
        notificacion = Notificacion.objects.filter(solicitud=solicitud).first()

        plantilla = PlantillaDocumento.objects.get(formato="viceministro/oficios/oficio-placa.html")
        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OP')
        nombre_documento = "%s_oficio_placa_%s" % (
            solicitud.pst.rif,
            solicitud.id
        )
        path = get_pst_file_path(notificacion,"")
        locationPath ='documents/files/'+ path

        oficio = Documento.objects.filter(nombre=nombre_documento).first()

        if oficio:
            oficio.fecha_aprobacion=datetime.datetime.now()
            oficio.save()
            #La notificacion respectiva al documento
            ndc = NotificacionDocumentoCompuesto.objects.filter(
                notificacion=notificacion,
                documento=oficio
            ).last()
            
        else:                                        
            data = Storage(
                nombre=nombre_documento,
                fecha_aprobacion=datetime.datetime.now(),
                plantilla_documento=plantilla,
                ruta_documento = '/documents/' + path + nombre_documento+'.pdf',
                extension = 'pdf',
                tipo_documento_compuesto=tipo_documento,
            )

            oficio = Documento.create(data)
            oficio.save()
            #La notificacion respectiva al documento
            ndc = NotificacionDocumentoCompuesto(
                notificacion = notificacion,
                documento = oficio
            )
            ndc.save()
            try:

                #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                direc = Registro_Direccion.objects.get(pst=solicitud.pst)
                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                    +str(direc.codigo_postal)
                lestatus = EstatusSolicitud.objects.get(codigo = 'EST_APROB')
                lpadre = TipoLicencia.objects.get(
                    codigo = 'LIC_ALO_T'
                )
                lsolicitudes = SolicitudLicencia.objects.filter(
                    sucursal = solicitud.sucursal,
                    estatus_solicitudid=lestatus,
                    tipo_licenciaid__padre=lpadre
                )
                rutas_licencias = []
                for lic in lsolicitudes:
                    if lic.tipo_licenciaid.nombre =="Hotel de Turismo":
                        rutas_licencias.append("static/img/placas/tipoHotel.jpg")
                    elif lic.tipo_licenciaid.nombre =="Posada de Turismo":
                        rutas_licencias.append("static/img/placas/tipoPosada.jpg")
                    elif lic.tipo_licenciaid.nombre =="Campamento de Turismo":
                        rutas_licencias.append("static/img/placas/tipoCampamento.jpg")
                    elif lic.tipo_licenciaid.nombre =="Hotel Turismo Internacional":
                        rutas_licencias.append("static/img/placas/tipoHotel.jpg")
                dprint(rutas_licencias)
                data = Storage(
                    pagesize='A4',
                    nombre_establecimiento=solicitud.pst.denominacion_comercial,
                    direccion=direccionPST,
                    nombre_pst=solicitud.pst.nombres + " " + solicitud.pst.apellidos,
                    rtn = solicitud.pst.rtn,
                    rutas_licencias = rutas_licencias,
                    licencia = "",
                    #nombre_funcionario = solicitud.funcionario.nombre\
                    #    +" "+ solicitud.funcionario.apellido,
                    telefonos = str(solicitud.pst.telefono_celular) + " / "\
                        +str(solicitud.pst.telefono_fijo),
                )
                generar_pdf.generar_pdf(
                    context=data,
                    ruta_template='viceministro/oficios/oficio-placa.html',
                    ruta_documento=locationPath,
                    nombre_documento=nombre_documento
                )
            except Exception, e:
                raise e
        
        jsontmp = {
            "err_msg": "",
            "success": "Pagina encontrada",
            "ruta_documento": str(oficio.ruta_documento)
        }

        return  HttpResponse(json.dumps(
            jsontmp,sort_keys=True),
            content_type="application/json",
            status=200
        )
"""

class Reconsideracion(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(Reconsideracion, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            s_id = request.POST['solicitud']
            dprint(s_id)
            
            ultima_notificacion=Notificacion.objects.filter(
                solicitud__id=s_id
                ).order_by('-fecha_emision').first()
            dprint(ultima_notificacion)
            
            if not request.POST.has_key('comentario-recon'):
                #observacion="No se han registrado observaciones"
                observacion=ultima_notificacion.observacion
            else:
                observacion=request.POST['comentario-recon']

            solicitud = Solicitud.objects.get(id=s_id)
            
            dprint(solicitud.funcionario)
            #tiporol = request.POST['tiporol']
            #tiporol = "coordinador_ct"
            """inspector = Asignacion.objects.filter(
                solicitud=solicitud,
                asignacion_habilitada=True
            ).first()
            #El pst solicita la reconsideracion
            """
            
            if not solicitud.funcionario:
                dprint("#####1")
                pst_id = int(request.user.pk)
                coordinador_id = algoritmo_asignacion.algoritmo_de_asignacion('coordinador_ct')
                dprint("#####2")
                estatus = Estatus.objects.get(abreviacion='RS')
                dprint("#####3")
                solicitud.estatus = estatus
                dprint("#####4")
                solicitud.funcionario_id = coordinador_id
                dprint("#####5")
                solicitud.save()
                tipoasig = TipoAsignacion.objects.get(abreviacion='C')
                asignacion = Asignacion(
                    funcionario_id=coordinador_id,
                    tipo_asignacion=tipoasig,
                    solicitud=solicitud
                )
                asignacion.save()
                notificacion = Notificacion(
                    emisor_id=pst_id,
                    receptor_id=asignacion.funcionario.user.id,
                    solicitud=solicitud,
                    fecha_emision=datetime.datetime.now(),
                    observacion=observacion,
                    estatus_actual=solicitud.estatus
                )
                notificacion.save()
                return HttpResponse(status=200)
            elif solicitud.funcionario.tiporol.nombre == 'coordinador_ct':
                op = request.POST['op']
                if op == 'aprobar':
                    estatus=Estatus.objects.get(abreviacion='PAA')
                    receptor=int(request.user.pk)
                elif op == 'negar':
                    solicitud.funcionario=None
                    ultima_notificacion=Notificacion.objects.filter(
                        solicitud__id=s_id,
                        receptor__id=solicitud.pst.id
                        ).order_by('-fecha_emision').first()
                    estatus=ultima_notificacion.estatus_actual
                    asignaciones = Asignacion.objects.filter(
                        solicitud=solicitud,
                        asignacion_habilitada=True
                    )
                    for asig in asignaciones:
                        asig.asignacion_habilitada=False
                        asig.save()
                    receptor=solicitud.pst.id
                coordinador_id = int(request.user.pk)
                solicitud.estatus = estatus
                solicitud.save()
                """director_id = algoritmo_asignacion.algoritmo_de_asignacion('director_ct')
                solicitud.funcionario_id = director_id
                solicitud.save()
                tipoasig = TipoAsignacion.objects.get(abreviacion='D')
                asignacion = Asignacion(
                    funcionario_id=director_id,
                    tipo_asignacion=tipoasig,
                    solicitud=solicitud
                )
                asignacion.save()
                """
                notificacion = Notificacion(
                    emisor_id=coordinador_id,
                    receptor_id=receptor,
                    solicitud=solicitud,
                    fecha_emision=datetime.datetime.now(),
                    estatus_actual=estatus
                )
                notificacion.save()

                return HttpResponse(status=200)
            """elif tiporol == 'director_ct' and inspector:
                director_id = int(request.user.pk)
                viceministro_id = algoritmo_asignacion.algoritmo_de_asignacion('viceministro')
                solicitud.funcionario_id = viceministro_id
                solicitud.save()
                tipoasig = TipoAsignacion.objects.get(abreviacion='V')
                asignacion = Asignacion(
                    funcionario_id=viceministro_id,
                    tipo_asignacion=tipoasig,
                    solicitud=solicitud
                )
                asignacion.save()
                notificacion = Notificacion(
                    emisor_id=director_id,
                    receptor_id=asignacion.funcionario.user.id,
                    solicitud=solicitud,
                    fecha_emision=datetime.datetime.now(),
                    estatus_actual=solicitud.estatus
                )
                notificacion.save()
                return HttpResponse(status=200)
            elif tiporol == 'viceministro':
                op = request.POST['op']
                if op == 'aprobar':
                    obs = "La solicitud de reconsideración fue aprobada."
                else:
                    obs = "La solicitud de reconsideración fue negada."
                viceministro_id = int(request.user.pk)
                estatus = Estatus.objects.get(abreviacion='A')
                solicitud.estatus = estatus
                solicitud.funcionario_id = None
                solicitud.save()
                notificacion = Notificacion(
                    emisor_id=viceministro_id,
                    receptor_id=solicitud.pst.user.id,
                    solicitud=solicitud,
                    fecha_emision=datetime.datetime.now(),
                    observacion=obs,
                    estatus_actual=estatus
                )
                notificacion.save()
                asignaciones = Asignacion.objects.filter(
                    solicitud=solicitud,
                    asignacion_habilitada=True
                )
                for asig in asignaciones:
                    asig.asignacion_habilitada=False
                    asig.save()

                return HttpResponse(status=200)
            """
        except Exception, e:
            return HttpResponse(str(e), status=400)

        
class BusquedaAvanzada(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(BusquedaAvanzada, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        
        if request.GET['bandeja'] == 'categorizacion_bandeja' or request.GET['bandeja']=='categorizacion_reporte' or request.GET['bandeja']=='historial_prestador' or request.GET['bandeja'] == 'procesos_bandeja':
            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{},
            }
            if user.role == ROLE_PST:
                pst = Pst.objects.get(user=user)
                solicitudes = Solicitud.objects.filter(pst=pst)
                estados= [e.estatus.abreviacion for e in solicitudes]
                estatus1 =[]
                estatus_pst = constants.ESTATUS_PST
                for e in estados:
                    for key,value in estatus_pst.items():
                        if e in value:
                            estatus1.append(key)

            elif user.role == ROLE_FUNCIONARIO:

                funcionarios = Funcionario.objects.filter(user_id=user.id).first()
                if request.GET['bandeja'] == 'categorizacion_reporte':
                    solicitudes = Solicitud.objects.all().distinct('sucursal')
                elif request.GET['bandeja'] == 'categorizacion_bandeja':
                    asignaciones = Asignacion.objects.filter(
                        funcionario=funcionarios, 
                        asignacion_habilitada=True
                    ).exclude(tipo_asignacion__abreviacion='LSR')
                    asignacion = [e.solicitud_id for e in asignaciones]
                    solicitudes = Solicitud.objects.filter(id__in=asignacion)
                else:
                    solicitudes = Solicitud.objects.all()

                solicituds = [e.id for e in solicitudes]
                estatus1= [e.estatus.nombre for e in solicitudes]
                analistax = coordinador_ctx = director_ctx = inspectorx = viceministrox =[]
                if request.GET['bandeja'] == 'historial_prestador' or request.GET['bandeja'] == 'procesos_bandeja':
                    asig_func = Asignacion.objects.filter(Q(solicitud_id__in=solicituds) 
                        & Q(asignacion_habilitada=True)
                        & (Q(funcionario__tiporol__nombre='analista')
                            | Q(funcionario__tiporol__nombre='inspector')
                            | Q(funcionario__tiporol__nombre='coordinador_ct')
                            | Q(funcionario__tiporol__nombre='director_ct')));
                    analistax=algoritmo_asignacion.array_de_funcionarios(asig_func,'analista')
                    inspectorx=algoritmo_asignacion.array_de_funcionarios(asig_func,'inspector')
                    coordinador_ctx=algoritmo_asignacion.array_de_funcionarios(asig_func,'coordinador_ct')
                    director_ctx= algoritmo_asignacion.array_de_funcionarios(asig_func,'director_ct')
                elif funcionarios.tiporol.nombre=='coordinador_ct':
                    asig_func = Asignacion.objects.filter(Q(solicitud_id__in=solicituds)
                        & Q(asignacion_habilitada=True) 
                        & Q(funcionario__tiporol__nombre='analista'))
                    analistax=algoritmo_asignacion.array_de_funcionarios(asig_func,'analista')

                elif funcionarios.tiporol.nombre=='coordinador_dif':
                    asig_func = Asignacion.objects.filter(Q(solicitud_id__in=solicituds)
                        & Q(asignacion_habilitada=True) 
                        & Q(funcionario__tiporol__nombre='inspector'))
                    inspectorx=algoritmo_asignacion.array_de_funcionarios(asig_func,'inspector')
                    
                elif funcionarios.tiporol.nombre=='director_ct':
                    asig_func = Asignacion.objects.filter(Q(solicitud_id__in=solicituds)
                        & Q(asignacion_habilitada=True) 
                        & (Q(funcionario__tiporol__nombre='analista')
                            | Q(funcionario__tiporol__nombre='coordinador_ct')))
                    analistax=algoritmo_asignacion.array_de_funcionarios(asig_func,'analista')
                    coordinador_ctx=algoritmo_asignacion.array_de_funcionarios(asig_func,'coordinador_ct') 

                elif funcionarios.tiporol.nombre=='viceministro':
                    asig_func = Asignacion.objects.filter(Q(solicitud_id__in=solicituds) 
                        & Q(asignacion_habilitada=True)
                        & (Q(funcionario__tiporol__nombre='analista') 
                            | Q(funcionario__tiporol__nombre='coordinador_ct')
                            | Q(funcionario__tiporol__nombre='director_ct')));
                    analistax=algoritmo_asignacion.array_de_funcionarios(asig_func,'analista')
                    coordinador_ctx=algoritmo_asignacion.array_de_funcionarios(asig_func,'coordinador_ct')
                    director_ctx= algoritmo_asignacion.array_de_funcionarios(asig_func,'director_ct')
                    
                elif funcionarios.tiporol.nombre=='ministro':
                    asig_func = Asignacion.objects.filter(Q(solicitud_id__in=solicituds) 
                        & Q(asignacion_habilitada=True)
                        & (Q(funcionario__tiporol__nombre='analista') 
                            | Q(funcionario__tiporol__nombre='coordinador_ct')
                            | Q(funcionario__tiporol__nombre='director_ct')
                            | Q(funcionario__tiporol__nombre='viceministro')));
                    analistax=algoritmo_asignacion.array_de_funcionarios(asig_func,'analista')
                    coordinador_ctx=algoritmo_asignacion.array_de_funcionarios(asig_func,'coordinador_ct')
                    director_ctx= algoritmo_asignacion.array_de_funcionarios(asig_func,'director_ct')
                    viceministrox= algoritmo_asignacion.array_de_funcionarios(asig_func,'viceministro')
                        

                jsontmp['data'].update({'analistax':analistax})
                jsontmp['data'].update({'inspectorx':inspectorx})
                jsontmp['data'].update({'coordinador_ctx':coordinador_ctx})
                jsontmp['data'].update({'directorx':director_ctx})
                jsontmp['data'].update({'viceministrox':viceministrox})

            estatus= sorted(set(estatus1))
            sucursales = [(e.sucursal.id, e.sucursal.nombre) if e.sucursal is not None else (0, "Sede Principal") for e in solicitudes]
            
            jsontmp['data'].update({'estados':estatus})
            jsontmp['data'].update({'sucursales':sucursales})

            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )                

        elif request.GET['bandeja'] == 'lsr_bandeja' or request.GET['bandeja'] == 'consignaciones' or request.GET['bandeja'] == 'por_entregar':
            if user.role == ROLE_PST:
                if request.GET['bandeja'] == 'consignaciones':
                    solicitudes = Consignacion.objects.filter(solicitud_libro__pst=pst)
                else:
                    solicitudes = SolicitudLibro.objects.filter(pst=user)
                solicituds = [e.id for e in solicitudes]
                estados1= [e.estatus.nombre for e in solicitudes]
                estados = sorted(set(estados1))

            elif user.role == ROLE_FUNCIONARIO:
                funcionarios = Funcionario.objects.filter(user__id=user.id).first()
                dprint(user.id)
                asignaciones=Asignacion.objects.filter(
                    funcionario=funcionarios,
                    asignacion_habilitada=True,
                    tipo_asignacion__abreviacion='LSR'
                ).values('solicitud_libro')
                if request.GET['bandeja'] == 'consignaciones':
                    consignaciones = Consignacion.objects.filter(
                        solicitud_libro_id__in=asignaciones
                    )
                    solicitudes=SolicitudLibro.objects.filter(
                        id__in=consignaciones.values('solicitud_libro')
                    )
                    estados1=[e.estatus.nombre for e in consignaciones]
                    estados = sorted(set(estados1))
                elif request.GET['bandeja'] == 'por_entregar':
                    solicitudes = SolicitudLibro.objects.exclude(estatus__abreviacion='E')
                    estados1= [e.estatus.nombre for e in solicitudes]
                    estados = sorted(set(estados1))
                else:
                    solicitudes = SolicitudLibro.objects.filter(id__in=asignaciones)
                    estados1= [e.estatus.nombre for e in solicitudes]
                    estados = sorted(set(estados1))
                solicituds = [e.id for e in solicitudes]
            #solicituts = SolicitudLibro.objects.filter(pst=user).distinct('sucursal')
            solicituts = solicitudes.distinct('sucursal')
            sucursales = [(e.sucursal.id, e.sucursal.nombre) if e.sucursal is not None else (0, "Sede Principal") for e in solicituts]
            estado1 = [(e.sucursal.estado.id, e.sucursal.estado.estado) if e.sucursal is not None else (Direccion.objects.get(pst=e.pst).estado.id, Direccion.objects.get(pst=e.pst).estado.estado) for e in solicitudes]
            estado =sorted(set(estado1))
            libro = LsrFisico.objects.filter(solicitud_libro_id__in=solicituds)
            libros = [e.identificador for e in libro]
            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "estado":estado,
                    "estados":estados,
                    "sucursales":sucursales,
                    "libros":libros,
                },
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )
        elif request.GET['bandeja']=='entrada_portal':
            try:
                if user.role == ROLE_PST:
                    entrada = Entrada.objects.filter(lsr__pst=user)
                elif user.role == ROLE_FUNCIONARIO:
                    entrada =Entrada.objects.all()

                if len(entrada)>0:
                    entradas = [e.id for e in entrada]
                    turist = [e.turista_id for e in entrada]
                    turistas = Turista.objects.filter(id__in=turist).distinct('id')
                    
                    nombre_tur = []
                    for e in turistas:
                        if e.nombre and e.apellido:
                            nombre_tur.append((e.id, e.nombre+" "+e.apellido))

                    tipo_comment = [e.tipo_comentario.nombre for e in entrada]
                    tipo_com = sorted(set(tipo_comment))
                    sev = []
                    for e in entrada:
                        if e.severidad:
                            sev.append(e.severidad.nombre)

                    severidad = sorted(set(sev))
                    estat = [e.estatus.nombre for e in entrada]
                    estatus = sorted(set(estat))
                    #sucurs = [e.lsr.sucursal.id if e.lsr.sucursal is not None for e in entrada]
                    #sucursals = Sucursales.objects.filter(id__in=sucurs).distinct('id')
                    sucursals = entrada.distinct('lsr')
                    sucursales = [(e.lsr.sucursal.id, e.lsr.sucursal.nombre) if e.lsr.sucursal is not None else (0, "Sede Principal") for e in sucursals]
                    estado = [(e.lsr.sucursal.estado.id, e.lsr.sucursal.estado.estado) if e.lsr.sucursal is not None else (Direccion.objects.get(pst=e.lsr.pst).estado.id, Direccion.objects.get(pst=e.lsr.pst).estado.estado) for e in sucursals]
                    estados = sorted(set(estado))

                    jsontmp = {
                        "err_msg": "",
                        "success": u"Cargando información",
                        "data":{
                            "turista":nombre_tur,
                            "tipo_comment":tipo_com,
                            "severidad":severidad,
                            "estados": estatus,
                            "estado": estados,
                            "sucursales":sucursales,

                        },
                    }
                   
                else:
                    jsontmp = {
                        "err_msg": "No encontrado",
                        "success": "",
                    }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=True),
                    content_type="application/json"
                )

            except Exception, e:
                raise e  
        elif request.GET['bandeja']=='gestion_casos':
            try:
                if user.role == ROLE_FUNCIONARIO:

                    funcionario = Funcionario.objects.all()
                    funcionarios = [e.id for e in funcionario]
                    tiporols = [e.tiporol.nombre for e in funcionario]
                    tiporol = sorted(set(tiporols))

                    nombres = [(e.id, e.nombre+" "+e.apellido) for e in funcionario]
                    
                    jsontmp = {
                        "err_msg": "",
                        "success": u"Cargando información",
                        "data":{
                            "tiporol":tiporol,
                            "funcionario": nombres,
                        },
                    }
                else:
                    jsontmp = {
                        "err_msg": "No encontrado",
                        "success": "",
                    }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=True),
                    content_type="application/json"
                )

            except Exception, e:
                raise e

        elif request.GET['bandeja'] == 'placas_bandeja':

            entidades = {}
            for e in Estado.objects.all().order_by('estado'):
                entidades.update({e.id:e.estado}) 

            if user.role == ROLE_PST:
                pst = Pst.objects.get(user=user)
                placa=Placa.objects.filter(documento__firmado=True, usuario_pst=pst)
            else:
                placa=Placa.objects.all().exclude(documento__firmado=True)     
            tipo=TipoLicencia.objects.filter(id__in=placa.values('licencia_asignada__tipo_licenciaid'))       
            tipos = {}
            sucursales = {}
            for t in tipo:
                tipos.update({t.id:t.nombre})
            
            for p in placa:
                l=p.licencia_asignada
                if l.sucursal:
                    sucursales.update({l.sucursal.id:l.sucursal.nombre})
                else:
                    sucursales.update({0:"Sede Principal"})
            

            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "sucursales": sucursales,
                    "tipos": tipos,
                    "entidades": entidades, 
                },
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )

        elif request.GET['bandeja'] == 'distribucion_placas':
            entidades = Estado.objects.all().order_by('estado')
            entidades = [e.id for e in entidades]

            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "entidades": entidades, 
                }
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )
        elif request.GET['bandeja'] == 'reporte_dist_eat' or request.GET['bandeja'] == 'reporte_comparativo_eat' or request.GET['bandeja'] == 'reporte_dist_lsr':

            entidades = {}
            for e in Estado.objects.all().order_by('estado'):
                entidades.update({e.id:e.estado}) 

            clasificaciones = {}
            if request.GET['bandeja'] == 'reporte_dist_lsr':
                for c in TipoLicencia.objects.all():
                    clasificaciones.update({c.id:c.nombre})
            else:   
                for c in TipoLicencia.objects.filter(padre__codigo='LIC_ALO_T'):
                    clasificaciones.update({c.id:c.nombre})

            estatus = {}
            if request.GET['bandeja'] == 'reporte_dist_eat':
                for e in Estatus.objects.filter(tipo_solicitud__abreviacion='SC'):
                    estatus.update({e.id:e.nombre})
            elif request.GET['bandeja'] == 'reporte_dist_lsr':
                for e in Estatus.objects.filter(tipo_solicitud__abreviacion='LSR'):
                    estatus.update({e.id:e.nombre})

            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "entidades": entidades, 
                    "clasificaciones": clasificaciones,
                    "estatus": estatus
                }
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )

        else:
            jsontmp = {
                "err_msg": "Error En la busqueda",
                "success": "",
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json",
            )

    def post(self, request, *args, **kwargs):
        user = request.user
        filters_dict={}
        if request.POST.has_key('estado_avanzado'):
            estado_id=request.POST['estado_avanzado']

            municipios={}
            for x in Municipio.objects.filter(estado__id=int(estado_id)):
                municipios.update({x.id:x.municipio})

            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "municipios": municipios
                }
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )

        elif request.POST.has_key('municipio_avanzado'):
            municipio_id=request.POST['municipio_avanzado']

            parroquias={}
            for x in Parroquia.objects.filter(municipio__id=int(municipio_id)):
                parroquias.update({x.id:x.parroquia})

            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "parroquias": parroquias
                }
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )

        elif request.POST.has_key('clasificacion_buscar'):
            clasificacion_id=request.POST['clasificacion_buscar']

            categorias={}
            for x in Categoria.objects.filter(tipo_pst__id=int(clasificacion_id)):
                categorias.update({x.id:x.nombre})

            jsontmp = {
                "err_msg": "",
                "success": u"Cargando información",
                "data":{
                    "categorias": categorias
                }
            }
            return HttpResponse(
                json.dumps(jsontmp, sort_keys=True),
                content_type="application/json"
            )

        else:
            try:
                if request.POST.has_key('bandeja'):
                    dprint(request.POST['bandeja'])
                    conditional = False
                    if user.role == ROLE_PST:
                        if request.POST['bandeja']!= 'entrada_portal' and request.POST['bandeja']!= 'placas_bandeja': 
                            filters_dict.update({'pst_id': user.id})
                        elif request.POST['bandeja']== 'entrada_portal':    
                            filters_dict.update({'lsr__pst_id': user.id})
                    else:
                        if request.POST['bandeja'] == 'gestion_casos':
                            dprint("hello")
                            if request.POST.has_key('funcionario'):
                                if request.POST['funcionario']:
                                    filters_dict.update({'id': request.POST['funcionario']})
                            if request.POST.has_key('tiporol'):
                                if  request.POST['tiporol']:
                                    filters_dict.update({'tiporol__nombre': request.POST['tiporol']})
                            funcionarios = Funcionario.objects.filter(**filters_dict)
                            sec= secure_value(pickle.dumps(filters_dict))
                            dprint(len(sec))
                            dprint(encode=sec)
                            sec1 = quote_plus(sec)
                            dprint(quote=sec1)
                            return HttpResponseRedirect(reverse('reportes', kwargs={'reporte': 'gestiondecasos'}) + '?busqueda=busqueda&solicitudes='+sec1)
                            if funcionarios:
                                func = [e.id for e in funcionarios]
                                jsontmp = {
                                    "err_msg": "",
                                    "success": "Busqueda exitosa",
                                    "data":{
                                        "solicitudes":func,
                                    },
                                }
                            else:
                                jsontmp = {
                                    "err_msg": "Busqueda Fallida",
                                    "success": "",
                                }
                            return HttpResponse(
                                json.dumps(jsontmp, sort_keys=True),
                                content_type="application/json"
                            )
                        elif request.POST['bandeja']=='categorizacion_bandeja' or request.POST['bandeja']== 'categorizacion_reporte' or request.POST['bandeja'] == 'historial_prestador' or request.POST['bandeja'] == 'procesos_bandeja':
                            arreglo = []
                            funcionario=Funcionario.objects.filter(user_id=user.id).first()
                            if request.POST['bandeja'] == 'categorizacion_bandeja':
                                asignacion = Asignacion.objects.filter(
                                    funcionario=funcionario,
                                    asignacion_habilitada=True
                                ).exclude(tipo_asignacion__abreviacion='LSR')
                                asignaciones = [e.solicitud_id for e in asignacion]
                            elif request.POST['bandeja'] == 'categorizacion_reporte':
                                asignacion = Solicitud.objects.all().distinct('sucursal')
                                asignaciones = [e.id for e in asignacion]
                            else:
                                asignacion = Solicitud.objects.all()
                                asignaciones = [e.id for e in asignacion]
                            filters_dict.update({'id__in': asignaciones})
                            if request.POST.has_key('analistas'):
                                if request.POST['analistas']:
                                    arreglo.append(request.POST['analistas'])
                                    conditional =True
                            if request.POST.has_key('inspectores'):
                                if request.POST['inspectores']:
                                    arreglo.append(request.POST['inspectores'])
                                    conditional =True
                            if request.POST.has_key('coordinador_cts'):
                                if request.POST['coordinador_cts']:
                                    arreglo.append(request.POST['coordinador_cts'])
                                    conditional =True
                            if request.POST.has_key('director_cts'):
                                if request.POST['director_cts']:
                                    arreglo.append(request.POST['director_cts'])
                                    conditional =True
                            if request.POST.has_key('viceministros'):
                                if request.POST['viceministros']:
                                    arreglo.append(request.POST['viceministros'])
                                    conditional =True
                            if conditional == True:
                                func_filtrados = Funcionario.objects.filter(
                                    id__in= arreglo)
                                if len(func_filtrados) > 0:
                                    solicitus_func = Asignacion.objects.filter(
                                        asignacion_habilitada=True,
                                        funcionario=func_filtrados
                                        ).exclude(tipo_asignacion__abreviacion='LSR')
                                    solicituss_func = [e.solicitud_id for e in solicitus_func]
                                    filters_dict.update({'id__in': solicituss_func})

                        if request.POST.has_key('buscar_texto'):
                            if request.POST['buscar_texto']:
                                array_texto = []
                                condition = False
                                if request.POST['bandeja']!= 'entrada_portal':
                                    if request.POST.has_key('razon_social'):
                                        if request.POST['razon_social']:
                                            array_texto.append(Q(pst__razon_social__contains= 
                                                request.POST['buscar_texto']))
                                            condition = True
                                    if request.POST.has_key('rtn'):
                                        if request.POST['rtn']:
                                            array_texto.append(Q(pst__rtn__contains= 
                                                request.POST['buscar_texto']))
                                            condition = True
                                    if request.POST.has_key('rif'):
                                        if request.POST['rif']:
                                            array_texto.append(Q(pst__rif__contains= 
                                                request.POST['buscar_texto']))
                                            condition = True
                                    if condition == False:
                                        array_texto.append(Q(pst__razon_social__contains= 
                                            request.POST['buscar_texto']))
                                        array_texto.append(Q(pst__rtn__contains= 
                                            request.POST['buscar_texto']))
                                        array_texto.append(Q(pst__rif__contains= 
                                            request.POST['buscar_texto']))
                                else:
                                    if request.POST.has_key('razon_social'):
                                        if request.POST['razon_social']:
                                            array_texto.append(Q(lsr__pst__razon_social__contains= 
                                                request.POST['buscar_texto']))
                                            condition = True
                                    if request.POST.has_key('rtn'):
                                        if request.POST['rtn']:
                                            array_texto.append(Q(lsr__pst__rtn__contains= 
                                                request.POST['buscar_texto']))
                                            condition = True
                                    if request.POST.has_key('rif'):
                                        if request.POST['rif']:
                                            array_texto.append(Q(lsr__pst__rif__contains= 
                                                request.POST['buscar_texto']))
                                            condition = True
                                    if condition == False:
                                        array_texto.append(Q(lsr__pst__razon_social__contains= 
                                            request.POST['buscar_texto']))
                                        array_texto.append(Q(lsr__pst__rtn__contains= 
                                            request.POST['buscar_texto']))
                                        array_texto.append(Q(lsr__pst__rif__contains= 
                                            request.POST['buscar_texto']))

                    if request.POST.has_key('periodo-desde'):
                        if request.POST['periodo-desde']:
                            fecha_desde = datetime.datetime.strptime(request.POST['periodo-desde'], "%m/%d/%Y")
                            if request.POST['bandeja']=='categorizacion_bandeja' or request.POST['bandeja']=='reporte_dist_eat' or request.POST['bandeja']=='reporte_comparativo_eat':
                                filters_dict.update({'fecha_apertura__gte': datetime.datetime(fecha_desde.year,fecha_desde.month,fecha_desde.day)})
                            elif request.POST['bandeja'] == 'lsr_bandeja' or request.POST['bandeja'] == 'reporte_dist_lsr':
                                filters_dict.update({'fecha_realizacion__gte': datetime.datetime(fecha_desde.year,fecha_desde.month,fecha_desde.day)})
                            elif request.POST['bandeja'] == 'entrada_portal':
                                filters_dict.update({'fecha_entrada__gte': datetime.datetime(fecha_desde.year,fecha_desde.month,fecha_desde.day)})
                    if request.POST.has_key('periodo-hasta'):
                        if request.POST['periodo-hasta']:
                            fecha_hasta = datetime.datetime.strptime(request.POST['periodo-hasta'], "%m/%d/%Y")
                            if request.POST['bandeja']=='categorizacion_bandeja' or request.POST['bandeja']=='reporte_dist_eat' or request.POST['bandeja']=='reporte_comparativo_eat':
                                filters_dict.update({'fecha_apertura__lte': datetime.datetime(fecha_hasta.year,fecha_hasta.month, calendar.monthrange(fecha_hasta.year,fecha_hasta.month)[1],23,59)})
                            elif request.POST['bandeja'] == 'lsr_bandeja' or request.POST['bandeja'] == 'reporte_dist_lsr':
                                filters_dict.update({'fecha_realizacion__lte': datetime.datetime(fecha_hasta.year,fecha_hasta.month, calendar.monthrange(fecha_hasta.year,fecha_hasta.month)[1],23,59,59)})          
                            elif request.POST['bandeja'] == 'entrada_portal':
                                filters_dict.update({'fecha_entrada__lte': datetime.datetime(fecha_hasta.year,fecha_hasta.month, calendar.monthrange(fecha_hasta.year,fecha_hasta.month)[1],23,59,59)})   
                    if request.POST.has_key('estatus') and not request.POST['bandeja'] == 'placas_bandeja':
                        if request.POST['estatus']:
                            if request.POST['bandeja']=='categorizacion_bandeja' or request.POST['bandeja']=='categorizacion_reporte':
                                if user.role==ROLE_FUNCIONARIO:
                                    estados = Estatus.objects.filter(
                                        nombre=request.POST['estatus']).first()
                                    if estados:
                                        filters_dict.update({'estatus__abreviacion':estados.abreviacion})
                                else:
                                    estado = constants.ESTATUS_PST[request.POST['estatus']]
                                    filters_dict.update({'estatus__abreviacion__in':estado})
                            elif request.POST['bandeja']=='reporte_dist_eat' or request.POST['bandeja'] == 'reporte_dist_lsr':
                                filters_dict.update({'estatus__id':int(request.POST['estatus'])})
                            else:
                                estados = Estatus.objects.filter(
                                    nombre= request.POST['estatus']).first()
                                if estados:
                                    filters_dict.update({'estatus__abreviacion':estados.abreviacion})
                    
                    if request.POST.has_key('sucursal'):
                        if request.POST['sucursal']:
                            sucursal=request.POST['sucursal']
                            if sucursal=='0':
                                sucursal=None
                            if request.POST['bandeja'] == 'categorizacion_bandeja' or request.POST['bandeja'] == 'consignaciones' or request.POST['bandeja'] == 'lsr_bandeja' or request.POST['bandeja'] == 'historial_prestador' or request.POST['bandeja'] == 'categorizacion_reporte':
                                filters_dict.update({'sucursal_id':sucursal})
                            elif request.POST['bandeja']=='entrada_portal':
                                filters_dict.update({'lsr__sucursal_id':sucursal})
                            elif request.POST['bandeja'] == 'placas_bandeja':
                                filters_dict.update({'licencia_asignada__sucursal_id':sucursal})

                    if request.POST['bandeja']=='categorizacion_bandeja' or request.POST['bandeja'] == 'categorizacion_reporte' or request.POST['bandeja'] == 'historial_prestador' or request.POST['bandeja'] == 'procesos_bandeja':
                        dprint(request.POST['bandeja'])
                        if request.POST.has_key('buscar_texto'):
                            if request.POST['buscar_texto']:
                                """
                                solicitudes = Solicitud.objects.filter(
                                    reduce(operator.or_,array_texto),**filters_dict)
                                """
                                dprint(array=array_texto)
                                filters_dict.update({'adicional':array_texto})
                                dprint(filter=filters_dict)
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                            else:
                                #solicitudes = Solicitud.objects.filter(**filters_dict)
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(len(sec))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                        else:
                            #solicitudes = Solicitud.objects.filter(**filters_dict)
                            sec= secure_value(pickle.dumps(filters_dict))
                            dprint(len(sec))
                            dprint(encode=sec)
                            sec1 = quote_plus(sec)
                            dprint(quote=sec1)
                            #aqui
                        if request.POST['bandeja']=='categorizacion_bandeja':
                            return HttpResponseRedirect(reverse('bandeja') + "?busqueda=busqueda&solicitudes="+sec1)
                        elif request.POST['bandeja'] == 'categorizacion_reporte':
                            return HttpResponseRedirect(reverse('reportes', kwargs={'reporte':'categorizaciones'}) + "?busqueda=busqueda&solicitudes="+sec1)
                        elif request.POST['bandeja'] == 'historial_prestador':
                            return HttpResponseRedirect(reverse('reportes', kwargs={'reporte':'historial'}) + "?busqueda=busqueda&solicitudes="+sec1)
                        elif request.POST['bandeja'] == 'procesos_bandeja':
                            return HttpResponseRedirect(reverse('operacion_director', kwargs={'operacion':'procesos'}) + "?busqueda=busqueda&solicitudes="+sec1)
                    elif request.POST['bandeja'] == 'lsr_bandeja' or request.POST['bandeja'] == 'por_entregar':
                        if request.POST.has_key('estados'):
                            if request.POST['estados']:
                                filters_dict.update({'sucursal__estado__id': request.POST['estados']})
                                if request.POST.has_key('municipios'):
                                    if request.POST['municipios']:
                                        filters_dict.update({'sucursal__municipio__id': request.POST['municipios']})
                                        if request.POST.has_key('parroquias'):
                                            if request.POST['parroquias']:
                                                filters_dict.update({'sucursal__parroquia__id': request.POST['parroquias']})
                        """
                        if request.POST.has_key('libro'):
                            if request.POST['libro']:
                                libro = LsrFisico.objects.filter(
                                    identificador=request.POST['libro']).first()
                                if libro:
                                    libros1 =[libro.solicitud_libro.id]
                                    if conditional == True: 
                                        array_extra = filters_dict['id__in']
                                        filters_dict.update({'id__in': list(libros1) + list(set(libros1)-set(array_extra))})
                                    else:
                                        filters_dict.update({'id__in': libros1})
                        """
                        if request.POST.has_key('buscar_texto'):
                            if request.POST['buscar_texto']:
                                """
                                solicitudes = SolicitudLibro.objects.filter(
                                    reduce(operator.or_,array_texto),**filters_dict)
                                """
                                dprint(array=array_texto)
                                filters_dict.update({'adicional':array_texto})
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                            else:
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                                #solicitudes = SolicitudLibro.objects.filter(**filters_dict)
                        else:
                            sec= secure_value(pickle.dumps(filters_dict))
                            dprint(encode=sec)
                            sec1 = quote_plus(sec)
                            dprint(quote=sec1)
                            #solicitudes = SolicitudLibro.objects.filter(**filters_dict)
                        if request.POST['bandeja'] == 'lsr_bandeja':
                            return HttpResponseRedirect(reverse('bandeja_libro') + "?busqueda=busqueda&solicitudes="+sec1)   
                        else:
                            return HttpResponseRedirect(reverse('por_entregar') + "?busqueda=busqueda&solicitudes="+sec1) 
                    elif request.POST['bandeja'] == 'consignaciones':
                        dprint(post=request.POST)
                        """
                        if request.POST.has_key('estatus'):
                            if request.POST['estatus']:
                                dprint(post=request.POST)
                        """

                        if request.POST.has_key('libro'):
                            if request.POST['libro']:
                                filters_dict.update({'lsr_fisico__identificador': request.POST['libro']})
                                """
                                libro = LsrFisico.objects.filter(
                                    identificador=request.POST['libro']).first()
                                if libro:
                                    filters_dict.update({'id__in': libros1})
                                    
                                    libros1 =[libro.solicitud_libro.id]
                                    if conditional == True: 
                                        array_extra = filters_dict['id__in']
                                        filters_dict.update({'id__in': list(libros1) + list(set(libros1)-set(array_extra))})
                                    else:
                                        filters_dict.update({'id__in': libros1})
                                """
                        if request.POST.has_key('buscar_texto'):
                            if request.POST['buscar_texto']:
                                """
                                solicitudes = SolicitudLibro.objects.filter(
                                    reduce(operator.or_,array_texto),**filters_dict)
                                """
                                dprint(array=array_texto)
                                filters_dict.update({'adicional':array_texto})
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                            else:
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                                #solicitudes = SolicitudLibro.objects.filter(**filters_dict)
                        else:
                            sec= secure_value(pickle.dumps(filters_dict))
                            dprint(encode=sec)
                            sec1 = quote_plus(sec)
                            dprint(quote=sec1)
                            #solicitudes = SolicitudLibro.objects.filter(**filters_dict)
                        return HttpResponseRedirect(reverse('oficios_respuesta',  kwargs={'operacion':'bandeja'}) + "?busqueda=busqueda&solicitudes="+sec1)    
                        
                    elif request.POST['bandeja'] == 'entrada_portal':
                        if request.POST.has_key('severidad'):
                            if request.POST['severidad']:
                                filters_dict.update({'severidad__nombre': request.POST['severidad']})
                        if request.POST.has_key('tipo_comentario'):
                            if request.POST['tipo_comentario']:
                                filters_dict.update({'tipo_comentario__nombre': request.POST['tipo_comentario']})
                        if request.POST.has_key('turista'):
                            if request.POST['turista']:
                                filters_dict.update({'turista_id': request.POST['turista']})
                        if request.POST.has_key('estados'):
                            if request.POST['estados']:
                                filters_dict.update({'lsr__sucursal__estado__id': request.POST['estados']})
                                if request.POST.has_key('municipios'):
                                    if request.POST['municipios']:
                                        filters_dict.update({'lsr__sucursal__municipio__id': request.POST['municipios']})
                                        if request.POST.has_key('parroquias'):
                                            if request.POST['parroquias']:
                                                filters_dict.update({'lsr__sucursal__parroquia__id': request.POST['parroquias']})
                        
                        if request.POST.has_key('buscar_texto'):
                            if request.POST['buscar_texto']:
                                dprint(array=array_texto)
                                filters_dict.update({'adicional':array_texto})
                                dprint(filter=filters_dict)
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)
                            else: 
                                sec= secure_value(pickle.dumps(filters_dict))
                                dprint(len(sec))
                                dprint(encode=sec)
                                sec1 = quote_plus(sec)
                                dprint(quote=sec1)   
                        else:
                            sec= secure_value(pickle.dumps(filters_dict))
                            dprint(len(sec))
                            dprint(encode=sec)
                            sec1 = quote_plus(sec)
                            dprint(quote=sec1)


                        if user.role == ROLE_PST:
                            return HttpResponseRedirect(reverse('portallsr', kwargs={'operacion':'entradas'})+ "?busqueda=busqueda&solicitudes="+sec1)
                        elif user.role == ROLE_FUNCIONARIO:
                            return HttpResponseRedirect(reverse('reportes', kwargs={'reporte':'portallsr'}) + "?busqueda=busqueda&solicitudes="+sec1)
                        #entrada= Entrada.objects.filter(**filters_dict)
                        if entrada:
                            entradas = [e.id for e in entrada]
                            jsontmp = {
                                "err_msg": "",
                                "success": "Busqueda exitosa",
                                "data":{
                                    "solicitudes":entradas,
                                }
                            }
                        else:
                            jsontmp = {
                                "err_msg": "Entradas",
                                "success": "",
                            }
                        return HttpResponse(
                            json.dumps(jsontmp, sort_keys=True),
                            content_type="application/json"
                        )
                    elif request.POST['bandeja'] == 'placas_bandeja':
                        dprint(request.POST)
                        #if user.role == ROLE_PST:
                        #flag_placa = False
                        array_licencia = []
                        if request.POST.has_key('estados'):
                            if request.POST['estados']:
                                filters_dict.update({'licencia_asignada__sucursal__estado__id': request.POST['estados']})
                                if request.POST.has_key('municipios'):
                                    if request.POST['municipios']:
                                        filters_dict.update({'licencia_asignada__sucursal__municipio__id': request.POST['municipios']})
                                        if request.POST.has_key('parroquias'):
                                            if request.POST['parroquias']:
                                                filters_dict.update({'licencia_asignada__sucursal__parroquia__id': request.POST['parroquias']})
                        """
                        if request.POST.has_key('licencias'):
                            if request.POST['licencias']:
                                flag_placa = True
                                array_licencia.append(int(request.POST['licencias']))
                        """

                        if request.POST.has_key('tipo_licencias'):
                            if request.POST['tipo_licencias']:
                                filters_dict.update({'licencia_asignada__tipo_licenciaid__id': request.POST['tipo_licencias']})
                                #flag_placa = True
                                #array_licencia.append(int(request.POST['tipo_licencias']))
                        """
                        if flag_placa == True:
                            filters_dict.update({'id__in': array_licencia})
                        """
                        sec= secure_value(pickle.dumps(filters_dict))
                        dprint(len(sec))
                        dprint(encode=sec)
                        sec1 = quote_plus(sec)
                        dprint(quote=sec1)

                        return HttpResponseRedirect(reverse('bandeja_placa')+ "?busqueda=busqueda&solicitudes="+sec1)

                    elif request.POST['bandeja'] == 'reporte_dist_eat' or request.POST['bandeja']=='reporte_comparativo_eat' or request.POST['bandeja'] == 'reporte_dist_lsr':
                        dprint(request.POST)
                        if request.POST['bandeja'] == 'reporte_dist_eat' and request.POST.has_key('categoria'):
                            if request.POST['categoria']:
                                filters_dict.update({'pst_categoria_doc__categoria__id':int(request.POST['categoria'])})

                        sec= secure_value(pickle.dumps(filters_dict))
                        sec1 = quote_plus(sec)
                        busqueda="?busqueda=busqueda&solicitudes="+sec1

                        if request.POST.has_key('clasificacion'):
                            if request.POST['clasificacion']:
                                filter_tipo=request.POST['clasificacion']
                                busqueda=busqueda+"&tipo="+filter_tipo

                        if request.POST.has_key('parroquias'):
                            if request.POST['parroquias']:
                                filter_parroquia=request.POST['parroquias']
                                busqueda=busqueda+"&parroquia="+filter_parroquia
                        if request.POST.has_key('municipios'):
                            if request.POST['municipios']:
                                filter_municipio=request.POST['municipios']
                                busqueda=busqueda+"&municipio="+filter_municipio
                        if request.POST.has_key('estados'):
                            if request.POST['estados']:
                                filter_estado=request.POST['estados']
                                busqueda=busqueda+"&estado="+filter_estado

                        if request.POST['bandeja'] == 'reporte_dist_eat':
                            return HttpResponseRedirect(reverse('reportes',  kwargs={'reporte':'distribucioneat'}) + busqueda)    
                        elif request.POST['bandeja'] == 'reporte_dist_lsr':
                            return HttpResponseRedirect(reverse('reportes', kwargs={'reporte':'distribucionlibros'}) + busqueda)
                        else:
                            return HttpResponseRedirect(reverse('reportes',  kwargs={'reporte':'comparativoeat'}) + busqueda)

                    if solicitudes:
                        solicituds = [e.id for e in solicitudes]
                        dprint(solicituds=solicituds)
                        jsontmp = {
                            "err_msg": "",
                            "success": "Busqueda exitosa",
                            "data":{
                                "solicitudes":solicituds,
                            },
                        }
                    else:
                        jsontmp = {
                            "err_msg": "Solicitudes",
                            "success": "",
                        }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=True),
                        content_type="application/json"
                    )
                else:
                    jsontmp = {
                            "err_msg": "Parametros invalidos",
                            "success": "",
                        }
                    return HttpResponse(
                        json.dumps(jsontmp, sort_keys=True),
                        content_type="application/json",
                        status=400
                    )
            except Exception, e:
                raise e


class Reportes(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(Reportes, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            user = request.user
            id_sesion = user.id
            funcionario = Funcionario.objects.get(user_id=int(id_sesion))
            reporte=kwargs['reporte']
            context={}
            busqueda_datos={}
            key='busqueda_cache'

            if reporte == 'categorizaciones':
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        if filter_dict.has_key('adicional'):
                            array_texto = filter_dict['adicional']
                            filter_dict.pop('adicional')
                            solicitudes = Solicitud.objects.filter(
                                reduce(operator.or_,array_texto),**filter_dict
                            ).order_by('sucursal', '-fecha_apertura').distinct('sucursal')
                        else:
                            solicitudes = Solicitud.objects.filter(**filter_dict).order_by(
                                'sucursal', '-fecha_apertura'
                            ).distinct('sucursal')
                    else:
                        solicitudes=Solicitud.objects.order_by(
                            'sucursal', '-fecha_apertura').distinct('sucursal')
                
                    busqueda_datos.update({
                        'solicitudes':solicitudes
                    })
                else:
                    x=cache.get(key)
                    solicitudes=x['solicitudes']

                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':
                        template = get_template('documentos/reportes/categorizacionespdf.html')
                        html = template.render(Context({'data':{'solicitudes': solicitudes}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(),content_type='application/pdf')

                mas =True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    sol= solicitudes
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    sol= solicitudes
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                clasificaciones=[]

                for s in solicitudes:

                    mx = Categoria.objects.filter(
                        tipo_pst = otp_prestador(s.pst, s.sucursal)
                    ).count()
                    
                    if s.pst_categoria_doc is not None:
                        clasificaciones.append(
                            (
                                s.pst_categoria_doc.categoria.valor, 
                                mx - s.pst_categoria_doc.categoria.valor
                            )
                        )
                    else:
                        clasificaciones.append(
                            (
                                0,
                                mx
                            )
                        )
                sol_cat=zip(solicitudes,clasificaciones)


                #else:
                context.update({
                    'actor': user.get_full_name(),
                    'solicitudes': sol_cat,
                })

                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': sol_cat, 'busqueda':True})

                user = funcionario.tiporol.nombre
                context.update({user: True, 'tiporol': user})

                return render(request, 'coordinador_ct/categorizaciones.html', context)

            elif reporte == 'gestiondecasos':
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        funcionarios = Funcionario.objects.filter(habilitado=True,**filter_dict)
                    else:
                        funcionarios=Funcionario.objects.filter(habilitado=True)

                    busqueda_datos.update({
                        'funcionarios':funcionarios
                    })
                else:
                    x=cache.get(key)
                    funcionarios=x['funcionarios']

                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':

                        asignaciones={}
                        asig=Asignacion.objects.filter(
                            asignacion_habilitada=True, funcionario_id__in=funcionarios).values(
                                'funcionario').annotate(
                                    count=Count('pk')).exclude(
                                        tipo_asignacion__abreviacion='LSR')

                        for a in asig:
                            asignaciones.update({a['funcionario']:a['count']})

                        template = get_template('documentos/reportes/gestiondecasospdf.html')
                        html = template.render(Context({'data':{'asignaciones': asignaciones, 'funcionarios': funcionarios}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(),content_type='application/pdf')

                mas =True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    func= funcionarios
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    funcionarios = funcionarios[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(func[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    func= funcionarios
                    funcionarios = funcionarios[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(func[num:num+1]) ==0:
                        mas = False


                funcs = [e.id for e in funcionarios]

                asignaciones={}
                asig=Asignacion.objects.filter(
                    asignacion_habilitada=True, funcionario_id__in=funcs).values(
                        'funcionario').annotate(
                            count=Count('pk')).exclude(
                                tipo_asignacion__abreviacion='LSR')

                for a in asig:
                    asignaciones.update({a['funcionario']:a['count']})

                #else:
                context.update({
                    'actor': user.get_full_name(),
                    'asignaciones': asignaciones,
                    'funcionarios': funcionarios
                })
                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})

                user = funcionario.tiporol.nombre
                context.update({user: True, 'tiporol': user})

                return render(request, 'coordinador_ct/gestiondecasos.html', context)
            elif reporte == 'historial':
                analistas={}
                inspectores={}
                directoresct={}
                coordinadoresct={}

                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        if filter_dict.has_key('adicional'):
                            array_texto = filter_dict['adicional']
                            filter_dict.pop('adicional')
                            solicitudes=Solicitud.objects.filter(
                                reduce(operator.or_,array_texto),**filter_dict
                            ).order_by('-fecha_apertura')
                        else:
                            solicitudes=Solicitud.objects.filter(**filter_dict
                            ).order_by('-fecha_apertura')
                    else:
                        solicitudes=Solicitud.objects.order_by('-fecha_apertura')
                    busqueda_datos.update({
                        'solicitudes':solicitudes
                    })

                else:
                    x=cache.get(key)
                    solicitudes=x['solicitudes']

                clasificaciones=[]
                for s in solicitudes:

                    mx = Categoria.objects.filter(
                        tipo_pst = otp_prestador(s.pst, s.sucursal)
                    ).count()
                    
                    if s.pst_categoria_doc is not None:
                        clasificaciones.append(
                            (
                                s.pst_categoria_doc.categoria.valor, 
                                mx - s.pst_categoria_doc.categoria.valor
                            )
                        )
                    else:
                        clasificaciones.append(
                            (
                                0,
                                mx
                            )
                        )
                    asignaciones=Asignacion.objects.filter(
                        solicitud=s).order_by(
                        'funcionario', 
                        '-fecha_asignacion'
                        ).distinct(
                            'funcionario'
                        )
                    for a in asignaciones:
                        nombre = a.funcionario.nombre+" "+a.funcionario.apellido
                        if a.funcionario.tiporol.nombre == 'analista':

                            if not analistas.has_key(s.id):
                                analistas.update({s.id:[]})
                            analistas[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion
                                }
                            )

                        elif a.funcionario.tiporol.nombre == 'inspector':
                            if not inspectores.has_key(s.id):
                                inspectores.update({s.id:[]})
                            try:
                                Notificacion.objects.get(
                                    receptor__id=a.funcionario.user.id, 
                                    estatus_actual__abreviacion='EI',
                                    solicitud=a.solicitud)
                                estatus= "Con Credenciales"
                            except:
                                estatus= "Sin Credenciales"
                            inspectores[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion,
                                    'estatus': estatus
                                }
                            )
                        elif a.funcionario.tiporol.nombre == 'coordinador_ct':
                            if not coordinadoresct.has_key(s.id):
                                coordinadoresct.update({s.id:[]})
                            coordinadoresct[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion
                                }
                            )
                        elif a.funcionario.tiporol.nombre == 'director_ct':
                            if not directoresct.has_key(s.id):
                                directoresct.update({s.id:[]})
                            directoresct[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion
                                }
                            )
                

                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':
                        template = get_template('documentos/reportes/historialpdf.html')
                        html = template.render(Context({'data':{'solicitudes': solicitudes, 'analistas':analistas, 'coordinadoresct': coordinadoresct, 'inspectores':inspectores, 'directoresct':directoresct}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(),content_type='application/pdf')

                mas =True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    sol= solicitudes
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    sol= solicitudes
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False
                #else:
                sol_cat=zip(solicitudes,clasificaciones)

                context.update({
                    'actor': user.get_full_name(),
                    'solicitudes': sol_cat,
                    'analistas': analistas,
                    'coordinadoresct' : coordinadoresct,
                    'inspectores' : inspectores,
                    'directoresct': directoresct,
                })

                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})

                user = funcionario.tiporol.nombre
                context.update({user: True, 'tiporol': user})

                return render(request, 'coordinador_ct/historial.html', context)
            elif reporte == 'portallsr':                
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        if filter_dict.has_key('adicional'):
                            array_texto = filter_dict['adicional']
                            filter_dict.pop('adicional')
                            entradas=Entrada.objects.filter(
                                reduce(operator.or_,array_texto),**filter_dict)
                        else:
                            entradas=Entrada.objects.filter(**filter_dict)
                    else:
                        entradas=Entrada.objects.all()

                    busqueda_datos.update({
                        'entradas':entradas
                    })
                    
                else:
                    x=cache.get(key)
                    entradas=x['entradas']

                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':
                        template = get_template('documentos/reportes/portalLSRpdf.html')
                        html = template.render(Context({'data':{'entradas': entradas}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(),content_type='application/pdf')

                mas =True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    ent= entradas
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    entradas = entradas[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(ent[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    ent= entradas
                    entradas = entradas[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(ent[num:num+1]) ==0:
                        mas = False

                context.update({
                    'actor': user.get_full_name(),
                    'entradas': entradas,
                })
                #else:
                context.update({
                    'actor': user.get_full_name(),
                    'entradas': entradas,
                })
                user = funcionario.tiporol.nombre
                context.update({user: True, 'tiporol': user})

                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})

                return render(request, 'coordinador_ct/portalLSR.html', context)

            elif reporte == 'historialsolicitud':
                id_solicitud=int(request.GET['solicitud'])
                solicitud=Solicitud.objects.get(id=id_solicitud)

                x=list(Notificacion.objects.filter(solicitud=solicitud).values())
                y=list(NotificacionBackup.objects.filter(solicitud=solicitud).values())

                l=x+y

                #mas =True
                #paginars = False
                """if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    le= l
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    l = l[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(le[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    le= l
                    l = l[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(le[num:num+1]) ==0:
                        mas = False

                """


                l.sort(order)
                historia=[]
                for n in l:
                    try:
                        f=Funcionario.objects.get(user_id=n['receptor_id'])
                        f=f.nombre+" "+f.apellido
                    except:
                        f="-"
                    estatus=Estatus.objects.get(id=n['estatus_actual_id'])
                    historia.append(
                        {
                            'fecha': n['fecha_emision'], 
                            'estatus': estatus.nombre,
                            'funcionario': f,
                            'abreviacion_estatus': estatus.abreviacion,
                            'des_estatus': estatus.descripcion,
                            'observacion': n['observacion']
                        }
                    )

                context.update({
                    'actor': user.get_full_name(),
                    'historial': historia,
                    'solicitud': solicitud,

                })

                """if paginars == True:
                    context.update({'p': p, 'mas': mas})
                """

                user = funcionario.tiporol.nombre
                context.update({user: True, 'tiporol':user})

                return render(request, 'coordinador_ct/historialsolicitud.html', context)

            elif reporte == 'verentrada':
                id_entrada=int(request.GET['entrada'])
                entrada=Entrada.objects.get(id=id_entrada)
                respuesta=RespuestaLsr.objects.filter(entrada=entrada).first()
                encuesta=RespuestaEncuesta.objects.filter(
                    entrada=entrada).order_by(
                        'seccion_encuesta', 
                        'valoracion__tipo_valoracion').distinct(
                            'seccion_encuesta', 
                            'valoracion__tipo_valoracion')
                seccion={}

                for e in encuesta:
                    item=Valoracion.objects.filter(
                        tipo_valoracion=e.valoracion.tipo_valoracion).aggregate(
                            Max('puntaje'), 
                            Min('puntaje'))
                    if not seccion.has_key(e.seccion_encuesta.nombre):
                        seccion.update({e.seccion_encuesta.nombre:[]})
                    seccion[e.seccion_encuesta.nombre].append(
                        {
                            'id_s':e.seccion_encuesta.id, 
                            'id_val':e.valoracion.tipo_valoracion.id,
                            'elementos': RespuestaEncuesta.objects.filter(
                                seccion_encuesta=e.seccion_encuesta,
                                valoracion__tipo_valoracion=e.valoracion.tipo_valoracion
                            ),
                            'valores':Valoracion.objects.filter(
                                tipo_valoracion=e.valoracion.tipo_valoracion
                            ),
                            'maximo':item['puntaje__max'],
                            'minimo':item['puntaje__min']-1
                        }
                    )

                context.update({
                    'actor': user.get_full_name(),
                    'respuesta': respuesta,
                    'entrada': entrada,
                    'secciones':seccion,
                })

                user = funcionario.tiporol.nombre
                context.update({user: True})

                return render(request, 'coordinador_ct/verentrada.html', context)

            elif reporte == 'distribucioneat':
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('solicitudes') and request.GET.has_key('busqueda'):
                        params = secure_value_decode(request.GET['solicitudes'])
                        filter_dict=pickle.loads(params)

                        solicitudesCT=Solicitud.objects.filter(**filter_dict).order_by(
                            'pst', 
                            'sucursal'
                        ).distinct(
                            'pst', 
                            'sucursal'
                        )
                    else:
                        solicitudesCT=Solicitud.objects.all().order_by(
                            'pst', 
                            'sucursal'
                        ).distinct(
                            'pst', 
                            'sucursal'
                        )

                    if request.GET.has_key('tipo') and request.GET.has_key('busqueda'):
                        tipos = TipoLicencia.objects.filter(id=int(request.GET['tipo']))
                    else:
                        tipos = TipoLicencia.objects.filter(padre=TipoLicencia.objects.get(codigo = 'LIC_ALO_T'))

                    if request.GET.has_key('busqueda') and request.GET.has_key('parroquia'):
                        parroquia=Parroquia.objects.get(id=int(request.GET['parroquia']))
                        municipio=Municipio.objects.get(id=parroquia.municipio.id)
                        estados=Estado.objects.filter(id=municipio.estado.id).order_by('estado')
                    elif request.GET.has_key('busqueda') and request.GET.has_key('municipio'):
                        municipio=Municipio.objects.get(id=int(request.GET['municipio']))
                        estados=Estado.objects.filter(id=municipio.estado.id).order_by('estado')
                    elif request.GET.has_key('busqueda') and request.GET.has_key('estado'):
                        estados=Estado.objects.filter(id=int(request.GET['estado'])).order_by('estado')
                    else:
                        estados=Estado.objects.all().order_by('estado')

                    busqueda_datos.update({
                        'solicitudesCT':solicitudesCT,
                        'tipos':tipos,
                        'estados':estados
                    })

                else:
                    x=cache.get(key)
                    solicitudesCT=x['solicitudesCT']
                    estados=x['estados']
                    tipos=x['tipos']

                estados2=estados
                sol = []
                consulta= []

                mas =True
                paginars = False
                if not request.GET.has_key('opcion') and request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    est= estados
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    estados = estados[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(est[num:num+1]) ==0:
                        mas = False

                if not request.GET.has_key('opcion') and (not request.GET.has_key('p') or not request.GET.has_key('s')):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    est= estados
                    estados = estados[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(est[num:num+1]) ==0:
                        mas = False

                for e in estados:
                    sucursales=Sucursales.objects.filter(
                        id__in=solicitudesCT.values('sucursal'),
                        estado__id=e.id
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=solicitudesCT.values('pst'),
                        estado__id=e.id
                    ).values('id')

                    total=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales)
                    )
                    
                    inter = []   
                    for t in tipos:                        
                        sol=LicenciaAsignada.objects.filter(
                            id__in=total.values('id'),
                            tipo_licenciaid=t
                        ).count()
                        inter.append({'cantidad': sol, 'show_name': t.nombre})
                    consulta.append({'datos': inter, 'show_name': e.estado, 'total':total.count()})   

                #Total de todos los Estados         
                if not mas or (request.GET.has_key('opcion') and str(request.GET['opcion'])=='verpdf'):
                    sucursales=Sucursales.objects.filter(
                        id__in=solicitudesCT.values('sucursal'),
                        estado__id__in=estados2.values('id')
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=solicitudesCT.values('pst'),
                        estado__id__in=estados2.values('id')
                    ).values('id')

                    total=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales)
                    )

                    inter = []
                    for t in tipos:     
                        sol=LicenciaAsignada.objects.filter(
                            id__in=total.values('id'),
                            tipo_licenciaid=t
                        ).count()   
                        inter.append({'cantidad': sol, 'show_name': t.nombre})
                    consulta.append({'datos': inter, 'show_name': 'Total', 'total':total.count()})
                   
                
                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':
                        template = get_template('documentos/reportes/distribucion_eatpdf.html')
                        html = template.render(Context({'data':{'consulta': consulta, 'tipos': tipos}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(), content_type='application/pdf')


                context.update({
                    'actor': user.get_full_name(),
                    'consulta': consulta,
                    'tipos': tipos,
                })

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )
                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                user = funcionario.tiporol.nombre
                context.update({user: True})

                return render(request, 'coordinador_ct/distribucion_eat.html', context)

            elif reporte == 'distribucionplacas':

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    dprint(decode=request.GET['solicitudes'])
                    params = secure_value_decode(request.GET['solicitudes'])
                    dprint(params=params)
                    filter_dict=pickle.loads(params)
                    dprint(filter_dict=filter_dict)
                    if filter_dict.has_key('adicional'):
                        array_texto = filter_dict['adicional']
                        filter_dict.pop('adicional')
                        solicitudes = Solicitud.objects.filter(
                            reduce(operator.or_,array_texto),**filter_dict
                        ).order_by('sucursal', '-fecha_apertura').distinct('sucursal')
                    else:
                        solicitudes = Solicitud.objects.filter(**filter_dict).order_by(
                            'sucursal', '-fecha_apertura'
                        ).distinct('sucursal')
                else:
                    placas=Placa.objects.order_by('pst').distinct('pst')
                    
                    tipos = TipoLicencia.objects.filter(padre=TipoLicencia.objects.get(codigo = 'LIC_ALO_T'))

                    sol = []
                    consulta= []
                    # para el total por columnas
                    totales_tipo = {'total':0}

                    for e in Estado.objects.all():
                        sucursales=Sucursales.objects.filter(
                            id__in=placas.values('licencia_asignada__sucursal'),
                            estado__id=e.id
                        ).values('id')
                        psts=Registro_Direccion.objects.filter(
                            pst__id__in=placas.values('pst'),
                            estado__id=e.id
                        ).values('id')
                        inter = []
                        total_fila = 0   
                        for t in tipos:                        
                            sol=LicenciaAsignada.objects.filter(
                                Q(usuario_pst__id__in=psts) | 
                                Q(sucursal__id__in=sucursales),
                                Q(tipo_licenciaid=t)
                            ).count()
                            inter.append({'cantidad': sol, 'show_name': t.nombre})
                            total_fila += sol
                            if not totales_tipo.has_key(t.nombre):
                                totales_tipo.update({t.nombre:0})
                            totales_tipo[t.nombre] += sol

                        totales_tipo['total']+=total_fila
                        inter.append({'cantidad': total_fila, 'show_name': 'total'})
                        consulta.append({'datos': inter, 'show_name': e.estado})
                    
                    context.update({
                        'actor': user.get_full_name(),
                        'consulta': consulta,
                        'tipos': tipos,
                        'totales_tipo': totales_tipo,
                    })
                    #print consulta
                    user = funcionario.tiporol.nombre
                    context.update({user: True})

                    return render(request, 'coordinador_ct/distribucion_placas.html', context)

            elif reporte == 'distribucionlibros':              
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('solicitudes') and request.GET.has_key('busqueda'):
                        params = secure_value_decode(request.GET['solicitudes'])
                        filter_dict=pickle.loads(params)

                        libros=SolicitudLibro.objects.filter(**filter_dict).order_by(
                            'pst', 
                            'sucursal'
                        ).distinct(
                            'pst', 
                            'sucursal'
                        )
                    else:
                        libros=SolicitudLibro.objects.all().order_by(
                            'pst', 
                            'sucursal'
                        ).distinct(
                            'pst', 
                            'sucursal'
                        )

                    if request.GET.has_key('tipo') and request.GET.has_key('busqueda'):
                        tipos = TipoLicencia.objects.filter(id=int(request.GET['tipo']))
                    else:
                        tipos = TipoLicencia.objects.filter(padre=TipoLicencia.objects.get(codigo = 'LIC_ALO_T'))

                    if request.GET.has_key('busqueda') and request.GET.has_key('parroquia'):
                        parroquia=Parroquia.objects.get(id=int(request.GET['parroquia']))
                        municipio=Municipio.objects.get(id=parroquia.municipio.id)
                        estados=Estado.objects.filter(id=municipio.estado.id).order_by('estado')
                    elif request.GET.has_key('busqueda') and request.GET.has_key('municipio'):
                        municipio=Municipio.objects.get(id=int(request.GET['municipio']))
                        estados=Estado.objects.filter(id=municipio.estado.id).order_by('estado')
                    elif request.GET.has_key('busqueda') and request.GET.has_key('estado'):
                        estados=Estado.objects.filter(id=int(request.GET['estado'])).order_by('estado')
                    else:
                        estados=Estado.objects.all().order_by('estado')

                    busqueda_datos.update({
                        'libros':libros,
                        'tipos':tipos,
                        'estados':estados
                    })

                else:
                    x=cache.get(key)
                    libros=x['libros']
                    estados=x['estados']
                    tipos=x['tipos']

                sol = []
                consulta= []

                estados2=estados
                mas =True
                paginars = False
                if not request.GET.has_key('opcion') and request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    est= estados
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    estados = estados[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(est[num:num+1]) ==0:
                        mas = False

                if not request.GET.has_key('opcion') and (not request.GET.has_key('p') or not request.GET.has_key('s')):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    est= estados
                    estados = estados[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(est[num:num+1]) ==0:
                        mas = False

                for e in estados:
                    sucursales=Sucursales.objects.filter(
                        id__in=libros.values('sucursal'),
                        estado__id=e.id
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=libros.values('pst'),
                        estado__id=e.id
                    ).values('id')

                    total=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales)
                    )
                    
                    inter = []   
                    for t in tipos:                        
                        sol=LicenciaAsignada.objects.filter(
                            id__in=total.values('id'),
                            tipo_licenciaid=t
                        ).count()
                        inter.append({'cantidad': sol, 'show_name': t.nombre})
                    consulta.append({'datos': inter, 'show_name': e.estado, 'total':total.count()})

                #Total de todos los Estados           
                if not mas or (request.GET.has_key('opcion') and str(request.GET['opcion'])=='verpdf'):
                    sucursales=Sucursales.objects.filter(
                        id__in=libros.values('sucursal'),
                        estado__id__in=estados2.values('id')
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=libros.values('pst'),
                        estado__id__in=estados2.values('id')
                    ).values('id')

                    total=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales)
                    )

                    inter = []
                    for t in tipos:     
                        sol=LicenciaAsignada.objects.filter(
                            id__in=total.values('id'),
                            tipo_licenciaid=t
                        ).count()   
                        inter.append({'cantidad': sol, 'show_name': t.nombre})
                    consulta.append({'datos': inter, 'show_name': 'Total', 'total':total.count()})

                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':
                        template = get_template('documentos/reportes/distribucion_librospdf.html')
                        html = template.render(Context({'data':{'consulta': consulta, 'tipos': tipos}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(),content_type='application/pdf')


                context.update({
                    'actor': user.get_full_name(),
                    'consulta': consulta,
                    'tipos': tipos,
                })

                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                user = funcionario.tiporol.nombre
                context.update({user: True})
                return render(request, 'coordinador_ct/distribucion_libros.html', context)

            elif reporte == 'comparativoeat':

                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('solicitudes') and request.GET.has_key('busqueda'):
                        params = secure_value_decode(request.GET['solicitudes'])
                        filter_dict=pickle.loads(params)

                        solicitudesCT=Solicitud.objects.filter(**filter_dict).order_by(
                            'pst', 
                            'sucursal'
                        ).distinct(
                            'pst', 
                            'sucursal'
                        )
                    else:
                        solicitudesCT=Solicitud.objects.all().order_by(
                            'pst', 
                            'sucursal'
                        ).distinct(
                            'pst', 
                            'sucursal'
                        )

                    if request.GET.has_key('tipo') and request.GET.has_key('busqueda'):
                        tipos = TipoLicencia.objects.filter(id=int(request.GET['tipo']))
                    else:
                        tipos = TipoLicencia.objects.filter(padre=TipoLicencia.objects.get(codigo = 'LIC_ALO_T'))

                    if request.GET.has_key('parroquia') and request.GET.has_key('busqueda'):
                        parroquia=Parroquia.objects.get(id=int(request.GET['parroquia']))
                        municipio=Municipio.objects.get(id=parroquia.municipio.id)
                        estados=Estado.objects.filter(id=municipio.estado.id).order_by('estado')
                    elif request.GET.has_key('municipio') and request.GET.has_key('busqueda'):
                        municipio=Municipio.objects.get(id=int(request.GET['municipio']))
                        estados=Estado.objects.filter(id=municipio.estado.id).order_by('estado')
                    elif request.GET.has_key('estado') and request.GET.has_key('busqueda'):
                        estados=Estado.objects.filter(id=int(request.GET['estado'])).order_by('estado')
                    else:
                        estados=Estado.objects.all().order_by('estado')

                    busqueda_datos.update({
                        'solicitudesCT':solicitudesCT,
                        'tipos':tipos,
                        'estados':estados
                    })
                else:
                    x=cache.get(key)
                    solicitudesCT=x['solicitudesCT']
                    estados=x['estados']
                    tipos=x['tipos']

                solicitudesPC=solicitudesCT.exclude(estatus__abreviacion__in=['A', 'NPI', 'SN'])
                solicitudesC=solicitudesCT.filter(estatus__abreviacion__in=['A', 'NPI', 'SN'])
                sol = []
                consulta= []

                estados2=estados

                mas =True
                paginars = False
                if not request.GET.has_key('opcion') and request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    est= estados
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    estados = estados[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(est[num:num+1]) ==0:
                        mas = False

                if not request.GET.has_key('opcion') and (not request.GET.has_key('p') or not request.GET.has_key('s')):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    est= estados
                    estados = estados[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(est[num:num+1]) ==0:
                        mas = False

                for e in estados:
                    #Con Categoria
                    sucursales=Sucursales.objects.filter(
                        id__in=solicitudesC.values('sucursal'),
                        estado__id=e.id
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=solicitudesC.values('pst'),
                        estado__id=e.id
                    ).values('id')

                    totalC=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales),
                        Q(tipo_licenciaid__id__in=tipos.values('id'))

                    )

                    #En proceso de categorizacion
                    sucursales=Sucursales.objects.filter(
                        id__in=solicitudesPC.values('sucursal'),
                        estado__id=e.id
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=solicitudesPC.values('pst'),
                        estado__id=e.id
                    ).values('id')

                    totalP=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales),
                        Q(tipo_licenciaid__id__in=tipos.values('id'))
                    )

                    #Sin categorizar
                    sucursales=Sucursales.objects.filter(
                        estado__id=e.id
                    ).exclude(id__in=solicitudesCT.values('sucursal')).values('id')
                    psts=Registro_Direccion.objects.filter(
                        estado__id=e.id
                    ).exclude(pst__id__in=solicitudesCT.values('pst')).values('id')

                    totalS=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales),
                        Q(tipo_licenciaid__id__in=tipos.values('id'))

                    )
                    
                    consulta.append({
                        'show_name': e.estado, 
                        'total_con':totalC.count(), 
                        'total_sin':totalS.count(), 
                        'total_pro':totalP.count(), 
                        'id_estado':e.id
                    })

                #Total de todos los Estados           
                if not mas or (request.GET.has_key('opcion') and str(request.GET['opcion'])=='verpdf'):
                    dprint(estados2)
                    #Con Categoria
                    sucursales=Sucursales.objects.filter(
                        id__in=solicitudesC.values('sucursal'),
                        estado__id__in=estados2.values('id')
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=solicitudesC.values('pst'),
                        estado__id__in=estados2.values('id')
                    ).values('id')

                    totalC=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales),
                        Q(tipo_licenciaid__id__in=tipos.values('id'))
                    )

                    #En proceso de categorizacion
                    sucursales=Sucursales.objects.filter(
                        id__in=solicitudesPC.values('sucursal'),
                        estado__id__in=estados2.values('id')
                    ).values('id')
                    psts=Registro_Direccion.objects.filter(
                        pst__id__in=solicitudesPC.values('pst'),
                        estado__id__in=estados2.values('id')
                    ).values('id')

                    totalP=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales),
                        Q(tipo_licenciaid__id__in=tipos.values('id'))
                    )

                    #Sin categorizar
                    sucursales=Sucursales.objects.filter(
                        estado__id__in=estados2.values('id')
                    ).exclude(
                        id__in=solicitudesCT.values('sucursal')
                    ).values('id')

                    psts=Registro_Direccion.objects.filter(
                        estado__id__in=estados2.values('id')
                    ).exclude(
                        pst__id__in=solicitudesCT.values('pst')
                    ).values('id')

                    totalS=LicenciaAsignada.objects.filter(
                        Q(usuario_pst__id__in=psts) | 
                        Q(sucursal__id__in=sucursales),
                        Q(tipo_licenciaid__id__in=tipos.values('id'))
                    )
                    
                    consulta.append({
                        'show_name': 'Total', 
                        'total_con':totalC.count(), 
                        'total_sin':totalS.count(), 
                        'total_pro':totalP.count(), 
                        'id_estado':'total'
                    })

                if request.GET.has_key('opcion'):
                    if str(request.GET['opcion'])=='verpdf':
                        template = get_template('documentos/reportes/comparativo_eatpdf.html')
                        html = template.render(Context({'data':{'consulta': consulta}}))
                        result = BytesIO()
                        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                        return HttpResponse(result.getvalue(),content_type='application/pdf')


                context.update({
                    'actor': user.get_full_name(),
                    'consulta': consulta
                })

                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                user = funcionario.tiporol.nombre
                context.update({user: True})

                return render(request, 'coordinador_ct/comparativo_eat.html', context)

            elif reporte == 'pstsincategorizar':
                estado_id=request.GET['estado_id']
                estado=request.GET['estado']
                solicitudesCT=Solicitud.objects.all().order_by(
                    'pst', 
                    'sucursal'
                ).distinct(
                    'pst', 
                    'sucursal'
                )
                if estado_id == 'total':
                    sucursales=Sucursales.objects.all().exclude(
                        id__in=solicitudesCT.values('sucursal')
                    ).values('id')
                    psts=Registro_Direccion.objects.all().exclude(
                        pst__id__in=solicitudesCT.values('pst')
                    ).values('id')
                else: 
                    sucursales=Sucursales.objects.filter(
                        estado__id=estado_id
                    ).exclude(id__in=solicitudesCT.values('sucursal')).values('id')
                    psts=Registro_Direccion.objects.filter(
                        estado__id=estado_id
                    ).exclude(pst__id__in=solicitudesCT.values('pst')).values('id')

                licencias=LicenciaAsignada.objects.filter(
                    Q(usuario_pst__id__in=psts) | 
                    Q(sucursal__id__in=sucursales),
                    Q(tipo_licenciaid__padre=TipoLicencia.objects.get(codigo = 'LIC_ALO_T'))
                )

                consulta=[]
                for l in licencias:
                    pst=Pst.objects.filter(user=l.usuario_pst).first()
                    contacto=RepresentanteContacto.objects.filter(pst=l.usuario_pst).first()
                    dprint(contacto)
                    rtn=CertificacionRTN.objects.filter(pst=pst).first()
                    consulta.append({
                        'rif': l.usuario_pst.rif,
                        'rtn': rtn.rtn if rtn else " ",
                        'razon_social': pst.razon_social,
                        'sucursal': l.sucursal.nombre if l.sucursal else "Sede Principal",
                        'representante': contacto.nombres + " " + contacto.apellidos if contacto else " ",
                        'tlf': contacto.telefono_fijo + " / " + contacto.telefono_celular if contacto else " ",
                        'correo': contacto.correo_electronico if contacto else " "
                    })

                template = get_template('documentos/reportes/pstsincategorizarpdf.html')
                html = template.render(Context({'data':{'consulta': consulta, 'estado':estado}}))
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=result)
                return HttpResponse(result.getvalue(),content_type='application/pdf')

          

        except Exception, e:
            raise e


class PortalLsr(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(PortalLsr, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            user = request.user
            id_sesion = user.id
            natural = juridica = False
            busqueda_datos={}
            key='busqueda_cache'

            if user.role == ROLE_PST:
                pst = user.pst_set.get()            

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True

                op=kwargs['operacion']
                context={}
                if op == 'entradas':
                    if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                        cache.delete(key)
                        if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                            dprint(decode=request.GET['solicitudes'])
                            params = secure_value_decode(request.GET['solicitudes'])
                            dprint(params=params)
                            filter_dict=pickle.loads(params)
                            dprint(filter_dict=filter_dict)
                            entradas=Entrada.objects.filter(
                                lsr__pst=pst, **filter_dict
                            ).order_by('fecha_entrada', 'severidad')
                            #).order_by('severidad', 'fecha_entrada')
                        else:
                           # entradas=Entrada.objects.filter(lsr__pst=pst).order_by('severidad', 'fecha_entrada')
                           entradas=Entrada.objects.filter(lsr__pst=pst).order_by('fecha_entrada', 'severidad')
                        busqueda_datos.update({'entradas':entradas})
                    else:
                        x=cache.get(key)
                        entradas=x['entradas']
                    
                    paginars = False
                    mas = True 
                    if request.GET.has_key('p') and request.GET.has_key('s'): 
                        paginars = True
                        p= int(request.GET['p'])
                        s= request.GET['s']
                        dprint(s)
                        if s == '-':
                            p -= 1
                        elif s == '+':
                            dprint(s)
                            p += 1
                        ent= entradas
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        entradas = entradas[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(ent[num:num+1]) ==0:
                            mas = False

                    if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                        p= 0
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        paginars = True
                        ent= entradas
                        entradas = entradas[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(ent[num:num+1]) ==0:
                            mas = False


                    context.update({
                        'pst': pst,
                        'entradas': entradas,
                        'natural': natural,
                        'juridica': juridica
                    })
                    if paginars == True:
                        context.update({'p': p, 'mas': mas})
                    if request.GET.has_key('busqueda'):
                        cache.set(
                            key,
                            busqueda_datos
                        )
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        solicit = quote_plus(request.GET['solicitudes'])
                        context.update({'sol_buscar': solicit, 'busqueda':True})

                    return render(request, 'pst/entradasLSR.html', context)

                elif op == 'verentrada':


                    id_entrada=int(request.GET['entrada'])
                    entrada=Entrada.objects.get(id=id_entrada)
                    respuesta=RespuestaLsr.objects.filter(entrada=entrada).first()

                    encuesta=RespuestaEncuesta.objects.filter(
                        entrada=entrada).order_by(
                            'seccion_encuesta', 
                            'valoracion__tipo_valoracion').distinct(
                                'seccion_encuesta', 
                                'valoracion__tipo_valoracion')
                    seccion={}

                    for e in encuesta:
                        item=Valoracion.objects.filter(
                            tipo_valoracion=e.valoracion.tipo_valoracion).aggregate(
                                Max('puntaje'), 
                                Min('puntaje'))
                        if not seccion.has_key(e.seccion_encuesta.nombre):
                            seccion.update({e.seccion_encuesta.nombre:[]})
                        seccion[e.seccion_encuesta.nombre].append(
                            {
                                'id_s':e.seccion_encuesta.id, 
                                'id_val':e.valoracion.tipo_valoracion.id,
                                'elementos': RespuestaEncuesta.objects.filter(
                                    seccion_encuesta=e.seccion_encuesta,
                                    valoracion__tipo_valoracion=e.valoracion.tipo_valoracion
                                ),
                                'valores':Valoracion.objects.filter(
                                    tipo_valoracion=e.valoracion.tipo_valoracion
                                ),
                                'maximo':item['puntaje__max'],
                                'minimo':item['puntaje__min']-1
                            }
                        )

                    context.update({
                        'pst': pst,
                        'respuesta': respuesta,
                        'entrada': entrada,
                        'secciones': seccion,
                        'natural': natural,
                        'juridica': juridica
                    })

                    return render(request, 'pst/entrada.html', context)
        except Exception, e:
            raise e

    def post(self, request, *args, **kwargs):

        try:
            user = request.user
            id_sesion = user.id
            natural = juridica = False

            if user.role == ROLE_PST:
                pst = user.pst_set.get()            

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True               
                op=kwargs['operacion']
                context={}
                if op == 'responder':
                    entrada_id=int(request.POST['entrada'])
                    dprint(request.POST['entrada'])
                    respuesta_pst=request.POST['respuesta']

                    entrada=Entrada.objects.get(id=entrada_id)
                    respuesta = RespuestaLsr(
                        emisor=pst,
                        comentario=respuesta_pst,
                        entrada=entrada)
                    entrada.estatus=Estatus.objects.get(abreviacion='R')
                    entrada.save()
                    respuesta.save()

                    #<--- Envio de Correo --->
                    htmly = get_template('correo/entrada_respondida.html')
                    text_plain = get_template('correo/entrada_respondida.txt')

                    context = Context({
                        'tipo_entrada': entrada.tipo_comentario,
                        'respuesta': respuesta_pst,
                        'nombre_turista': entrada.turista.nombre+' '+entrada.turista.apellido if entrada.turista.nombre is not None else "Anónimo",
                        'razon_social': entrada.lsr.pst.razon_social
                     })

                    html_content = htmly.render(context)
                    text_content = text_plain.render(context)
                    """
                    Busqueda de correo en parametros de configuracion
                    try:
                        corr = ParametroConfiguracion.objects.get(
                            clave="correo_interno"
                            )
                    except ParametroConfiguracion.DoesNotExist:
                        raise e
                    corrs = str(corr.valor)
                    """

                    thread_correo = threading.Thread(
                        name='thread_correo', 
                        target=correo, 
                        args=(
                            u'[MINTUR] Entrada respondida',  
                            html_content, 
                            text_content, 
                            'gccdev@cgtscorp.com', 
                            ['gccdev@cgtscorp.com'], 
                            None, 
                            None)
                        )
                    thread_correo.start()

                    return HttpResponse(status=200)

        except Exception, e:
            raise e


class EntradaLibroLsr(View):
    def dispatch(self, *args, **kwargs):
        return super(EntradaLibroLsr, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            turista = True
            op=kwargs['operacion']
            context={}
            if op == 'formulario':
                lsr=LsrDigital.objects.all().distinct('sucursal')
                #sucursal=Sucursales.objects.filter(id__in=a)
                tipo=TipoComentario.objects.all()
                severidad=Severidad.objects.all()
                ciudad=Ciudad.objects.all()
                tipodocumento=TipoDocumentoIdentidad.objects.all()
                context.update({
                    'lsr':lsr,
                    'turista': turista,
                    'tipo': tipo,
                    'severidad': severidad,
                    'ciudad':ciudad,
                    'tipodocumento':tipodocumento
                })
                return render(request, 'turista/formulario.html', context) 

            elif op == 'mostrarencuesta':
                entrada=Entrada.objects.get(id=int(request.GET['entrada']))
                tipo = otp_prestador(entrada.lsr.pst, entrada.lsr.sucursal)
                elem=ElementoEncuestaSeccionEncuesta.objects.filter(
                    Q(encuesta__tipo_pst= tipo.padre) | 
                    Q(encuesta__tipo_pst=tipo)).values(
                    'seccion_encuesta_id',
                    'seccion_encuesta__nombre',
                    'elemento_encuesta_id',
                    'elemento_encuesta__nombre'
                    ).order_by('seccion_encuesta', 'elemento_encuesta')
                valoracion = []
                for e in elem:
                    tipo_valoracion = ElementoEncuesta.objects.get(id=e['elemento_encuesta_id']).tipo_valoracion.id 
                    x= Valoracion.objects.filter(tipo_valoracion_id = tipo_valoracion).order_by('id')
                    aux = []
                    for e in x:
                        aux.append((e.id,e.nombre))
                    valoracion.append(aux)

                if len(elem):
                    encuesta=zip(elem,valoracion)
                    jsontmp = {
                        "data": {"encuesta": encuesta}
                    }
                    status_code = 200
                else:
                    jsontmp ={
                        "error": 'No hay encuesta configuradas para el tipo de prestador seleccionado'
                    }
                    status_code = 400

                r = HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json"
                )
                r.status_code = status_code
                return r
        except Exception, e:
            raise e

    def post(self, request, *args, **kwargs):

        try:             
            op=kwargs['operacion']
            context={}

            if op == 'enviarformulario':
                anonimo = request.POST['anonimo']
                if request.POST['correo']:
                    if str(request.POST['tipo'])!='-1' and int(request.POST['lsr'])>0 and request.POST['observaciones']:
                        tipo=request.POST['tipo']
                    else:
                        raise FieldError("Faltan datos de la entrada")

                    if anonimo == 'no':
                        if request.POST['nombre'] and request.POST['apellido'] and int(request.POST['tipodoc'])>0 and request.POST['numerodoc'] and request.POST['telefono'] and int(request.POST['ciudad'])>0:
                            if not Turista.objects.filter(correo_electronico=request.POST['correo']).first():
                                turista = Turista(
                                    nombre = request.POST['nombre'],
                                    apellido = request.POST['apellido'],
                                    tipo_documento_identidad=TipoDocumentoIdentidad.objects.get(id=int(request.POST['tipodoc'])),
                                    numero_documento_identidad= request.POST['numerodoc'],
                                    telefono_contacto= request.POST['telefono'],
                                    correo_electronico= request.POST['correo'],
                                    ciudad_id=int(request.POST['ciudad'])
                                    )
                            else:
                                turista=Turista.objects.get(correo_electronico=request.POST['correo'])
                                if not turista.nombre:
                                    turista.nombre = request.POST['nombre']
                                    turista.apellido = request.POST['apellido']
                                    turista.tipo_documento_identidad=TipoDocumentoIdentidad.objects.get(id=int(request.POST['tipodoc']))
                                    turista.numero_documento_identidad= request.POST['numerodoc']
                                    turista.telefono_contacto= request.POST['telefono']
                                    turista.ciudad=Ciudad.objects.get(id=int(request.POST['ciudad']))

                            turista.save()

                            es_anonimo=False
                        else:
                            raise FieldError("Faltan datos del Turista")

                    else:
                        if not Turista.objects.filter(correo_electronico=request.POST['correo']).first():
                            turista = Turista(
                                correo_electronico= request.POST['correo']
                                )
                            turista.save()
                        es_anonimo=True

                else:
                    raise FieldError("El correo del Turista es obligatorio")

                if tipo == 'F':
                    severidad=None
                else:
                    if int(request.POST['severidad'])>0:
                        severidad=request.POST['severidad']
                    else:
                        raise FieldError("La severidad es requerida para este tipo de entrada")
                entrada= Entrada(
                    tipo_comentario = TipoComentario.objects.get(abreviacion = tipo),
                    turista = Turista.objects.get(correo_electronico = request.POST['correo']),
                    lsr = LsrDigital.objects.get(id = int(request.POST['lsr'])),
                    severidad_id = severidad,
                    estatus = Estatus.objects.get(abreviacion = 'SR'),
                    comentario = request.POST['observaciones'],
                    fecha_entrada = datetime.datetime.now(),
                    es_anonimo=es_anonimo
                    )
                entrada.save()
                jsontmp = {
                "data": {"id_entrada": entrada.id}
                }
                return HttpResponse(
                    json.dumps(jsontmp, sort_keys=False),
                    content_type="application/json",
                    status=200
                )
            elif op=='enviarencuesta':
                entrada=Entrada.objects.get(id=int(request.POST['identrada']))
                elementos=ElementoEncuestaSeccionEncuesta.objects.filter(
                    encuesta__tipo_pst=otp_prestador(entrada.lsr.pst, entrada.lsr.sucursal)).values_list(
                    'seccion_encuesta_id',
                    'elemento_encuesta_id',
                    )
                for e in elementos:
                    if request.POST.has_key('respuesta_'+str(e[0])+'_'+str(e[1])):
                        if request.POST.has_key('observacion_'+str(e[0])+'_'+str(e[1])):
                            observacion=str(request.POST['observacion_'+str(e[0])+'_'+str(e[1])])
                        else:
                            observacion=None
                        respuesta=RespuestaEncuesta(
                            entrada=entrada,
                            valoracion_id=int(request.POST['respuesta_'+str(e[0])+'_'+str(e[1])]),
                            elemento_encuesta_id=int(e[1]),
                            seccion_encuesta_id=int(e[0]),
                            observacion=observacion
                        )
                        respuesta.save()
                return HttpResponseRedirect(reverse('entrada_turista', kwargs={'operacion': 'formulario'}))

        except Exception, e:
            return  HttpResponse(str(e), content_type="application/json", status=400)


class DirectorCTOperacion(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(DirectorCTOperacion, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            user = request.user
            id_sesion = user.id
            funcionario = Funcionario.objects.get(user_id=int(id_sesion))
            op=kwargs['operacion']
            context={}
            busqueda_datos={}
            key='busqueda_cache'

            if op == 'procesos':
                analistas={}
                inspectores={}
                directoresct={}
                coordinadoresct={}
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        if filter_dict.has_key('adicional'):
                            array_texto = filter_dict['adicional']
                            filter_dict.pop('adicional')
                            solicitudes = Solicitud.objects.filter(
                                reduce(operator.or_,array_texto),**filter_dict
                            ).order_by('-fecha_apertura')
                        else:
                           solicitudes = Solicitud.objects.filter(**filter_dict).order_by('-fecha_apertura')
                    else:
                        solicitudes=Solicitud.objects.order_by('-fecha_apertura')
                    busqueda_datos.update({'solicitudes':solicitudes})
                else:
                    x=cache.get(key)
                    solicitudes=x['solicitudes']
                    
                mas= True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    sol= solicitudes
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    sol= solicitudes
                    solicitudes = solicitudes[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(sol[num:num+1]) ==0:
                        mas = False

                sol_abierta = False
                if solicitudes:
                    if solicitudes[0].fecha_clausura is None:
                        sol_abierta = True

                clasificaciones = []
                for s in solicitudes:

                    mx = Categoria.objects.filter(
                        tipo_pst = otp_prestador(s.pst, s.sucursal)
                    ).count()
                    
                    if s.pst_categoria_doc is not None:
                        clasificaciones.append(
                            (
                                s.pst_categoria_doc.categoria.valor, 
                                mx - s.pst_categoria_doc.categoria.valor
                            )
                        )
                    else:
                        clasificaciones.append(
                            (
                                0,
                                mx
                            )
                        )

                    asignaciones=Asignacion.objects.filter(
                        solicitud=s).order_by(
                        'funcionario', 
                        '-fecha_asignacion').distinct(
                            'funcionario')
                    for a in asignaciones:
                        nombre = a.funcionario.nombre+" "+a.funcionario.apellido
                        if a.funcionario.tiporol.nombre == 'analista':
                            if not analistas.has_key(s.id):
                                analistas.update({s.id:[]})
                            analistas[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion
                                }
                            )
                        elif a.funcionario.tiporol.nombre == 'inspector':
                            if not inspectores.has_key(s.id):
                                inspectores.update({s.id:[]})
                            try:
                                Notificacion.objects.get(
                                    receptor__id=a.funcionario.user.id, 
                                    estatus_actual__abreviacion='EI',
                                    solicitud=a.solicitud)
                                estatus= "Con Credenciales"
                            except:
                                estatus= "Sin Credenciales"
                            inspectores[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion,
                                    'estatus': estatus
                                }
                            )
                        elif a.funcionario.tiporol.nombre == 'coordinador_ct':
                            if not coordinadoresct.has_key(s.id):
                                coordinadoresct.update({s.id:[]})
                            coordinadoresct[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion
                                }
                            )
                        elif a.funcionario.tiporol.nombre == 'director_ct':
                            if not directoresct.has_key(s.id):
                                directoresct.update({s.id:[]})
                            directoresct[s.id].append(
                                {
                                    'nombre': nombre.capitalize(),
                                    'fecha': a.fecha_asignacion
                                }
                            )
                sol_cat= zip(solicitudes,clasificaciones)
                context.update({
                    'actor': user.get_full_name(),
                    'solicitudes': sol_cat,
                    'analistas': analistas,
                    'coordinadoresct' : coordinadoresct,
                    'inspectores' : inspectores,
                    'directoresct': directoresct,
                    'tiporol': funcionario.tiporol.nombre
                })

                user = funcionario.tiporol.nombre
                context.update({user: True})

                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})

                return render(request, 'director_ct/procesos.html', context)
            
            elif op == 'verproceso':
                id_solicitud=int(request.GET['solicitud'])
                solicitud=Solicitud.objects.get(id=id_solicitud)
                notificaciones=Notificacion.objects.filter(solicitud=solicitud)
                documentos=NotificacionDocumentoCompuesto.objects.filter(
                    Q(notificacion__solicitud=solicitud)
                    | Q(notificacion_backup__solicitud=solicitud)).distinct('documento')

                x=list(notificaciones.values())
                y=list(NotificacionBackup.objects.filter(solicitud=solicitud).values())

                l=x+y

                l.sort(order)
                historia=[]
                for n in l:
                    try:
                        f=Funcionario.objects.get(user_id=n['receptor_id'])
                        f=f.nombre+" "+f.apellido
                    except:
                        f="-"
                    estatus=Estatus.objects.get(id=n['estatus_actual_id'])
                    historia.append(
                        {
                            'fecha': n['fecha_emision'], 
                            'estatus': estatus.nombre,
                            'funcionario': f,
                            'abreviacion_estatus': estatus.abreviacion,
                            'des_estatus': estatus.descripcion
                        }
                    )

                funcionarios_doc={}
                for n in documentos:
                    if n.notificacion:
                        if not n.notificacion.emisor.is_pst():
                            funcionarios_doc.update({n.id:n.notificacion.emisor.nombres+" "+n.notificacion.emisor.apellidos})
                    elif n.notificacion_backup:
                        if not n.notificacion_backup.emisor.is_pst():
                            funcionarios_doc.update({n.id:n.notificacion_backup.emisor.nombres+" "+n.notificacion_backup.emisor.apellidos})
                   
                context.update({
                    'actor': user.get_full_name(),
                    'funcionarios_doc': funcionarios_doc,
                    'historial': historia,
                    'documentos': documentos,
                    'solicitud': solicitud
                })

                user = funcionario.tiporol.nombre
                context.update({user: True})

                return render(request, 'director_ct/proceso.html', context)
        except Exception, e:
            raise e


class ObtenerRequisitosDocumentales(View):    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(ObtenerRequisitosDocumentales, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        sucursal = None
        if kwargs.has_key("sucursal"):
            sucursal = int(kwargs["sucursal"])
            if sucursal == 0:
                sucursal = None

            user = request.user
            pst = Pst.objects.get(user = user)

            rd = SubseccionConfig.objects.filter(
                Q(tipo_subseccion__abreviacion='RD')|Q(tipo_subseccion__tipopadre__abreviacion= constants.TIPO_SUBSECCIONES['req_doc']),
                Q(seccion_config__aspecto_config__tabulador = obtener_tabulador_actual.version_actual(
                    otp_prestador(pst, sucursal))
                ),
                Q(creado_en__isnull=True)
            )

            r = [e.to_json() for e in rd]

            res = HttpResponse(
                json.dumps(r, sort_keys=False),
                content_type="application/json"
                )
            res.status_code = 200
            return res
        else:
            res = HttpResponse(
                json.dumps(
                    {"err_msg": "No se han encontrado requisitos documentales asociados (Contacte con nuestro personal para mas asitencia)"},
                    sort_keys=False),
                content_type="application/json"
            )
            res.status_code = 400
            return res


class BandejaPlaca(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(BandejaPlaca, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):   
        
        try:
            user = request.user
            id_sesion = user.id
            natural = juridica = False
            placas={}
            busqueda_datos={}
            key='busqueda_cache'

            if user.role == ROLE_FUNCIONARIO:
                funcionario = Funcionario.objects.get(user=user)
                """
                pst = user.pst_set.get()   

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True
                tipo=TipoLicencia.objects.filter(
                    Q(codigo='LIC_ALIM_BEBI') | Q(padre__codigo='LIC_ALIM_BEBI') |
                    Q(codigo='LIC_AGEN_T') | Q(padre__codigo='LIC_AGEN_T') |
                    Q(codigo='LIC_TRANS_T') | Q(padre__codigo='LIC_TRANS_T') |
                    Q(padre__codigo='LIC_ALO_T')
                )
                """

                activar_placa=False
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        placas_sinfirmar=Placa.objects.filter(**filter_dict).exclude(documento__firmado=True)
                        #sucursales=LicenciaAsignada.objects.filter(**filter_dict)
                        #sucursales=LicenciaAsignada.objects.filter(usuario_pst=pst, **filter_dict)
                    else:
                        placas_sinfirmar=Placa.objects.exclude(documento__firmado=True)
                        #sucursales=LicenciaAsignada.objects.filter(tipo_licenciaid__in=tipo)
                        #sucursales=LicenciaAsignada.objects.filter(tipo_licenciaid__in=tipo, usuario_pst=pst)
                    busqueda_datos.update({'placas_sinfirmar':placas_sinfirmar})
                else:
                    x=cache.get(key)
                    placas_sinfirmar=x['placas_sinfirmar']

                mas= True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    pla= placas_sinfirmar
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    placas_sinfirmar = placas_sinfirmar[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(pla[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    pla= placas_sinfirmar
                    placas_sinfirmar = placas_sinfirmar[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(pla[num:num+1]) ==0:
                        mas = False
 
                for pl in placas_sinfirmar:
                    s=pl.licencia_asignada
                    """
                    x=list(Notificacion.objects.filter(
                        solicitud__sucursal=s.sucursal, 
                        solicitud__pst=pl.pst, 
                        estatus_actual__abreviacion='A').values())
                    y=list(NotificacionBackup.objects.filter(
                        solicitud__sucursal=s.sucursal, 
                        solicitud__pst=pl.pst, 
                        estatus_actual__abreviacion='A').values())

                    l=x+y
                    l.sort(order)
                    """

                    activar_placa=True
                    """
                    #La validación debe ser si tiene diseño publicado o no
                    if s.tipo_licenciaid.padre.codigo != 'LIC_ALO_T':
                        dprint("---")
                        if not placas.has_key(s.id):
                            placas.update({s.id:[]})
                        
                        if val == True:
                            if cont2 == cont1:
                                cont2+=1
                                continue
                            elif cont2>=cont:
                                placas[s.id].append(
                                {
                                    'rtn': pl.pst.rtn,
                                    'licencia': s.numero_licencia,
                                    'tipo_lic':s.tipo_licenciaid.nombre,
                                    'sucursal': s.sucursal.nombre if s.sucursal is not None else "Sede Principal"
                                }
                                )
                                cont2+=1
                            elif cont2<cont:
                                cont2+=1
                        else:
                        
                        placas[s.id].append(
                            {
                            'rtn': pl.pst.rtn,
                            'licencia': s.numero_licencia,
                            'tipo_lic':s.tipo_licenciaid.nombre,
                            'sucursal': s.sucursal.nombre if s.sucursal is not None else "Sede Principal"
                            }
                        )

                    elif s.tipo_licenciaid.padre.codigo == 'LIC_ALO_T':
                    """
                    if not placas.has_key(s.id):
                        placas.update({s.id:[]})
                        """
                        if val == True:
                            if cont2 == cont1:
                                cont2+=1
                                continue
                            elif cont2 >= cont:
                                placas[s.id].append(
                                    {
                                        'rtn': pl.pst.rtn,
                                        'licencia': s.numero_licencia,
                                        'tipo_lic':s.tipo_licenciaid.nombre,
                                        'sucursal': s.sucursal.nombre if s.sucursal is not None else "Sede Principal"
                                    }
                                )
                                cont2+=1
                            elif cont2<cont:
                                cont2+=1

                        else:
                        """
                    placas[s.id].append(
                            {
                                'rtn': pl.pst.rtn,
                                'licencia': s.numero_licencia,
                                'tipo_lic':s.tipo_licenciaid.nombre,
                                'sucursal': s.sucursal.nombre if s.sucursal is not None else "Sede Principal"
                            }
                        )
                """
                if val == True:
                    if cont2-1 == cont1:
                        mas = True
                """
                if request.session.has_key('error'):
                    errors = request.session['error']
                    del request.session['error']
                else:
                    errors=""
                context={
                    'activar_placa': activar_placa,
                    """
                    'pst': pst,
                    'natural':natural,
                    'juridica':juridica,
                    """
                    'tiporol': funcionario.tiporol.nombre,
                    'error': errors,
                    'actor': user.get_full_name(),
                    'placas':placas
                }
                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                dprint(context=context)

                user = funcionario.tiporol.nombre
                context.update({user: True})

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})
                #TODO: Cambiar HTML
                return render(request, 'placas.html', context)

            elif user.role == ROLE_PST:
                pst = user.pst_set.get() 

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True

                activar_placa=False
                if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                    cache.delete(key)
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        dprint(decode=request.GET['solicitudes'])
                        params = secure_value_decode(request.GET['solicitudes'])
                        dprint(params=params)
                        filter_dict=pickle.loads(params)
                        dprint(filter_dict=filter_dict)
                        placas_sinfirmar=Placa.objects.filter(documento__firmado=True, pst__user=pst, **filter_dict)
                        #sucursales=LicenciaAsignada.objects.filter(**filter_dict)
                        #sucursales=LicenciaAsignada.objects.filter(usuario_pst=pst, **filter_dict)
                    else:
                        placas_sinfirmar=Placa.objects.filter(documento__firmado=True, pst__user=pst)
                    busqueda_datos.update({'placas_sinfirmar':placas_sinfirmar})
                else:
                    x=cache.get(key)
                    placas_sinfirmar=x['placas_sinfirmar']

            
                mas= True
                paginars = False
                if request.GET.has_key('p') and request.GET.has_key('s'): 
                    paginars = True
                    p= int(request.GET['p'])
                    s= request.GET['s']
                    dprint(s)
                    if s == '-':
                        p -= 1
                    elif s == '+':
                        dprint(s)
                        p += 1
                    pla= placas_sinfirmar
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    placas_sinfirmar = placas_sinfirmar[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(pla[num:num+1]) ==0:
                        mas = False

                if  not request.GET.has_key('p') or not request.GET.has_key('s'):
                    p= 0
                    num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                    paginars = True
                    pla= placas_sinfirmar
                    placas_sinfirmar = placas_sinfirmar[(p*constants.ELEMENTO_POR_PAGINA):num]
                    if len(pla[num:num+1]) ==0:
                        mas = False
 
                for pl in placas_sinfirmar:
                    s=pl.licencia_asignada
                    activar_placa=True
                    if not placas.has_key(s.id):
                        placas.update({s.id:[]})
                    placas[s.id].append(
                            {
                                'rtn': pl.pst.rtn,
                                'licencia': s.numero_licencia,
                                'tipo_lic':s.tipo_licenciaid.nombre,
                                'sucursal': s.sucursal.nombre if s.sucursal is not None else "Sede Principal"
                            }
                        )

                if request.session.has_key('error'):
                    errors = request.session['error']
                    del request.session['error']
                else:
                    errors=""
                context={
                    'activar_placa': activar_placa,
                    'pst': pst,
                    'natural':natural,
                    'juridica':juridica,
                    'error': errors,
                    'actor': user.get_full_name(),
                    'placas':placas
                }
                if paginars == True:
                    context.update({'p': p, 'mas': mas})

                if request.GET.has_key('busqueda'):
                    cache.set(
                        key,
                        busqueda_datos
                    )

                dprint(context=context)
                """
                user = funcionario.tiporol.nombre
                context.update({user: True})
                """

                if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                    solicit = quote_plus(request.GET['solicitudes'])
                    context.update({'sol_buscar': solicit, 'busqueda':True})
                return render(request, 'pst/placas.html', context)
        except Exception, e:
            raise e

class OficiosRespuesta(View):
    
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(OficiosRespuesta, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            
            user = request.user
            id_sesion = user.id
            natural = juridica = False

            op = kwargs['operacion']

            if op == 'bandeja':

                if request.session.has_key('error'):
                    error = request.session['error']
                    request.session.__delitem__('error')
                else:
                    error = None

                busqueda_datos={}
                key='busqueda_cache'
                if user.role == ROLE_PST:

                    pst = user.pst_set.get()            

                    if pst.tipo_figura == PERSONA_NATURAL:
                        natural = True
                    else:
                        juridica = True

                    #consignaciones=Consignacion.objects.filter(pst=pst)

                    if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                        cache.delete(key)
                        if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                            dprint(decode=request.GET['solicitudes'])
                            params = secure_value_decode(request.GET['solicitudes'])
                            dprint(params=params)
                            filter_dict=pickle.loads(params)
                            dprint(filter_dict=filter_dict)
                            if filter_dict.has_key('adicional'):
                                array_texto = filter_dict['adicional']
                                filter_dict.pop('adicional')
                                solicitudes = SolicitudLibro.objects.filter(
                                    reduce(operator.or_,array_texto), **filter_dict
                                ).order_by('-fecha_realizacion')
                            else:    
                                solicitudes = SolicitudLibro.objects.filter(
                                    **filter_dict).order_by(
                                    '-fecha_realizacion'
                                )
                            consignaciones = Consignacion.objects.filter(
                                lsr_fisico__pst=pst,
                                solicitud_libro_id__in=solicitudes.values('id')
                            )                    
                        else:
                            consignaciones = Consignacion.objects.filter(lsr_fisico__pst=pst, estatus__abreviacion='ORE')
                        busqueda_datos.update({'consignaciones':consignaciones})
                    else:
                        x=cache.get(key)
                        consignaciones=x['consignaciones']
                    
                    mas =True
                    paginars = False
                    if request.GET.has_key('p') and request.GET.has_key('s'): 
                        paginars = True
                        p= int(request.GET['p'])
                        s= request.GET['s']
                        if s == '-':
                            p -= 1
                        elif s == '+':
                            dprint(s)
                            p += 1
                        con= consignaciones
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        consignaciones = consignaciones[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(con[num:num+1]) ==0:
                            mas = False

                    if not request.GET.has_key('p') or not request.GET.has_key('s'):
                        p= 0
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        paginars = True
                        con= consignaciones
                        consignaciones = consignaciones[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(con[num:num+1]) ==0:
                            mas = False

                    notificacion={}
                    documentos={}      

                    for c in consignaciones:

                        n=Notificacion.objects.filter(
                            solicitud_libro = c.solicitud_libro,
                            receptor_id = int(id_sesion)
                        ).order_by(
                            '-fecha_emision'
                        ).first()
                        
                        if n:
                            if not notificacion.has_key(c.id):
                                notificacion.update({c.id:[]})

                            try:
                                doc=NotificacionDocumentoCompuesto.objects.get(
                                    notificacion=n, 
                                    documento__tipo_documento_compuesto__abreviacion='N'
                                ).documento
                                src=doc.ruta_documento
                                extension=doc.extension
                            except:
                                src=None
                                extension=None
                            notificacion[c.id].append(
                                {
                                    'observacion': n.observacion,
                                    'src': src,
                                    'extension': extension
                                }
                            )

                        #Documentos asociados
                        notificacion_doc= NotificacionDocumentoCompuesto.objects.filter(
                            documento=c.documento
                        )

                        if notificacion_doc:
                            if not documentos.has_key(c.id):
                                documentos.update({c.id:[]})

                            for doc in notificacion_doc:
                                documentos[c.id].append(
                                    {
                                        'nombre': doc.documento.tipo_documento_compuesto.nombre,
                                        #'abreviacion': doc.documento.tipo_documento_compuesto.abreviacion,
                                        'ruta': doc.documento.ruta_documento
                                    }
                            )

                    documentos={}
                    context={
                        'pst': pst,
                        'natural':natural,
                        'juridica':juridica,
                        'actor': user.get_full_name(),
                        'consignaciones': consignaciones,
                        'documentos': documentos,      
                        'error': error,
                    }
                    if paginars == True:
                        context.update({'p': p, 'mas': mas})

                    if request.GET.has_key('busqueda'):
                        cache.set(
                            key,
                            busqueda_datos
                        )

                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        solicit = quote_plus(request.GET['solicitudes'])
                        context.update({'busqueda':True})

                    return render(request, 'LSR/consignaciones.html', context)
                    
                elif user.role == ROLE_FUNCIONARIO:
                    funcionario = Funcionario.objects.get(user_id=int(id_sesion))

                    if funcionario.tiporol.nombre == "administrador":
                        raise Http404

                    asignaciones=Asignacion.objects.filter(
                        funcionario=funcionario,
                        asignacion_habilitada=True
                    ).values('solicitud_libro')

                    if cache.get(key) is None or request.GET.has_key('busqueda') or (request.GET.has_key('ver') and request.GET['ver'] == 'todo'):
                        cache.delete(key)
                        if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                            dprint(decode=request.GET['solicitudes'])
                            params = secure_value_decode(request.GET['solicitudes'])
                            dprint(params=params)
                            filter_dict=pickle.loads(params)
                            dprint(filter_dict=filter_dict)
                            if filter_dict.has_key('adicional'):
                                array_texto = filter_dict['adicional']
                                filter_dict.pop('adicional')
                                solicitudes = SolicitudLibro.objects.filter(
                                    reduce(operator.or_,array_texto),id__in=asignaciones,
                                ).order_by('-fecha_realizacion')
                            else:    
                                solicitudes = SolicitudLibro.objects.filter(
                                    id__in=asignaciones).order_by(
                                    '-fecha_realizacion'
                                )
                            consignaciones = Consignacion.objects.filter(
                                solicitud_libro_id__in=solicitudes.values('id'),
                                **filter_dict
                            )                    
                        else:

                            consignaciones=Consignacion.objects.filter(
                                solicitud_libro_id__in=asignaciones
                            )
                        busqueda_datos.update({'consignaciones':consignaciones})
                    else:
                        x=cache.get(key)
                        consignaciones=x['consignaciones']

                    mas =True
                    paginars = False
                    if request.GET.has_key('p') and request.GET.has_key('s'): 
                        paginars = True
                        p= int(request.GET['p'])
                        s= request.GET['s']
                        if s == '-':
                            p -= 1
                        elif s == '+':
                            dprint(s)
                            p += 1
                        con= consignaciones
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        consignaciones = consignaciones[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(con[num:num+1]) ==0:
                            mas = False

                    if not request.GET.has_key('p') or not request.GET.has_key('s'):
                        p= 0
                        num=((p+1)*constants.ELEMENTO_POR_PAGINA)
                        paginars = True
                        con= consignaciones
                        consignaciones = consignaciones[(p*constants.ELEMENTO_POR_PAGINA):num]
                        if len(con[num:num+1]) ==0:
                            mas = False

                    notificacion={}
                    documentos={}      

                    for c in consignaciones:

                        n=Notificacion.objects.filter(
                            solicitud_libro = c.solicitud_libro,
                            receptor_id = int(id_sesion)
                        ).order_by(
                            '-fecha_emision'
                        ).first()
                        
                        if n:
                            if not notificacion.has_key(c.id):
                                notificacion.update({c.id:[]})

                            try:
                                doc=NotificacionDocumentoCompuesto.objects.get(
                                    notificacion=n, 
                                    documento__tipo_documento_compuesto__abreviacion='N'
                                ).documento
                                src=doc.ruta_documento
                                extension=doc.extension
                            except:
                                src=None
                                extension=None
                            notificacion[c.id].append(
                                {
                                    'observacion': n.observacion,
                                    'src': src,
                                    'extension': extension
                                }
                            )

                        #Documentos asociados
                        notificacion_doc= NotificacionDocumentoCompuesto.objects.filter(
                            documento=c.documento
                        )

                        if notificacion_doc:
                            if not documentos.has_key(c.id):
                                documentos.update({c.id:[]})

                            for doc in notificacion_doc:
                                documentos[c.id].append(
                                    {
                                        'nombre': doc.documento.tipo_documento_compuesto.nombre,
                                        #'abreviacion': doc.documento.tipo_documento_compuesto.abreviacion,
                                        'ruta': doc.documento.ruta_documento
                                    }
                            )

                    context={}

                    context.update({
                        'actor': user.get_full_name(),
                        'natural': natural,
                        'juridica':juridica,
                        'funcionario_id': funcionario.id,
                        'consignaciones': consignaciones,
                        'documentos': documentos,
                        'notificacion':notificacion,
                        'tiporol': funcionario.tiporol.nombre,
                    })

                    if paginars == True:
                        context.update({'p': p, 'mas': mas})

                    if request.GET.has_key('busqueda'):
                        cache.set(
                            key,
                            busqueda_datos
                        )

                    if funcionario.tiporol.nombre == 'analista':
                        folios=Folio.objects.filter(
                            lsr_fisico__solicitud_libro__funcionario=funcionario, 
                            consignacion=None
                        )

                        context.update({
                            'folios': True if len(folios) else False,
                        })
                    if request.GET.has_key('busqueda') and request.GET.has_key('solicitudes'):
                        solicit = quote_plus(request.GET['solicitudes'])
                        context.update({'sol_buscar': solicit, 'busqueda':True})

                    user = funcionario.tiporol.nombre
                    context.update({user: True})


                    return render(request, 'LSR/consignaciones.html', context)   
            else:

                if op == 'verfoliosconsignados':
                    try:
                        consignacion=request.GET['consignacion']
                        folios={}
                        f=Folio.objects.filter(consignacion__id=consignacion)
                        for x in f:
                            folios.update({x.numero:x.file_path.url})

                        jsontmp = {"folios":folios}

                        return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
                    except:
                        error="Ocurrió un error visualizando folios consignados"
                        return  HttpResponse(error, content_type="application/json", status=400)

                else:
                    #if op == 'verlibros' or op == 'verfolios':
                    try:
                        funcionario = Funcionario.objects.get(user_id=int(id_sesion))
                        if funcionario.tiporol.nombre == 'analista':
                            if op == 'verlibros':
                                libros={}

                                l=Folio.objects.filter(
                                        lsr_fisico__solicitud_libro__funcionario=funcionario, 
                                        consignacion=None
                                ).distinct('lsr_fisico')

                                for x in l:
                                    datos="%s de %s - %s" % (
                                            x.lsr_fisico.identificador,
                                            x.lsr_fisico.pst.razon_social,
                                            x.lsr_fisico.sucursal.nombre
                                    )
                                    libros.update({x.lsr_fisico.id:datos})

                                jsontmp = {'libros':libros}
                                #key = 'libros'
                                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

                            elif op == 'verfolios' and request.GET.has_key('libro'):
                                folios={}

                                f=Folio.objects.filter(
                                    lsr_fisico__id=request.GET['libro'],
                                    consignacion=None
                                )

                                for x in f:
                                    folios.update({x.numero:x.file_path.url})

                                jsontmp = {'folios':folios}
                                #key = 'folios'                       
                                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

                        else:
                            error="Esta opción no es válida"
                            return  HttpResponse(error, content_type="application/json", status=400)

                        """
                        mtemp = serializers.serialize(
                            'json',
                            jsontmp
                        )

                        return  HttpResponse(
                            json.dumps( {key:mtemp}, sort_keys=True ),
                            content_type="application/json", status=200
                        )
                        """

                    except:
                        error="No es un funcionario habilitado para esta opción"
                        return  HttpResponse(error, content_type="application/json", status=400)

        except Exception, e:
            raise e

    def post(self,request,*args,**kwargs):
        try:
            user = request.user
            id_sesion = user.id
            funcionario = Funcionario.objects.get(user_id=int(id_sesion))
            op = kwargs['operacion']

            if op == 'consignar' and funcionario.tiporol.nombre == 'analista':
                try:
                    estatus=Estatus.objects.get(abreviacion='EOR')
                    dprint(estatus=estatus)
                    dprint(id_libro=request.POST['libro'])
                    libro=LsrFisico.objects.get(id=int(request.POST['libro']))
                    
                    consignacion=Consignacion(
                        funcionario=funcionario,
                        estatus=estatus,
                        observacion=request.POST['observacion-oficiorespuesta'],
                        solicitud_libro=libro.solicitud_libro,
                        lsr_fisico=libro
                    )
                    consignacion.save()

                    notificacion=Notificacion(
                        emisor=libro.solicitud_libro.pst.user,
                        receptor=funcionario.user,
                        solicitud_libro=libro.solicitud_libro,
                        estatus_actual=estatus
                    )
                    notificacion.save()

                    folios=Folio.objects.filter(
                        lsr_fisico=libro,
                        consignacion=None
                    )
                    rango_folios="%s hasta el %s" % (folios.first().numero, folios.last().numero)
                    for f in folios:
                        f.consignacion=consignacion
                        f.save()

                    plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_respuesta_folios.html")
                    

                    try:
                        #Creando el documento
                        tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OR')
                        nombre_documento = "%s_oficio_respuesta_folios_%s" % (
                            consignacion.id,
                            libro.identificador
                        )

                        path = model_list.get_file_path(
                            libro.pst.user.rif,
                            'oficios',
                            "",
                        )

                        locationPath = os.path.join(
                            BASE_DIR,
                            'documents',
                            'files', 
                            path
                        )

                        oficio = Documento.objects.filter(nombre=nombre_documento).first()
                        if oficio:
                            oficio.fecha_emision=datetime.datetime.now()
                            oficio.eliminado=False
                        else:
                            data = Storage(
                                nombre=nombre_documento,
                                fecha_emision=datetime.datetime.now(),
                                plantilla_documento=plantilla,
                                ruta_documento = '/documents/' + path + '/' + nombre_documento + '.pdf',
                                extension = 'pdf',
                                tipo_documento_compuesto=tipo_documento,
                            )
                            oficio = Documento.create(data)
                        oficio.save()

                        consignacion.documento=oficio
                        consignacion.save()
                        #La notificacion respectiva a uno de los inspectores
                        ndc = NotificacionDocumentoCompuesto(
                            notificacion = notificacion,
                            documento = oficio
                        )
                        ndc.save()
                        texto = consignacion.observacion
                        r = re.sub('<br\s*?>', '\n',texto)
                        r = BeautifulSoup(r)

                        try:
                            #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                            direc = Registro_Direccion.objects.filter(pst=libro.pst).first()
                            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                                +str(direc.codigo_postal)
                            data = Storage(
                                nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                                oficio=oficio,
                                fecha=datetime.date.today(),
                                razon_social=libro.pst.razon_social,
                                direccion=direccionPST,
                                telefono=libro.pst.telefono_fijo if libro.pst.telefono_fijo else "" + " / " + libro.pst.telefono_celular if libro.pst.telefono_celular else "",
                                contacto=RepresentanteContacto.objects.filter(pst=libro.pst).first(),
                                numero_lsr=libro.identificador,
                                rango_folios=rango_folios,
                                rtn=libro.pst.rtn,
                                observacion=r.get_text(),
                                firma=None
                            )

                            generar_pdf.generar_pdf(
                                context=data,
                                ruta_template='documentos/oficios/oficio_respuesta_folios.html',
                                ruta_documento=locationPath,
                                nombre_documento=nombre_documento
                            )

                            locationAttach = os.path.join(
                                locationPath,
                                nombre_documento + '.pdf'
                            )
                        except Exception, error:
                            #raise e
                            return  HttpResponse(error, content_type="application/json", status=400)
                        
                    except Exception, error:
                        #raise e
                        return  HttpResponse(error, content_type="application/json", status=400)


                    return HttpResponseRedirect(
                        reverse(
                            'oficios_respuesta',
                            kwargs={'operacion': 'bandeja'}
                        )
                    )
                except Exception, error:
                    #error="Ocurrió un error generando la consignacion"
                    return  HttpResponse(error, content_type="application/json", status=400)
            elif op == 'enviar':
                
                id_c = request.POST['consignacion']
                consignacion=Consignacion.objects.get(id=id_c)
                ultima_notificacion=Notificacion.objects.filter(
                    solicitud_libro=consignacion.solicitud_libro
                    ).order_by('-fecha_emision').first()

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-enviaroficiorespuesta'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-enviaroficiorespuesta']

                tipoasig=TipoAsignacion.objects.get(abreviacion='LSR')
                if funcionario.tiporol.nombre == 'analista':
                    tiporol= TipoRol.objects.filter(nombre='director_ct').first()
                    estatus= Estatus.objects.filter(abreviacion='IOR').first()
                elif funcionario.tiporol.nombre == 'director_ct':
                    tiporol= TipoRol.objects.filter(nombre='viceministro').first()
                    estatus= Estatus.objects.filter(abreviacion='AOR').first()

                #Verificamos los fucionarios involucrados en esta solicitud
                asig=Asignacion.objects.filter(
                    solicitud_libro=consignacion.solicitud_libro, 
                    funcionario__tiporol=tiporol, 
                    asignacion_habilitada=True
                ).order_by('-fecha_asignacion').first()

                if not asig:
                    funcionario_id = algoritmo_asignacion.algoritmo_de_asignacion(tiporol.nombre)
                    asig = Asignacion(
                        funcionario_id=funcionario_id,
                        tipo_asignacion=tipoasig, 
                        solicitud_libro=consignacion.solicitud_libro,
                        fecha_asignacion=datetime.datetime.now(),
                        asignacion_habilitada=True
                        )
                    asig.save()

                receptor = Funcionario.objects.filter(id=asig.funcionario.id).first()
                
                notificacion= Notificacion(
                    emisor=funcionario.user,
                    receptor=receptor.user, 
                    solicitud_libro=consignacion.solicitud_libro,
                    estatus_actual=estatus,
                    observacion=observacion
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        consignacion.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()

                consignacion.estatus=estatus
                consignacion.funcionario=receptor
                consignacion.save()

                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)
            elif op == 'devolver':
                
                id_c = request.POST['consignacion']
                consignacion=Consignacion.objects.get(id=id_c)
                ultima_notificacion=Notificacion.objects.filter(
                    solicitud_libro=consignacion.solicitud_libro
                    ).order_by('-fecha_emision').first()

                validacion = val(
                    request.FILES,
                    'archivo',
                    ['application/pdf', 'image/jpeg', 'image/png'] ,
                    2621440) if request.FILES.has_key('archivo') else False

                if len (request.POST['comentario-devolveroficiorespuesta'])==0:
                    observacion=ultima_notificacion.observacion
                else:
                    observacion=request.POST['comentario-devolveroficiorespuesta']

                if funcionario.tiporol.nombre == 'director_ct':
                    tiporol= TipoRol.objects.filter(nombre='analista').first()
                    estatus= Estatus.objects.filter(abreviacion='EOR').first()
                elif funcionario.tiporol.nombre == 'viceministro':
                    tiporol= TipoRol.objects.filter(nombre='director_ct').first()
                    estatus= Estatus.objects.filter(abreviacion='IOR').first()

                #Verificamos los fucionarios involucrados en esta solicitud
                asig=Asignacion.objects.filter(
                    solicitud_libro=consignacion.solicitud_libro, 
                    funcionario__tiporol=tiporol, 
                    asignacion_habilitada=True
                ).order_by('-fecha_asignacion').first()

                receptor = Funcionario.objects.filter(id=asig.funcionario.id).first()
                
                notificacion= Notificacion(
                    emisor=funcionario.user,
                    receptor=receptor.user, 
                    solicitud_libro=consignacion.solicitud_libro,
                    estatus_actual=estatus,
                    observacion=observacion
                )
                notificacion.save()
                if validacion:
                    #TODO: volver plantilla documento nulo
                    nombre_documento = "archivo_notificacion_%s_%s" % (
                        notificacion.id,
                        consignacion.id
                    )
                    documento = Documento(
                        nombre = nombre_documento,
                        ruta_documento=request.FILES['archivo'],
                        tipo_documento_compuesto=TipoDocumentoCompuesto.objects.filter(abreviacion='N').first(),
                        extension = str(request.FILES['archivo']).split(".")[1]
                    )
                    documento.save()

                    notificaciondoc= NotificacionDocumentoCompuesto(
                        notificacion=notificacion,
                        documento=documento
                    )
                    notificaciondoc.save()

                consignacion.estatus=estatus
                consignacion.funcionario=receptor
                consignacion.save()

                jsontmp = {"estado":estatus.nombre, "descripcion":estatus.descripcion}
                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json", status=200)

            elif op == 'editar':

                id_c = request.POST['consignacion']
                consignacion=Consignacion.objects.get(id=id_c)


                folios=Folio.objects.filter(
                    consignacion=consignacion
                )
                rango_folios="%s hasta el %s" % (folios.first().numero, folios.last().numero)

                plantilla = PlantillaDocumento.objects.get(formato="documentos/oficios/oficio_respuesta_folios.html")

                try:
                    #Creando el documento
                    tipo_documento = TipoDocumentoCompuesto.objects.get(abreviacion='OR')
                    nombre_documento = "%s_oficio_respuesta_folios_%s" % (
                        consignacion.id,
                        consignacion.lsr_fisico.identificador
                    )

                    path = model_list.get_file_path(
                        consignacion.lsr_fisico.pst.user.rif,
                        'oficios',
                        "",
                    )

                    locationPath = os.path.join(
                        BASE_DIR,
                        'documents',
                        'files', 
                        path
                    )

                    oficio = Documento.objects.filter(nombre=nombre_documento).first()
                    
                    oficio.fecha_emision=datetime.datetime.now()
                    oficio.eliminado=False
                    
                    oficio.save()

                    consignacion.observacion=request.POST['comentario-edicionoficiorespuesta']
                    consignacion.documento=oficio
                    consignacion.save()
                    texto = consignacion.observacion
                    r = re.sub('<br\s*?>', '\n',texto)
                    r = BeautifulSoup(r)

                    try:
                        #PARAMETROS IMPORTANTES ENVIADOS POR CONTEXTO
                        direc = Registro_Direccion.objects.filter(pst=consignacion.lsr_fisico.pst).first()
                        direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                            +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                            + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                            +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                            +str(direc.codigo_postal)
                        data = Storage(
                            nomenclatura_oficios=ParametroConfiguracion.objects.get(clave='nomenclatura_oficios').valor,
                            oficio=oficio,
                            fecha=datetime.date.today(),
                            razon_social=consignacion.lsr_fisico.pst.razon_social,
                            direccion=direccionPST,
                            telefono=consignacion.lsr_fisico.pst.telefono_fijo if consignacion.lsr_fisico.pst.telefono_fijo else "" + " / " + consignacion.lsr_fisico.pst.telefono_celular if consignacion.lsr_fisico.pst.telefono_celular else "",
                            contacto=RepresentanteContacto.objects.filter(pst=consignacion.lsr_fisico.pst).first(),
                            numero_lsr=consignacion.lsr_fisico.identificador,
                            rango_folios=rango_folios,
                            rtn=consignacion.lsr_fisico.pst.rtn,
                            observacion=r.get_text(),
                            firma=None
                        )

                        generar_pdf.generar_pdf(
                            context=data,
                            ruta_template='documentos/oficios/oficio_respuesta_folios.html',
                            ruta_documento=locationPath,
                            nombre_documento=nombre_documento
                        )

                        locationAttach = os.path.join(
                            locationPath,
                            nombre_documento + '.pdf'
                        )
                    except Exception, error:
                        #raise e
                        return  HttpResponse(error, content_type="application/json", status=400)
                    
                except Exception, error:
                    #raise e
                    return  HttpResponse(error, content_type="application/json", status=400)


                return HttpResponseRedirect(
                    reverse(
                        'oficios_respuesta',
                        kwargs={'operacion': 'bandeja'}
                    )
                )

        except Exception, error:
            return  HttpResponse(error, content_type="application/json", status=400)