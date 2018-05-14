# -*- coding: utf-8 -*-
"""
Vistas para factibilidad de pst.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import json
from utils.gluon.storage import Storage
from django.http import HttpResponse, Http404
from django.views.generic import View, TemplateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from apps.cuentas.models import MinturUser as User
from apps.cuentas.mixins import MenuPSTMixin
from utils import views_helpers as helpers
from braces.views import LoginRequiredMixin
from venezuela.models import Estado, Municipio, Parroquia
from registro.models import Pst
from apps.factibilidad.models import *
from apps.factibilidad.forms import RecaudosEstablecimientosForm
from apps.factibilidad.forms import RecaudosTransporteTuristicoForm
from apps.factibilidad.forms import RecaudosActividadesRecreativasForm

class IndexFactibilidad(TemplateView, MenuPSTMixin):
    template_name='factibilidad/pst/solicitudes.html'

    def get_context_data(self, **kwargs):
        context = super(IndexFactibilidad, self).get_context_data()
        context['proyectos'] = Proyecto.objects.all()
        tipo_solicitud = [{"id": i[0], "nombre": i[1]} for i in TIPO_SOLICITUD]
        tipo_actividad = [{"id": i[0], "nombre": i[1]} for i in TIPO_ACTIVIDAD]
        context['tipo_solicitud'] = json.dumps(tipo_solicitud, ensure_ascii=True)
        context['tipo_actividad'] = json.dumps(tipo_actividad, ensure_ascii=True)
        context['solicitud_activa'] = ACTIVO

        return context


class FactibilidadPasoUno(UpdateView, MenuPSTMixin):
    """
    Paso uno para crear la factibilidad -- Datos del proyecto
    """
    template_name='factibilidad/pst/solicitudes_nueva_1.html'
    success_url = 'pst_solicitudes_factibilidad_paso_dos'
    model = Proyecto

    def get_context_data(self, **kwargs):
        context = super(FactibilidadPasoUno, self).get_context_data()
        try:
            proyecto = Proyecto.objects.get(
                pk=self.kwargs['pk'], 
                user=self.request.user, 
                estado=ACTIVO
            )
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")
        indole = Indole.objects.filter(proyecto=proyecto)
        aspecto = AspectoSocial.objects.filter(proyecto=proyecto)
        unidad = UnidadTransporte.objects.filter(proyecto=proyecto)
        context['indole'] = [{"tipo": i.tipo} for i in indole]
        context['aspecto_social'] = [{"tipo":i.tipo} for i in aspecto]
        context['unidad_transporte'] = [{"tipo":i.tipo} for i in unidad]
        context['proyecto'] = proyecto
        context['tipos_proyectos'] = TIPO_PROYECTO
        context['unidades_transportes'] = UNIDAD_TRANSPORTE
        context['tipos_aspectos'] = TIPOS_ASPECTOS
        context['tipos_indole'] = TIPOS_INDOLE

        return context

    def post(self, request, *args, **kwargs):
        """
        Guardamos los datos del proyecto para de la factibiliad
        Parametros (QueryDict):
            - numero_cabanias
            - numero_suites
            - numero_habitaciones
            - empleos_directos
            - empleos_indirectos
            - otro_alojamiento
            - otra_indole
            - nombre_proyecto
            - monto_proyecto
            - numero_apartamentos
        Retorna
        - Return (Html): redirect 
        """
        proyecto = None
        try:
            proyecto = Proyecto.objects.get(
                pk=self.kwargs['pk'], 
                user=request.user, 
                estado=ACTIVO
            )
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")
        else:
            proyecto.nombre = request.POST['nombre_proyecto']
            proyecto.monto = str(request.POST['monto_proyecto'])
            proyecto.tipo_proyecto = request.POST['tipo_proyecto']
            proyecto.empleos_directos = request.POST['empleos_directos']
            proyecto.empleos_indirectos = request.POST['empleos_indirectos']
            proyecto.otra_indole = request.POST['otra_indole']
            proyecto.otro_aspecto = request.POST['otro_aspecto']
            # Creando filtro de buqueda
            filter = Storage(proyecto=proyecto)

            data_alojamiento =  Storage(
                numero_habitaciones = request.POST['numero_habitaciones'],
                numero_apartamentos = request.POST['numero_apartamentos'],
                numero_cabanias = request.POST['numero_cabanias'],
                numero_suites = request.POST['numero_suites'],
                otro_alojamiento = request.POST['otro_alojamiento']
            )
            alojamiento = UnidadesAlojamiento(**data_alojamiento)
            alojamiento.save()

            # Eliminando las indoles creadas
            Indole.objects.filter(**filter).delete()
            # Creando las nuevas indoles para el proyecto
            tipos_indoles = request.POST.getlist('tipo_indole[indole]')
            for indole in tipos_indoles:
                i = Indole(tipo=int(indole), proyecto=proyecto)
                i.save()

            # Eliminando aspecto social creados
            AspectoSocial.objects.filter(**filter).delete()
            # Creando el Aspecto social
            aspecto_social = request.POST.getlist('tipo_aspecto[aspecto]')
            for aspecto in aspecto_social:
                i = AspectoSocial(tipo=int(aspecto), proyecto=proyecto)
                i.save()

            # Eliminando unidades de transportes creados
            UnidadTransporte.objects.filter(**filter).delete()
            # Creando nuevos unidades de transportes
            unidades_transportes = request.POST.getlist('unidad_transporte[transporte]')
            for unidad in unidades_transportes:
                i = UnidadTransporte(tipo=int(unidad), proyecto=proyecto)
                i.save()

            # Guardando el proyecto
            proyecto.alojamiento = alojamiento 
            proyecto.save()

            url = reverse_lazy(self.success_url, kwargs={'pk': proyecto.id})

            if proyecto:
                return redirect(url)


class FactibilidadPasoDos(UpdateView, MenuPSTMixin):
    """
    Paso dos para crear la factibilidad -- direccion del proyecto
    """
    template_name = 'factibilidad/pst/solicitudes_nueva_2.html'
    success_url = 'pst_solicitudes_factibilidad_paso_tres'
    model = Proyecto

    def get_context_data(self, **kwargs):
        context = super(FactibilidadPasoDos, self).get_context_data()
        filter = Storage(pk=self.kwargs['pk'], user=self.request.user, estado=ACTIVO)
        try:
            proyecto = Proyecto.objects.get(**filter)
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")

        try:
            direccion = DireccionProyecto.objects.get(proyecto=proyecto)
        except DireccionProyecto.DoesNotExist:
            direccion = None 
        
        estados = [{"id": e.id, "nombre": e.estado} for e in Estado.objects.all().order_by('estado')]
        servicios = ServicioProyecto.objects.filter(proyecto=proyecto)
        servicios = [{"servicio": i.servicio_basico.id} for i in servicios]
        context['estados'] = json.dumps(estados, ensure_ascii=True, encoding="utf-8")
        context['proyecto'] = proyecto
        context['direccion'] = direccion
        context['servicios'] = json.dumps(servicios, ensure_ascii=True, encoding="utf-8") 
        context['tipografias'] = CARACTERISTICAS_TOPOGRAFICAS
        context['vialidades'] = TIPOS_VIALIDADES
        context['tipos_servicios'] = ServicioBasico.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """
        Guardamos los datos del proyecto para de la factibiliad
        Parametros (QueryDict):
            - estado 
            - municipio 
            - parroquia 
            - direccion 
            - zona_urbana 
            - zona_rural 
            - zit_mintur 
            - parque_nacional 
            - superficie 
            - tipografia 
            - otra_topografia 
            - vialidad 
            - otra_vialidad 
        Retorna
        - Return (Html): redirect 
        """
        proyecto = None
        
        try:
            proyecto = Proyecto.objects.get(
                pk=self.kwargs['pk'], 
                user=request.user, 
                estado=ACTIVO
            )
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")
        else:
            filter = Storage(proyecto=proyecto)
            data = Storage(
                estado = Estado.objects.get(pk=int(request.POST['estado'])),
                municipio = Municipio.objects.get(pk=int(request.POST['municipio'])),
                parroquia = Parroquia.objects.get(pk=int(request.POST['parroquia'])),
                tipografia = int(request.POST['tipografia']),
                vialidad = int(request.POST['vialidad']),
                direccion = request.POST['direccion'],
                zona_urbana = request.POST['zona_urbana'],
                zona_rural = request.POST['zona_rural'],
                zit_mintur = request.POST['zit_mintur'],
                parque_nacional = request.POST['parque_nacional'],
                superficie = request.POST['superficie'],
                otra_topografia = request.POST['otra_topografia'],
                otra_vialidad = request.POST['otra_vialidad'],
                otro_servicio = request.POST['otro_servicio'],
            )

            # eliminando los servicios anteriores 
            ServicioProyecto.objects.filter(**filter).delete()
            # Creando los nuevos Servicios del proyecto 
            servicios = request.POST.getlist('servicio[tipo]')
            for servicio in servicios:
                items = Storage(
                    servicio_basico=ServicioBasico.objects.get(pk=int(servicio)),
                    proyecto=proyecto
                )
                s = ServicioProyecto(**items)
                s.save()

            if DireccionProyecto.objects.filter(**filter).count():
                DireccionProyecto.objects.filter(**filter).update(**data)
            else:
                data.proyecto = proyecto
                direccion = DireccionProyecto(**data)
                direccion.save()

        url = reverse_lazy(self.success_url, kwargs={'pk': proyecto.id})
        if proyecto:
            return redirect(url)
    

class FactibilidadPasoTres(UpdateView, MenuPSTMixin):
    """
    Paso tres para crear la factibilidad -- tipo y categoria del proyecto
    """
    template_name = 'factibilidad/pst/solicitudes_nueva_3.html'
    success_url = 'pst_factibilidad_vista_previa'
    model = Proyecto

    def get_context_data(self, **kwargs):
        context = super(FactibilidadPasoTres, self).get_context_data()
        filter = Storage(pk=self.kwargs['pk'], user=self.request.user, estado=ACTIVO)
        try:
            proyecto = Proyecto.objects.get(**filter)
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")
        context['proyecto'] = proyecto
        context['range'] = range(1, 6)
        return context

    def post(self, request, *args, **kwargs):
        """
        Guardamos las categoria del del proyecto
        Parametros (QueryDict):
            - hotel
            - hotel_residencia
            - posada
            - posada_familiar
            - parador_turistico
            - balneario
            - campamentos_estancias
        Retorna
        - Return (Html): redirect       
        """
        try:
            proyecto = Proyecto.objects.get(
                pk=self.kwargs['pk'], 
                user=self.request.user, 
                estado=ACTIVO
            )
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")

        campamentos_estancias = None
        parador_turistico = None
        hotel_residencia = None
        posada_familiar = None
        balneario = None
        posada = None
        hotel = None
        url = reverse_lazy(
            'pst_solicitudes_factibilidad_paso_tres', kwargs={'pk': proyecto.id}
        )

        if request.POST.has_key('campamentos_estancias'):
            campamentos_estancias = request.POST['campamentos_estancias']

        if request.POST.has_key('parador_turistico'):
            parador_turistico = request.POST['parador_turistico']

        if request.POST.has_key('hotel_residencia'):
            hotel_residencia = request.POST['hotel_residencia']

        if request.POST.has_key('posada_familiar'):
            posada_familiar = request.POST['posada_familiar']

        if request.POST.has_key('balneario'):
            balneario = request.POST['balneario']

        if request.POST.has_key('posada'):
            posada = request.POST['posada']

        if request.POST.has_key('hotel'):
            hotel = request.POST['hotel']

        data = Storage(
            hotel = hotel,
            hotel_residencia = hotel_residencia,
            posada = posada,
            posada_familiar = posada_familiar,
            parador_turistico = parador_turistico,
            balneario = balneario,
            campamentos_estancias = campamentos_estancias
        )

        if proyecto.categoria:
            Categoria.objects.filter(pk=proyecto.categoria.id).update(**data)
        else:
            categoria = Categoria(**data)
            categoria.save()
            proyecto.categoria = categoria
            proyecto.save()

        if proyecto.categoria:
            url = reverse_lazy(self.success_url, kwargs={'pk': proyecto.id})

        return redirect(url) 


class FactibilidadPasoCuatro(helpers.FormViewBaseClass, MenuPSTMixin): 
    template_name = 'factibilidad/pst/solicitudes_nueva_4.html'
    success_url = reverse_lazy('pst_solicitudes_factibilidad') 

    def get_initial(self):
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk'], user=self.request.user)
        initial_data = super(FactibilidadPasoCuatro, self).get_initial(
            SocioTecnicoProyecto, {'proyecto': proyecto}
        )
        initial_data.update({'proyecto': proyecto })
        return initial_data

    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y redirigir a la URL proporcionada.
        """
        data = helpers.get_files_from_form(form)
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk'], user=self.request.user, estado=ACTIVO)
        data.update(Storage(proyecto = proyecto))
        helpers.save_or_update(SocioTecnicoProyecto, {'proyecto': proyecto}, data)
        
        return super(FactibilidadPasoCuatro, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk'], user=self.request.user, estado=ACTIVO)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(
            form=form, 
            proyecto=proyecto,
            establecimiento_turistico = ESTABLECIMIENTO_TURISTICO,
            transporte_turistico = TRANSPORTES_TURISTICOS,
            actividades_recreativas = ACTIVIDADES_RECREATIVAS
        )
        return self.render_to_response(context)
    
    def get_form_class(self):
        """
        Genera el formulario depende del tipo de proyecto
        """
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk'], user=self.request.user)

        if proyecto.tipo_actividad == ESTABLECIMIENTO_TURISTICO:
            self.form_class = RecaudosEstablecimientosForm

        if proyecto.tipo_actividad == TRANSPORTES_TURISTICOS:
            self.form_class = RecaudosTransporteTuristicoForm

        if proyecto.tipo_actividad == ACTIVIDADES_RECREATIVAS:
            self.form_class = RecaudosActividadesRecreativasForm
        
        return self.form_class 


