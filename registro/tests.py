# -*- coding: utf-8 -*-
from django.test import TestCase
from registro import forms
from registro import models
from django.contrib.auth.models import User
from utils.gluon.storage import Storage

import helpers


# Formularios (Natural) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Paso1NaturalFormTest(helpers.DatosBasicosFormTest):
    def __init__(self, *args, **kwargs):
        super(Paso1NaturalFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.natural.Paso1Form

        self.required_fields = self.form_cls.base_fields.keys()
        self.required_fields.remove('rtn')
        self.required_fields.remove('telefono_celular')


class Paso2NaturalFormTest(helpers.DireccionFormTest):
    def __init__(self, *args, **kwargs):
        super(Paso2NaturalFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.natural.Paso2Form

        self.required_fields = self.form_cls.base_fields.keys()
        self.required_fields.remove('oficina_apartamento')
        self.required_fields.remove('punto_referencia')


class Paso4NaturalAgenteFormTest(helpers.FormTestCase):
    def __init__(self, *args, **kwargs):
        super(Paso4NaturalAgenteFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.natural.Paso4AgenteForm

        self.required_fields = self.form_cls.base_fields.keys()
        self.required_fields.remove('titulo_universitario')


class Paso4NaturalConductorFormTest(helpers.FormTestCase):
    def __init__(self, *args, **kwargs):
        super(Paso4NaturalConductorFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.natural.Paso4ConductorForm

        self.required_fields = self.form_cls.base_fields.keys()
        self.required_fields.remove('idiomas')


class Paso4NaturalGuiaFormTest(helpers.FormTestCase):
    def __init__(self, *args, **kwargs):
        super(Paso4NaturalGuiaFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.natural.Paso4GuiaForm

        self.required_fields = [
            'ciudad_primeros_auxilios',
            'fecha_primeros_auxilios',
            'primeros_auxilios',
        ]

    def test_egresado_instituto_validation(self):
        data = self.get_empty_data()

        data['egresado_instituto'] = 'Instituto'
        form = self.form_cls(data=data)
        self.assertFalse('egresado_instituto' in form.errors)
        self.assertTrue('fecha_curso' in form.errors)
        self.assertTrue('nombre_curso' in form.errors)

        data['egresado_instituto'] = 'Instituto'
        data['nombre_curso'] = 'Curso'
        data['fecha_curso'] = '25/05/2014'
        form = self.form_cls(data=data)
        self.assertFalse('egresado_instituto' in form.errors)
        self.assertFalse('fecha_curso' in form.errors)
        self.assertFalse('nombre_curso' in form.errors)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Formularios (Emprendedor) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Paso1EmprendedorFormTest(helpers.DatosBasicosFormTest):
    def __init__(self, *args, **kwargs):
        super(Paso1EmprendedorFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.emprendedor.Paso1Form

        self.required_fields = self.form_cls.base_fields.keys()
        self.required_fields.remove('telefono_celular')


class Paso2EmprendedorFormTest(helpers.DireccionFormTest):
    def __init__(self, *args, **kwargs):
        super(Paso2EmprendedorFormTest, self).__init__(*args, **kwargs)

        self.form_cls = forms.emprendedor.Paso2Form

        self.required_fields = self.form_cls.base_fields.keys()
        self.required_fields.remove('oficina_apartamento')
        self.required_fields.remove('punto_referencia')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RegistroTest(TestCase):
    """Implementando pruebas unitarias para Registros """

    def setUp(self):
        self.RTN = 8902006000831
        self.PERSONA_NATURAL = 2
        self.PERSONA_JURIDICA = 1
        self.COMPANIA_ANONIMA = 1

    def test_A_Paso1JuridicaForm(self):
        """
        Implementando pruebas para el formulario Paso1JuridicaForm
        1.- ¿El formulario valida cuando se envian todos los datos?
        2.- ¿El formulario valida los campos requeridos?
        3.- ¿El formulario valida cuando se ingresa un rif sin formato requerido?
        4.- ¿El formulario valida cuando se ingresa un pagina web invalida?
        5.- ¿El formulario valida cuando en tipo_juridica, tipo_figura se ingresa un string?
        6.- ¿El formulario valida cuando en tipo_juridica, tipo_figura se ingresa un valor fuera del Choice por defecto?
        """
        print "Aplicando pruebas para el formulario Paso1JuridicaForm"


        datos = {
            "tipo_juridica": self.COMPANIA_ANONIMA,
            "rif": "J-00012651-8",
            "razon_social": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do",
            "pagina_web": "www.localhost.com",
            "denominacion_comercial": "FIGYCLP, C.A.",
            "tipo_figura": self.PERSONA_JURIDICA,
            "rtn": self.RTN
            }

        #1) R = True
        form = forms.Paso1JuridicaForm(data=datos)
        self.assertTrue(form.is_valid())

        #2) R = False
        data = datos.copy()
        data['denominacion_comercial'] = ""
        form = forms.Paso1JuridicaForm(data=data)
        self.assertEqual(form.errors.items()[0][0], 'denominacion_comercial')
        self.assertEqual(form.errors.items()[0][1][0], 'Este campo es requerido.')
        self.assertFalse(form.is_valid())

        data = datos.copy()
        data['rif'] = ""
        form = forms.Paso1JuridicaForm(data=data)
        if self.assertEqual(form.errors.items()[0][0], 'rif'):
            self.assertEqual(form.errors.items()[0][1][0], 'Este campo es requerido.')
        self.assertFalse(form.is_valid())

        data = datos.copy()
        data['razon_social'] = ""
        form = forms.Paso1JuridicaForm(data=data)
        if self.assertEqual(form.errors.items()[0][0], 'razon_social'):
            self.assertEqual(form.errors.items()[0][1][0], 'Este campo es requerido.')
        self.assertFalse(form.is_valid())

        data = datos.copy()
        data['pagina_web'] = ""
        form = forms.Paso1JuridicaForm(data=data)
        if self.assertEqual(form.errors.items()[0][0], 'pagina_web'):
            self.assertEqual(form.errors.items()[0][1][0], 'Este campo es requerido.')
        self.assertFalse(form.is_valid())


        data = datos.copy()
        data['rtn'] = ""
        form = forms.Paso1JuridicaForm(data=data)
        if self.assertEqual(form.errors.items()[0][0], 'rtn'):
            self.assertEqual(form.errors.items()[0][1][0], 'Este campo es requerido.')
        self.assertFalse(form.is_valid())

        #3) R = False
        data = datos.copy()
        data['rif'] = "R-44225526771233--as"
        form = forms.Paso1JuridicaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.items()[0][1][0], 'El formato del Rif. proporcionado no es correcto.')

        #4) R = False
        data = datos.copy()
        data['pagina_web'] = "ESTA NO ES UNA PAGINA WEB"
        form = forms.Paso1JuridicaForm(data=data)
        if self.assertEqual(form.errors.items()[0][0], 'pagina_web'):
            self.assertEqual(form.errors.items()[0][1][0], u'Introduzca una URL valida.')
        self.assertFalse(form.is_valid())

        #5) R = False
        data = datos.copy()
        data['tipo_figura'] = "Lorem ipsum dolor sit amet"
        data['tipo_juridica'] = "Lorem ipsum dolor sit amet"

        with self.assertRaisesRegexp(KeyError, u"invalid_choice"):
            form = forms.Paso1JuridicaForm(data=data)
            self.assertFalse(form.is_valid())

        data = datos.copy()
        data['rtn'] = "Lorem ipsum dolor sit amet"
        form = forms.Paso1JuridicaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.items()[0][1][0], u'Introduzca un número entero')

        #6) R = False
        data = datos.copy()
        data['tipo_figura'] = 9999
        data['tipo_juridica'] = 9999
        with self.assertRaisesRegexp(KeyError, u"invalid_choice"):
            form = forms.Paso1JuridicaForm(data=data)
            self.assertFalse(form.is_valid())

    def test_B_TipoPst_create(self):
        """
        Implementando pruebas unitarias para el metodo create del TipoPst
        ¿Se guarda correctamente los valores ingresados?
        ¿Genera error cuando no se envia los parametros correctamente?
        """
        print "Aplicando pruebas para el metodo create del TipoPst"

        TipoPstObject = models.TipoPst.create('Lorem ipsum dolor sit amet', self.PERSONA_JURIDICA, 'Lorem ipsum dolor sit amet')
        TipoPstObject.save()
        self.assertIsNotNone(TipoPstObject.id)
        self.assertEqual(TipoPstObject.nombre, 'Lorem ipsum dolor sit amet')
        self.assertEqual(TipoPstObject.tipo_persona, self.PERSONA_JURIDICA)
        self.assertEqual(TipoPstObject.descripcion, 'Lorem ipsum dolor sit amet')

        TipoPstObject = models.TipoPst.create('Sed ut perspiciatis unde omnis iste', self.PERSONA_NATURAL, 'Lorem ipsum dolor sit amet')
        TipoPstObject.save()
        self.assertIsNotNone(TipoPstObject.id)
        self.assertEqual(TipoPstObject.nombre, 'Sed ut perspiciatis unde omnis iste')
        self.assertEqual(TipoPstObject.tipo_persona, self.PERSONA_NATURAL)
        self.assertEqual(TipoPstObject.descripcion, 'Lorem ipsum dolor sit amet')

        self.assertEqual(models.TipoPst.objects.count(), 2)

        # 2) R = False
        name = list()
        tipo = int()
        des = dict()

        with self.assertRaisesRegexp(NameError, "Error de Tipo. Los parametros enviados no son correctos"):
            PstObject = models.TipoPst.create(name, tipo, des)


    def test_C_Pst_create(self):
        """
        Implementando pruebas unitarias para el metodo create del PST
        ¿Se guarda correctamente los valores ingresados?
        ¿Genera error cuando no se envia los parametros correctamente?
        """
        print "Aplicando pruebas para el metodo create del PST"

        user = User.objects.create_user('Name Test', 'test@thebeatles.com', 'testpass')
        TipoPstObject = models.TipoPst.create('Sed ut perspiciatis unde omnis iste', self.PERSONA_JURIDICA, 'Lorem ipsum dolor sit amet')
        TipoPstObject.save()
        intTipoPst = 1

        # 1) R = True
        data = Storage(
            user = user,
            tipo_juridica = self.COMPANIA_ANONIMA,
            rif = "J-00012651-8",
            razon_social = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do",
            pagina_web = "www.localhost.com",
            denominacion_comercial = "FIGYCLP, C.A.",
            tipo_figura = self.PERSONA_JURIDICA,
            rtn = self.RTN,
            cedula = "V18478770",
            nombres = "Lorem ipsum dolor Name",
            apellidos = "Lorem ipsum dolor Apellido",
            tipo_pst = intTipoPst,
            telefono_fijo = "0212-1552277",
            telefono_celular = "0412-6628877",
            correo_electronico = "Lorem-ipsum-dolor@gmail.com",
            emprendedor = False,
            archivo_pasaporte = None,
            archivo_cedula = None,
            archivo_rif = None
        )


        PstObject = models.Pst.create(data)
        PstObject.save()
        self.assertIsNotNone(PstObject.id)
        self.assertEqual(PstObject.user, user)
        self.assertEqual(PstObject.tipo_juridica, data.tipo_juridica)
        self.assertEqual(PstObject.rif, data.rif)
        self.assertEqual(PstObject.razon_social, data.razon_social)
        self.assertEqual(PstObject.pagina_web, data.pagina_web)
        self.assertEqual(PstObject.denominacion_comercial, data.denominacion_comercial)
        self.assertEqual(PstObject.tipo_figura, data.tipo_figura)
        self.assertEqual(PstObject.rtn, data.rtn)
        self.assertEqual(PstObject.cedula, data.cedula)
        self.assertEqual(PstObject.nombres, data.nombres)
        self.assertEqual(PstObject.apellidos, data.apellidos)
        self.assertEqual(PstObject.tipo_pst, TipoPstObject)
        self.assertEqual(PstObject.telefono_fijo, data.telefono_fijo)
        self.assertEqual(PstObject.telefono_celular, data.telefono_celular)
        self.assertEqual(PstObject.correo_electronico, data.correo_electronico)
        self.assertEqual(PstObject.emprendedor, data.emprendedor)
        self.assertEqual(PstObject.archivo_pasaporte, data.archivo_pasaporte)
        self.assertEqual(PstObject.archivo_cedula, data.archivo_cedula)
        self.assertEqual(PstObject.archivo_rif, data.archivo_rif)

        # 2) R = False
        data = list()
        with self.assertRaisesRegexp(NameError, "Error de Tipo. Los parametros enviados no son correctos"):
            PstObject = models.Pst.create(data)


    def test_C_Direccion_create(self):
        """
        Implementando pruebas unitarias para el metodo create de la Direccion
        ¿Se guarda correctamente los valores ingresados?
        ¿Genera error cuando no se envia los parametros correctamente?
        """
        print "Aplicando pruebas para el metodo create del objeto Direccion"
        ##Falta implementar prurbas uniaraias

    def test_D_Paso2JuridicaForm(self):
        """
        Implementando pruebas unitarias para el el formulario de la Direccion Paso2JuridicaForm

        """
        print "Aplicando pruebas para el formulario Paso2JuridicaForm"
        ##Falta implementar prurbas uniaraias