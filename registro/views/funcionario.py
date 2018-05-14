# -*- coding: utf-8 -*-

"""
Vistas para el proceso de la primera certificación de los documentos por parte del funcionario.
"""

# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import datetime

from easy_pdf.views import PDFTemplateView

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from registro import models
from registro.models import Pst, PERSONA_NATURAL, MODIFICACION, ORIGINAL
from utils import views_helpers as helpers
from utils.email import MailMan
from utils.gluon.storage import Storage
from utils.mixins import SendEmailMixin
from apps.cuentas.mixins import MenuPSTMixin

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PST_AGENTE = u'Agente Turístico'

PST_CONDUCTOR = u'Conductor Turístico'

PST_GUIA = u'Guía Turístico'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ListPstView(TemplateView):
    template_name = 'registro/funcionario/lista_solicitudes.html'

    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(ListPstView, self).dispatch(*args, **kwargs)

    @helpers.requerir_funcionario()
    def get(self, *args, **kwargs):
        return super(ListPstView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ListPstView, self).get_context_data(
            *args, **kwargs
        )

        solicitudes = []

        if 'tipo' not in self.request.GET or self.request.GET['tipo'] == '1':
            cached_pst_list = set(
                row.relacion_id for row in models.Cache.objects.all()
            )

            pst_queryset = Pst.objects.filter(
                ~ Q(estatus=models.ESTATUS_REGISTRO_SIN_COMPLETAR),
                ~ Q(estatus=models.ESTATUS_REGISTRO_EN_ESPERA),
                Q(Q(numero_contribuyente=None) | Q(id__in=cached_pst_list)),
                emprendedor=False,
            )

            solicitudes.extend(
                Pst.objects.get(pk=row.pk, cached=True) for row in pst_queryset
            )

        if 'tipo' not in self.request.GET or self.request.GET['tipo'] == '2':
            solicitudes.extend(list(models.SolicitudCambioPerfil.objects.filter(
                activo=True
            ).order_by('pst__rif')))

        solicitudes.sort(
            key=(lambda solicitud: helpers.make_datetime_tz_aware(
                solicitud.creado_el if isinstance(solicitud, models.Pst)
                else solicitud.fecha_generacion
            )),
            reverse=True
        )

        for solicitud in solicitudes:
            solicitud.className = solicitud.__class__.__name__

        paginator_handler = paginator.Paginator(solicitudes, 15)
        page = self.request.GET.get('page')

        try:
            context['solicitudes'] = paginator_handler.page(page)

        except paginator.PageNotAnInteger:
            context['solicitudes'] = paginator_handler.page(1)

        except paginator.EmptyPage:
            context['solicitudes'] = paginator_handler.page(
                paginator_handler.num_pages
            )

        return context


