# -*- coding: utf-8 -*-

"""
Vistas para el registro de una persona juridica.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import json
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, ListView, View

from apps.cuentas.models import MinturUser as User
from apps.cuentas.mixins import MenuPSTMixin
from apps.configuracion.models import Horarios

from registro.models import REPRESENTANTE, CONTACTO, ESTATUS_REGISTRO_SIN_COMPLETAR
from registro.models import ESTATUS_REGISTRO_COMPLETADO, ORIGINAL, MODIFICACION
from registro.models import ESTATUS_REGISTRO_PRIMERA_CERTIFICACION, ACTIVIDAD_PRINCIPAL
from registro.models import COOPERATIVA, TIPOS_PERSONAS_JURIDICA, PERSONA_JURIDICA
from registro.models import ACTIVIDAD_SECUNDARIA, OTRAS

from registro.models import Pst, TipoPst, Direccion, RepresentanteContacto
from registro.models import Acta, Circunscripcion, RegistroMercantil, Sunacoop
from registro.models import Accionista, Sucursales, ActividadComercial

from registro import forms
from registro.serializers import AccionistaSerializer, ActaSerializer
from utils.views_helpers import FormViewBaseClass
from utils.views_helpers import save_or_update
from utils import views_helpers as helpers
from utils.gluon.storage import Storage
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Classes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Paso1View(helpers.FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 1 para el prestador de servicio juridico
    Registro de Pst - Datos básicos
    """

    template_name = 'registro/juridica_paso1.html'
    success_url = reverse_lazy('cuentas_juridica_2')
    form_class = forms.juridica.Paso1Form

    def get_initial(self):
        initial_data = super(Paso1View, self).get_initial(
            Pst, {'user': self.request.user, 'cached': True}
        )
        return initial_data

    def get_context_data(self, *args, **kwargs):
        context = super(Paso1View, self).get_context_data(*args, **kwargs)
        pst_obj = Pst.objects.get(user=self.request.user)

        context.update({
            'profile': (
                'Emprendedor' if pst_obj.emprendedor
                else 'Prestador de Servicios Turísticos'
            ),
            'estatus': pst_obj.get_estatus_display(),
            'tipo_figura_display': pst_obj.get_tipo_figura_display(),
            'lock_field': (
                not pst_obj.emprendedor and pst_obj.estatus not in [1, 2]
            ),
        })

        return context

    @helpers.registrar_paso(1, 'juridica')
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y
        redirigir a la URL proporcionada.
        """
        user = self.request.user
        data = helpers.get_files_from_form(form)

        data.update(
            Storage(
                tipo_juridica=form.cleaned_data['tipo_juridica'],
                rif=form.cleaned_data['rif'],
                razon_social=form.cleaned_data['razon_social'],
                pagina_web=form.cleaned_data['pagina_web'],
                denominacion_comercial=form.cleaned_data['denominacion_comercial'],
                rtn=form.cleaned_data['rtn'],
                tipo_figura=form.cleaned_data['tipo_figura'],
                estado_contribuyente=form.cleaned_data['estado_contribuyente'],
                inicio_actividad_comercial=form.cleaned_data['inicio_actividad_comercial'],
                user=user,
            )
        )

        helpers.save_or_update(Pst, {'user': user}, data)
        return super(Paso1View, self).form_valid(form)


class Paso2View(helpers.FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 2 para el prestador de servicio juridico
    Registro de Domicilio Fiscal
    """

    template_name = 'registro/juridica_paso2.html'
    success_url = reverse_lazy('cuentas_juridica_2')
    form_class = forms.juridica.Paso2Form

    def get_initial(self):
        initial_data = super(Paso2View, self).get_initial(
            Direccion, {
                'pst': Pst.objects.get(user=self.request.user),
                'cached': True
            }
        )
        return initial_data

    @helpers.registrar_paso(2, 'juridica')
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y
        redirigir a la URL proporcionada.
        """
        pst = Pst.objects.get(user=self.request.user)
        data = Storage(
            pst=pst,
            estado=form.cleaned_data['estado'],
            municipio=form.cleaned_data['municipio'],
            parroquia=form.cleaned_data['parroquia'],
            urbanizacion=form.cleaned_data['urbanizacion'],
            edificio=form.cleaned_data['edificio'],
            avenida_calle=form.cleaned_data['avenida_calle'],
            oficina_apartamento=form.cleaned_data['oficina_apartamento'],
            codigo_postal=form.cleaned_data['codigo_postal'],
            punto_referencia=form.cleaned_data['punto_referencia']
        )

        helpers.save_or_update(Direccion, {'pst': pst}, data)
        return super(Paso2View, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Paso2View, self).get_context_data(**kwargs)
        pst = Pst.objects.get(user=self.request.user)
        context['sucursales'] = Sucursales.objects.filter(pst=pst, cached=True)
        context['domicilio'] = Direccion.objects.filter(pst=pst, cached=True)
        return context


class Paso3View(helpers.FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 3 para el prestador de servicio juridico
    Registro de Representante legal
    """

    template_name = 'registro/juridica_paso3.html'
    success_url = reverse_lazy('cuentas_juridica_4')
    form_class = forms.juridica.Paso3Form
    edit = False

    def get_initial(self):
        initial_data = super(Paso3View, self).get_initial(
            RepresentanteContacto,{
                'pst': Pst.objects.get(user=self.request.user),
                'tipo': REPRESENTANTE,
                'cached': True
            }
        )

        return initial_data

    @helpers.registrar_paso(3, 'juridica')
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y redirigir a la URL proporcionada.
        """
        pst = Pst.objects.get(user=self.request.user)
        data = helpers.get_files_from_form(form)
        data.update(
            Storage(
                pst=pst,
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                cedula=form.cleaned_data['cedula'],
                rif=form.cleaned_data['rif'],
                cargo_empresa=form.cleaned_data['cargo_empresa'],
                telefono_fijo=form.cleaned_data['telefono_fijo'],
                telefono_celular=form.cleaned_data['telefono_celular'],
                correo_electronico=form.cleaned_data['correo_electronico'],
                tipo=REPRESENTANTE
            )
        )

        helpers.save_or_update(RepresentanteContacto, {'pst': pst, 'tipo': REPRESENTANTE}, data)
        return super(Paso3View, self).form_valid(form)


class Paso4View(helpers.FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 4 para el prestador de servicio juridico
    Registro de Persona de contacto
    """

    template_name = 'registro/juridica_paso4.html'
    success_url = reverse_lazy('cuentas_juridica_5')
    form_class = forms.juridica.Paso4Form

    def get_initial(self):
        initial_data = super(Paso4View, self).get_initial(
            RepresentanteContacto,{
                'pst': Pst.objects.get(user=self.request.user),
                'tipo': CONTACTO,
                'cached': True
            }
        )
        return initial_data

    def get_context_data(self, **kwargs):
        context = super(Paso4View, self).get_context_data(**kwargs)
        pst = Pst.objects.get(user=self.request.user)
        context['representante_es_contacto'] = True

        if self.request.POST:
            if self.request.POST['optionsRadios'] == 'No':
                context['representante_es_contacto'] = False

        try:
            RepresentanteContacto.objects.get(
                pst=pst, tipo=CONTACTO, cached=True
            )
            context['representante_es_contacto'] = False
        except RepresentanteContacto.DoesNotExist:
            pass

        return context

    @helpers.registrar_paso(4, 'juridica')
    def get(self, request):
        return super(Paso4View, self).get(request)

    @helpers.registrar_paso(4, 'juridica')
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y
        redirigir a la URL proporcionada.
        """
        pst = Pst.objects.get(user=self.request.user)
        data = helpers.get_files_from_form(form)

        data.update(
            Storage(
                pst=pst,
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                cedula=form.cleaned_data['cedula'],
                rif=form.cleaned_data['rif'],
                cargo_empresa=form.cleaned_data['cargo_empresa'],
                telefono_fijo=form.cleaned_data['telefono_fijo'],
                telefono_celular=form.cleaned_data['telefono_celular'],
                correo_electronico=form.cleaned_data['correo_electronico'],
                tipo=CONTACTO
            )
        )

        helpers.save_or_update(RepresentanteContacto, {'pst': pst, 'tipo': CONTACTO}, data)
        return super(Paso4View, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Funcion Post valida si el formulario es valido y si el representante es contacto
        para eliminar el registro pasar el formulario, en caso contrario retorna form_invalid
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid() == False and request.POST['optionsRadios'] == 'Si':
            return redirect(self.success_url)

        if form.is_valid() == False and request.POST['optionsRadios'] != 'Si':
            return self.form_invalid(form)

        if form.is_valid() == True and request.POST['optionsRadios'] == 'No':
            return self.form_valid(form)

        if form.is_valid() == True and request.POST['optionsRadios'] == 'Si':
            try:
                pst = Pst.objects.get(user=self.request.user)
                contacto = RepresentanteContacto.objects.get(
                    pst=pst, tipo=CONTACTO, cached=True
                )
                contacto.delete(cached=True)
            except RepresentanteContacto.DoesNotExist:
                pass

            return redirect(self.success_url)


class Paso5View(FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 5 para el prestador de servicio juridico
    Registro de Tipo de Prestador de Servicios Turísticos
    """

    template_name = 'registro/juridica_paso5.html'
    success_url = reverse_lazy('cuentas_juridica_6')
    form_class = forms.juridica.Paso5Form

    def get_initial(self):
        initial_data = super(Paso5View, self).get_initial(
            ActividadComercial, {
                'pst': Pst.objects.get(user=self.request.user),
                'cached': True,
                'tipo_actividad': ACTIVIDAD_PRINCIPAL
            }
        )

        actividad_principal = helpers.get_object_or_none(
            ActividadComercial,
            pst=Pst.objects.get(user=self.request.user),
            tipo_actividad=ACTIVIDAD_PRINCIPAL,
            cached=True
        )

        if actividad_principal:
            initial_data.update({
                'actividad_principal_licencia': actividad_principal.licencia
            })

        return initial_data

    def get_context_data(self, *args, **kwargs):
        context = super(Paso5View, self).get_context_data(*args, **kwargs)
        filter = Storage(
            tipo_actividad=ACTIVIDAD_SECUNDARIA,
            pst=Pst.objects.get(user=self.request.user),
            cached=True

        )
        actividades_list = []
        act_sec = []
        tipos = TipoPst.objects.filter(tipo_persona__in=[PERSONA_JURIDICA, OTRAS])
        for t in tipos:
            group = "Actividades relacionadas con turismo"
            if t.tipo_persona == OTRAS:
                group = "Otras"
            actividades_list.append({
                "id": t.id, "nombre": t.nombre, "group": group,
            })

        for a in ActividadComercial.objects.filter(**filter):
            group = "Actividades relacionadas con turismo"
            if a.actividad.tipo_persona == OTRAS:
                group = "Otras"
            act_sec.append({
                "id": a.id, 
                "nombre": a.actividad.nombre,
                "licencia": a.licencia, 
                "actividad_id": a.actividad.id,
                "group": group
            })

        context['actividad_list'] = json.dumps(actividades_list, ensure_ascii=True)
        context['actividades_secundarias'] = json.dumps(act_sec, ensure_ascii=True)

        return context

    @helpers.registrar_paso(5, 'juridica')
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y
        redirigir a la URL proporcionada.
        """
        pst = Pst.objects.get(user=self.request.user)
        data = Storage(
            actividad=form.cleaned_data['actividad'],
            licencia=form.cleaned_data['actividad_principal_licencia']
        )

        helpers.save_or_update(ActividadComercial,
            {'pst': pst, "tipo_actividad":ACTIVIDAD_PRINCIPAL}, data
        )
        return super(Paso5View, self).form_valid(form)


class Paso6View(helpers.FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 6 para el prestador de servicio juridico
    Registro de Detalles del acta constitutiva
    """
    template_name = 'registro/juridica_paso6.html'
    success_url = reverse_lazy('cuentas_juridica_6')
    form_class = forms.juridica.Paso6Form

    def get_initial(self):
        initial_data = super(Paso6View, self).get_initial(
            Acta, {
                'pst': Pst.objects.get(user=self.request.user),
                'tipo_acta':ORIGINAL,
                'cached': True
            }
        )
        return initial_data

    @helpers.registrar_paso(6, 'juridica')
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda y
        redirige a la URL proporcionada.
        """
        pst = Pst.objects.get(user=self.request.user)
        data = helpers.get_files_from_form(form)
        data.update(
            Storage(
                pst = pst,
                circuito_circunscripcion = form.cleaned_data['circuito_circunscripcion'],
                registro_mercantil = form.cleaned_data['registro_mercantil'],
                tomo = form.cleaned_data['tomo'],
                numero_tomo = form.cleaned_data['numero_tomo'],
                fecha_registro = form.cleaned_data['fecha_registro'],
                fecha_ultima_asamblea = form.cleaned_data['fecha_ultima_asamblea'],
                duracion = form.cleaned_data['duracion'],
                capital_suscrito = form.cleaned_data['capital_suscrito'],
                capital_pagado = form.cleaned_data['capital_pagado']
            )
        )

        helpers.save_or_update(Acta, {'pst': pst}, data)
        return super(Paso6View, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Paso6View, self).get_context_data(**kwargs)
        pst = Pst.objects.get(user=self.request.user)
        context['modificaciones'] = Acta.objects.filter(
            pst=pst, tipo_acta=MODIFICACION, cached=True
        )

        context['acta'] = Acta.objects.filter(
            pst=pst, tipo_acta=ORIGINAL, cached=True
        )

        return context


class Paso7View(ListView, MenuPSTMixin):
    """
    Vista para el formulario paso 6 para el prestador de servicio juridico
    Registro de Accionistas/Socios/Asociados
    """
    template_name = 'registro/juridica_paso7.html'
    queryset = None

    @helpers.registrar_paso(7, 'juridica')
    def get(self, request):
        return super(Paso7View, self).get(request)

    def get_queryset(self):
        pst = Pst.objects.get(user=self.request.user)
        self.queryset = Accionista.objects.filter(pst=pst, cached=True)
        return self.queryset


class Paso8View(helpers.FormViewBaseClass, MenuPSTMixin):
    """
    Vista para el formulario paso 8 para el prestador de servicio juridico
    Registro de otros documentos - Cooperativas
    """
    template_name = 'registro/juridica_paso8.html'
    success_url = reverse_lazy('cuentas_juridica_9')
    form_class = forms.juridica.Paso8Form

    def get_initial(self):
        initial_data = super(Paso8View, self).get_initial(
            Sunacoop, {
                'pst': Pst.objects.get(user=self.request.user),
                'cached': True
            }
        )

        return initial_data

    @helpers.registrar_paso(8, 'juridica', es_opcional=True)
    def form_valid(self, form):
        """
        Si el formulario es válido, crea el objeto, guarda
        y redirige a la URL proporcionada.
        """
        pst = Pst.objects.get(user=self.request.user)

        data = helpers.get_files_from_form(form)
        data.update(
            Storage(
                pst=pst,
                numero=form.cleaned_data['numero'],
                fecha=form.cleaned_data['fecha']
            )
        )

        helpers.save_or_update(Sunacoop, {'pst': pst}, data)
        return super(Paso8View, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Obtiene el objeto Pst y verifica si es coperativa retorna en el
        contex True, False dependiendo de estado del pst
        """
        context = super(Paso8View, self).get_context_data(**kwargs)
        pst = Pst.objects.get(user=self.request.user, cached=True)
        context['cooperativa'] = False

        if pst.tipo_juridica == COOPERATIVA:
            context['cooperativa'] = True

        return context


