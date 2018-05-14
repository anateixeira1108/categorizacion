# -*- coding: utf-8 -*-
from utils.decorators import json_response, requires_get
from venezuela.models import Municipio, Parroquia
import json

@json_response
@requires_get
def municipios_json(request, pk):
    """
    Obtiene una lista de los municipios por cada estado seleccionado
    Parametros
    - pk (int) = clave primaria del estado
    Reorna
    -  {'success': Boolean, 'municipios': Diccionario}
    Ejm:
    - Json {
        'success': True, 
        'municipios': 
            {"id": 223, "nombre": "Acevedo"}, 
            {"id": 224, "nombre": "Andres Bello"}, 
            {...}, {...}}
    """

    if pk:
        pk = int(pk)
        municipo = Municipio.objects.filter(estado=pk)
        municipo_list = [{"id": m.id, "nombre": m.municipio} for m in municipo]
        return {'success': True, 'municipios': municipo_list}

    return {'success': False, 'error': "No se pudo obtener la lista de municipios"}

@json_response
@requires_get
def parroquias_json(request, pk):
    """
    Obtiene una lista de las parroquias por cada municipio seleccionado
    Parametros
    - pk (int) = clave primaria del municipio
    Reorna
    -  {'success': Boolean, 'parroquia': Diccionario}
    Ejm:
    - Json {
        'success': True, 
        'parroquia': 
            {"id": 223, "nombre": "Acevedo"}, 
            {"id": 224, "nombre": "Andres Bello"}, 
            {...}, {...}}
    """

    if pk:
        pk = int(pk)
        parroquia = Parroquia.objects.filter(municipio=pk)
        parroquia_list = [{"id": p.id, "nombre": p.parroquia} for p in parroquia]
        return {'success': True, 'parroquias': parroquia_list}

    return {'success': False, 'error': "No se pudo obtener la lista de las parroquias"}