class FactibilidadVistaPrevia(TemplateView, MenuPSTMixin):
    template_name = 'factibilidad/pst/solicitud_vista_previa.html'

    def get_context_data(self, **kwargs):
        context = super(FactibilidadVistaPrevia, self).get_context_data()
        try:
            proyecto = Proyecto.objects.get(
                pk=self.kwargs['pk'], 
                user=self.request.user, 
                estado=ACTIVO
            )
        except Proyecto.DoesNotExist:
            raise Http404("Error de registro. La factibilidad no existe")
        context['proyecto'] = proyecto
        context['unidad_transporte'] = UnidadTransporte.objects.filter(proyecto = proyecto)
        context['direccion'] = DireccionProyecto.objects.get(proyecto = proyecto)
        context['servicios'] = ServicioProyecto.objects.filter(proyecto = proyecto)
        context['categoria'] = Categoria.objects.get(proyecto = proyecto)
        context['alianzas'] = AspectoSocial.objects.filter(proyecto = proyecto)
        context['indole'] = Indole.objects.filter(proyecto = proyecto)
        context['unidades'] = UnidadesAlojamiento.objects.get(proyecto = proyecto)
        
        return context


## Class REST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CrearNuevaFactibilidad(View, MenuPSTMixin):
    """ Clase para crear Factibilidades """

    def post(self, request, *args, **kwargs):
        """
        Metodo que crea una nueva factibilidad y redirige a la interfaz indicada
        Parametros:
            - actividad (String): Tipo de actividad turística
            - solicitud (String): Tipo de solicitud 

        - Return (Json) o redirect: 
            - "sucess": (boolean)
            - "message": (String)      
        """
        proyecto, pst = None, None
        response = dict(success=False, message=u"Error al crear la factibilidad")
        
        try:
            pst = Pst.objects.get(user=request.user)
        except Pst.DoesNotExist:
            response = dict(success=False, message=u"No tiene un Pst asignado para este usuario")
        else:
            datos = Storage(
                tipo_actividad = int(request.POST['actividad']),
                tipo_solicitud = int(request.POST['solicitud']),
                pst = pst, user = request.user
            )
            proyecto = Proyecto(**datos)
            proyecto.save()

        if proyecto:
            url = reverse_lazy('pst_solicitudes_factibilidad_paso_uno', args=[proyecto.id])
            response = dict(
                success=True, 
                message=u"Se creo correctamente la factibilidad", 
                url=url.lower()
            )

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class AnularFactibilidad(View, MenuPSTMixin):
    """Clase para eliminar las factibilidades creadas"""
    def post(self, request, *args, **kwargs):
        """
        Retorna
        - Return (Json): 
            - "sucess":(boolean)
            - "message": (String)
        """
        id = int(request.POST['id_factibilidad'])
        justificacion = request.POST['justificacion']
        response = dict(success=False, message=u"Error al anular la factibilidad")
        
        proyecto = Proyecto.objects.get(pk=id, user=self.request.user, estado=ACTIVO)
        proyecto.justificacion = justificacion
        proyecto.estado = ANULADO
        proyecto.save()

        if proyecto:
            response = dict(success=True, message=u"Se anuló correctamente la factibilidad")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class FactibilidadDatosProyectos(View, MenuPSTMixin):
    """Clase para guardar los datos del proyecto de la factibilidad"""
    def post(self, request, *args, **kwargs):
        """
        Guardamos los datos del proyecto para de la factibiliad
        Retorna
        - Return (Json): 
            - "sucess":(boolean)
            - "message": (String)
        """
        response = dict(success=False, message=u"No logro registrar el Accionista")
        response = json.dumps(response, ensure_ascii=True)
        
        return HttpResponse(response, content_type='application/json')


#clases funcionario~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class FuncionarioListFactivilidadView(LoginRequiredMixin, ListView):
    """
        Vista utilizada para cargar la lista de factibilidades
    """
    model = Pst
    template_name = 'factibilidad/funcionario/solicitudes.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FuncionarioListFactivilidadView, self).get_context_data()
        #retorna solo los registros sin completar y que no sean emprendedores
        context['factibilidades'] = Proyecto.objects.all()
        return context