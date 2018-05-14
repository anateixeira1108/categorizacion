#-*- encoding:utf-8 -*-

from django import template
from datetime import date, timedelta
from apps.categorizacion.models import *
from apps.categorizacion.helpers.validar_flujo import *
import re
register = template.Library()

@register.filter
def keyvalue(dict, key):
    try:
        return dict[key]
    except Exception, e:   	
        return ''

@register.filter
def inspeccion(solicitud):    
    return validate_requisitos_principales(solicitud, 'RE')

@register.filter
def convert_to_underscore_case(s=""):
	return re.sub("([a-z])([A-Z])","\g<1>_\g<2>",s).lower().replace(" ","_")

@register.filter
def ranges(valor=0):
	if valor!= None:
		return range(0,valor)
	else:
		return range(0,0)

		
@register.filter
def verificacion_IT(documentos=None, id_s=None):
	if documentos == None:
		return False
	else:
		for d in documentos[id_s]:
		    if d['abreviacion'] == 'IT':
		        return True
		return False
		
@register.filter
def verificacion_R(documentos=None, id_s=None):
	if documentos == None:
		return False
	else:
		for d in documentos[id_s]:
		    if d['abreviacion'] == 'ODM' and d['firmado'] == True:
		        return True
		return False
		
@register.filter
def verificacion_ITR(documentos=None, id_s=None):
	if documentos == None:
		return False
	else:
		for d in documentos[id_s]:
		    if d['abreviacion'] == 'ITR':
		        return True
		return False

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
