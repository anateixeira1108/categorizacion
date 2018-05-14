# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from apps.cuentas.models import MinturUser
from django.contrib.auth import authenticate
from apps.cuentas.models import (
    Question, QuestionUser, GROUP_1, GROUP_2, GROUP_3
)

from passwords.fields import PasswordField
from utils import checkers


PST = 2

EMPRENDEDOR = 3

TIPO_PST_REGISTRO = (
    (PST, u'Prestador de servicios turisticos'),
    (EMPRENDEDOR, u'Emprendedor')
)


class PSTUserRegistrationForm(forms.ModelForm):
    """ User registration form """
    password1 = PasswordField(
        label=u'Contraseña',
        widget=forms.PasswordInput(render_value=False),
        required=True
    )

    password2 = forms.CharField(
        label=u'Confirmación de Contraseña',
        widget=forms.PasswordInput(render_value=False),
        required=True
    )

    tipo_pst = forms.ChoiceField(
        label=u'Perfil de usuario',
        widget=forms.Select(),
        choices=TIPO_PST_REGISTRO,
        required=True
    )

    pregunta_1 = forms.ModelChoiceField(
        label=u'Escoja su primera pregunta secreta',
        queryset=Question.objects.filter(group=GROUP_1)
    )

    pregunta_2 = forms.ModelChoiceField(
        label=u'Escoja su segunda pregunta secreta',
        queryset=Question.objects.filter(group=GROUP_2)
    )

    pregunta_3 = forms.ModelChoiceField(
        label=u'Escoja su tercera pregunta secreta',
        queryset=Question.objects.filter(group=GROUP_3)
    )

    respuesta_1 = forms.CharField(
        label=u'Respuesta a su primera pregunta',
        max_length=255,
        required=True
    )

    respuesta_2 = forms.CharField(
        label=u'Respuesta a su segunda pregunta',
        max_length=255,
        required=True
    )

    respuesta_3 = forms.CharField(
        label=u'Respuesta a su tercera pregunta',
        max_length=255,
        required=True
    )

    def clean(self):
        """ Validates that the values entered into the two password fields match. """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                msg = u'Las contraseñas proporcionadas no coinciden.'
                raise forms.ValidationError(msg)

        if 'correo_electronico' in self.cleaned_data and 'correo_electronico2' in self.cleaned_data:
            correo1 = self.cleaned_data['correo_electronico']
            correo2 = self.cleaned_data['correo_electronico2']
            if correo1 == correo2:
                msg = u'La direcciones de correo electrónico porporcionadas no pueden ser iguales.'
                raise forms.ValidationError(msg)

            elif correo1.split('@')[1] == correo2.split('@')[1]:
                msg = u'La direcciones de correo electrónico no pueden pertenecer al mismo dominio.'
                raise forms.ValidationError(msg)

        return self.cleaned_data

    def clean_nombres(self):
        """ Valida los nombres """

        nombres = self.cleaned_data['nombres'].strip()

        if not checkers.is_valid(nombres, 'nombres/apellidos'):
            msg = (
                u'Solo se permiten vocales, consonantes y espacios.'
            )
            raise forms.ValidationError(msg)

        return nombres

    def clean_apellidos(self):
        """ Valida los apellidos """

        apellidos = self.cleaned_data['apellidos'].strip()

        if not checkers.is_valid(apellidos, 'nombres/apellidos'):
            msg = (
                u'Solo se permiten vocales, consonantes y espacios.'
            )
            raise forms.ValidationError(msg)

        return apellidos

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data['correo_electronico']

        if MinturUser.objects.filter(correo_electronico=correo_electronico):
            msg = u'El correo electrónico proporcionado ya esta siendo usado.'
            raise forms.ValidationError(msg)

        return correo_electronico

    def clean_correo_electronico2(self):
        correo_electronico2 = self.cleaned_data['correo_electronico2']

        if MinturUser.objects.filter(correo_electronico2=correo_electronico2):
            msg = u'El correo electrónico secundario proporcionado ya esta siendo usado.'
            raise forms.ValidationError(msg)

        return correo_electronico2

    def clean_rif(self):
        """ Valida el RIF y verifica que éste sea único """

        user = MinturUser.objects.filter(rif=self.cleaned_data['rif'])

        if not checkers.is_valid(self.cleaned_data['rif'], 'rif'):
            msg = u'El formato del RIF proporcionado no es correcto.'
            raise forms.ValidationError(msg)

        if user and user[0].rif != self.initial.get('rif'):
            msg = u'Este RIF ya está en uso, por favor ingrese uno diferente'
            raise forms.ValidationError(msg)

        return self.cleaned_data['rif']

    class Meta:
        model = MinturUser
        fields = ('correo_electronico', 'correo_electronico2', 'nombres', 'apellidos', 'rif')


