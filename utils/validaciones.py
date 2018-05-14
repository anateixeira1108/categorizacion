# -*- coding: utf-8 -*-
import json
from django.views.generic.base import View
from django.http import HttpResponse
from registro.models import Accionista

class ValidarUnicoRif(View):
    """
    Valida que el rif sea unico
    Method POST
        - rif (str): string con el numero de rif => J-76665554
    """

    def post(self, request, *args, **kwargs):
        response = dict(success=False, message=u'El rif no esta definido', item="rif")
        rif = request.POST['rif']
        if rif != "":
            response['message'] = u'Este RIF ya está en uso, por favor ingrese uno diferente'
            if not Accionista.objects.filter(rif__exact=rif):
                response = dict(success=True, item="rif")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')


class ValidarUnicoDocumento(View):
    """
    Valida que la cedula sea unica
    Method POST
        - cedula (str): string con el numero de cedula => V-76665554
    """
    
    def post(self, request, *args, **kwargs):
        response = dict(success=False, message=u'La cedula no esta definida', item="cedula")
        cedula = request.POST['cedula']
        if cedula != "":
            response['message'] = u'Este cedula ya está en uso, por favor ingrese una diferente'
            if not Accionista.objects.filter(cedula__exact=cedula):
                response = dict(success=True, item="cedula")

        response = json.dumps(response, ensure_ascii=True)
        return HttpResponse(response, content_type='application/json')

