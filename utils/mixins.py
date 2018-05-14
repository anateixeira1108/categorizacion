# Create your views here.
# -*- coding: utf-8 -*-

import json

from apps.configuracion import models as cfg_models
from collections import OrderedDict
from datetime import date
from django import http
from django.template.loader import render_to_string
from django.core.mail import send_mail

from utils.gluon.storage import Storage

class JSONResponseMixin(object):
    """
        Vista utilizada para realizar peticiones AJAX.
    """

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class SendEmailMixin(object):
    def send_email(self, data):
        if not isinstance(data, Storage):
            raise NameError(
                u'Error de Tipo. Los parametros enviados no son correctos'
            )
        context = {
            u'user': (
                data.user.razon_social
                or u'{} {}'.format(data.user.nombres, data.user.apellidos)
            ),
            u'tipo_certificacion': data.tipo_certificacion,
            u'estado': data.estado,
            u'observaciones': data.observaciones,
            u'horarios_atencion': get_horarios_atencion(),
        }
        asunto = render_to_string(
            u'notificaciones_correo_electronico/asunto_certificacion.txt',
            context
        )

        asunto = ''.join(asunto.splitlines())

        mensaje = render_to_string(
            'notificaciones_correo_electronico/mensaje_body_certificacion.txt',
            context
        )
        send_mail(
            asunto,
            mensaje,
            u'mintur@mintur.gob.ve',
            [data.user.correo_electronico, ],
            fail_silently=False
        )


def get_horarios_atencion():
    queryset = cfg_models.HorariosAtencion.objects.filter(
        horario__valido_desde__lt=date.today(),
        horario__valido_hasta__gt=date.today(),
    ).order_by('desde', 'dia')

    horarios_atencion = OrderedDict()

    for dia in cfg_models.Dias.objects.all():
        subqueryset = queryset.filter(dia=dia)

        if subqueryset.count() != 0:
            horarios_atencion[dia.nombre] = subqueryset

    return horarios_atencion