class UserAuthenticationForm(forms.Form):
    """ Authentication form """
    correo_electronico = forms.EmailField(
        label=u'Correo electrónico',
    )

    password = forms.CharField(
        label=u'Contraseña',
        widget=forms.PasswordInput(render_value=False)
    )

    def clean(self):
        correo_electronico = self.cleaned_data['correo_electronico']
        password = self.cleaned_data['password']

        user = authenticate(correo_electronico=correo_electronico, password=password)

        if not user:
            msg = u'La combinación correo electrónico y contraseña son incorrectos.'
            raise forms.ValidationError(msg)

        elif not user.is_active and user.activation_key:
            msg = u'La cuenta que esta intentando utilizar aún no se ha activado ' \
                  u'por favor ingrese a su correo para conocer los detalles para activar la misma'
            raise forms.ValidationError(msg)

        elif not user.is_active:
            msg = u'La cuenta que esta intentando utilizar se encuentra desactivada ' \
                  u'por favor contacte a Mintur para resolver este incidente.'
            raise forms.ValidationError(msg)

        return self.cleaned_data


OLVIDE_PASSWORD = 1

OLVIDE_CORREO_ELECTRONICO = 2

OLVIDE = (
    (OLVIDE_PASSWORD, u'He olvidado mi contraseña'),
    (OLVIDE_CORREO_ELECTRONICO, u'He olvidado mi correo electrónico')
)


class NeedhelpForm(forms.Form):
    olvide = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=OLVIDE,
        required=True,
        error_messages={'required': u'Debe escoger una opcion para recuperación de contraseña'}
    )

    correo_electronico = forms.EmailField(
        label=u'Correo electrónico',
        required=False
    )

    rif = forms.CharField(
        label=u'RIF',
        required=False
    )

    def clean(self):
        if 'olvide' in self.cleaned_data.keys():
            opcion = int(self.cleaned_data['olvide'])
            correo_electronico = self.cleaned_data['correo_electronico']
            rif = self.cleaned_data['rif']

            if opcion == OLVIDE_PASSWORD:
                if not MinturUser.objects.filter(correo_electronico=correo_electronico):
                    self._errors["correo_electronico"] = ErrorList([
                        u'El correo electrónico proporcionado no se encuentra registrado en Mintur.'])

            if opcion == OLVIDE_CORREO_ELECTRONICO:
                if not MinturUser.objects.filter(rif=rif):
                    self._errors["rif"] = ErrorList([
                        u'El RIF proporcionado no se encuentra registrado en Mintur.'])

            return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password1 = PasswordField(
        label=u'Contraseña',
        widget=forms.PasswordInput(render_value=False),
        required=True
    )

    password2 = forms.CharField(
        label=u'Confirmación de Contraseña',
        widget=forms.PasswordInput(render_value=False),
        required=True
    )

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                msg = u'Las contraseñas proporcionadas no coinciden.'
                raise forms.ValidationError(msg)

        return self.cleaned_data


class SecretQuestionsForm(forms.Form):
    rif = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=255,
        required=True
    )

    pregunta_1 = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )

    pregunta_2 = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )

    respuesta_1 = forms.CharField(
        max_length=255,
        required=True
    )

    respuesta_2 = forms.CharField(
        max_length=255,
        required=True
    )

    def clean_rif(self):
        rif = self.cleaned_data['rif']

        if not MinturUser.objects.filter(rif=rif):
            msg = u'El RIF proporcionado no existe.'
            raise forms.ValidationError(msg)

        return rif

    def clean(self):
        super(forms.Form, self).clean()
        if 'rif' and 'pregunta_1' and 'pregunta_2' and 'respuesta_1' and 'respuesta_2' in self.cleaned_data.keys():
            rif = self.cleaned_data['rif']
            try:
                # Obtenemos el usuario
                usuario = MinturUser.objects.get(rif=rif)

                # Obtenemos sus preguntas
                preguntas_usuario = usuario.questionuser_set.all()
                preguntas_id = [pregunta.question.id for pregunta in preguntas_usuario]

                # verificamos que la pregunta 1 y 2 le pertenezcan a este usuario
                pregunta_1 = int(self.cleaned_data['pregunta_1'])
                pregunta_2 = int(self.cleaned_data['pregunta_2'])

                if not (pregunta_1 and pregunta_2 in preguntas_id):
                    msg = u'Estas preguntas no le pertenecen al usuario.'
                    raise forms.ValidationError(msg)

                # verificamos que las respuestas sean correctas
                respuesta_1 = self.cleaned_data['respuesta_1']
                respuesta_2 = self.cleaned_data['respuesta_2']

                pregunta_usuario_1 = QuestionUser.objects.get(user=usuario, question=pregunta_1, answer=respuesta_1)
                pregunta_usuario_2 = QuestionUser.objects.get(user=usuario, question=pregunta_2, answer=respuesta_2)

            except MinturUser.DoesNotExist:
                msg = u'El usuario no se encuentra registrado en Mintur.'
                raise forms.ValidationError(msg)

            except QuestionUser.DoesNotExist:
                msg = u'Ha contestado incorrectamente una o mas preguntas secretas.'
                raise forms.ValidationError(msg)

        return self.cleaned_data

