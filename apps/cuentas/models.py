# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from .signals import create_new_user_signal


ROLE_ADMIN = 1
ROLE_PST = 2
ROLE_FUNCIONARIO = 3
ROLE_FUNCIONARIO_APOYO = 4

ROLE_CHOICES = (
    (ROLE_ADMIN, u'Administrador'),
    (ROLE_PST, u'PST'),
    (ROLE_FUNCIONARIO, u'Funcionario'),
    (ROLE_FUNCIONARIO_APOYO, u'Funcionario_apoyo'),
)


class MinturUserManager(BaseUserManager):
    def create_user(self, correo_electronico, correo_electronico2, rif, nombres, apellidos, password=None, is_superuser=False):
        """ Creates and saves a User with the given email, RIF , password. """

        if not correo_electronico:
            msg = u'Usuarios deben tener un correo electrónico'
            raise ValueError(msg)

        if not correo_electronico2:
            msg = u'Usuarios deben tener un correo electrónico secundario'
            raise ValueError(msg)

        if not rif:
            msg = u'Usuarios deben tener un RIF'
            raise ValueError(msg)

        if not nombres:
            msg = u'Usuarios deben tener un Nombre'
            raise ValueError(msg)

        if not apellidos:
            msg = u'Usuarios deben tener un Apellido'
            raise ValueError(msg)

        user = self.model(
            correo_electronico=MinturUserManager.normalize_email(correo_electronico),
            correo_electronico2=MinturUserManager.normalize_email(correo_electronico2),
            rif=rif,
            nombres=nombres,
            apellidos=apellidos,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, correo_electronico2, rif, nombres, apellidos, password):
        """ Creates and saves a superuser with the given email, rif and password. """
        user = self.create_user(
            correo_electronico=correo_electronico,
            correo_electronico2=correo_electronico2,
            password=password,
            rif=rif,
            nombres=nombres,
            apellidos=apellidos,
            is_superuser=True
        )

        user.is_superuser = True
        user.is_admin = True
        user.role = ROLE_ADMIN
        user.save(using=self._db)
        return user


class MinturUser(AbstractBaseUser, PermissionsMixin):
    """ Model for the PST User """
    nombres = models.CharField(verbose_name=u'Nombres', max_length=255)
    apellidos = models.CharField(verbose_name=u'Apellidos', max_length=255)
    rif = models.CharField(verbose_name=u'RIF', max_length=20, unique=True)
    cedula = models.CharField(verbose_name=u'Cedula', max_length=20, unique=True, null=True, blank=True)
    correo_electronico = models.EmailField(verbose_name=u'Correo electrónico', max_length=255, unique=True)
    correo_electronico2 = models.EmailField(verbose_name=u'Correo electrónico secundario', max_length=255, unique=True)
    
    activation_key = models.CharField(max_length=255, null=True, blank=True)
    account_activation_date = models.DateTimeField(null=True, blank=True)
    reset_password_key = models.CharField(max_length=255, null=True, blank=True)
    reset_password_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ROLE_PST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MinturUserManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'rif', 'correo_electronico2']

    def get_full_name(self):
        return u'%s %s' % (self.nombres, self.apellidos)

    def get_short_name(self):
        return self.email

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def is_staff(self):
        return False

    def is_pst(self):
        return self.role == ROLE_PST

    def is_funcionario(self):
        return self.role == ROLE_FUNCIONARIO

    # def save(self, *args, **kwargs):
    #     self.email = MinturUserManager.normalize_email(self.correo_electronico)
    #     super(MinturUser, self).save(*args, **kwargs)

    def activar_cuenta(self):
        self.is_active = True
        self.activation_key = ''
        self.account_activation_date = datetime.datetime.now()
        self.save()

    def __unicode__(self):
        return u'%s - %s' % (self.correo_electronico, self.rif)


GROUP_1 = 1
GROUP_2 = 2
GROUP_3 = 3

QUESTION_GROUP = (
    (GROUP_1, u'Grupo 1'),
    (GROUP_2, u'Grupo 2'),
    (GROUP_3, u'Grupo 3')
)


class Question(models.Model):
    """
    Atributos para el objeto Question
    Contiene las preguntas genericas para los usuarios
    """
    question = models.CharField(max_length=255, verbose_name=u'Pregunta secreta')
    group = models.IntegerField(choices=QUESTION_GROUP, default=GROUP_1)

    def __unicode__(self):
        return self.question

class QuestionUser(models.Model):
    """
    Atributos para el objeto QuestionUser
    Contiene las respuestas de las preguntas seleccionadas por el usuario
    """
    question = models.ForeignKey(Question, verbose_name=u'Pregunta secreta')
    user = models.ForeignKey(MinturUser, verbose_name=u'Usuario')
    answer = models.CharField(max_length=255, verbose_name=u'Respuesta')


signals.post_save.connect(create_new_user_signal, sender=MinturUser)