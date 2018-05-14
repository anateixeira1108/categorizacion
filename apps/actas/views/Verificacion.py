# -*- coding: utf-8 -*-

from datetime import datetime
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect

from apps.verificacion.models import Verificacion as modelo
from apps.actas.models import ActaDocumentos, TipoActa, Requisito, ActaRequisito, ANULADA, NO_NOTIFICADA, NOTIFICADA
from utils.gluon.storage import Storage
from utils.factory import FactoryCodigoActas


class VerificacionObject(object):
    """
        Clasa utilizada para realizar operaciones responsable de la verificacion de actas
    """

    MENSAJE_NO_TIENE_FECHA = "No ha ingresado una fecha"

    def __init__(self, data):
        if isinstance(data, Storage):
            self.post = data.post
            self.is_a_util = data.is_a_util
            self.validar_datos()
        else:
            raise NameError('Error de Tipo. Los parametros enviados no son correctos')

    def get_codigo_verificacion(self):
        codigo = 'codigo_objeto'
        return self.post[codigo] if codigo in self.post else None

    def get_fecha_notificacion(self):
        fecha = 'fecha_notificacion_acta'
        return self.post[fecha] if fecha in self.post else None

    def get_codigo_acta(self):
        codigo = 'codigo_acta'
        return self.post[codigo] if codigo in self.post else None

    def get_tipo_acta(self):
        tipo = 'tipo_acta'
        return self.post[tipo] if tipo in self.post else None

    def get_observaciones_acta(self):
        observaciones = 'observaciones_acta'
        return self.post[observaciones] if observaciones in self.post else ""

    def get_condicion_acta(self):
        condicion = 'condicion_acta_ch'
        return self.post[condicion] if condicion in self.post else ""

    def get_criterio_acta(self):
        criterio = 'criterio_acta_ch'
        return self.post[criterio] if criterio in self.post else ""

    def get_efecto_acta(self):
        efecto = 'efecto_acta_ch'
        return self.post[efecto] if efecto in self.post else ""

    def get_materia_acta(self):
        efecto = 'materia_acta_ch'
        return self.post[efecto] if efecto in self.post else ""

    def get_evidencia_acta(self):
        evidencia = 'evidencia_acta_ch'
        return self.post[evidencia] if evidencia in self.post else ""

    def get_date_with_correct_format(self):
        if self.get_fecha_notificacion():
            # aplica el formato correcto a la fecha
            # se pasa del formato dd-mm-yyyy al formato yyyy-mm-dd
            return datetime.strptime(
                self.get_fecha_notificacion(),
                "%d/%m/%Y"
            ).strftime(
                "%Y-%m-%d"
            )
        else:
            return None

    def get_object_verificacion(self):
        return modelo.objects.get(pk=self.get_codigo_verificacion())

    def get_object_tipo_acta(self):
        return TipoActa.objects.get(nombre=self.get_tipo_acta())

    def get_object_tipo_acta_cedula_de_hallazgo(self):
        return TipoActa.objects.get(codigo_documento='CH')

    def get_object_tipo_acta_providencia(self):
        return TipoActa.objects.get(nombre='Providencia')

    def get_object_tipo_acta_requerimientos_cerrada(self):
        return TipoActa.objects.get(nombre='Acta de requerimiento cerrada')

    def get_object_providencia(self):
        try:
            # obtiene el acta providencia de esa verificacion que no este anulada
            objeto_providencia = ActaDocumentos.objects.get(
                ~Q(estatus=ANULADA),
                tipo=self.get_object_tipo_acta_providencia(),
                verificacion=self.get_object_verificacion()
            )
        except ObjectDoesNotExist:
            # solo tiene providencia ANULADA, puede ingresar otra providencia
            objeto_providencia = None

        return objeto_providencia

    def es_cerrada(self):
        """
            Funcion que verifica si el tipo de acta es cerrada
        """
        return self.get_object_tipo_acta().nombre.find('cerrada') != -1

    def puede_ingresar_acta_tipo_providencia(self):
        """
            Función encargada de verificar si es una acta de tipo providencia
            y si puede ingresarla
            Siempre llamar a esta funcion antes de crear una nueva acta
        """
        if self.get_object_tipo_acta() == self.get_object_tipo_acta_providencia():
            # si tiene providencia entonces no puede ingresar otra
            if self.get_object_providencia():
                return False
            else:
                return True
        return True

    def redirigir(self):
        """
            Funcion que redirige al usuario, actualiza la pagina
        """
        return redirect('funcionario_detalle_verificacion', pk=self.get_codigo_verificacion())

    def get_requisitos(self):
        """
            Funcion que extrae los requisitos de la peticion y los retorna en un diccionario
        """
        if self.es_cerrada():
            requisitos = OrderedDict()
            for i in range(1, 19):
                name = "requisito" + str(i)
                requisitos[i] = self.post[name] if name in self.post else None
            return requisitos
        else:
            return None

    def objecto_esta_notificado(self, object):
        return True if object.fecha_notificacion else False

    def get_estatus(self):
        # si no tiene datos la fecha de notificacion del objeto self
        if not self.get_fecha_notificacion() or self.get_fecha_notificacion() == self.MENSAJE_NO_TIENE_FECHA:
            estatus = NO_NOTIFICADA
        else:
            # si tiene datos el objeto la fecha de notificacion del self, entonces se pasa el estatus a notificada
            estatus = NOTIFICADA
        return estatus

    def crear_acta(self):
        if not self.puede_ingresar_acta_tipo_providencia():
            return self.redirigir()

        # parametros del constructor de acta de documentos
        data = Storage(
            codigo=self.get_codigo_acta(),
            tipo=self.get_object_tipo_acta(),
            providencia=self.get_object_providencia(),
            estatus=self.get_estatus(),
            pst=self.get_object_verificacion().pst,
            verificacion=self.get_object_verificacion(),
            fiscalizacion=None,
            fecha_notificacion=self.get_date_with_correct_format(),
            observaciones=self.get_observaciones_acta()
        )

        if self.get_object_tipo_acta() == self.get_object_tipo_acta_cedula_de_hallazgo():
            data.hallazgos_criterio = self.get_criterio_acta()
            data.hallazgos_condicion = self.get_condicion_acta()
            data.hallazgos_evidencia = self.get_evidencia_acta()
            data.hallazgos_efecto = self.get_efecto_acta()
            data.hallazgos_materia = self.get_materia_acta()

        acta = ActaDocumentos.create(data)
        acta.save()

        # se verifica si es un acta cerrada
        if self.es_cerrada():
            # se obtienen los requisitos de la peticion POST
            requisitos = self.get_requisitos()
            # se itera sobre los requisitos
            for pk in requisitos:
                # se crea un storage por cada objeto, cargando sus datos especificos
                data_requisito = Storage(
                    acta=acta,
                    requisito=Requisito.objects.get(pk=pk),
                )
                # si el valor NO ES None, entonces fue checkeado el checkbox
                if requisitos[pk] != None:
                    # se setea el valor booleano
                    data_requisito.entrego = True
                else:
                    # no fue checkeado el checkbox
                    # se setea el valor booleano
                    data_requisito.entrego = False

                # se instancia el objeto y se crea
                req = ActaRequisito.create(data_requisito)
                # se guardan los cambios de ese objeto
                req.save()

    def editar_acta(self):
        # se obtiene el acta a modificar
        acta = ActaDocumentos.objects.get(codigo=self.get_codigo_acta())
        # se verifica si tiene observaciones
        if self.get_observaciones_acta():
            # si tiene observaciones se setean al modelo
            acta.observaciones = self.get_observaciones_acta()
            # se carga la fecha de notificacion con el formato correxto

        # si el objeto no esta notificado
        if not self.objecto_esta_notificado(acta):
            # se verifica el nuevo estado
            acta.estatus = self.get_estatus()

        # si ha sido ingresada una fecha de notitifacion valida, entonces no se aplica el formato correcto
        if self.get_fecha_notificacion() != self.MENSAJE_NO_TIENE_FECHA:
            acta.fecha_notificacion = self.get_date_with_correct_format()

        # se verifica si se va a editar una cedula de hallazgo
        if self.get_object_tipo_acta() == self.get_object_tipo_acta_cedula_de_hallazgo():
            if self.get_criterio_acta():
                acta.hallazgos_criterio = self.get_criterio_acta()
            if self.get_condicion_acta():
                acta.hallazgos_condicion = self.get_condicion_acta()
            if self.get_evidencia_acta():
                acta.hallazgos_evidencia = self.get_evidencia_acta()
            if self.get_efecto_acta():
                acta.hallazgos_efecto = self.get_efecto_acta()
            if self.get_materia_acta():
                acta.hallazgos_materia = self.get_materia_acta()
        # se guardan los cambios al objeto
        acta.save()
        # se verifica si es un acta cerrada y si no es de tipo de requerimientos cerrada
        if self.es_cerrada() and self.get_object_tipo_acta() != self.get_object_tipo_acta_requerimientos_cerrada():
            # se obtienen los requisitos de la peticion POST
            requisitos = self.get_requisitos()
            # se itera sobre los requisitos del acta
            for index, object in enumerate(ActaRequisito.objects.filter(acta=acta)):
                # si el valor NO ES None, entonces fue checkeado el checkbox
                if requisitos[index + 1] != None:
                    # se setea el valor booleano
                    object.entrego = True
                else:
                    # no fue checkeado el checkbox
                    # se setea el valor booleano
                    object.entrego = False

                # se guardan los cambios de ese objeto
                object.save()


    def get_utils_codigo(self):
        """
            Función utilizada para ver los datos a editar o mostrar en la vista
        """
        # se realiza una verificacion
        if 'tipo_acta' not in self.post \
                and 'codigo_acta' not in self.post \
                and 'codigo_objeto' not in self.post:
            context = {'success': False}
            return context

        # datos utilizados para generar el codigo de acta
        data = Storage(
            tipo_procedimiento=FactoryCodigoActas.TIPO_VERIFICACION,
            objeto_tipo_acta=self.get_object_tipo_acta(),
            objeto=self.get_object_verificacion()
        )

        # Clase factory utilizada para generar el codigo y otros metodos utiles para verificacion
        factory = FactoryCodigoActas(data)

        # no tiene providencia registrada y desea ingresar una que no sea de tipo providencia
        if self.get_object_providencia() == None \
                and self.get_object_tipo_acta() != self.get_object_tipo_acta_providencia():
            data_json = OrderedDict()
            # se carga el mensaja a mostrar al usuario
            data_json['msn'] = 'No tiene providencia, ingrese una primero'
            # se crea otro diccionario ordenado
            context = OrderedDict()
            # se indica que fallo el proceso
            context['success'] = False
            # se carga la data
            context['data'] = data_json
            return context

        # se genera el codigo
        codigo = factory.make_codigo()
        #
        # Se verifica si el nuevo documento es una providencia
        # porque solo debe haber un documento de providencia
        #
        if not self.puede_ingresar_acta_tipo_providencia():
            # se crea un diccionario ordenado
            data_json = OrderedDict()
            # se carga el mensaja a mostrar al usuario
            data_json['msn'] = 'No puede ingresar otra providencia'
            # se crea otro diccionario ordenado
            context = OrderedDict()
            # se indica que fallo el proceso
            context['success'] = False
            # se carga la data
            context['data'] = data_json
            # se retorna la data
            return context

        # se crea un diccionario ordenado
        data_json = OrderedDict()
        # se carga el nombre del documento
        data_json['tipo_acta'] = self.get_object_tipo_acta().nombre
        data_json['codigo_tipo_acta'] = self.get_object_tipo_acta().codigo_documento
        # se carga el codigo del documento
        data_json['codigo'] = codigo

        # se verifica si es un acta cerrada
        if self.es_cerrada():
            # se cargan los requisitos
            requisitos = [{'id': r.id, 'nombre': r.requisito} for r in Requisito.objects.all()]
            # se indica que tiene requisitos
            data_json['tiene_requisitos'] = True
            # se cargan los requisitos
            data_json['requisitos'] = requisitos

        # se crea otro diccionario ordenado
        context = OrderedDict()
        # se indica que la operacion fue exitosa
        context['success'] = True
        # se cargan la data
        context['data'] = data_json
        # retorna la data
        return context

    def get_utils_data(self):
        """
            Función utilizada para ver los datos a editar o mostrar en la vista
        """
        # se realiza una verificacion
        if 'tipo_acta' not in self.post \
                and 'codigo_acta' not in self.post \
                and 'codigo_objeto' not in self.post:
            context = {'success': False}
            return context

        # se obtiene el objeto que se desea modificar
        acta = ActaDocumentos.objects.get(codigo=self.get_codigo_acta())
        # se crea un diccionario ordenado de datos
        data_json = OrderedDict()
        # se cargan las observaciones en la data
        data_json['observaciones'] = acta.observaciones
        data_json['codigo_tipo_acta'] = acta.tipo.codigo_documento

        if self.get_object_tipo_acta() == self.get_object_tipo_acta_cedula_de_hallazgo():
            data_json['hallazgos_condicion'] = acta.hallazgos_condicion
            data_json['hallazgos_criterio'] = acta.hallazgos_criterio
            data_json['hallazgos_efecto'] = acta.hallazgos_efecto
            data_json['hallazgos_evidencia'] = acta.hallazgos_evidencia
            data_json['hallazgos_materia'] = acta.hallazgos_materia

        # se verifica si tiene fecha el objeto
        if self.objecto_esta_notificado(acta):
            fecha_notificacion_acta = str(acta.fecha_notificacion)
            # aplica el formato correcto a la fecha
            # se pasa del formato yyyy-mm-dd al formato dd-mm-yyyy
            fecha_notificacion_acta = datetime.strptime(fecha_notificacion_acta, "%Y-%m-%d").strftime(
                "%d/%m/%Y")
        else:
            fecha_notificacion_acta = self.MENSAJE_NO_TIENE_FECHA
            # se agrega la fecha a la data
        data_json['fecha_notificacion'] = fecha_notificacion_acta
        # se verifica si es un acta cerrada
        if self.es_cerrada():
            # se recojen los requisitos de esa acta a cargar
            requisitos = [{'id': (index + 1),
                           'nombre': object.requisito.requisito,
                           'activo': object.entrego
                          }
                          for index, object in enumerate(ActaRequisito.objects.filter(acta=acta))]
            # se indica que si tiene requisitos
            data_json['tiene_requisitos'] = True
            # se cargan los requisitos a la data
            data_json['requisitos'] = requisitos

        # se crea otro diccionario ordenado
        context = OrderedDict()
        # se indica que todo salio bien
        context['success'] = True
        # se cargan los datos
        context['data'] = data_json
        # se retorna la data
        return context

    def validar_datos(self):
        # verifica si es solo una utilidad para generar codigo o data
        if self.is_a_util:
            if 'tipo_acta' not in self.post \
                    and 'codigo_acta' not in self.post \
                    and 'codigo_objeto' not in self.post:
                raise NameError(
                    'Error de Tipo. La petición no cuenta con todos los parametros necesarios para realizar las operaciones'
                )
        else:  # sino, entonces es una operacion de creacion o edicion
            if 'fecha_notificacion_acta' not in self.post \
                    and 'codigo_acta' not in self.post \
                    and 'tipo_acta' not in self.post \
                    and 'codigo_objeto' not in self.post:
                raise NameError(
                    'Error de Tipo. La petición no cuenta con todos los parametros necesarios para realizar las operaciones'
                )