class Paso9View(TemplateView, MenuPSTMixin):
    """
    Vista previa de lo registrado para el Pst
    """
    template_name = 'registro/juridica_paso9.html'

    def get_context_data(self, **kwargs):
        context = super(Paso9View, self).get_context_data(**kwargs)

        try:
            self.prestador = Pst.objects.get(user=self.request.user, cached=True)
            context['pst'] = self.prestador
        except Pst.DoesNotExist:
            pass

        try:
            actividad_prncipal = ActividadComercial.objects.get(
                pst=self.prestador, cached=True, tipo_actividad=ACTIVIDAD_PRINCIPAL
            )
            context['actividad_principal'] = actividad_prncipal
        except ActividadComercial.DoesNotExist:
            pass

        try:
            actividad_secundaria = ActividadComercial.objects.filter(
                pst=self.prestador, cached=True, tipo_actividad=ACTIVIDAD_SECUNDARIA
            )
            context['actividades_secundarias'] = actividad_secundaria
        except Exception:
            pass

        try:
            direccion = Direccion.objects.get(pst=self.prestador, cached=True)
            context['direccion'] = direccion
        except Direccion.DoesNotExist:
            pass

        try:
            accionistas = Accionista.objects.filter(pst=self.prestador, cached=True)
            context['accionistas'] = accionistas
        except Exception:
            pass

        try:
            acta = Acta.objects.get(pst=self.prestador, tipo_acta=ORIGINAL, cached=True)
            context['acta'] = acta
        except Acta.DoesNotExist:
            pass

        try:
            modif_acta = Acta.objects.filter(
                pst=self.prestador, tipo_acta=MODIFICACION, cached=True
            )
            context['modificaciones'] = modif_acta
        except Exception:
            pass

        try:
            contacto = RepresentanteContacto.objects.get(
                pst=self.prestador, tipo=CONTACTO, cached=True
            )
            context['contacto'] = contacto
        except RepresentanteContacto.DoesNotExist:
            pass

        try:
            representante = RepresentanteContacto.objects.get(
                pst=self.prestador, tipo=REPRESENTANTE, cached=True
            )
            context['representante'] = representante
        except RepresentanteContacto.DoesNotExist:
            pass

        return context

    @helpers.verificar_pasos('juridica', 7)
    def get(self, request):
        return super(Paso9View, self).get(request)


