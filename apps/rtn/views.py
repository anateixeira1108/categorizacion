# -*- coding: utf-8 -*-

"""
Vistas para el proceso de la segunda certificación de los documentos por parte del funcionario.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from collections import OrderedDict
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, UpdateView
from django.views.generic.detail import DetailView

from registro.models import PERSONA_NATURAL
from registro.models import Direccion, RepresentanteContacto, Acta, Accionista
from registro import models
from registro.models import Pst
from utils import views_helpers as helpers
from utils.gluon.storage import Storage
from utils.mixins import SendEmailMixin
from mintur.settings import PREFIJO_INICIAL_GENERACION_RTN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PST_AGENTE = u'Agente Turístico'

PST_CONDUCTOR = u'Conductor Turístico'

PST_GUIA = u'Guía Turístico'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ListPstView(LoginRequiredMixin, ListView):
    """
        Vista utilizada para cargar la lista de pst que no hayan sido certificados
    """
    model = Pst
    template_name = 'rtn/funcionario/solicitudes.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListPstView, self).get_context_data()

        # retorna solo los registros sin completar
        context['psts'] = []

        context['psts'].extend(Pst.objects.filter(
            estatus=models.ESTATUS_REGISTRO_COMPLETADO,
            emprendedor=False,
            rtn=None,
            cached=True,
        ))

        context['psts'].extend(Pst.objects.filter(
            estatus=models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION,
            emprendedor=False,
            rtn=None,
            cached=True,
        ))

        return context


class PstDetailJuridicaView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles de los datos de pst de tipo juridico
    """
    model = Pst
    template_name = 'rtn/funcionario/detalle_registro_persona_juridica.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(PstDetailJuridicaView, self).get_context_data(**kwargs)
        # se crean las variables correspondientes a cada uno de los campos relaciones con el pst
        pst = get_object_or_404(Pst, pk=self.kwargs['pk'])
        direccion = Direccion.objects.filter(pst=pst)
        representante = RepresentanteContacto.objects.filter(pst=pst)
        acta = Acta.objects.filter(pst=pst)
        accionistas = Accionista.objects.filter(pst=pst)
        # se agregan las variables al contexto de la plantilla
        context['direccion'] = direccion[0] if direccion else None
        context['representante'] = representante[0] if representante else None
        context['acta'] = acta[0] if acta else None
        context['accionistas'] = accionistas

        return context


