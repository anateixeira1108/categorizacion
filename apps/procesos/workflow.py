# coding=utf-8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# Copyright (C) 2014 4geeks <correo.4geeks.com.ve>
# License: http://www.4geeks.co/inicio
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from django.shortcuts import render
from apps.procesos.models import Proceso,  Flujo, FlujoSecuencia
from apps.procesos.models import ProcesoPst, HistorialSecuencia
from registro.models import Pst, ESTATUS_REGISTRO_SIN_COMPLETAR
from utils.gluon.storage import Storage
from datetime import datetime

from apps.cuentas.models import MinturUser as User

INICIO = 'Inicio'
ACTUALIZAR = 'Siguiente'

class Workflow(object):
    """
    Clase que manejara las funciones del Workflow para los pst
    """

    def __init__(self, pst, nombre_proceso, observaciones="", cargar=""):
        """
        Inicia el Workflow para un pst
        Parametros
        - pst (Object): Objeto pst
        - nombre_proceso (String): Nombre del proceso que se activara
        - observaciones (String): Observaciones que se desean registrar
        - cargar (String|list|tuple): usada para indicar que atributos cargar
        """
        self.pst = pst
        self.nombre_proceso = nombre_proceso
        self.observaciones = observaciones
        self.proceso = None
        self.procesoPst = None
        self.nombre_estado = None
        self.fecha_inicio = None
        self.historial = None

        # Funciones
        self.validar_datos()
        self.obtener_proceso_pst()

        if cargar == "*" or 'datos' in cargar:
            self.cargar_estado()

        if cargar == "*" or 'historial' in cargar:
            self.cargar_historial()

    def iniciar(self):
        """
        Inicia el Workflow con el nombre solicitado para un pst y lo guarda
        Retorna
        - procesoPst (Object): Objeto ProcesoPst
        """
        if self.procesoPst:
            raise NameError('Error de operacion. Ya se ha iniciado el proceso para el Pst indicado')

        estado = self.obtener_estado(INICIO)

        data = Storage(
            pst = self.pst, proceso = self.proceso,
            estado = estado, nombre_estado = estado.nombre,
            activo = True, fecha_inicio = datetime.now()
        )
        self.procesoPst = ProcesoPst(**data)
        self.nombre_estado = estado.nombre
        self.procesoPst.save()
        self.registrar_historial(estado)

        return self.procesoPst

    def actualizar(self, siguiente_estado):
        """
        Actualiza el Workflow solicitado para un pst y lo guarda
        Parametros
        - siguiente_estado (Int): Integer con el id del siguiente estado
        Retorna
        - proceso_pst
        """
        if not self.procesoPst:
            raise NameError('Error de operacion. No se puedo actualizar si no se ha iniciado el proceso')
        estado = self.obtener_estado(ACTUALIZAR, siguiente_estado)

        if self.procesoPst.estado == estado:
            raise NameError('Error de operacion. Ya se encuentra en el estado indicado')

        self.procesoPst.estado = estado
        self.procesoPst.nombre_estado = estado.nombre
        self.nombre_estado = estado.nombre

        if estado.fin == True:
            self.procesoPst.activo = False
            self.procesoPst.fecha_fin = datetime.now()

        self.procesoPst.save()
        self.registrar_historial(estado)

        return self.procesoPst

    def validar_datos(self):
        """
        Funcion que valida los tipos parametros enviados al crear una instancia de
        Workflow
        Nota: Esta funcion se llama automaticamente cuando se inicia el Workflow
        """
        if not isinstance(self.pst, Pst):
            raise NameError('Error de Tipo. El atributo pst debe ser una instancia Pst')

        if self.pst.estatus == ESTATUS_REGISTRO_SIN_COMPLETAR:
            raise NameError('Error de Estado. El Pst debe tener un estado de registro completado')

        try:
           self.proceso = Proceso.objects.get(nombre__exact=str(self.nombre_proceso), activo=True)
        except Proceso.DoesNotExist:
            raise NameError('Error de Registro. El proceso que solicito no esta registrado o activo')

        if not Flujo.objects.filter(proceso=self.proceso):
            raise NameError('Error de Registro. No hay Flujos registrados para el proceso Iniciado')

        if not FlujoSecuencia.objects.filter(proceso=self.proceso):
            raise NameError('Error de Registro. No hay secuencias registradas para el flujo del proceso indicado')

    def obtener_estado(self, tipo, id_estado=""):
        """
        Funcion que obtiene el estado del proceso que se esta ejecutando para un pst
        Retorna
        - estado (Object): Flujo
        """
        estado = None

        if tipo == INICIO:
            search = Storage(proceso=self.proceso, inicio=True)

        if tipo == ACTUALIZAR and id_estado != "":
            search = Storage(pk=id_estado)

        estado = Flujo.objects.get(**search)

        return estado

    def obtener_proceso_pst(self):
        """
        Funcion que obtiene el proceso activo para un pst
        """
        proceso_pst = []

        try:
            self.procesoPst = ProcesoPst.objects.get(proceso=self.proceso, activo=True, pst=self.pst)
        except ProcesoPst.DoesNotExist:
            pass

        if not self.procesoPst:
            search = Storage(nombre__exact=str(self.nombre_proceso), activo=False)
            procesos = Proceso.objects.filter(**search)

            if any(procesos):
                search = Storage(proceso__in=procesos, activo=True)
                proceso_pst = ProcesoPst.objects.filter(**search)

                if proceso_pst:
                    self.procesoPst = proceso_pst[0]
                    self.proceso = proceso_pst[0].proceso

    def cargar_estado(self):
        """
        Funcion que carga el estado actual de proceso iniciado
        """
        if self.procesoPst:
            proceso_pst = ProcesoPst.objects.get(pst=self.pst, proceso=self.proceso, activo=True)
            self.nombre_estado = proceso_pst.nombre_estado
            self.fecha_inicio = proceso_pst.fecha_inicio

    def cargar_historial(self):
        """
        Funcion que carga el historial del proceso iniciado
        """
        if self.procesoPst:
            self.historial = HistorialSecuencia.objects.filter(proceso_pst=self.procesoPst)

    def registrar_historial(self, estado):
        """
        Funcion que guarda el historial de los pasos realizados para cada proceso
        Parametros
        - Estado (Object): Objeto estado para generar el historial
        """
        user = User.objects.get(pk=1) # Usuario defecto
        if self.request.user:
            user = self.request.user
            
        data = Storage(
            user = user, proceso_pst = self.procesoPst,
            estado = estado, observaciones = self.observaciones,
            proceso = self.proceso
        )

        historial = HistorialSecuencia(**data)
        historial.save()