class PstDetailJuridicaView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles de los datos de pst de tipo juridico
    """
    model = Pst
    template_name = 'registro/funcionario/detalle_registro_persona_juridica.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(PstDetailJuridicaView, self).get_context_data(**kwargs)
        # se crean las variables correspondientes a cada uno de los campos relaciones con el pst
        # pst = get_object_or_404(Pst, pk=self.kwargs['pk'])
        pst = context['pst'] = Pst.objects.get(pk=int(self.kwargs['pk']), cached=True)
        direccion = models.Direccion.objects.filter(pst=pst, cached=True)
        # representante = models.RepresentanteContacto.objects.filter(pst=pst, tipo=models.REPRESENTANTE, cached=True)
        acta = models.Acta.objects.filter(pst=pst, tipo_acta=ORIGINAL, cached=True)
        modificaciones_actas = models.Acta.objects.filter(pst=pst, tipo_acta=MODIFICACION, cached=True)
        accionistas = models.Accionista.objects.filter(pst=pst, cached=True)
        # se agregan las variables al contexto de la plantilla
        context['archivo_rif'] = pst.archivo_rif
        contacto = models.RepresentanteContacto.objects.filter(pst=pst, tipo=models.CONTACTO, cached=True)
        representante = models.RepresentanteContacto.objects.filter(pst=pst, tipo=models.REPRESENTANTE, cached=True)
        if representante:  # si tiene representantes
            context['archivo_cedula_representante_pst'] = representante[0].archivo_cedula
            context['archivo_rif_representante_pst'] = representante[0].archivo_rif
        else:  # si no tiene representantes entonces el representante es el contacto
            if contacto:  # se valida que el contacto sea valido
                context['archivo_cedula_representante_pst'] = contacto[0].archivo_cedula
                context['archivo_rif_representante_pst'] = contacto[0].archivo_cedula
        context['direccion'] = direccion[0] if direccion else None
        context['representante'] = representante[0] if representante else None
        context['acta'] = acta[0] if acta else None
        context['modificaciones_actas'] = modificaciones_actas
        context['accionistas'] = accionistas

        return context


class PstDetailNaturalView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles de los datos de pst de tipo natural
    """
    model = Pst
    template_name = 'registro/funcionario/detalle_registro_persona_natural.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(PstDetailNaturalView, self).get_context_data(**kwargs)

        pst = context['pst'] = Pst.objects.get(
            pk=int(self.kwargs['pk']), cached=True
        )

        # Codigo utilizado de la vista natural para mantener el mismo formato
        context['actividad_principal'] = helpers.get_object_or_none(
            models.ActividadComercial,
            pst=pst,
            tipo_actividad=models.ACTIVIDAD_PRINCIPAL,
            cached=True
        )

        context['actividades_secundarias'] = helpers.filter_object_or_list(
            models.ActividadComercial,
            pst=pst,
            tipo_actividad=models.ACTIVIDAD_SECUNDARIA,
            cached=True
        )

        context['datos_especificos'] = (
            helpers.get_datos_especificos_para_pst_natural(
                pst, context['actividad_principal']
            )
        )

        context['direccion'] = helpers.get_object_or_none(
            models.Direccion, pst=pst, cached=True
        )

        return context