class PstDetailNaturalView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles de los datos de pst de tipo natural
    """
    model = Pst
    template_name = 'rtn/funcionario/detalle_registro_persona_natural.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(PstDetailNaturalView, self).get_context_data(**kwargs)
        # se crean las variables correspondientes a cada uno de los campos relaciones con el pst
        pst = get_object_or_404(Pst, pk=self.kwargs['pk'])

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


class PstCertificarPersonaJuridicaView(LoginRequiredMixin, DetailView):
    """
        Vista para mostrar la lista de documentos a certificar por el funcionario
        Aplica solo para pst de tipo juridicos
    """
    model = Pst
    template_name = 'rtn/funcionario/certificar_documentos_persona_juridica.html'
    context_object_name = "pst"
    success_url = reverse_lazy('rtn_funcionario_solicitudes')

    def get_context_data(self, **kwargs):
        context = super(PstCertificarPersonaJuridicaView, self).get_context_data(**kwargs)
        pst = get_object_or_404(Pst, pk=self.kwargs['pk'])

        context['rif_pst'] = pst.archivo_rif
        context['tipo_contribuyente'] = models.TIPO_PERSONA[pst.tipo_figura - 1][1]
        contacto = RepresentanteContacto.objects.filter(pst=pst, tipo=models.CONTACTO)
        representante = RepresentanteContacto.objects.filter(pst=pst, tipo=models.REPRESENTANTE)
        if representante:  # si tiene representantes
            context['cedula_representante_pst'] = representante[0].archivo_cedula
            context['rif_representante_pst'] = representante[0].archivo_rif
        else:  # si no tiene representantes entonces el representante es el contacto
            if contacto:
                context['cedula_representante_pst'] = contacto[0].archivo_cedula
                context['rif_representante_pst'] = contacto[0].archivo_cedula

        acta = Acta.objects.get(pst=pst, tipo_acta=models.ORIGINAL)
        acta_modificaciones = Acta.objects.filter(pst=pst, tipo_acta=models.MODIFICACION)

        if acta:  # verifica si tiene actas registradas
            context['acta_constitutiva'] = acta.archivo_acta_constitutiva
            if acta_modificaciones:  # se verifica si se registraron modificaciones del acta
                context['actas_constitutiva_tiene_modificaciones'] = True

                # se iteran sobre cada una de las modificaciones y se agregan a una lista
                lista_actas_mod = []
                for index, value in enumerate(acta_modificaciones):  # se recorre la lista de socios
                    aux = {}
                    aux['acta_constitutiva'] = value.archivo_acta_constitutiva
                    lista_actas_mod.append(aux)
                    # se agrega al contexto la lista de modificaciones del acta
                context['actas_constitutiva_modificaciones'] = lista_actas_mod
            else:
                context['actas_constitutiva_tiene_modificaciones'] = False
        else:
            context['acta_constitutiva'] = 'No hay datos registrados'

        socios = Accionista.objects.filter(pst=pst)
        lista_socios = []

        if socios:  # verifica si tiene socios registrados
            context['tiene_socios'] = True  # flag para utilizar en la template
            for index, value in enumerate(socios):  # se recorre la lista de socios
                aux = {}
                aux['cedula_socio'] = value.archivo_cedula
                aux['rif_socio'] = value.archivo_rif
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
    template_name = 'rtn/funcionario/certificar_documentos_persona_natural.html'
    context_object_name = "pst"
    success_url = reverse_lazy('rtn_funcionario_solicitudes')

    def get_context_data(self, **kwargs):
        context = super(PstCertificarPersonaNaturalView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=self.kwargs['pk'])
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
        context['cedula_pst'] = pst.archivo_cedula
        context['actividad_principal'] = actividad_principal
        context['rif_pst'] = pst.archivo_rif
        context['foto_pst'] = pst.archivo_pasaporte
        context['copia_recibo_servicio'] = pst.archivo_servicio
        context['tipo_contribuyente'] = models.TIPO_PERSONA[pst.tipo_figura - 1][1]
        # #verificacion necesaria para evitar una excepcion al momento de consultar estos datos
        try:
            representante_legal = RepresentanteContacto.objects.get(pst=pst)
        except Exception:
            representante_legal = None
        if representante_legal:
            context['cedula_representante_pst'] = representante_legal.archivo_cedula
            context['rif_representante_pst'] = representante_legal.archivo_rif
        else:
            context['cedula_representante_pst'] = 'No hay datos registrados'
            context['rif_representante_pst'] = 'No hay datos registrados'
        return context


class PstSolicitudAprobacionNaturalView(LoginRequiredMixin, DetailView):
    """
    Vista que se utiliza para registrar la aceptacion de  los documentos por parte del funcionario
    """
    model = Pst
    template_name = 'rtn/funcionario/solicitud_aprobacion_persona_natural.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(PstSolicitudAprobacionNaturalView, self).get_context_data(**kwargs)
        # se crean las variables correspondientes a cada uno de los campos relaciones con el pst
        pst = get_object_or_404(Pst, pk=self.kwargs['pk'])
        direccion = Direccion.objects.get(pst=pst)
        representante = RepresentanteContacto.objects.filter(pst=pst)
        # se agregan las variables al contexto de la plantilla
        context['direccion'] = direccion if direccion else None
        context['representante'] = representante[0] if representante else None

        # Codigo utilizado de la vista natural para mantener el mismo formato
        listed_fields = {}

        if pst.tipo_pst.nombre == u'Agente Turístico':
            listed_fields = (
                ('anios_experiencia', u'Años de experiencia'),
                ('archivo_curriculum', u'Currículum Vitae'),
                ('titulo_universitario', u'Título universitario'),
            )

        elif pst.tipo_pst.nombre == u'Conductor Turístico':
            listed_fields = (
                ('archivo_certificado', u'Copia del certificado médico'),
                ('archivo_licencia', u'Copia de la licencia de conducir'),
                ('certificado_medico', u'No. del Certificado Médico'),
                ('fecha_vencimiento_certificado', u'Vencimiento del certificado'),
                ('fecha_vencimiento_licencia', u'Vencimiento de la licencia'),
                ('get_grado_licencia_display', u'Grado de la licencia de conducir'),
            )

        elif pst.tipo_pst.nombre == u'Guía Turístico':
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

        dato_especifico = helpers.get_object_or_none(
            models.DatoEspecifico, pst=pst
        )

        if dato_especifico is not None:
            context['datos_especificos'] = OrderedDict()

            for field, alias in listed_fields:
                context['datos_especificos'][alias] = (
                    helpers.process_field_value(getattr(dato_especifico, field))
                )

        return context


class PstSolicitudAprobacionJuridicaView(LoginRequiredMixin, DetailView):
    model = Pst
    template_name = 'rtn/funcionario/solicitud_aprobacion_persona_juridica.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(PstSolicitudAprobacionJuridicaView, self).get_context_data(**kwargs)
        # se crean las variables correspondientes a cada uno de los campos relaciones con el pst
        pst = get_object_or_404(Pst, pk=self.kwargs['pk'])
        direccion = Direccion.objects.filter(pst=pst)
        representante = RepresentanteContacto.objects.filter(pst=pst)
        acta = Acta.objects.filter(pst=pst)
        accionistas = Accionista.objects.filter(pst=pst)
        # se agregan las variables al contexto de la plantilla
        context['direccion'] = direccion[0] if direccion else None
        context['representante'] = representante[0] if representante else None
        context['acta'] = acta[0] if acta else None
        context['accionistas'] = accionistas

        return context


class PstAceptarCertificacionView(LoginRequiredMixin, UpdateView, SendEmailMixin):
    """
    Vista que se utiliza para registrar la aceptacion de  los documentos por parte del funcionario
    """
    model = Pst
    context_object_name = "pst"
    success_url = reverse_lazy('rtn_funcionario_solicitudes')

    def post(self, request, *args, **kwargs):
        super(PstAceptarCertificacionView, self).post(request, *args, **kwargs)
        if 'pk' in self.kwargs:
            if 'respuesta' in request.POST:
                respuesta_generar_rtn = str(request.POST['respuesta']).lower()
            else:
                # si no se encuentra la variable, entonces se genera por default el RTIFTUR
                respuesta_generar_rtn = 'si'

            # se obtiene el pst asociado a la accion
            pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
            # se cambia el estatus
            pst.estatus = models.ESTATUS_REGISTRO_SEGUNDA_CERTIFICACION
            # se guardan los cambios
            pst.save(force=True)

            if pst.rtn:  # si ya tiene registrado un RTN, entonces
                # lo redirige a la lista de solicitantes de RTN
                return redirect(self.success_url)
            else:  # si no tiene registrado un RTN
                # se genera el RTN
                pst.rtn = self.generar_rtn()
                # se guardan los cambios
                pst.save(force=True)
                # se actualiza el estatus a: Primera Certificación
                # pst.estatus = models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
                # obtiene un objeto certificación para crear el log correspondiente
                log_certificacion = models.CertificacionesPST()
                log_certificacion.pst = pst
                log_certificacion.funcionario = request.user
                log_certificacion.tipo = models.TIPO_CERTIFICACION_SEGUNDA
                log_certificacion.observaciones = ""
                log_certificacion.save()

                # envia el correo
                data = Storage(
                    user=pst,
                    tipo_certificacion=u'Solicitud de generacion de RTN',
                    estado=u'Validada'
                )
                self.send_email(data)
                # se verifica el tipo de figura, para redireccionar a su respectiva vista
                if pst.tipo_figura == models.PERSONA_JURIDICA:
                    return redirect(
                        'registro_funcionario_rtn_imprimir_certificado_persona_juridica',
                        pk=pst.pk
                    )
                else:
                    return redirect(
                        'registro_funcionario_rtn_imprimir_certificado_persona_natural',
                        pk=pst.pk
                    )
        else:
            return redirect(self.success_url)

    def generar_rtn(self):
        registros_con_rtn = Pst.objects.filter(~Q(rtn=None))
        numero_registros = Pst.objects.count()
        numero_registro_sin_rtn = Pst.objects.filter(rtn=None).count()
        ultimo_pst_con_rtn = registros_con_rtn.last()
        # si no hay registros rtn, entonces inicia con el prefijo
        if numero_registro_sin_rtn == numero_registros:
            rtn = PREFIJO_INICIAL_GENERACION_RTN + 1
        else:  # si hay registros con rtn, entonces se crea un consecutivo
            rtn = ultimo_pst_con_rtn.rtn + 1
        return rtn


class PstRechazarCertificacionView(LoginRequiredMixin, UpdateView, SendEmailMixin):
    """
    Vista que se utiliza para registrar el rechazo de  los documentos por parte del funcionario
    """
    model = Pst
    context_object_name = "pst"
    success_url = reverse_lazy('rtn_funcionario_solicitudes')

    def post(self, request, *args, **kwargs):
        super(PstRechazarCertificacionView, self).post(request, *args, **kwargs)
        if 'pk' in self.kwargs:
            # obtiene el PST al que se esta certificando
            pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)
            # se actualiza el estatus a: ESTATUS_REGISTRO_PRIMERA_CERTIFICACION para que pase al estado de registrar nuevamente sus datos
            pst.estatus = models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
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
                tipo_certificacion=u'Solicitud de generacion de RTN',
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
     Vista utilizada para mostrar el comprobante de certificacion y generar el numero de RTN
     al momento de certificar los documentos por parte del funcionario
    """
    model = Pst
    template_name = 'rtn/funcionario/imprimir_certificado_persona_natural.html'
    context_object_name = "pst"

    def get_context_data(self, **kwargs):
        context = super(ImprimirCertificadoPersonaNaturalView, self).get_context_data(**kwargs)
        pst = Pst.objects.get(id=int(self.kwargs['pk']), cached=True)

        try:
            registro_codigos = models.CertificacionRTN.objects.get(pst=pst)
        except ObjectDoesNotExist:
            registro_codigos = None
        # si no se ha registrado, se registra
        if not registro_codigos:
            now = datetime.now()
            numero_comprobante = self.get_numero_comprobante()
            # se agregan las variables al contexto de la plantilla
            context['fecha_certificacion'] = now
            context['rtn'] = pst.rtn
            context['numero_comprobante'] = numero_comprobante
            # se crea un nuevo registro
            codigos_certificacion = models.CertificacionRTN()
            codigos_certificacion.pst = pst
            codigos_certificacion.funcionario = self.request.user
            codigos_certificacion.numero_comprobante = numero_comprobante
            codigos_certificacion.rtn = pst.rtn
            codigos_certificacion.save()
        else:
            context['fecha_certificacion'] = registro_codigos.fecha_certificacion
            context['rtn'] = registro_codigos.rtn
            context['numero_comprobante'] = registro_codigos.numero_comprobante

        direccion = pst.direccion_set.get()
        if direccion is not None:
            context['direccion'] = direccion

        natural, juridica, emprendedor = self.perfiles(pst)
        context['emprendedor'] = emprendedor
        context['natural'] = natural
        context['juridica'] = juridica
        return context

    def perfiles(self, pst):
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

    def get_numero_comprobante(self):
        now = datetime.now()
        # se obtiene el numero de registros y se le suma 1
        numero_consecutivo = models.CertificacionRTN.objects.count() + 1
        # se convierte a string y se rellena de 6 ceros el numero
        str_numero_consecutivo = str(numero_consecutivo).zfill(6)
        # se crean las variables que forman el numero de comprobante
        year_str, month_str, N = str(now.year), str(now.month).zfill(2), 'RTN'
        # se crea el numero de comprobante
        numero_comprobante = year_str + month_str + N + str_numero_consecutivo
        return numero_comprobante