class Paso10View(TemplateView, MenuPSTMixin):
    """
    Confirmación de registro para Juridica
    """
    template_name = 'registro/juridica_paso10.html'
    url = reverse_lazy('cuentas_juridica_11')

    @helpers.verificar_pasos('juridica', 7)
    def get(self, request):
        return super(Paso10View, self).get(request)

    def post(self, request, *args, **kwargs):
        if request.POST['csrfmiddlewaretoken']:
            pst = Pst.objects.get(user=request.user, cached=True)

            if pst.emprendedor:
                pst.estatus = ESTATUS_REGISTRO_PRIMERA_CERTIFICACION
                pst.save()
                helpers.CertificarRegistro.certificar(pst)

            else:
                pst = Pst.objects.get(user=request.user)
                pst.estatus = ESTATUS_REGISTRO_COMPLETADO
                pst.save(force=True)

            return HttpResponseRedirect(self.url)


class Paso11View(TemplateView, MenuPSTMixin):
    template_name = 'registro/juridica_paso11.html'

    @helpers.verificar_pasos('juridica', 7)
    def get(self, request):
        return super(Paso11View, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(Paso11View, self).get_context_data(**kwargs)
        context.update({
            'emprendedor': Pst.objects.get(user=self.request.user).emprendedor
        })
        return context


# Class REST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RegistroAccionista(View):
    """
    Clase para agregar Accionistas
    parametros Method POST
    - nombres (str): nombre del accionista
    - apellidos (str): apellido del accionista
    - cedula (str): cedula del accionista
    - rif (str): rif del accionista
    - fecha_incorporacion (date):fecha de incorporación a la empresa
    - archivo_cedula (FILE): archivo con la copia de la cedula
    - archivo_rif (FILE): archivo con la copia del rif
    - numero_acciones (int): numero de acciones
    """

    def post(self, request, *args, **kwargs):
        """
        Guardamos los accionistas para su posterior consulta
        Retorna
        - Response (Json)=
            { "sucess":(boolean), "message": (String) }
        - Ej.
            { "success": True,
              "message": u"Se ha guardado correctamente el Accionista" }
        """
        response = dict(success=False, message=u"No logro registrar el Accionista")

        try:
            fecha_incorporacion = request.POST['fecha_incorporacion']
            incorporacion = datetime.strptime(fecha_incorporacion, '%d/%m/%Y').date()

        except ValueError as e:
            raise Http404("Parametros malformados %s" % e.message)

        data = Storage(
                pst=Pst.objects.get(user=request.user),
                nombres=request.POST['nombre'],
                apellidos=request.POST['apellido'],
                cedula=request.POST['cedula'],
                rif=request.POST['rif'],
                director=False,
                numero_acciones=request.POST['numero_acciones'],
                fecha_incorporacion=incorporacion,
                archivo_cedula=request.FILES.get('archivo_cedula'),
                archivo_rif=request.FILES.get('archivo_rif'),
        )

        if 'director' in request.POST:
            data['director'] = True

        accionista = Accionista.create(data)
        accionista.save(force_cached=True)

        if accionista.id is not None:
            response = dict(success=True,
                            message=u"Se ha guardado correctamente el Accionista")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class ModificacionActa(View):
    """
    Clase para crear modificaciones de la acta constitutiva
    parametros Method POST
    - _circuito_circunscripcion (int): pk del registro circuncripción
    - _registro_mercantil (int): pk del registro mercantil
    - _fecha_registro (date): fecha de registro accionista
    - _numero_tomo (int): numero de tomo
    - _tomo (str): string con el tomo
    - _archivo_acta_constitutiva (file): archivo de la acta
    - _objeto_modificacion (str): string con el objetivo de la modiicación de la acta
    """

    def post(self, request):
        """
        Guardamos la modificacion de la Acta para su posterior consulta
        Retorna
        - Response (Json)= {
            "sucess":(boolean), "message": (String)
        }
        - Ej.
            { "success": True, "message": u"Se ha guardado correctamente la modificacion de la acta" }
        """
        pst = Pst.objects.get(user=request.user)
        try:
            circunscripcion = Circunscripcion.objects.get(
                pk=int(request.POST['_circuito_circunscripcion'])
            )
            registro_mercantil = RegistroMercantil.objects.get(
                pk=int(request.POST['_registro_mercantil'])
            )
            fecha_registro = request.POST['_fecha_registro']
            registro = datetime.strptime(fecha_registro, '%d/%m/%Y').date()
            fecha_asamblea = request.POST['_fecha_ultima_asamblea']
            ultima_asamblea = datetime.strptime(fecha_asamblea, '%d/%m/%Y').date()

        except Exception as e:
            raise Http404("Parametros malformados %s" % e.message)


        if len(Acta.objects.filter(pst=pst, tipo_acta=ORIGINAL, cached=True)) == 1:
            try:
                data = Storage(
                    pst = pst,
                    circuito_circunscripcion=circunscripcion,
                    registro_mercantil=registro_mercantil,
                    fecha_registro=registro,
                    fecha_ultima_asamblea=ultima_asamblea,
                    tomo=request.POST['_tomo'],
                    numero_tomo=request.POST['_numero_tomo'],
                    archivo_acta_constitutiva=request.FILES.get('_archivo_acta_constitutiva'),
                    objetivo_modificacion=request.POST['_objetivo_modificacion'],
                    motivo_modificacion=request.POST['_motivo_modificacion'],
                    tipo_acta=MODIFICACION
                )

                acta = Acta.create(data)
                acta.save(force_cached=True)
                response = dict(
                    success=True,
                    message=u"Se ha guardado correctamente la modificacion de la acta")
            except Exception as e:
                raise Http404("Parametros malformados %s" % e.message)
        else:
            response = dict(
                success=False,
                message=u"Debe registrar una acta original, para realizar modificaciones"
            )

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EliminarModificacionActa(View):
    """
    Clase para para eliminar la modificación de la acta
    parametros Method POST
    - id (int): pk de la acta
    - csrfmiddlewaretoken (str): token de acceso
    """

    def post(self, request):
        """
        Eliminamos las Modificaciones de las Actas
        Retorna
        - Response (Json) = {
            "sucess":(boolean), "message": (String)
        }
        - Ej.
            { "success": True, "message": u"Se ha eliminado correctamente la modificacion de la acta" }
        """
        response = dict(
            success=False,
            message=u"Error al eliminar la modificacion de la acta")

        if request.POST['id']:
            id = int(request.POST['id'])
            acta = Acta.objects.get(
                pk=id, pst=Pst.objects.get(user=request.user), cached=True
            )
            acta.delete(cached=True)
            response = dict(
                success=True,
                message=u"Se ha eliminado correctamente la modificacion de la acta")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EliminarAccionista(View):
    """
    Clase para para eliminar el Accionista
    parametros Method POST
    - id (int): pk del accionista
    - csrfmiddlewaretoken (str): token de acceso
    Response (Json)= {
            "sucess":(boolean), "message": (String)
        }
    """

    def post(self, request):
        """
        funcion para eliminar el Accionista
        """
        response = dict(success=False, message=u"Error al eliminar el Accionista")

        if request.POST['id']:
            id = int(request.POST['id'])
            accionista = Accionista.objects.get(
                pk=id, pst=Pst.objects.get(user=request.user), cached=True
            )
            accionista.delete(cached=True)
            response = dict(success=True, message=u"Se ha eliminado correctamente el Accionista")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EditarAccionista(View):
    """
    Clase para para editar el Accionista
    """

    def post(self, request):
        """
        funcion para editar el accionista
        """
        accionista = None
        try:
            filter = Storage(
                pk = int(request.POST['pk_element']),
                pst = Pst.objects.get(user=request.user),
                cached = True
            )
            accionista = Accionista.objects.get(**filter)
            fecha_incorporacion = request.POST['fecha_incorporacion']
            incorporacion = datetime.strptime(fecha_incorporacion, '%d/%m/%Y').date()

            accionista.nombres = request.POST['nombre']
            accionista.apellidos = request.POST['apellido']
            accionista.cedula = request.POST['cedula']
            accionista.rif = request.POST['rif']
            accionista.numero_acciones = request.POST['numero_acciones']
            accionista.fecha_incorporacion = incorporacion
            accionista.archivo_cedula = request.FILES.get('archivo_cedula')
            accionista.archivo_rif = request.FILES.get('archivo_rif')
            accionista.director = False

            if str(request.POST['director']) == 'on':
                accionista.director = True
            accionista.save()

        except Accionista.DoesNotExist:
            response = dict(success=False, message=u"El registro no existe")
        except ValueError as e:
            response = dict(success=False, message=u"Los parametros enviados no son correctos")
        except MultipleObjectsReturned:
            response = dict(success=False, message=u"Error al realizar la consulta 'MultipleObjectsReturned' ")

        if accionista:
            response = dict(success=True, message=u"Se modifico correctamente el accionista")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


    def get(self, request, pk):
        """
        Funcion que obtiene el accionista
        parametros
            - id (int): pk del accionista
            - csrfmiddlewaretoken (str): token de acceso
        Response (Json) =
            { "sucess":(boolean), "message": (String), "data": (Object Accionista) }
        """
        if pk:
            try:
                filter = dict(pk=int(pk), pst=Pst.objects.get(user=request.user), cached=True)
                accionista = Accionista.objects.get(**filter)
                S_accionista = AccionistaSerializer(accionista)
                response = dict(success=True, message=u"existe", data=S_accionista.data)
            except Accionista.DoesNotExist:
                response = dict(success=False, message=u"Error al Obtener el objeto, no hay registro que coincida")
            except MultipleObjectsReturned:
                response = dict(success=False, message=u"Error obtener el objeto, se retornan mas de lo esperado")
            except MultiValueDictKeyError:
                response = dict(success=False, message=u"Error al extraer los parametros enviados")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class RegistroSucursal(View):
    """
    Clase para agregar la Sucursal
    parametros Method POST
    - nombre (str): nombre de la sucursal
    - estado (int): estado donde se encuentra
    - municipio (int): municipio donde se encuentra
    - parroquia (int): parroquia donde se encuentra
    - urbanizacion (str): urbanizacion donde se encuentra
    - edificio (str): edificio donde se encuentra
    - avenida_calle (str): Avenida/Calle/Carrera de la localidad
    - oficina_apartamento (str): Oficina/Apto/No.
    - codigo_postal (int): codigo postal
    - punto_referencia (str): Punto de referencia
    """

    def post(self, request):
        """
        Registramos la sucursal del Pst
        Retorna
        - Response (Json)= {
            "sucess":(boolean), "message": (String)
        }
        - Ej.
            { "success": True, "message": u"Se ha guardado correctamente La sucursal" }
        """
        response = dict(success=False, message=u"Error al registrar la sucursal")
        pst = Pst.objects.get(user=request.user)

        if len(Direccion.objects.filter(pst=pst, cached=True)) == 1:
            data = Storage(
                pst=pst,
                nombre=request.POST['_nombre_sucursal'],
                estado=request.POST['_estado'],
                municipio=request.POST['_municipio'],
                parroquia=request.POST['_parroquia'],
                urbanizacion=request.POST['_urbanizacion'],
                edificio=request.POST['_edificio'],
                avenida_calle=request.POST['_avenida_calle'],
                oficina_apartamento=request.POST['_oficina_apartamento'],
                codigo_postal=request.POST['_codigo_postal'],
                punto_referencia=request.POST['_punto_referencia']
            )
            sucursal = Sucursales.create(data)
            sucursal.save(force_cached=True)

            if sucursal.id:
                response = dict(success=True,
                                message=u"Se ha guardado correctamente La sucursal")
        else:
            response = dict(success=False, message=u"Debe registrar el Domicilio fiscal de la institución")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EliminarSucursal(View):
    """
    Clase para para eliminar una sucursal asociada
    parametros Method POST
    - id (int): pk de la sucursal
    - csrfmiddlewaretoken (str): token de acceso
    """

    def post(self, request):
        """
        Eliminamos la Sucursal
        Retorna
        - Response (Json)= {
            "sucess":(boolean), "message": (String)
        }
        - Ej.
            { "success": True, "message": u"Se ha eliminado correctamente la Sucursal" }
        """
        response = dict(success=False, message=u"Error al eliminar la Sucursal")

        if request.POST['id']:
            id = int(request.POST['id'])
            sucursal = Sucursales.objects.get(
                pk=id, pst=Pst.objects.get(user=request.user), cached=True
            )
            sucursal.delete(cached=True)
            response = dict(success=True, message=u"Se ha eliminado correctamente la Sucursal")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class ObtenerModificacionActa(View):

    def get(self, request, pk):
        if pk:
            try:
                filter = dict(pk=int(pk), pst=Pst.objects.get(user=request.user), cached=True)
                acta = Acta.objects.get(**filter)
                S_acta = ActaSerializer(acta)
                response = dict(success=True, message=u"existe", data=S_acta.data)
            except Acta.DoesNotExist:
                response = dict(success=False, message=u"El registro no existe")
            except MultipleObjectsReturned:
                response = dict(
                    success=False,
                    message=u"Error al realizar la consulta 'MultipleObjectsReturned'"
                )

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EditarModificacionActa(View):
    """
    Clase para editar las modificaciones de a acta
    """

    def post(self, request):
        acta = None
        try:
            id = int(request.POST['pk_element'])
            filter = dict(pk=id, pst=Pst.objects.get(user=request.user), cached=True)
            acta = Acta.objects.get(**filter)

            mercantil = RegistroMercantil.objects.get(pk=int(request.POST['_registro_mercantil']))
            circuito = Circunscripcion.objects.get(pk=int(request.POST['_circuito_circunscripcion']))
            ultima_asamblea = request.POST['_fecha_ultima_asamblea']
            fecha_registro = request.POST['_fecha_registro']
            acta.objetivo_modificacion = request.POST['_objetivo_modificacion']
            acta.motivo_modificacion = request.POST['_motivo_modificacion']
            acta.archivo_acta_constitutiva = request.FILES.get('_archivo_acta_constitutiva')
            acta.tomo = request.POST['_tomo']
            acta.fecha_ultima_asamblea = datetime.strptime(ultima_asamblea, '%d/%m/%Y').date()
            acta.fecha_registro = datetime.strptime(fecha_registro, '%d/%m/%Y').date()
            acta.numero_tomo = request.POST['_numero_tomo']
            acta.registro_mercantil = mercantil
            acta.circuito_circunscripcion = circuito
            acta.save()

        except Acta.DoesNotExist:
            response = dict(
                success=False,
                message=u"Error al Obtener el objeto, no hay registro que coincida"
            )
        except ValueError as e:
            response = dict(
                success=False,
                message=u"Los parametros enviados no son correctos"
            )
        except MultipleObjectsReturned:
            response = dict(
                success=False,
                message=u"Error obtener el objeto, se retornan mas de lo esperado"
            )
        except MultiValueDictKeyError:
            response = dict(
                success=False,
                message=u"Error al extraer los parametros enviados"
            )
        if acta:
            response = dict(
                success=True,
                message=u"Se Realizo correctamente la modificacion de la acta"
            )

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class AgregarActividadSecundaria(View):
    """
    Clase para agregar la actividad secundaria para el pst
    Method POST:
      - parametros:
          - licencia (integer): numero de licencia
          - actividad(dict):
                - id: id de la actividad
                - nombre: nombre de la actividad
    """
    def post(self, request):
        response = dict(success=False)
        filter = dict(
            licencia=(
                int(request.POST['licencia'])
                if request.POST['licencia'].isdigit() else None
            )
        )
        count = ActividadComercial.objects.filter(**filter).count()
        if count > 1:
            response['message'] = u"La licencia esta registrada para otra actividad"
        else:
            try:
                data = Storage(
                    pst=Pst.objects.get(user=self.request.user),
                    licencia=filter['licencia'],
                    actividad=TipoPst.objects.get(pk=int(request.POST['actividad[id]'])),
                    tipo_actividad=ACTIVIDAD_SECUNDARIA
                )
                actividad_comercial = ActividadComercial(**data)
                actividad_comercial.save(force_cached=True)
            except Exception:
                response['message'] = u"No se registro la actividad comercial"

            if actividad_comercial:
                response = dict(
                    success=True,
                    message=u"Se registró correctamente la actividad comercial",
                    data=dict(
                        nombre=actividad_comercial.actividad.nombre,
                        id=actividad_comercial.id,
                        licencia=actividad_comercial.licencia,
                        actividad_id=actividad_comercial.actividad.id
                    )
                )

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class EliminarActividadSecundaria(View):
    """
    Clase para eliminar la actividad comercial
    Method: POST
      - parametros:
        - actividad_id (integer): Id de la actividad
    """
    def post(self, request):
        response = dict(success=False)
        actividad_comercial = None

        try:
            data = dict(
                pk=int(request.POST['actividad_id[0][0]']),
                pst=Pst.objects.get(user=self.request.user),
                cached=True
            )
            actividad_comercial = ActividadComercial.objects.get(**data)
        except AssertionError:
            response['message'] = u"Es imposible determinar el PST asociado a este modelo"
        except ActividadComercial.DoesNotExist:
            response['message'] = u"No existe el elemento para el Pst indicado"
        except Exception:
            response['message'] = u"No se pudo eliminar actividad comercial"

        if actividad_comercial:
            response = dict(
                success=True,
                message=u"Se eliminó correctamente la actividad comercial",
                data=dict(
                    nombre=actividad_comercial.actividad.nombre,
                    actividad_id=actividad_comercial.actividad.id,
                    licencia=actividad_comercial.licencia,
                    id=actividad_comercial.id
                )
            )
            actividad_comercial.delete(cached=True)

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')
