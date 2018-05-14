# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.procesos.workflow import Workflow
from apps.procesos.models import Proceso, Flujo, FlujoSecuencia
from apps.procesos.models import ProcesoPst, HistorialSecuencia
from registro.models import Pst, ESTATUS_REGISTRO_COMPLETADO
from apps.cuentas.models import MinturUser as User
from django.contrib.auth.models import Group
from utils.gluon.storage import Storage
from datetime import datetime
import random
# import pdb; pdb.Pdb(skip=['django.*']).set_trace()


class WorkflowTest(TestCase):
    """Implementando pruebas unitarias para la clase Workflow """

    fixtures = [
        'fixtures/000_tipo_pst.json',
        'fixtures/001_cuentas_pst.json',
        'fixtures/002_registro_pst_inicial.json'
    ]

    def setUp(self):
        self.wf = None

        # Creamos los datos del proceso para pruebas
        self.p = [
            Storage(
                id=1, nombre="Prueba",
                descripcion="esta es una prueba de un proceso", activo = True,
                fecha_desactivacion = None
            ),
            Storage(
                id=2, nombre="Prueba Numero Dos",
                descripcion="esta es una prueba de un proceso", activo = True,
                fecha_desactivacion = None
            ),
            Storage(
                id=3, nombre="Prueba Numero Tres",
                descripcion="esta es una prueba de un proceso", activo = True,
                fecha_desactivacion = None
            ),
            Storage(
                id=4, nombre="Prueba",
                descripcion="esta es una prueba de un proceso version 2", activo = False,
                fecha_desactivacion = None
            )

        ]

        self.inactivo =Storage(
            id=5, nombre="Prueba Inactivo",
            descripcion="esta es una prueba de un proceso", activo = False,
            fecha_desactivacion = datetime.now()
        )

        self.sin_flujo = Storage(
            id=6, nombre="Prueba Sin flujo",
            descripcion="esta es una prueba de un proceso", activo = True,
            fecha_desactivacion = None
        )


        #Creamos grupos de usuarios
        self.objGroup = []
        grupos = [
            Storage(name="Nombre del grupo uno"),
            Storage(name="Nombre del grupo dos"),
            Storage(name="Nombre del grupo tres"),
            Storage(name="Nombre del grupo cuatro")
        ]
        # Guardamos los datos del proceso y los grupos de usuarios
        self.proceso_inactivo = Proceso(**self.inactivo)
        self.proceso_sin_flujo = Proceso(**self.sin_flujo)
        self.proceso_inactivo.save()
        self.proceso_sin_flujo.save()

        for p in self.p:
            self.proceso = Proceso(**p)
            self.proceso.save()

        for gp in grupos:
            g = Group(**gp)
            g.save()
            self.objGroup.append(g)

        #Asignamos grupos a los usuarios registrados
        users = User.objects.all()[0:4]
        for i, u in enumerate(users):
            u.groups.add(self.objGroup[1-i])

        # Creamos los datos del flujo para el proceso
        flujos = [
            Storage(proceso=None, grupo=self.objGroup[0], nombre="Primer paso", inicio=True, fin=False),
            Storage(proceso=None, grupo=self.objGroup[1], nombre="Segundo paso", inicio=False, fin=False),
            Storage(proceso=None, grupo=self.objGroup[0], nombre="Regresando paso uno", inicio=False, fin=False),
            Storage(proceso=None, grupo=self.objGroup[2], nombre="Tercer paso", inicio=False, fin=False),
            Storage(proceso=None, grupo=self.objGroup[3], nombre="Cuarto paso fin", inicio=False, fin=True)
        ]

        # Creamos instancias de los objetos y los guardamos
        for p in self.p:
            fls = flujos
            for fl in fls:
                fl.proceso=Proceso.objects.get(pk=p.id)
                f = Flujo(**fl)
                f.save()

        for p in self.p:
            fls = Flujo.objects.filter(proceso=p.id)
            proceso=Proceso.objects.get(pk=p.id)
            fujos_secuencias = [
                Storage(actual=fls[0].id, siguiente=fls[1].id, proceso=proceso),
                Storage(actual=fls[1].id, siguiente=fls[2].id, proceso=proceso),
                Storage(actual=fls[2].id, siguiente=fls[0].id, proceso=proceso),
                Storage(actual=fls[3].id, siguiente=fls[4].id, proceso=proceso)
            ]
            for fs in fujos_secuencias:
                f = FlujoSecuencia(**fs)
                f.save()

        #Obteniendo pst aleatorio para las pruebas
        self.proceso = Proceso.objects.get(pk=random.randint(1, len(self.p)-1) )
        random_id = random.randint(1, Pst.objects.count())
        self.pst = Pst.objects.get(id=random_id)

    def test_A_validar_datos(self):
        """
        ¿Validando que se crearon los procesos para prueba?
        ¿Valida que el tipo de dato pst sea un Objeto pst?
        ¿Valida que el que el pst tenga estado de registro completado?
        ¿Valida que el proceso solicitado exista?
        ¿Se crea correctamente la instancia del Workflow?
        """
        print "## Prueba para metodo validar_datos ##"

        # Validando que se crearon los datos de prueba
        self.assertEqual(FlujoSecuencia.objects.count(), 16)
        self.assertEqual(Flujo.objects.count(), 20)

        # Validando que el parametro pst se instancia Pst
        with self.assertRaisesRegexp(NameError, 'Error de Tipo. El atributo pst debe ser una instancia Pst'):
            wf = Workflow(int(), self.proceso.nombre)

        # Validando estado de registro del pst
        with self.assertRaisesRegexp(NameError, 'Error de Estado. El Pst debe tener un estado de registro completado'):
            wf = Workflow(self.pst, self.proceso.nombre)

        # Cambiamos estado del pst
        self.pst.estatus = ESTATUS_REGISTRO_COMPLETADO
        self.pst.save()

        # Validando que exista el proceso
        with self.assertRaisesRegexp(NameError, 'Error de Registro. El proceso que solicito no esta registrado o activo'):
            wf = Workflow(self.pst, '2')

        with self.assertRaisesRegexp(NameError, 'Error de Registro. El proceso que solicito no esta registrado o activo'):
            wf = Workflow(self.pst, self.inactivo.nombre)

        with self.assertRaisesRegexp(NameError, 'Error de Registro. No hay Flujos registrados para el proceso Iniciado'):
            wf = Workflow(self.pst, self.sin_flujo.nombre)

        # Creando instancia Workflow
        wf = Workflow(self.pst, self.proceso.nombre)
        self.assertIsNotNone(wf)

    def test_B_iniciar(self):
        """
        ¿Se inicia el proceso correctamente?
        ¿El ProcesoPst iniciado es igual que el proceso creado?
        ¿Se pueden crear dos procesos para el mismo pst con el mismo nombre?
        ¿Se crea el historial para el Proceso Pst iniciado?
        ¿El estado de proceso es el inicial?
        ¿El nombre del estado es el correcto?
        ¿Esta activo el proceso en procesoPst?
        ¿Se creo el historial para el inicio del proceso?
        ¿Verificamos que el historial sea una instancia de HistorialSecuencia?
        ¿El historial es igual al del proceso iniciado?
        ¿Se registro la observacion correctamente?
        ¿El historial tiene usuario asignado?
        ¿El usuario de historial es una instancia de MinturUser?
        """
        print "## Prueba para metodo iniciar ##"

        self.pst.estatus = ESTATUS_REGISTRO_COMPLETADO
        self.pst.save()

        # Creando instancia Workflow
        parametros = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            observaciones="Observaciones para registro"
        )

        wf = Workflow(**parametros)
        proceso_test = Proceso.objects.get(nombre__exact=self.proceso.nombre, activo=True)

        # Verificamos el inicio del proceso correctamente
        proceso_pst = wf.iniciar()
        self.assertIsNotNone(proceso_pst)

        # Verificamos que el proceso no se inicie nuevamente
        with self.assertRaisesRegexp(NameError, 'Error de operacion. Ya se ha iniciado el proceso para el Pst indicado'):
            wf.iniciar()

        # Verificamos que el procesoPst iniciado sea igual al proceso Creado
        self.assertEqual(proceso_test, proceso_pst.proceso)

        # #Verificamos que se creo el
        historial = HistorialSecuencia.objects.get(proceso_pst=proceso_pst)
        self.assertIsNotNone(historial)

        # #Verificamos que el estado creado sea el inicial
        estado = Flujo.objects.get(proceso=proceso_test, inicio=True)
        self.assertIsNotNone(estado)
        self.assertEqual(historial.estado, estado)

        # Creamos un nueva instancia de Workflow
        data = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            cargar="*"
        )
        wf = Workflow(**data)

        # Verificamos si el proceso esta activo
        self.assertTrue(wf.procesoPst.activo)

        # Verificamos si se creo el historial
        self.assertEqual(len(wf.historial), 1)

        # Validamos que sea una instancia de historial
        historial = wf.historial[0]
        self.assertIsInstance(historial, HistorialSecuencia)

        # Validamos que el primer registro sea del estado correcto
        self.assertEqual(historial.estado, estado)

        # El Historial creado es del proceso_pst correcto
        proceso_pst = ProcesoPst.objects.get(pst=self.pst, proceso=self.proceso)
        self.assertEqual(historial.proceso_pst, proceso_pst)

        # Validamos que se guardo las observaciones correctamente
        self.assertEqual(historial.observaciones, parametros.observaciones)

        # Validamos que el usuario que creo no sea nulo
        self.assertIsNotNone(historial.user)

        # Validamos que sea una instancia de MinturUser
        self.assertIsInstance(historial.user, User)

    def test_C_obtener_proceso_pst(self):
        """
        ¿Obtenemos el proceso del pst ya iniciado?
        ¿Obtenemos el estado del proceso inicial?
        ¿Validamos que el atributo activo sea True?
        ¿El estado que se registro es el correcto?
        ¿Se desactiva el proceso correctamente?
        ¿Se obtiene el proceso iniciado anteriormente cuando ya esta desactivado?
        ¿Se obtiene un solo registro de historial?
        """
        print "## Prueba para metodo obtener_proceso_pst ##"

        self.pst.estatus = ESTATUS_REGISTRO_COMPLETADO
        self.pst.save()

        # Iniciamos varios procesos para un pst
        parametros = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            observaciones="Vamos a crear una Observacion"
        )
        wf = Workflow(**parametros)
        wf.iniciar()

        data_inicio = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            cargar="*"
        )
        wf = Workflow(**data_inicio)

        # validamos que el proceso pst no sea none
        self.assertIsNotNone(wf.procesoPst)

        # Validamos si activo es True
        self.assertTrue(wf.procesoPst.activo)

        # Validamos que el estado sea el que iniciamos
        estado = Flujo.objects.get(proceso=self.proceso, inicio=True)
        self.assertEqual(wf.procesoPst.estado, estado)

        # Validamos nombre del estado
        self.assertEqual(wf.procesoPst.nombre_estado, estado.nombre)
        self.assertEqual(wf.nombre_estado, estado.nombre)

        # Desactivamos el proceso anterior
        proceso_viejo = Proceso.objects.get(pk=self.proceso.id)
        proceso_viejo.activo = False
        proceso_viejo.fecha_desactivacion = datetime.now()
        proceso_viejo.save()

        # Verificamos que el proceso de desactivo
        self.assertFalse(proceso_viejo.activo)

        # Verificamos que el que se desactivo sea igual al creado
        self.assertEqual(proceso_viejo.nombre, self.proceso.nombre)
        self.assertEqual(proceso_viejo.id, self.proceso.id)

        # Creamos un proceso nuevo
        data = Storage(
            id = 7, nombre = self.proceso.nombre,
            descripcion = "Esta es una modificacion del proceso prueba", activo = True,
            fecha_desactivacion = None
        )
        proceso_nuevo = Proceso(**data)
        proceso_nuevo.save()

        flujos = [
            Storage(proceso=proceso_nuevo, grupo=self.objGroup[0], nombre="Primer paso", inicio=True, fin=False),
            Storage(proceso=proceso_nuevo, grupo=self.objGroup[1], nombre="Segundo paso", inicio=False, fin=False),
            Storage(proceso=proceso_nuevo, grupo=self.objGroup[0], nombre="Regresando paso uno", inicio=False, fin=False),
            Storage(proceso=proceso_nuevo, grupo=self.objGroup[2], nombre="Tercer paso", inicio=False, fin=False),
            Storage(proceso=proceso_nuevo, grupo=self.objGroup[3], nombre="Cuarto paso fin", inicio=False, fin=True)
        ]

        for fl in flujos:
            f = Flujo(**fl)
            f.save()

        fls = Flujo.objects.filter(proceso=proceso_nuevo)
        fujos_secuencias = [
            Storage(actual=fls[0].id, siguiente=fls[1].id, proceso=proceso_nuevo),
            Storage(actual=fls[1].id, siguiente=fls[2].id, proceso=proceso_nuevo),
            Storage(actual=fls[2].id, siguiente=fls[0].id, proceso=proceso_nuevo),
            Storage(actual=fls[3].id, siguiente=fls[4].id, proceso=proceso_nuevo)
        ]

        for fs in fujos_secuencias:
            f = FlujoSecuencia(**fs)
            f.save()


        # Creamos una instancia con el proceso viejo
        data_vieja = Storage(
            pst=self.pst,
            nombre_proceso=proceso_nuevo.nombre,
            cargar="*"
        )

        # import pdb; pdb.Pdb(skip=['django.*']).set_trace()
        #Creamos una instancia de proceso desactivado
        wf_viejo = Workflow(**data_vieja)
        self.assertEqual(wf_viejo.procesoPst.proceso, proceso_viejo)

        # Existe un solo registro de historial
        self.assertEqual(len(wf_viejo.historial), 1)

        # El historial es obtenido el creado originalmente
        historial = wf_viejo.historial[0]
        estado_inicial = Flujo.objects.get(proceso=wf_viejo.proceso, inicio=True)
        self.assertIsInstance(historial, HistorialSecuencia)
        self.assertEqual(historial.observaciones, parametros.observaciones)
        self.assertEqual(historial.estado, estado_inicial)
        self.assertEqual(historial.proceso, wf_viejo.proceso)


    def test_D_actualizar(self):
        """
        ¿Se puede actualizar el proceso que no se ha iniciado?
        ¿Un pst puede tener dos procesos activos del mismo tipo?
        ¿Se actualiza correctamente el proceso iniciado?
        ¿El estado actualizado es el correcto?
        ¿El flujo secuencia es el correcto?
        ¿La cantidad del historial creada es la misma cantidad registrada?
        ¿El historial se creo correctamente?
        ¿El primer registro del historial es de la secuencia inicial?
        ¿El historial creado es del proceso indicado?
        ¿El segundo registro del historial es de la secuencia actualizada?
        ¿El el historial del procesoPst sea el correspondiente?
        ¿Se Registro correctamente las observaciones?
        ¿Se Finalizo el proceso correctamente?
        ¿Se registro el historial de finalizacion?
        """
        print "## Prueba para metodo actualizar ##"

        estado = Flujo.objects.filter(proceso=self.proceso)[1]
        self.pst.estatus = ESTATUS_REGISTRO_COMPLETADO
        self.pst.save()

        parametros_iniciales = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            observaciones= "este es un comentario de prueba"
        )

        wf = Workflow(**parametros_iniciales)

        # Actualizamos un proceso no iniciado
        with self.assertRaisesRegexp(NameError, 'Error de operacion. No se puedo actualizar si no se ha iniciado el proceso'):
            wf.actualizar(estado.id)

        wf.iniciar() # iniciamos el proceso

        # Validamos que no se inicie el proceso nuevamente
        with self.assertRaisesRegexp(NameError, 'Error de operacion. Ya se ha iniciado el proceso para el Pst indicado'):
            wf.iniciar()

        parametros_cambios = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            observaciones= "este es un comentario de prueba numero dos",
            cargar="*"
        )

        wf = Workflow(**parametros_cambios)

        # Comprobamos que se haya actualizado el proceso

        proceso_pst_actualizado = wf.actualizar(estado.id)

        self.assertIsNotNone(proceso_pst_actualizado)

        # Validamos que el estado nuevo sea diferente al anterior
        with self.assertRaisesRegexp(NameError, 'Error de operacion. Ya se encuentra en el estado indicado'):
            wf.actualizar(estado.id)

        # Creamos un nueva instancia de Workflow
        data = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            cargar="*"
        )
        wf = Workflow(**data)

        # Validamos si se actualizo el proceso
        self.assertEqual(wf.nombre_estado, estado.nombre)

        # obtenemos el estado inicial para el proceso
        estado_inicial = Flujo.objects.get(proceso=self.proceso, inicio=True)

        # Validamos que el flujo secuencia sea el correcto
        self.assertEqual(wf.procesoPst.estado, estado)

        # Validamos que el historial se creo correctamente
        self.assertEqual(len(wf.historial), 2)

        # Validamos que no sea None el historial
        historial = wf.historial[0]
        self.assertIsNotNone(historial)

        # Comprobamos que el historial sea una instancia de HistorialSecuencia
        self.assertIsInstance(historial, HistorialSecuencia)

        # Validamos que el primer registro sea de la secuencia inicial
        self.assertEqual(historial.estado, estado_inicial)

        # Validamos que sean las mismas observaciones
        self.assertEqual(historial.observaciones, parametros_iniciales.observaciones)

        # Comprobamos que el proceso sea el mismo
        self.assertEqual(historial.proceso, self.proceso)

        # Validamos que el proceso sea creado anteriormente
        proceso_pst = ProcesoPst.objects.get(proceso=self.proceso, activo=True, pst=self.pst)
        self.assertEqual(historial.proceso_pst, proceso_pst)

        # Validamos que no sea None el historial
        historial = wf.historial[1]
        self.assertIsNotNone(historial)

        # Validamos que el segundo historial sea de la secuencia actualizada
        self.assertEqual(historial.estado, estado)

        # Comprobamos que el proceso sea el mismo
        self.assertEqual(historial.proceso, self.proceso)

        # Comprobamos que el historial sea una instancia de HistorialSecuencia
        self.assertIsInstance(historial, HistorialSecuencia)

        # Validamos si el proceso sea igual al indicado
        self.assertEqual(wf.procesoPst.estado.proceso, self.proceso)
        self.assertEqual(wf.proceso, self.proceso)

        # Verificamos que se hayan guardados las observaciones
        self.assertEqual(historial.observaciones, parametros_cambios.observaciones)

        # Obtenemos un proceso finalizacion
        estado_final = Flujo.objects.get(proceso=self.proceso, fin=True)

        # Creamos una instancia nueva de Workflow
        parametros = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            observaciones= "Finalizamos el proceso con este comentario"
        )

        wf = Workflow(**parametros)

        # Actualizamos el registro al estado final
        wf.actualizar(estado_final.id)

        # Verificamos que el procesoPst sea Falso
        self.assertFalse(wf.procesoPst.activo)

        # Creamos una instancia nueva de Workflow
        parametros = Storage(
            pst=self.pst,
            nombre_proceso=self.proceso.nombre,
            cargar="*"
        )
        wf = Workflow(**parametros)

        # Ya no se puede obtener una instancia del proceso por que esta finalizado
        self.assertIsNone(wf.procesoPst)


        proceso_pst = ProcesoPst.objects.get(pst=self.pst, proceso=self.proceso)

        self.assertIsNotNone(proceso_pst)
        self.assertEqual(proceso_pst.estado, estado_final)
        self.assertEqual(proceso_pst.nombre_estado, estado_final.nombre)
        self.assertFalse(proceso_pst.activo)
        self.assertIsNotNone(proceso_pst.fecha_fin)

