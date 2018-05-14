# -*- coding: utf-8 -*-

from django.test import TestCase

from utils.gluon.storage import Storage
from apps.actas.models import TipoActa, ActaDocumentos
from apps.actas.views.VerificacionView import VerificacionObject
from apps.verificacion.models import Verificacion


class FactoryCodigoActaTestCase(TestCase):
    fixtures = [
        'fixtures/002_registro_pst_inicial.json',
        'fixtures/012_tipos_actas.json',
        'fixtures/013_verificaciones.json',
        'fixtures/015_providencias_actas.json',
        'fixtures/024_actas_to_test.json'
    ]

    def setUp(self):
        self.post_utils = {
            'codigo_objeto': Verificacion.objects.last().id,
            'tipo_acta': 'Informe fiscal',
        }

        self.post_data = {
            'codigo_objeto': Verificacion.objects.get(pk=3).id,
            'fecha_notificacion_acta': '05/05/2014',
            'codigo_acta': 'INATUR/DE/GRF/VDF/IF140000030002',
            'tipo_acta': 'Informe fiscal',
            'observaciones_acta': 'observaciones de prueba'
        }


    ###
    ###    TEST UNITARIOS PARA VISTA DE VERIFICACION
    ###

    def test_get_utils_codigo(self):
        data = Storage(
            post=self.post_utils,
            is_a_util=True
        )
        verificacion = VerificacionObject(data)
        #se obtiene el codigo
        context = verificacion.get_utils_codigo()
        self.assertEqual(context['success'], True)

    def test_get_utils_data(self):
        #codigo existente en el base de datos
        self.post_utils['codigo_acta'] = u'INATUR/DE/GRF/VDF/IF140000030001'
        data = Storage(
            post=self.post_utils,
            is_a_util=True
        )
        verificacion = VerificacionObject(data)
        #se obtienen los datos
        context = verificacion.get_utils_data()
        self.assertEqual(context['success'], True)

    def test_crear_acta(self):
        data = Storage(
            post=self.post_data,
            is_a_util=False
        )
        verificacion = VerificacionObject(data)
        verificacion.crear_acta()
        #se obtiene la ultima acta registrada
        ultima_verificacion_registrada = ActaDocumentos.objects.last()
        #se comparan los codigos para ver si son iguales
        self.assertEqual(verificacion.get_codigo_acta(), ultima_verificacion_registrada.codigo)


    def test_editar_acta(self):
        datos_a_editar = {
            'codigo_acta': u'INATUR/DE/GRF/VDF/IF140000030001',
            'fecha_notificacion_acta': u'07/09/2014',
            'observaciones_acta': u'Nuevas observaciones de prueba'
        }
        #se cargan los datos a editar a la data
        self.post_data['codigo_acta'] = datos_a_editar['codigo_acta']
        self.post_data['fecha_notificacion_acta'] = datos_a_editar['fecha_notificacion_acta']
        self.post_data['observaciones_acta'] = datos_a_editar['observaciones_acta']
        data = Storage(
            post=self.post_data,
            is_a_util=False
        )
        verificacion = VerificacionObject(data)
        #se edita el acta con los datos especificados
        verificacion.editar_acta()
        #se obtiene el acta editada
        acta_editada = ActaDocumentos.objects.get(codigo=datos_a_editar['codigo_acta'])
        #se cargan los datos editados en un diccionario
        datos_editados = {
            'codigo_acta': acta_editada.codigo,
            'fecha_notificacion_acta': acta_editada.fecha_notificacion.strftime('%d/%m/%Y'),
            'observaciones_acta': acta_editada.observaciones
        }
        #se comparan los diccionarios de datos
        self.assertDictEqual(datos_a_editar, datos_editados)






