# -*- coding: utf-8 -*-
import re
import random
from datetime import datetime

from django.template.context import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.views.generic import View, FormView, CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from braces.views import LoginRequiredMixin

from apps.cuentas.forms import (
    PSTUserRegistrationForm, UserAuthenticationForm, NeedhelpForm, ChangePasswordForm,
    OLVIDE_PASSWORD, OLVIDE_CORREO_ELECTRONICO,
    SecretQuestionsForm)
from apps.cuentas.forms import EMPRENDEDOR
from apps.cuentas.models import MinturUser, QuestionUser, Question, ROLE_FUNCIONARIO, ROLE_PST, ROLE_ADMIN
from apps.cuentas.lib import reset_password_send_email
from registro.models import Pst, PERSONA_JURIDICA, PERSONA_NATURAL, ESTATUS_REGISTRO_SIN_COMPLETAR


####################################################################
# CGTS DevTeam                                                     #
# Imports para permitir acceso con el modulo de calidad turistica  #
####################################################################

from apps.categorizacion.helpers.acceso_cuentas import obtener_template
from django.core.urlresolvers import reverse
from django.shortcuts import *


class NuevaCuentaView(CreateView):
    form_class = PSTUserRegistrationForm
    model = MinturUser
    template_name = 'cuentas/nueva.html'
    success_url = reverse_lazy('cuentas_login')

    def form_valid(self, form):
        patron_persona_juridica = '^J-\d+-\d'

        # Creamos el usuario del PST
        user = MinturUser.objects.create_user(
            correo_electronico=form.cleaned_data['correo_electronico'],
            correo_electronico2=form.cleaned_data['correo_electronico2'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            rif=form.cleaned_data['rif'],
            password=form.cleaned_data['password1']
        )

        # Creamos un Registro para el PST para que inicie el proceso de registo/actualizacion de datos
        pst = Pst()

        # verificamos el tipo de persona
        if re.search(patron_persona_juridica, form.cleaned_data['rif']):
            pst.tipo_figura = PERSONA_JURIDICA
        else:
            pst.tipo_figura = PERSONA_NATURAL

        # verificamos si es emprendedor
        if int(form.cleaned_data['tipo_pst']) != EMPRENDEDOR:
            pst.emprendedor = False

        pst.user = user
        pst.correo_electronico = user.correo_electronico
        pst.nombres = user.nombres
        pst.apellidos = user.apellidos
        pst.rif = form.cleaned_data['rif']
        pst.tipo_figura = determinar_tipo_figura(form.cleaned_data['rif'])
        pst.save(force=True)

        # Agregamos las preguntas secretas escogidas por el PST
        user_question_answer1 = QuestionUser()
        user_question_answer1.question = form.cleaned_data['pregunta_1']
        user_question_answer1.answer = form.cleaned_data['respuesta_1']
        user_question_answer1.user = user
        user_question_answer1.save()

        user_question_answer2 = QuestionUser()
        user_question_answer2.question = form.cleaned_data['pregunta_2']
        user_question_answer2.answer = form.cleaned_data['respuesta_2']
        user_question_answer2.user = user
        user_question_answer2.save()

        user_question_answer3 = QuestionUser()
        user_question_answer3.question = form.cleaned_data['pregunta_3']
        user_question_answer3.answer = form.cleaned_data['respuesta_3']
        user_question_answer3.user = user
        user_question_answer3.save()

        mensaje = u'¡Su cuenta para acceso a Mintur fue creada correctamente, por favor revise su correo electrónico' \
                  u' para conocer los detalles para activar la misma!'

        messages.info(self.request, mensaje)

        return redirect(reverse_lazy('cuentas_login'))


class ActivarCuentaView(View):
    # TODO mostrar mensaje y correo para notificar que se ha creado activado el PST
    def get(self, request, *args, **kwargs):
        activation_key = kwargs.get('activation_key', 0)

        try:
            user = MinturUser.objects.get(activation_key=activation_key)
            user.activar_cuenta()
            mensaje = u'¡Su cuenta de acceso a Mintur se ha activado correctamente!'
            messages.info(self.request, mensaje)

        except MinturUser.DoesNotExist:
            mensaje = u'¡Su token de activación de cuenta ya fue utilizado!, por favor inicie sesión. ' \
                      u'Si olvido la contraseña seleccione la opción "Necesito Ayuda"'
            messages.warning(self.request, mensaje)

        return redirect(reverse_lazy('cuentas_login'))


class IngresarView(FormView):
    # TODO mostrar mensaje de bienvenida al Sistema
    form_class = UserAuthenticationForm
    template_name = 'cuentas/ingresar.html'
    success_url = reverse_lazy('cuentas_detectar_usuario')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('cuentas_logout'))

        return super(IngresarView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        correo_electronico = form.cleaned_data['correo_electronico']
        password = form.cleaned_data['password']

        # Logeamos al usuario, si el form es valido esto no debria fallar nunca
        user = authenticate(correo_electronico=correo_electronico, password=password)
        login(self.request, user)

        return super(IngresarView, self).form_valid(form)


class SalirView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            mensaje = u'¡Ha cerrado sesión en Mintur correctamente!'
            messages.info(self.request, mensaje)

        return redirect(reverse_lazy('cuentas_login'))


class NecesitaAyudaView(FormView):
    form_class = NeedhelpForm
    template_name = 'cuentas/necesita_ayuda.html'

    def form_valid(self, form):
        opcion = int(form.cleaned_data['olvide'])
        correo_electronico = form.cleaned_data['correo_electronico']
        rif = form.cleaned_data['rif']

        if opcion == OLVIDE_PASSWORD:
            # enviamos el correo para reset de password del Usuario
            usuario = get_object_or_404(MinturUser, correo_electronico=correo_electronico)
            reset_password_send_email(usuario)

            mensaje = u'¡Se le ha enviado un correo electrónico con los detalles para restablecer su contraseña!'
            messages.info(self.request, mensaje)
            return redirect(reverse_lazy('cuentas_login'))

        elif opcion == OLVIDE_CORREO_ELECTRONICO:
            # Buscamos las preguntas secretas para el Usuario
            usuario = get_object_or_404(MinturUser, rif=rif)

            # Obtenemos las preguntas del usuario
            preguntas = usuario.questionuser_set.all()
            preguntas_id = [pregunta.question.id for pregunta in preguntas]

            # Seleccionamos 2 preguntas aleatorias de las 3 del usuario
            preguntas = random.sample(preguntas_id, 2)
            pregunta_1 = Question.objects.get(pk=preguntas[0])
            pregunta_2 = Question.objects.get(pk=preguntas[1])

            # Instanciamos el formulario con el usuario
            form = SecretQuestionsForm(
                initial={"rif": usuario.rif, "pregunta_1": preguntas[0], "pregunta_2": preguntas[1]}
            )

            # renderizamos la plantilla donde se muestran las preguntas secretas
            return render_to_response(
                'cuentas/preguntas_secretas.html',
                {
                    'form': form,
                    'pregunta_1': pregunta_1,
                    'pregunta_2': pregunta_2
                },
                RequestContext(self.request)
            )
        else:
            return redirect(reverse_lazy('cuentas_login'))


class PreguntasSecretasView(FormView):
    form_class = SecretQuestionsForm
    template_name = 'cuentas/preguntas_secretas.html'

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('cuentas_login'))

    def form_valid(self, form):
        rif = form.cleaned_data['rif']
        usuario = get_object_or_404(MinturUser, rif=rif)

        return render_to_response(
            'cuentas/recuperacion_correo_electronico.html',
            {
                'usuario': usuario
            },
            RequestContext(self.request)
        )

    def form_invalid(self, form):
        # renderizamos la plantilla donde se muestran las preguntas secretas
        pregunta_1_id = int(form.cleaned_data['pregunta_1'])
        pregunta_2_id = int(form.cleaned_data['pregunta_2'])

        pregunta_1 = get_object_or_404(Question, pk=pregunta_1_id)
        pregunta_2 = get_object_or_404(Question, pk=pregunta_2_id)

        return render_to_response(
            'cuentas/preguntas_secretas.html',
            {
                'form': form,
                'pregunta_1': pregunta_1,
                'pregunta_2': pregunta_2
            },
            RequestContext(self.request)
        )


class ResetPasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'cuentas/restablecer_contrasena.html'

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        reset_password_key = self.kwargs.get('reset_password_key', 0)
        context['usuario'] = get_object_or_404(MinturUser, reset_password_key=reset_password_key)
        return context

    def form_valid(self, form):
        reset_password_key = self.kwargs.get('reset_password_key', 0)
        usuario = get_object_or_404(MinturUser, reset_password_key=reset_password_key)
        password = form.cleaned_data['password1']
        usuario.set_password(password)
        usuario.reset_password_key = ''
        usuario.reset_password_date = datetime.now()
        usuario.save()
        mensaje = u'¡Ha cambiado su clave de acceso a Mintur correctamente!'
        messages.info(self.request, mensaje)
        return redirect(reverse_lazy('cuentas_login'))


class DetectarUsuarioView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated() and user.is_active:

            if user.role == ROLE_ADMIN:
                mensaje = u'¡El rol Administrador no se encuentra activo!'
                messages.info(self.request, mensaje)
                return redirect(reverse_lazy('cuentas_logout'))

            elif user.role == ROLE_PST:
                # Obtenemos el registro PST
                pst = user.pst_set.get()  
                natural = False
                juridica = False

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True

                return render_to_response(
                    'home/home_pst.html',
                    {
                        'pst': pst,
                        'usuario': request.user,
                        'natural': natural,
                        'juridica': juridica,
                        'nuevo_registro': (pst.estatus == 1),
                        'mostrar_cambio_perfil': (
                            pst.emprendedor
                            and pst.estatus != ESTATUS_REGISTRO_SIN_COMPLETAR
                        )
                    },
                    RequestContext(request)
                )
            elif user.role == ROLE_FUNCIONARIO:

                #######################################
                # Modificacion necesaria CGTS DevTeam #
                #######################################
                
                stt = obtener_template(user)                                
                
                if stt is not False:
                    return HttpResponseRedirect(reverse(stt))
                else:
                    return render_to_response(
                        'home/home_funcionario.html',
                        {
                            'usuario': request.user
                        },
                        RequestContext(request)
                    )

        elif user.is_authenticated() and not user.is_active:
            mensaje = u'¡Su cuenta en mintur se encuentra desactivada, por favor contacte al equipo de soporte!'
            messages.info(self.request, mensaje)

        return redirect(reverse_lazy('cuentas_logout'))


def determinar_tipo_figura(rif_unicode):
    if rif_unicode.lower().startswith(u'v'):
        return PERSONA_NATURAL
    return PERSONA_JURIDICA
