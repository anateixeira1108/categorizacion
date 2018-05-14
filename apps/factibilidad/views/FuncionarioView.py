# -*- coding: utf-8 -*-
"""
Vistas para factibilidad de pst.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from django.views.generic import ListView, UpdateView
from django.views.generic.detail import DetailView
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from apps.factibilidad import models as model_app_factibilidad
from registro import models as model_app_registro
from registro.models import CertificacionesPST
from registro.models import PERSONA_NATURAL
from utils.gluon.storage import Storage
from utils.mixins import SendEmailMixin


class ListFactibilidadView(LoginRequiredMixin, ListView):
    """
        Vista utilizada para cargar la lista de factibilidades
    """
    model = model_app_factibilidad.Proyecto
    template_name = 'factibilidad/funcionario/solicitudes.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListFactibilidadView, self).get_context_data()
        # lista de factibilidades
        context['factibilidades'] = model_app_factibilidad.Proyecto.objects.all()
        return context


class DetailFactibilidadView(LoginRequiredMixin, DetailView):
    """
        Vista que muestra los detalles de los datos de factibilidad
    """
    model = model_app_factibilidad.Proyecto
    template_name = 'factibilidad/funcionario/solicitud_aprobacion.html'
    context_object_name = "factibilidad"

    def get_context_data(self, **kwargs):
        context = super(DetailFactibilidadView, self).get_context_data(**kwargs)
        # se crean las variables correspondientes a cada uno de los campos relaciones con la factibilidad
        proyecto = get_object_or_404(model_app_factibilidad.Proyecto, pk=self.kwargs['pk'])
        # se agregan al contexto las variables
        context['is_pst_figura_natural'] = True if proyecto.pst.tipo_figura == PERSONA_NATURAL else False
        context['factibilidad'] = proyecto
        context['unidades_transporte'] = model_app_factibilidad.UnidadTransporte.objects.filter(proyecto=proyecto)
        context['indoles'] = model_app_factibilidad.Indole.objects.filter(proyecto=proyecto)
        context['aspecto_sociales'] = model_app_factibilidad.AspectoSocial.objects.filter(proyecto=proyecto)
        return context


class CertificarFactibilidadView(LoginRequiredMixin, DetailView):
    """
        Vista para mostrar la lista de documentos a certificar por el funcionario
    """
    model = model_app_factibilidad.Proyecto
    template_name = 'factibilidad/funcionario/certificar_documentos.html'
    context_object_name = "factibilidad"
    success_url = reverse_lazy('registro_funcionario_solicitudes')

    def get_context_data(self, **kwargs):
        context = super(CertificarFactibilidadView, self).get_context_data(**kwargs)
        proyecto = get_object_or_404(model_app_factibilidad.Proyecto, pk=self.kwargs['pk'])
        proyecto_archivos = model_app_factibilidad.SocioTecnicoProyecto.objects.get(proyecto=proyecto)
        # obtiene el tipo de actividad
        tipo_actividad = proyecto.tipo_actividad
        # se crea un diccionario de listas de archivos por cada tipo de actividad
        archivos = {
            model_app_factibilidad.ESTABLECIMIENTO_TURISTICO: (
                # (u'nombre_campo', u'Nombre de label del campo en html')
                (u'archivo_titulo_propiedad', u'Titulo de propiedad'),
                (u'archivo_contrato', u'Contrato'),
                (u'archivo_autorizacion', u'Autorización'),
                (u'archivo_uso_turistico', u'Uso turistico'),
                (u'archivo_memoria_descriptiva', u'Memoria descriptiva'),
                (u'archivo_presupuesto', u'Presupuesto')
            ),
            model_app_factibilidad.TRANSPORTES_TURISTICOS: (
                # (u'nombre_campo', u'Nombre de label del campo en html')
                (u'archivo_conformidad_competente', u'Conformidad competente'),
                (u'archivo_factura_proforma', u'Factura proforma'),
                (u'archivo_visto_bueno', u'Visto bueno'),
                (u'archivo_factibilidad_economica', u'Factibilidad economica')
            ),
            model_app_factibilidad.ACTIVIDADES_RECREATIVAS: (
                # (u'nombre_campo', u'Nombre de label del campo en html')
                (u'archivo_conformidad_aval', u'Conformidad aval')
            )
        }
        # se crea una funcion para verificar si el tipo de actividad esta entre las opciones validas
        is_in = lambda tipo: any([tipo in tipo_actividad for tipo_actividad in model_app_factibilidad.TIPO_ACTIVIDAD])
        # se verifica si el tipo de actividad es valido y se busca la lista en el diccionario
        lista_archivos = archivos[tipo_actividad] if is_in(tipo_actividad) else None
        # se verifica si todo salio bien
        if lista_archivos:
            # se crea una lista de diccionarios de archivos
            lista_objetos = []
            for archivo in lista_archivos:
                archivo_dict = {
                    # se agrega el nombre del archivo por defecto
                    'nombre': archivo[1]
                }
                # se verifica si el proyecto cuenta con el archivo
                if hasattr(proyecto_archivos, archivo[0]):
                    # si tiene el archivo el proyecto, entonces agrega el path del archivo
                    archivo_dict['path'] = getattr(proyecto_archivos, archivo[0])
                else:  # si no, entonces el path se hace nulo (#)
                    archivo_dict['path'] = '#'

                # se agrega el diccionario a la lista
                lista_objetos.append(archivo_dict)

            # se agrega la lista de diccionarios al contexto de la plantilla
            context['archivos'] = lista_objetos
            return context


class AceptarCertificacionFactibilidadView(LoginRequiredMixin, UpdateView, SendEmailMixin):
    """
    Vista que se utiliza para registrar la aceptacion de  los documentos por parte del funcionario
    """
    model = model_app_factibilidad.Proyecto
    template_name = 'factibilidad/funcionario/certificar_documentos.html'
    context_object_name = "factibilidad"
    success_url = reverse_lazy('funcionario_factibilidad_solicitudes')

    def post(self, request, *args, **kwargs):
        super(AceptarCertificacionFactibilidadView, self).post(request, *args, **kwargs)
        if 'pk' in self.kwargs:
            # obtiene la factibilidad que se esta certificando
            factibilidad = model_app_factibilidad.Proyecto.objects.get(id=int(self.kwargs['pk']))
            factibilidad.estado = model_app_factibilidad.APROBADO
            factibilidad.save()
            # obtiene un objeto certificación para crear el log correspondiente
            log_certificacion = CertificacionesPST()
            log_certificacion.pst = factibilidad.pst
            log_certificacion.funcionario = request.user
            log_certificacion.tipo = model_app_registro.TIPO_CERTIFICACION_FACTIBILIDAD
            log_certificacion.observaciones = ""
            log_certificacion.save()

            data = Storage(
                user=factibilidad.user,
                tipo_certificacion=u'Factibilidad económica',
                estado=u'Validada'
            )
            self.send_email(data)
            return redirect(self.success_url)
        return redirect(self.success_url)


class RechazarCertificacionFactibilidadView(LoginRequiredMixin, UpdateView, SendEmailMixin):
    """
    Vista que se utiliza para registrar el rechazo de  los documentos por parte del funcionario
    """
    model = model_app_factibilidad.Proyecto
    template_name = 'factibilidad/funcionario/certificar_documentos.html'
    context_object_name = "factibilidad"
    success_url = reverse_lazy('funcionario_factibilidad_solicitudes')

    def post(self, request, *args, **kwargs):
        super(RechazarCertificacionFactibilidadView, self).post(request, *args, **kwargs)
        if 'pk' in self.kwargs:
            post = request.POST
            # obtiene la factibilidad que se esta certificando
            factibilidad = model_app_factibilidad.Proyecto.objects.get(id=int(self.kwargs['pk']))
            factibilidad.estado = model_app_factibilidad.ANULADO
            factibilidad.save()
            # obtiene un objeto certificación para crear el log correspondiente
            log_certificacion = CertificacionesPST()
            log_certificacion.pst = factibilidad.pst
            log_certificacion.funcionario = request.user
            log_certificacion.tipo = model_app_registro.TIPO_CERTIFICACION_FACTIBILIDAD
            observaciones = post['observaciones'] if 'observaciones' in post else ''
            log_certificacion.observaciones = observaciones
            log_certificacion.save()

            data = Storage(
                user=factibilidad.user,
                tipo_certificacion=u'Factibilidad económica',
                estado=u'Rechazada'
            )
            self.send_email(data)
            # se verifica que tipo de figura es para enviar la petición a la plantilla correspondiente
            return redirect(self.success_url)
        return redirect(self.success_url)