class ImprimirCertificadoPersonaJuridicaView(ImprimirCertificadoPersonaNaturalView):
    """
     Vista utilizada para mostrar el comprobante de certificacion y generar el numero de RTN
     al momento de certificar los documentos por parte del funcionario
    """
    template_name = 'rtn/funcionario/imprimir_certificado_persona_juridica.html'


def BusquedaPstPorRifView(request):
    def get_solicitudes(request, query=None):
        parameters = Storage(
            emprendedor=False,
        )
        if query:
            parameters.rif__iexact = query

        solicitudes = Pst.objects.filter(
            Q(rtn=None),  # registro que no tenga rtn asignado
            (
                Q(estatus=models.ESTATUS_REGISTRO_COMPLETADO) |
                Q(estatus=models.ESTATUS_REGISTRO_PRIMERA_CERTIFICACION)
            ),  # registros que esten registrados correctamente
            **parameters
        )
        for solicitud in solicitudes:
            solicitud.className = solicitud.__class__.__name__
        return solicitudes

    """
        Vista encargada de realizar la busqueda de pst por rif
    """
    if 'query' in request.GET:
        query = request.GET['query']
        if query:
            psts = get_solicitudes(request, query)
            # si hay registros en la busqueda entonces error=False
            error = False if psts else True
            context = {}
            context['error'] = error
            if not error:
                context['psts'] = psts
            return render(request,
                          'rtn/funcionario/solicitudes.html',
                          context
            )
        else:  # si no ingreso nada en el campo de busqueda, busca todos los registros
            psts = get_solicitudes(request)
            return render(request,
                          'rtn/funcionario/solicitudes.html',
                          {'psts': psts}
            )
    else:  # si se desconoce la busqueda
        return render(request,
                      'rtn/funcionario/solicitudes.html',
                      {'error': True}
        )