class PstRegistrarRechazo(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        # se verifica que los datos sean enviados correctamente por http
        if 'rechazar_registro_observaciones' in request.POST and \
                        'rechazar_registro_conclusiones' in request.POST:
            # se capturan los datos enviados por el metodo POST de http
            pk_pst = self.kwargs['pk']
            observaciones = str(request.POST['rechazar_registro_observaciones']).strip()
            conclusiones = str(request.POST['rechazar_registro_conclusiones']).strip()
            print(observaciones, conclusiones)
            # se crea una instancia del pst
            pst = Pst.objects.get(pk=pk_pst)
            # TODO => No se sabe que estatus se debe colocar, esperando informacion
            pst.estatus = models.ESTATUS_REGISTRO_SIN_COMPLETAR
            # se guardan los cambios
            pst.save(force=True)
            # se guardan los datos en el modelo
            certificacion = models.CertificacionesPST()
            certificacion.observaciones = ''
            certificacion.conclusiones_analisis = conclusiones
            certificacion.observaciones_analisis = observaciones
            certificacion.funcionario = self.request.user
            certificacion.pst = pst
            certificacion.tipo = models.TIPO_CERTIFICACION_RECHAZADA
            certificacion.save()

            MailMan.registro_usuario_rechazado(
                data_dict={
                    'razon_social': pst.razon_social,
                    'observaciones': observaciones
                },
                receptor_email=pst.user.correo_electronico
            )

            return redirect(
                'registro_funcionario_solicitudes'
            )


class PstCertificarPersonaJuridicaView(LoginRequiredMixin, DetailView):
    """
        Vista para mostrar la lista de documentos a certificar por el funcionario
        Aplica solo para pst de tipo juridicos
    """
    model = Pst
    template_name = 'registro/funcionario/certificar_documentos_persona_juridica.html'
    context_object_name = "pst"
    success_url = reverse_lazy('registro_funcionario_solicitudes')

    def get_context_data(self, **kwargs):
        context = super(PstCertificarPersonaJuridicaView, self).get_context_data(**kwargs)
        pst = get_object_or_404(Pst, pk=self.kwargs['pk'])
        pst = context['pst'] = Pst.objects.get(pk=int(self.kwargs['pk']), cached=True)

        context['archivo_rif_pst'] = pst.archivo_rif
        context['tipo_contribuyente'] = models.TIPO_PERSONA[pst.tipo_figura - 1][1]
        contacto = models.RepresentanteContacto.objects.filter(pst=pst, tipo=models.CONTACTO, cached=True)
        representante = models.RepresentanteContacto.objects.filter(pst=pst, tipo=models.REPRESENTANTE, cached=True)
        if representante:  # si tiene representantes
            context['archivo_cedula_representante_pst'] = representante[0].archivo_cedula
            context['archivo_rif_representante_pst'] = representante[0].archivo_rif
        else:  # si no tiene representantes entonces el representante es el contacto
            if contacto:
                context['archivo_cedula_representante_pst'] = contacto[0].archivo_cedula
                context['archivo_rif_representante_pst'] = contacto[0].archivo_cedula

        acta = models.Acta.objects.get(pst=pst, tipo_acta=models.ORIGINAL, cached=True)

        if acta:  # verifica si tiene actas registradas
            context['archivo_acta_constitutiva'] = acta.archivo_acta_constitutiva
            # se consultan todas las modificaciones que pueda tener el pst del acta
            acta_modificaciones = models.Acta.objects.filter(pst=pst, tipo_acta=models.MODIFICACION, cached=True)
            # se verifica si se registraron modificaciones del acta
            if acta_modificaciones:
                context['actas_constitutiva_tiene_modificaciones'] = True

                # se iteran sobre cada una de las modificaciones y se agregan a una lista
                lista_actas_mod = []
                for index, value in enumerate(acta_modificaciones):  # se recorre la lista de socios
                    aux = {}
                    aux['archivo_acta_constitutiva'] = value.archivo_acta_constitutiva
                    lista_actas_mod.append(aux)
                    # se agrega al contexto la lista de modificaciones del acta
                context['actas_constitutiva_modificaciones'] = lista_actas_mod
            else:
                context['actas_constitutiva_tiene_modificaciones'] = False

        else:
            context['acta_constitutiva'] = 'No hay datos registrados'

        try:
            sunacoop = models.Sunacoop.objects.get(pst=pst, cached=True)
        except Exception:
            sunacoop = None
        if sunacoop:
            context['tiene_sunacoop'] = True
            context['archivo_comprobante_sunacoop'] = sunacoop.archivo_comprobante
        else:
            context['tiene_sunacoop'] = False

        socios = models.Accionista.objects.filter(pst=pst, cached=True)
        lista_socios = []

        if socios:  # verifica si tiene socios registrados
            context['tiene_socios'] = True  # flag para utilizar en la template
            for index, value in enumerate(socios):  # se recorre la lista de socios
                aux = {}
                aux['archivo_cedula_socio'] = value.archivo_cedula
                aux['archivo_rif_socio'] = value.archivo_rif
                lista_socios.append(aux)
            context['lista_socios'] = lista_socios
        else:
            context['tiene_socios'] = False
        return context


class PstCertificarPersonaNaturalView(LoginRequiredMixin, DetailView):
    """
        Vista para mostrar la lista de documentos a certificar por el funcionario
        Aplica solo para pst de tipo natural
    """
    model = Pst
    template_name = 'registro/funcionario/certificar_documentos_persona_natural.html'
    context_object_name = "pst"
    success_url = reverse_lazy('registro_funcionario_solicitudes')

    def get_context_data(self, **kwargs):
        context = super(PstCertificarPersonaNaturalView, self).get_context_data(**kwargs)
        pst = context['pst'] = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        datos_especificos = models.DatoEspecifico.objects.get(pst=pst, cached=True)

        actividad_principal = helpers.get_object_or_none(
            models.ActividadComercial,
            pst=pst,
            tipo_actividad=models.ACTIVIDAD_PRINCIPAL,
            cached=True
        )

        tipo_pst_guia = models.TipoPst.objects.get(nombre='Guía Turístico')
        tipo_pst_agente = models.TipoPst.objects.get(nombre='Agente Turístico')
        tipo_pst_conductor = models.TipoPst.objects.get(nombre='Conductor Turístico')

        if actividad_principal.actividad == tipo_pst_agente:
            context['archivo_curriculum'] = datos_especificos.archivo_curriculum

        if actividad_principal.actividad == tipo_pst_conductor:
            context['archivo_licencia'] = datos_especificos.archivo_licencia
            context['archivo_certificado_medico'] = datos_especificos.archivo_certificado

        if actividad_principal.actividad == tipo_pst_guia:
            context['archivo_certificado_guia_especializado'] = (
                datos_especificos.archivo_certificado_guia_especializado
            )
            context['archivo_constancia_curso_primeros_auxilios'] = (
                datos_especificos.archivo_constancia_curso_primeros_auxilios
            )

        context['actividad_principal'] = actividad_principal
        context['archivo_cedula_pst'] = pst.archivo_cedula
        context['archivo_rif_pst'] = pst.archivo_rif
        context['archivo_foto_pst'] = pst.archivo_pasaporte
        context['archivo_copia_recibo_servicio'] = pst.archivo_servicio
        context['tipo_contribuyente'] = models.TIPO_PERSONA[pst.tipo_figura - 1][1]
        # #verificacion necesaria para evitar una excepcion al momento de consultar estos datos
        try:
            representante_legal = models.RepresentanteContacto.objects.get(pst=pst, cached=True)
        except Exception:
            representante_legal = None
        if representante_legal:
            context['cedula_representante_pst'] = representante_legal.archivo_cedula
            context['rif_representante_pst'] = representante_legal.archivo_rif
        else:
            context['cedula_representante_pst'] = 'No hay datos registrados'
            context['rif_representante_pst'] = 'No hay datos registrados'
        return context


class PstAceptarCertificacionRIFTURView(LoginRequiredMixin, UpdateView, SendEmailMixin):
    """
    Vista que se utiliza para registrar la aceptacion de  los documentos por parte del funcionario
    """
    model = Pst
    template_name = 'registro/funcionario/certificar_documentos_persona_juridica.html'
    context_object_name = "pst"
    success_url = reverse_lazy('registro_funcionario_solicitudes')

    def post(self, request, *args, **kwargs):
        super(PstAceptarCertificacionRIFTURView, self).post(request, *args, **kwargs)
        if 'pk' in self.kwargs:
            if 'respuesta' in request.POST:
                if request.POST['respuesta']:
                    respuesta_generar_rif = request.POST['respuesta']
                else:
                    respuesta_generar_rif = 'si'
            else:
                # si no se encuentra la variable, entonces se genera por default el RTIFTUR
                respuesta_generar_rif = 'si'

            print(respuesta_generar_rif)
            # obtiene el PST al que se esta certificando
            pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
            # se actualiza el estatus a: Primera Certificación
            pst.estatus = models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
            # se guardan los cambios
            pst.save()
            # obtiene un objeto certificación para crear el log correspondiente
            log_certificacion = models.CertificacionesPST()
            log_certificacion.pst = pst
            log_certificacion.funcionario = request.user
            log_certificacion.tipo = models.TIPO_CERTIFICACION_PRIMERA
            log_certificacion.observaciones = ""
            log_certificacion.save()
            # envia el correo
            data = Storage(
                user=pst,
                tipo_certificacion=u'Prestador de servicios turísticos',
                estado=u'Validada'
            )
            self.send_email(data)
            # Maneja la certificación a nivel de cache
            helpers.CertificarRegistro.certificar(pst)

            # se verifica si ya se registro la certificacion
            try:
                registro_codigos = models.CertificacionRIFTUR.objects.get(pst=pst)
            except ObjectDoesNotExist:
                registro_codigos = None

            # si ya tiene registrado el numero de contribuyente se redirecciona a la lista de solicitudes
            if registro_codigos:
                return redirect(self.success_url)
            else:  # si no tiene registrado el numero de contribuyente entonces
                # se verifica si se desea generar el riftur
                if respuesta_generar_rif == 'si':
                    # se verifica que tipo de figura es para enviar la petición a la plantilla correspondiente
                    if pst.tipo_figura == models.PERSONA_JURIDICA:
                        return redirect('registro_funcionario_imprimir_certificado_riftur_persona_juridica', pk=pst.id)
                    else:
                        return redirect('registro_funcionario_imprimir_certificado_riftur_persona_natural', pk=pst.id)
                else:  # si no se desea generar el riftur entonces se redirecciona a la lista de solicitudes
                    return redirect(self.success_url)
        else:
            return redirect(self.success_url)


class PstRechazarCertificacionView(LoginRequiredMixin, UpdateView, SendEmailMixin):
    """
    Vista que se utiliza para registrar el rechazo de  los documentos por parte del funcionario
    """
    model = Pst
    template_name = 'registro/funcionario/certificar_documentos_persona_juridica.html'
    context_object_name = "pst"
    success_url = reverse_lazy('registro_funcionario_solicitudes')

    def post(self, request, *args, **kwargs):
        super(PstRechazarCertificacionView, self).post(request, *args, **kwargs)
        if 'pk' in self.kwargs:
            # obtiene el PST al que se esta certificando
            pst = Pst.objects.get(id=int(self.kwargs['pk']))
            # se actualiza el estatus a: registro sin completar para que pase al estado de registrar nuevamente sus datos
            pst.estatus = models.ESTATUS_REGISTRO_EN_ESPERA
            # se guardan los cambios
            pst.save(force=True)
            # obtiene un objeto certificación para crear el log correspondiente
            log_certificacion = models.CertificacionesPST()
            log_certificacion.pst = pst
            log_certificacion.funcionario = request.user
            log_certificacion.tipo = models.TIPO_CERTIFICACION_RECHAZADA
            if 'observaciones' in request.POST:
                observaciones = request.POST['observaciones']
            else:
                observaciones = ''
            log_certificacion.observaciones = observaciones
            log_certificacion.save()
            # enviar correo
            data = Storage(
                user=pst,
                tipo_certificacion=u'Prestador de servicios turísticos',
                estado=u'Rechazada',
                observaciones=observaciones
            )
            self.send_email(data)
            # se verifica que tipo de figura es para enviar la petición a la plantilla correspondiente
            return redirect(self.success_url)
        else:
            return redirect(self.success_url)


class ImprimirCertificadoPersonaNaturalView(LoginRequiredMixin, DetailView):
    """
     Vista utilizada para mostrar el comprobante de certificacion y generar el numero de contribuyente
     al momento de certificar los documentos por parte del funcionario
    """
    model = Pst
    template_name = 'registro/funcionario/imprimir_certificado_persona_natural_riftur.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(ImprimirCertificadoPersonaNaturalView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        # se verifica si ya se registro la certificacion
        try:
            registro_codigos = models.CertificacionRIFTUR.objects.get(pst=pst)
        except ObjectDoesNotExist:
            registro_codigos = None

        # si no se ha registrado, se registra
        if not pst.numero_contribuyente:
            now = datetime.now()
            numero_contribuyente = self.get_numero_contribuyente(pst.rif)
            numero_comprobante = self.get_numero_comprobante()
            # se crea un nuevo registro
            codigos_certificacion = models.CertificacionRIFTUR()
            codigos_certificacion.pst = pst
            codigos_certificacion.funcionario = self.request.user
            codigos_certificacion.numero_comprobante = numero_comprobante
            codigos_certificacion.numero_contribuyente = numero_contribuyente
            codigos_certificacion.save()
            # se agregan las variables al contexto de la plantilla
            context['fecha_certificacion'] = now
            context['numero_contribuyente'] = numero_contribuyente
            context['numero_comprobante'] = numero_comprobante
            # se registra el numero de contribuyente del pst
            pst.numero_contribuyente = numero_contribuyente
            pst.save(force=True)
        else:  # si ya registro la certificacion, entonces consulta los datos
            context['fecha_certificacion'] = registro_codigos.fecha_certificacion
            context['numero_contribuyente'] = registro_codigos.numero_contribuyente
            context['numero_comprobante'] = registro_codigos.numero_comprobante

        context['pst'] = pst
        direccion = pst.direccion_set.get()
        if direccion is not None:
            context['direccion'] = direccion

        natural, juridica, emprendedor = self.get_perfiles(pst)
        context['emprendedor'] = emprendedor
        context['natural'] = natural
        context['juridica'] = juridica
        return context

    def get_perfiles(self, pst):
        natural = False
        juridica = False
        emprendedor = False

        if pst.tipo_figura == PERSONA_NATURAL:
            if pst.emprendedor:
                emprendedor = True
            else:
                natural = True
        else:
            juridica = True
        return natural, juridica, emprendedor

    def get_numero_contribuyente(self, rif_pst):
        # se obtiene el numero de registros y se le suma 1
        numero_consecutivo = models.CertificacionRIFTUR.objects.count() + 1
        # se convierte a string y se rellena de 6 ceros el numero
        str_numero_consecutivo = str(numero_consecutivo).zfill(6)
        # se concatena el numero consecutivo con el rif
        numero_contribuyente = str(rif_pst) + "-" + str_numero_consecutivo
        return numero_contribuyente

    def get_numero_comprobante(self):
        now = datetime.now()
        # se obtiene el numero de registros y se le suma 1
        numero_consecutivo = models.CertificacionRIFTUR.objects.count() + 1
        # se convierte a string y se rellena de 6 ceros el numero
        str_numero_consecutivo = str(numero_consecutivo).zfill(6)
        # se crean las variables que forman el numero de comprobante
        year_str, month_str, N = str(now.year), str(now.month).zfill(2), 'RIFTUR'
        # se crea el numero de comprobante
        numero_comprobante = year_str + month_str + N + str_numero_consecutivo
        return numero_comprobante


class ImprimirCertificadoPersonaJuridicaView(ImprimirCertificadoPersonaNaturalView):
    """
     Vista utilizada para mostrar el comprobante de certificacion y generar el numero de contribuyente
     al momento de certificar los documentos por parte del funcionario
    """
    template_name = 'registro/funcionario/imprimir_certificado_persona_juridica_riftur.html'


# ####################### Imprimir certificado en vista de PST ########################
class ImprimirCertificadoRIFTURPersonaJuridicaPstMenuView(LoginRequiredMixin, DetailView, MenuPSTMixin):
    """
     Vista utilizada para mostrar el comprobante de certificacion en el menu pst solo si ya lo tiene registrado
    """
    model = Pst
    template_name = 'registro/funcionario/imprimir_certificado_persona_juridica_riftur_menu_pst.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(ImprimirCertificadoRIFTURPersonaJuridicaPstMenuView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        rtn = models.CertificacionRIFTUR.objects.get(pst=pst)
        direccion = models.Direccion.objects.get(pst=pst)
        context['direccion'] = direccion
        context['certificacion'] = rtn
        context['pst'] = pst
        return context


class ImprimirCertificadoRIFTURPersonaNaturalPstMenuView(LoginRequiredMixin, DetailView, MenuPSTMixin):
    """
     Vista utilizada para mostrar el comprobante de certificacion en el menu pst solo si ya lo tiene registrado
    """
    model = Pst
    template_name = 'registro/funcionario/imprimir_certificado_persona_natural_riftur_menu_pst.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(ImprimirCertificadoRIFTURPersonaNaturalPstMenuView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        rtn = models.CertificacionRIFTUR.objects.get(pst=pst)
        direccion = models.Direccion.objects.get(pst=pst)
        context['direccion'] = direccion
        context['certificacion'] = rtn
        context['pst'] = pst
        return context


class ImprimirCertificadoRTNPersonaJuridicaPstMenuView(LoginRequiredMixin, DetailView, MenuPSTMixin):
    """
     Vista utilizada para mostrar el comprobante de certificacion en el menu pst solo si ya lo tiene registrado
    """
    model = Pst
    template_name = 'registro/funcionario/imprimir_certificado_persona_juridica_rtn_menu_pst.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(ImprimirCertificadoRTNPersonaJuridicaPstMenuView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        rtn = models.CertificacionRTN.objects.get(pst=pst)
        direccion = models.Direccion.objects.get(pst=pst)
        context['direccion'] = direccion
        context['certificacion'] = rtn
        context['pst'] = pst
        return context


class ImprimirCertificadoRTNPersonaNaturalPstMenuView(LoginRequiredMixin, DetailView, MenuPSTMixin):
    """
     Vista utilizada para mostrar el comprobante de certificacion en el menu pst solo si ya lo tiene registrado
    """
    model = Pst
    template_name = 'registro/funcionario/imprimir_certificado_persona_natural_rtn_menu_pst.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(ImprimirCertificadoRTNPersonaNaturalPstMenuView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
        rtn = models.CertificacionRTN.objects.get(pst=pst)
        direccion = models.Direccion.objects.get(pst=pst)
        context['direccion'] = direccion
        context['certificacion'] = rtn
        context['pst'] = pst
        return context


# ######################################## Busquedas #########################################
def BusquedaPstPorRifView(request):
    def get_solicitudes(request, query=None):
        cached_pst_list = set(
            row.relacion_id for row in models.Cache.objects.all()
        )
        parameters = Storage(
            emprendedor=False,
        )
        if query:
            parameters.rif__iexact = query

        solicitudes = Pst.objects.filter(
            ~ Q(estatus=models.ESTATUS_REGISTRO_SIN_COMPLETAR),
            Q(Q(numero_contribuyente=None) | Q(id__in=cached_pst_list)),
            **parameters
        )
        for solicitud in solicitudes:
            solicitud.className = solicitud.__class__.__name__
        return solicitudes

    """
        Vista encargad de realizar la busqueda de pst por rif
    """
    if 'query' in request.GET:
        query = request.GET['query']
        if query:
            # si hay registros en la busqueda entonces error=False
            solicitudes = get_solicitudes(request, query)
            error = False if solicitudes else True
            context = {}
            context['error'] = error
            print(query, solicitudes)
            if not error:
                context['solicitudes'] = solicitudes
            return render(request,
                          'registro/funcionario/lista_solicitudes.html',
                          context
            )
        else:  # si no ingreso nada en el campo de busqueda, busca todos los registros
            solicitudes = get_solicitudes(request)
            error = False if solicitudes else True
            context = {}
            context['error'] = error
            context['solicitudes'] = solicitudes
            return render(request,
                          'registro/funcionario/lista_solicitudes.html',
                          context
            )
    else:  # si se desconoce la busqueda
        return render(request,
                      'registro/funcionario/lista_solicitudes.html',
                      {'error': True}
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas (Funciones) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
@helpers.requerir_funcionario(view_function=True)
def cambio_de_perfil_aprobar_json(request):
    if request.method != 'PUT':
        return helpers.json_response({
            'error': -1, 'msg': 'Method not allowed.'
        })

    request.PUT = QueryDict(request.body)

    if 'solicitud_pk' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'You should provide the <solicitud_pk> field'
        })

    try:
        solicitud = models.SolicitudCambioPerfil.objects.get(
            pk=request.PUT['solicitud_pk']
        )

    except models.SolicitudCambioPerfil.DoesNotExist:
        return helpers.json_response({
            'error': -3, 'msg': 'There\'s not solicitud with the pk provided'
        })

    else:
        solicitud.activo = False
        solicitud.fecha_verificacion = datetime.now()
        solicitud.pst.emprendedor = False
        solicitud.pst.estatus = models.ESTATUS_REGISTRO_COMPLETADO
        solicitud.pst.save(force=True)
        solicitud.save()

        MailMan.cambio_de_perfil_aprobada(
            data_dict={
                'razon_social': solicitud.pst.razon_social,
            },
            receptor_email=solicitud.pst.user.correo_electronico
        )

    return helpers.json_response({'error': 0, 'result': ''})


