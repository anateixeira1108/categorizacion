# -*- coding: utf-8 -*-

import random

from django.test import TestCase

from utils.factory import FactoryCodigoActas
from utils.gluon.storage import Storage
from apps.actas.models import TipoActa
from apps.verificacion.models import Verificacion
from apps.fiscalizacion.models import Fiscalizacion


class FactoryCodigoActaTestCase(TestCase):
    fixtures = [
        'fixtures/002_registro_pst_inicial.json',
        'fixtures/012_tipos_actas.json',
        'fixtures/013_verificaciones.json',
        'fixtures/015_providencias_actas.json',
        'fixtures/019_fiscalizaciones.json'
    ]

    def setUp(self):
        # acta de Informe fiscal => se supone que cada verificacion ya cuenta con un acta de providencia registrada
        objeto_tipo_acta = TipoActa.objects.get(nombre='Informe fiscal')
        # cuenta la cantidad de fiscalizaciones y verificaciones registradas
        count_verificacion, count_fiscalizacion = Verificacion.objects.count(), Fiscalizacion.objects.count()
        # crea un numero aleatorio de verificacion en caso de existir registros en el modelo
        random_id_verificacion = random.randint(1, count_verificacion) if count_verificacion > 0 else 1
        # crea un numero aleatorio de fiscalizacion en caso de existir registros en el modelo
        random_id_fiscalizacion = random.randint(1, count_fiscalizacion) if count_fiscalizacion > 0 else 1

        # objeto verificacion que se carga al momento de seleccionar una verificacion de la lista mostrada en el template
        objeto_verificacion = Verificacion.objects.get(pk=random_id_verificacion)
        # objeto fiscalizacion que se carga al momento de seleccionar una fiscalizacion de la lista mostrada en el template
        objeto_fiscalizacion = Fiscalizacion.objects.get(pk=random_id_fiscalizacion)

        data_verificacion = Storage(
            tipo_procedimiento=FactoryCodigoActas.TIPO_VERIFICACION,
            objeto_tipo_acta=objeto_tipo_acta,
            objeto=objeto_verificacion
        )

        data_fiscalizacion = Storage(
            tipo_procedimiento=FactoryCodigoActas.TIPO_FISCALIZACION,
            objeto_tipo_acta=objeto_tipo_acta,
            objeto=objeto_fiscalizacion
        )

        self.factory_verificacion = FactoryCodigoActas(data_verificacion)
        self.factory_fiscalizacion = FactoryCodigoActas(data_fiscalizacion)

    # ##
    # ##    TEST UNITARIOS PARA VERIFICACION
    # ##

    def test_get_consecutivo_anyo_verificacion(self):
        anyo = self.factory_verificacion.get_consecutivo_anyo()
        self.assertEqual(anyo, '14')

    def test_get_object_acta_tipo_providencia_verificacion(self):
        acta_tipo_providencia = self.factory_verificacion.get_object_acta_tipo_providencia()
        self.assertEqual(acta_tipo_providencia.nombre, 'Providencia')

    def test_get_codigo_documento_verificacion(self):
        codigo = self.factory_verificacion.get_codigo_documento()
        self.assertEqual(codigo, 'IF')

    def test_get_tipo_procedimiento_verificacion(self):
        tipo = self.factory_verificacion.get_tipo_procedimiento()
        self.assertEqual(tipo, 'VDFP')

    def test_get_consecutivo_dentro_providencia_verificacion(self):
        consecutivo = self.factory_verificacion.get_consecutivo_dentro_providencia()
        self.assertEqual(consecutivo, 1)

    def test_get_object_providencia_verificacion(self):
        objeto_providencia = self.factory_verificacion.get_object_providencia()
        self.assertNotEqual(objeto_providencia, None)

    def test_make_codigo_verificacion(self):
        codigo = self.factory_verificacion.make_codigo()
        id_verificacion = str(self.factory_verificacion.get_object_providencia().id).zfill(5)
        self.assertEqual(codigo, 'INATUR/DE/GRF/VDFP/IF14' + id_verificacion.zfill(6) + '0001')

    def test_is_in_tipos_procedimientos_verificacion(self):
        is_in = self.factory_verificacion.is_in_tipos_procedimientos(FactoryCodigoActas.TIPO_VERIFICACION)
        self.assertEqual(is_in, True)

    # ##
    # ##    TEST UNITARIOS PARA FISCALIZACION
    # ##

    def test_get_consecutivo_anyo_fiscalizacion(self):
        anyo = self.factory_fiscalizacion.get_consecutivo_anyo()
        self.assertEqual(anyo, '14')

    def test_get_object_acta_tipo_providencia_fiscalizacion(self):
        acta_tipo_providencia = self.factory_fiscalizacion.get_object_acta_tipo_providencia()
        self.assertEqual(acta_tipo_providencia.nombre, 'Providencia')

    def test_get_codigo_documento_fiscalizacion(self):
        codigo = self.factory_fiscalizacion.get_codigo_documento()
        self.assertEqual(codigo, 'IF')

    def test_get_tipo_procedimiento_fiscalizacion(self):
        tipo = self.factory_fiscalizacion.get_tipo_procedimiento()
        self.assertEqual(tipo, 'FSC')

    def test_get_consecutivo_dentro_providencia_fiscalizacion(self):
        consecutivo = self.factory_fiscalizacion.get_consecutivo_dentro_providencia()
        self.assertEqual(consecutivo, 1)

    def test_get_object_providencia_fiscalizacion(self):
        objeto_providencia = self.factory_fiscalizacion.get_object_providencia()
        self.assertNotEqual(objeto_providencia, None)

    def test_make_codigo_fiscalizacion(self):
        codigo = self.factory_fiscalizacion.make_codigo()
        id_fiscalizacion = str(self.factory_fiscalizacion.get_object_providencia().id).zfill(5)
        self.assertEqual(codigo, 'INATUR/DE/GRF/FSC/IF14' + id_fiscalizacion.zfill(6) + '0001')

    def test_is_in_tipos_procedimientos_fiscalizacion(self):
        is_in = self.factory_verificacion.is_in_tipos_procedimientos(FactoryCodigoActas.TIPO_FISCALIZACION)
        self.assertEqual(is_in, True)
