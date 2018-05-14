# coding=utf-8
from django.db import models
from utils.gluon.storage import Storage
from registro.models import Pst
from django.conf import settings
from django.contrib.auth.models import Group


class Proceso(models.Model):
    """
    Modelo Proceso
    Contiene los procesos que se realizaran en el sistema
    -> Nota Importante: Solo puede haber un proceso activo con el mismo nombre <-
    Descripcion:
        - nombre: nombre del proceso
        - descripcion: descripcion del proceso
        - activo: define si el proceso esta activo o no
        - fecha_creacion: fecha de creacion del proceso
        - fecha_desactivacion: fecha desactivacion del proceso
    """
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion =  models.DateTimeField(auto_now_add=True)
    fecha_desactivacion = models.DateTimeField(blank=True, null=True)


class Flujo(models.Model):
    """
    Modelo Flujo
    Contiene los flujos que se realizaran en el sistema para cada proceso
    Descripcion:
        - proceso: proceso que pertenece este flujo
        - grupo: grupo que manejara el flujo
        - nombre: nombre del flujo
        - inicio: define si el flujo inicia el proceso
        - fin: define si el flujo finaliza el proceso
    """
    proceso = models.ForeignKey(Proceso)
    grupo = models.ForeignKey(Group)
    nombre = models.CharField(max_length=75)
    inicio = models.BooleanField(default=False)
    fin = models.BooleanField(default=False)


class FlujoSecuencia(models.Model):
    """
    Modelo Flujo
    Contiene las secuencias de los flujos para cada proceso creado
    -> Nota Importante: el actual y el siguiente son relacion del objeto Flujo <-
    Descripcion:
        - actual: posicion actual del flujo en la secuencia
        - siguiente: posicion que deberia ir en la secuencia
        - proceso: proceso que pertenece esta secuencia
    """
    actual = models.IntegerField()
    siguiente = models.IntegerField()
    proceso = models.ForeignKey(Proceso)


class ProcesoPst(models.Model):
    """
    Modelo ProcesoPst
    Contiene el estado para los procesos que se inicien para cada pst
    Descripcion:
        - pst: objeto Pst
        - proceso: obejo proceso
        - estado: estado actual del objeto flujo
        - nombre_estado: nombre del estado actual del objeto flujo
        - activo: boolean que define si el proceso esa activo
        - fecha_inicio: fecha se cuando se inicio el proceso
        - fecha_fin: fecha cuando se finalizo el proceso
    """
    pst = models.ForeignKey(Pst)
    proceso = models.ForeignKey(Proceso)
    estado = models.ForeignKey(Flujo)
    nombre_estado = models.CharField(max_length=75)
    activo = models.BooleanField(default=True)
    fecha_inicio =  models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)


class HistorialSecuencia(models.Model):
    """
    Modelo HistorialSecuencia
    Contiene el historial de flujos ejecutados para cada pst
    Descripcion: 
        - user: usuario que creo la secuencia
        - proceso_pst: objeto ProcesoPst que pertenece a la secuencia
        - proceso: proceso que pertenece la secuencia
        - estado: estado actual de la secuencia
        - observaciones: observaciones realizadas
        - fecha_registro: fecha de registro
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    proceso_pst = models.ForeignKey(ProcesoPst)
    proceso = models.ForeignKey(Proceso)
    estado = models.ForeignKey(Flujo)
    observaciones = models.TextField(max_length=250, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