@login_required(login_url=reverse_lazy('cuentas_login'))
@helpers.requerir_funcionario(view_function=True)
def cambio_de_perfil_rechazar_json(request):
    if request.method != 'PUT':
        return helpers.json_response({
            'error': -1, 'msg': 'Method not allowed.'
        })

    request.PUT = QueryDict(request.body)

    if 'solicitud_pk' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'You should provide the <solicitud_pk> field'
        })

    if 'observaciones' not in request.PUT:
        return helpers.json_response({
            'error': -2, 'msg': 'You should provide the <observaciones> field'
        })

    try:
        solicitud = models.SolicitudCambioPerfil.objects.get(
            pk=request.PUT['solicitud_pk']
        )

    except models.SolicitudCambioPerfil.DoesNotExist:
        return helpers.json_response({
            'error': -3, 'msg': 'There\'s not solicitud with the pk provided'
        })

    else:
        solicitud.activo = False
        solicitud.fecha_verificacion = datetime.now()
        solicitud.observaciones = request.PUT['observaciones']
        solicitud.save()

        MailMan.cambio_de_perfil_rechazada(
            data_dict={
                'razon_social': solicitud.pst.razon_social,
                'observaciones': solicitud.observaciones,
            },
            receptor_email=solicitud.pst.user.correo_electronico
        )

    return helpers.json_response({'error': 0, 'result': ''})


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from easy_pdf.views import PDFTemplateView
class TestPDFView(PDFTemplateView):
    template_name = "base_pdf/html/acta_reparo.html"

    def get_context_data(self, **kwargs):
        context = super(TestPDFView, self).get_context_data(**kwargs)
        context['pagesize'] = 'A5'
        context['lista_pst'] = Pst.objects.all()
        return context
