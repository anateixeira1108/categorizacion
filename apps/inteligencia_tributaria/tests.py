# -*- coding: utf-8 -*-

from django.test import TestCase
from .providencia import Providencia
from apps.fiscalizacion.models import Fiscalizacion
from apps.verificacion.models import Verificacion
from apps.actas.models import ActaDocumentos
from registro.models import Pst
from utils.gluon.storage import Storage
import random

class ProvidenciaTest(TestCase):
    """Implementando pruebas unitarias para la clase Providencia """

    fixtures = [
        'fixtures/000_tipo_pst.json',
        'fixtures/001_cuentas_pst.json',
        'fixtures/002_registro_pst_inicial.json',
        'fixtures/012_tipos_actas.json',
        'fixtures/013_verificaciones.json',
    ]

    def setUp(self):
        """
        """
        self.verificacion = Verificacion.objects.all()
        self.fiscalizacion = Fiscalizacion.objects.all()
        
        random_id = random.randint(1, Pst.objects.count())
        self.pst = Pst.objects.get(id=random_id)

    def test_A_crear_providencia_verificacion(self):
        """
        ¿Se genera la providencia correctamente?
        """
        for verificacion in self.verificacion:
            data = Storage(pst=self.pst, verificacion=verificacion)
            providencia = Providencia(**data)
            p = providencia.crear()
            self.assertIsInstance(p, ActaDocumentos)


    def test_B_crear_providencia_fiscalizacion(self):
        """
        ¿Se genera la providencia correctamente?
        """
        for fiscalizacion in self.fiscalizacion:
            data = Storage(pst=self.pst, fiscalizacion=fiscalizacion)
            providencia = Providencia(**data)
            p = providencia.crear()
            self.assertIsInstance(p, ActaDocumentos)

    def test_C_busqueda_avanzada(self):
        """
        ¿Se realizan las busquedaspor estados?
        """
        pass