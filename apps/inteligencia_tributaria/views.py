# -*- coding: utf-8 -*-
"""
Vistas para las inteligencia_tributaria de revision de pst.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import json
from django.db import IntegrityError
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import View, TemplateView, UpdateView
from utils.views_helpers import get_dict_array
from utils.gluon.storage import Storage
from registro.models import Pst, TipoPst, Direccion, ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
from venezuela.models import Estado
from apps.cuentas.models import MinturUser as User
from apps.cuentas.models import ROLE_FUNCIONARIO_APOYO
from apps.verificacion.models import *
from apps.fiscalizacion.models import *
from .models import *
from .serializers import PstSerializer, UserSerializer, FuncionarioSerializer
from .providencia import Providencia
from datetime import datetime, date
from braces.views import LoginRequiredMixin
from django.db.models import Q
from .busqueda import BusquedaPst
import calendar

MESES = {
    "Enero": 1, "Febrero": 2, "Marzo": 3,
    "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9,
    "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

class IndexCrearSolicitud(TemplateView):
    """
    Clase para mostrar la vista principal para crear las solicitudes
    a los candidatos
    """
    template_name='inteligencia_tributaria/funcionario/nueva_solicitud.html'

    def get_context_data(self, **kwargs):
        context = super(IndexCrearSolicitud, self).get_context_data()
        estados = [
            {"id": e.id, "nombre": e.estado}
            for e in Estado.objects.all().order_by('estado')
        ]
        actividad = [{"id": t.id, "nombre": t.nombre} for t in TipoPst.objects.all()]
        context['actividad_economica'] = json.dumps(actividad, ensure_ascii=True)
        context['estados'] = json.dumps(estados, ensure_ascii=True)
        tipo_apoyo = [{"id": i[0], "nombre": i[1]} for i in TIPO_APOYO]
        context['tipo_apoyo'] = json.dumps(tipo_apoyo, ensure_ascii=True)

        return context


class ListarSolicitudes(TemplateView):
    """
    Clase para mostrar la vista principal para crear las solicitudes
    a los candidatos
    """
    template_name='inteligencia_tributaria/funcionario/solicitudes.html'

    def get_context_data(self, **kwargs):
        context = super(ListarSolicitudes, self).get_context_data()
        context['verificaciones'] = Verificacion.objects.all()
        context['fiscalizaciones'] = Fiscalizacion.objects.all()
        return context


class BuscarCandidatos(View, LoginRequiredMixin):
    """
    Clase para buscar los candidatos para una solicitud
    parametros Method POST
    - id (int): pk de la sucursal
    - csrfmiddlewaretoken (str): token de acceso
    """

    def post(self, request):
        """
        Busca los candidatos creados mediante una busqueda avanzada o basica
        Retorna
        - Response (Json):{ "sucess":(boolean), "message": (String) }
        """
        response = dict(success=False, message=u"No se encontaron candidatos disponibles")
        post = request.POST.copy()

        del post['csrfmiddlewaretoken']
        busquedaPst = BusquedaPst(post['busqueda'], post)
        res = busquedaPst.busqueda()
        serializer = PstSerializer(res.objects, many=True)
        if any(serializer.data):
            response = dict(success=True, data=serializer.data, criterio=res.criterio)

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class BuscarFuncionarios(View, LoginRequiredMixin):
    """
    Busca los funcionarios
    """
    def post(self, request):
        funcionarios = None
        cedula = ''
        response = dict(success=False, message=u"No se encontro el Funcionario con la cedula solicitada")
        filter = Storage()
        try:
            cedula = request.POST['cedula']
        except Exception as e:
            pass

        if cedula != '':
            funcionarios = User.objects.filter(Q(cedula=cedula))
        else:
            funcionarios = User.objects.filter(
                            Q(groups__name='funcionarios_dggt') |
                            Q(role=ROLE_FUNCIONARIO_APOYO)
                        )

        serializer = UserSerializer(funcionarios, many=True)
        response = dict(success=True, data=serializer.data)

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class CrearSolicitud(View, LoginRequiredMixin):
    """
    Crea una nueva solicitud verificacion ó fiscalizacion a partir de la
    iformacion suministrada
    """

    def post(self, request):
        candidatos = get_dict_array(request.POST, 'data', ["funcionario", "coordinador", "verificacion", "apoyo", "criterio"])

        for id in candidatos:
            data = Storage()
            pst = Pst.objects.get(pk=int(id))
            candidato = candidatos[id] #Obtenemos los datos del candidato
            fecha = candidato['inicio'].split('-');
            desde = date(int(fecha[1]), MESES[str(fecha[0])], 1)
            fecha = candidato['fin'].split('-');
            days = calendar.monthrange(int(fecha[1]), MESES[str(fecha[0])])
            hasta = date(int(fecha[1]), MESES[str(fecha[0])], days[1])
            # Creamos los elementos para guardar la solicitud
            data.pst = pst
            data.rif = pst.rif
            data.desde = desde
            data.hasta = hasta
            data.estado = APROBACION_SOLICITUD
            data.tipo_solicitud = int(candidato['solicitud'])
            data.criterio = ",".join(candidato['criterio'])
            if int(candidato['solicitud']) == VERIFICACION:
                data.tipo_verificacion = int(candidato['verificacion'][0])

            if int(candidato['solicitud']) == FISCALIZACION:
                data.tipo_verificacion = DOMICILIO_FISCAL

            solicitud = Solicitud(**data)
            solicitud.save()

            for i, id in enumerate(candidato['funcionario']):
                analista = Storage()
                analista.funcionario = User.objects.get(pk=int(id))
                analista.es_coordinador = False
                analista.es_apoyo = False
                if candidato['coordinador'][i] == "true":
                    analista.es_coordinador = True
                if candidato['apoyo'][i] == "true":
                    analista.es_apoyo = True
                analista.solicitud = solicitud
                funcionario = FuncionariosSolicitud(**analista)
                funcionario.save()

        return redirect(reverse_lazy('funcionario_crear_solicitud'))


class VerificacionGerente(TemplateView):
    """
    Clase para listar las solicitudes creadas
    """
    template_name = 'inteligencia_tributaria/funcionario/verificacion_gerente.html'

    def get_context_data(self, **kwargs):
        context = super(VerificacionGerente, self).get_context_data()
        context['solicitudes'] = Solicitud.objects.filter(estado=APROBACION_SOLICITUD)
        context['verificacion'] = VERIFICACION
        return context

    def post(self, request):
        """
        Guarda las solicitudes seleccionadas para crear verificaciones o fiscalizaciones
        """
        post = request.POST.copy()
        tipo = post['tipo']
        del post['csrfmiddlewaretoken']
        del post['tipo']
        if tipo == "rechazar":
            observaciones = post['comentarios']
            del post['comentarios']
            generados = []
            response = dict(success=False, message="error al rechazar las solicitudes")
            for i in range(len(post)):
                msg = "Se han rechazado las solicitudes correctamente"
                posicion = 'solicitud[%d]' % i
                id = post[posicion]
                solicitud = Solicitud.objects.get(pk=id, estado=APROBACION_SOLICITUD)
                solicitud.estado = SOLICITUD_NEGADA
                solicitud.observaciones = observaciones
                solicitud.save()
                generados.append(solicitud)

        if tipo == "aprobar":
            generados = []
            response = dict(success=False, message="error al aprobar las solicitudes")

            for i in range(len(post)):
                data, nueva_solicitud = Storage(), None
                verificacion = None
                fiscalizacion = None
                msg = "Se han aprobado las solicitudes correctamente"

                posicion = 'solicitud[%d]' % i
                id = post[posicion]
                solicitud = Solicitud.objects.get(pk=id, estado=APROBACION_SOLICITUD)
                funcionarios = FuncionariosSolicitud.objects.filter(solicitud=solicitud)
                data.pst = solicitud.pst
                data.rif = solicitud.rif
                data.desde = solicitud.desde
                data.hasta = solicitud.hasta

                if solicitud.tipo_solicitud == FISCALIZACION or \
                    solicitud.tipo_solicitud == VERIFICACION_FISCALIZACION:
                    fiscalizacion = Fiscalizacion(**data)
                    fiscalizacion.save()
                    providencia = Providencia(pst=data.pst, fiscalizacion=fiscalizacion)

                    providencia.crear()

                if solicitud.tipo_solicitud == VERIFICACION or \
                    solicitud.tipo_solicitud == VERIFICACION_FISCALIZACION:
                    
                    if solicitud.tipo_solicitud == VERIFICACION_FISCALIZACION:
                        data.tipo_verificacion = EN_SEDE
                    else: 
                        data.tipo_verificacion = solicitud.tipo_verificacion

                    verificacion = Verificacion(**data)
                    verificacion.save()
                    providencia = Providencia(pst=data.pst, verificacion=verificacion)
                    providencia.crear()

                if verificacion or fiscalizacion:
                    nueva_solicitud = verificacion if verificacion else fiscalizacion
                    generados.append(nueva_solicitud)
                    solicitud.estado = SOLICITUD_APROBADA
                    solicitud.save()

                for funcionario in funcionarios:
                    if isinstance(fiscalizacion, Fiscalizacion):
                        data = Storage(
                            es_coordinador = funcionario.es_coordinador,
                            es_apoyo = funcionario.es_apoyo,
                            funcionario = funcionario.funcionario,
                            asignado_el = funcionario.asignado_el,
                            fiscalizacion = fiscalizacion
                        )
                        f = FuncionariosFiscalizacion(**data)
                        f.save()

                    if isinstance(verificacion, Verificacion):
                        data = Storage(
                            es_coordinador = funcionario.es_coordinador,
                            es_apoyo = funcionario.es_apoyo,
                            funcionario = funcionario.funcionario,
                            asignado_el = funcionario.asignado_el,
                            verificacion = verificacion
                        )
                        f = FuncionariosVerificacion(**data)
                        f.save()

        if len(generados) == len(post):
            response = dict(success=True, message=msg)

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EditarSolicitud(UpdateView):
    """
    Clase para editar las solicitudes creadas por los funcionarios
    """
    template_name='inteligencia_tributaria/funcionario/edicion_gerente.html'
    model = Solicitud

    def get_context_data(self, **kwargs):
        context = super(EditarSolicitud, self).get_context_data()
        self.pk = self.kwargs['pk']
        solicitud = Solicitud.objects.get(pk=self.pk)
        context['solicitud'] = solicitud
        context['verificacion'] = VERIFICACION
        # Verificacion.objects.filter(pst=self.pk).order_by('-creado_el')
        context['ultima_verificacion'] = ""
        context['ultima_fiscalizacion'] = ""
        tipo_verificacion = [{"id": v[0], "nombre": v[1]} for v in TIPO_VERIFICACION]
        context['tipos_verificacion'] = json.dumps(tipo_verificacion, ensure_ascii=True)
        funcionarios = FuncionariosSolicitud.objects.filter(solicitud=solicitud)
        funcionarios = FuncionarioSerializer(funcionarios, many=True)
        context['funcionarios'] = json.dumps(funcionarios.data, ensure_ascii=True)
        tipo_apoyo = [{"id": i[0], "nombre": i[1]} for i in TIPO_APOYO]
        context['tipo_apoyo'] = json.dumps(tipo_apoyo, ensure_ascii=True)

        return context

    def post(self, request, **kwargs):
        """
        Metodo que guarda la modificacion de la solicitud
        Method: POST
        """
        fecha_hoy = datetime.now()
        candidatos = get_dict_array(request.POST, 'data', ['funcionario'])
        solicitud = Solicitud.objects.get(pk=int(request.POST['id_solicitud']))

        # Datos para actualizar de la solicitud
        desde = request.POST['desde'].split('-');
        hasta = request.POST['hasta'].split('-');
        solicitud.desde = date(int(desde[1]), MESES[str(desde[0])], fecha_hoy.day)
        solicitud.hasta = date(int(hasta[1]), MESES[str(hasta[0])], fecha_hoy.day)

        if request.POST['tipo_solicitud'] == VERIFICACION:
            solicitud.tipo_verificacion = tipos_verificacion

        solicitud.save()

        # Asignamos usuarios
        funcionarios = FuncionariosSolicitud.objects.filter(solicitud=solicitud)
        func_ids = [f.funcionario.id for f in funcionarios]

        for id in candidatos:
            data = Storage()
            if id in func_ids:
                lugar = func_ids.index(id)
                del func_ids[lugar]
            else:
                data.funcionario = User.objects.get(pk=id)
                data.es_coordinador = False
                data.solicitud = solicitud
                if candidatos[id]['es_coordinador']== 'true':
                    data.es_coordinador = True

                f = FuncionariosSolicitud(**data)
                f.save()
        FuncionariosSolicitud.objects.filter(funcionario__in=func_ids).delete()
        return redirect(reverse_lazy('verificar_solicitud_gerente'))


class AgregarFuncionarioApoyo(View, LoginRequiredMixin):
    """
    Clase para editar las solicitudes creadas por los funcionarios
    """

    def post(self, request, **kwargs):
        """
        Metodo que guarda la modificacion de la solicitud
        Method: POST
        """
        usuario = None

        correo = "%s.%s@mailapoyo.com" % (request.POST['nombres'],request.POST['apellidos'])
        correo2 = "%s.%s@mailapoyo2.com" % (request.POST['nombres'],request.POST['apellidos'])
        cedula = request.POST['cedula'][2:]
        rif = "J-%s-0" % cedula

        data = Storage(
            nombres = request.POST['nombres'],
            apellidos = request.POST['apellidos'],
            rif = rif,
            cedula = request.POST['cedula'],
            correo_electronico = correo,
            correo_electronico2 = correo2,
            is_active = False,
            role = ROLE_FUNCIONARIO_APOYO
        )
        try:
            usuario = User(**data)
            usuario.save()
            data = Storage(
                tipo_apoyo = request.POST['tipo_apoyo'], funcionario = usuario
            )
            tipo = FuncionarioTipoApoyo(**data)
            tipo.save()
        except IntegrityError:
            response = dict(success=False, message="Funcionario ya se encuentra registrado")


        if usuario.id:
            serializer = UserSerializer(usuario)
            response = dict(
                success = True,
                message = "El funcionario de apoyo se agregó correctamente",
                data = serializer.data
            )

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')
