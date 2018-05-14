# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseNotAllowed
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.db.models.query import QuerySet
import json


def add_http_var(variable_name, required=True):
    """
    funcion decoradora que agrega una variable 'nombre_variable' para 
    GET/POST, si esta variable es marcada como requerida y no se encuentra
    en GET/POST el HttpResponseBadRequest retornara especificamente que la 
    varible no se enuentra.
    """
    def wrap(func):
        def decorator(request, *args, **kwargs):
            http_var = request.REQUEST.get(nombre_variable, None)
            if http_var:
                kwargs[nombre_variable] = http_var
            elif required:
                return HttpResponseBadRequest(
                    'definir la variable GET or POST %s' % nombre_variable)
            else:
                pass
            return func(request, *args, **kwargs)
        return decorator
    return wrap


def json_response(func):
    """
    Funcion decoradora que convierte en JSON el return de un de una vista
    peuede ser llamada por metodo GET o POST 
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            if isinstance(objects, QuerySet):
                data = serializers.serialize("json", objects)
            else:
                data = json.dumps(objects, cls=DjangoJSONEncoder)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "application/javascript")
        except:
            data = json.dumps(str(objects), cls=DjangoJSONEncoder)
        return HttpResponse(data, "application/json")
    return decorator


def requires_post(func):
    """
    Retorna un HTTP 405 cuando el método de la petición no es POST.
    """
    def decorator(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        return HttpResponseNotAllowed(['POST'])
    return decorator

def requires_get(func):
    """
    Retorna un HTTP 405 cuando el método de la petición no es GET.
    """
    def decorator(request, *args, **kwargs):
        if request.method == 'GET':
            return func(request, *args, **kwargs)
        return HttpResponseNotAllowed(['GET'])
    return decorator
