# -*- coding: utf-8 -*-

"""
Utilidades cuyo uso está enfocado en las pruebas (test.py).
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: edinson.padron.urdaneta@gmail.com
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.test import TestCase
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Formularios (Genérico) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class FormTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(FormTestCase, self).__init__(*args, **kwargs)

    def get_empty_data(self):
        return {key: '' for key in self.form_cls.base_fields.iterkeys()}

    def test_submit_empty(self):
        data = self.get_empty_data()
        form = self.form_cls(data=data)

        for field in self.required_fields:
            self.assertTrue(field in form.errors)
        self.assertFalse(form.is_valid())


class DatosBasicosFormTest(FormTestCase):
    def __init__(self, *args, **kwargs):
        super(DatosBasicosFormTest, self).__init__(*args, **kwargs)

    def test_rif_validation(self):
        data = self.get_empty_data()

        data['rif'] = 'j-12345678'
        form = self.form_cls(data=data)
        self.assertTrue('rif' in form.errors)

        data['rif'] = 'J-12345678-'
        form = self.form_cls(data=data)
        self.assertTrue('rif' in form.errors)

        data['rif'] = 'J-12345678-0'
        form = self.form_cls(data=data)
        self.assertFalse('rif' in form.errors)

    def test_cedula_validation(self):
        data = self.get_empty_data()

        data['cedula'] = 'p1234567'
        form = self.form_cls(data=data)
        self.assertTrue('cedula' in form.errors)

        data['cedula'] = '12345678'
        form = self.form_cls(data=data)
        self.assertTrue('cedula' in form.errors)

        data['cedula'] = 'V-12345678'
        form = self.form_cls(data=data)
        self.assertFalse('cedula' in form.errors)

    def test_telefono_fijo_validation(self):
        data = self.get_empty_data()

        data['telefono_fijo'] = '0212818495'
        form = self.form_cls(data=data)
        self.assertTrue('telefono_fijo' in form.errors)

        data['telefono_fijo'] = '0212-818495'
        form = self.form_cls(data=data)
        self.assertTrue('telefono_fijo' in form.errors)

        data['telefono_fijo'] = '02128184958'
        form = self.form_cls(data=data)
        self.assertFalse('telefono_fijo' in form.errors)

    def test_correo_electronico_validation(self):
        data = self.get_empty_data()

        data['correo_electronico'] = 'somerandomwords'
        form = self.form_cls(data=data)
        self.assertTrue('correo_electronico' in form.errors)

        data['correo_electronico'] = 'name.domain.com'
        form = self.form_cls(data=data)
        self.assertTrue('correo_electronico' in form.errors)

        data['correo_electronico'] = 'name@domain.com'
        form = self.form_cls(data=data)
        self.assertFalse('correo_electronico' in form.errors)

        data['correo_electronico'] = 'NAME@DOMAIN.COM'
        form = self.form_cls(data=data)
        self.assertFalse('correo_electronico' in form.errors)


class DireccionFormTest(FormTestCase):
    def __init__(self, *args, **kwargs):
        super(DireccionFormTest, self).__init__(*args, **kwargs)

    def test_codigo_postal_validation(self):
        data = self.get_empty_data()

        data['codigo_postal'] = 'words'
        form = self.form_cls(data=data)
        self.assertTrue('codigo_postal' in form.errors)

        data['codigo_postal'] = '002'
        form = self.form_cls(data=data)
        self.assertTrue('codigo_postal' in form.errors)

        data['codigo_postal'] = '4004'
        form = self.form_cls(data=data)
        self.assertFalse('codigo_postal' in form.errors)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
