# -*- encoding: utf-8 -*-

from apps.categorizacion.helpers import camel_case_converter
from django.db.models import get_app, get_models, get_model
from os import path
from utils import models as custom_models

def get_model_list(model=""):
	try:
		l=[]
		for e in model:
			if e.administrable == True:
				l.append({
					"nombre_mostrar":camel_case_converter.convert_to_space_case(e.show_name), 
					"url": "%s" % e.__name__.lower()
				})
		l.sort()
		return l
	except Exception, e:
		raise e

def get_model_list_nuevo(model=""):
	try:
		l={}
		for e in model:
			if e.administrable == True:
				if e.grupo is not None:
					if not l.has_key(e.grupo):
						l.update({e.grupo:[]})
					l[e.grupo].append({
						e.prioridad:{
						"nombre_mostrar":camel_case_converter.convert_to_space_case(e.show_name), 
						"url": "%s" % e.__name__.lower()
					}})
					l[e.grupo].sort()
		return l
	except Exception, e:
		raise e

def normalize_filename(string="", pass_blank_name=False):
	try:
		from datetime import datetime
		re = ''.join(e if ord(e) < 128 else '' for e in string if e.isalnum() or e == ".")
		if len(re):
			return re
		elif not pass_blank_name:
			return "archivo_%s" % (datetime.now().strftime('%d%m%Y'))
		else:
			return ''
	except Exception, e:
		raise e

def get_instance_model(app="", model=""):
	try:
		m=get_model(app,model)
		return m
	except Exception, e:
		raise e

# FUncion para obtener la ruta dodne se van a guardar los archivos de un PST en específico
def get_pst_file_path(instance, filename):
    return path.join(
    	custom_models.gen_path_str_from_key_str(
    		instance.solicitud.pst.rif
    	),
    	'categorizacion',
    	normalize_filename(filename.lower())
    )

def get_funcionario_file_path(instance, filename):
	return path.join(
		custom_models.gen_path_str_from_key_str(
    		str(instance.fecha_emision)
    	),
    	'adjunto_notificacion',
    	normalize_filename(filename.lower())
    )
#firma digitales, horita sin uso
def get_funcionario_signature_file_path(instance, filename):
	return path.join(
		custom_models.gen_path_str_from_key_str(
    		str(instance.fecha_emision)
    	),
    	'firmado',
    	normalize_filename(filename.lower())
    )

def get_file_path(rif, filename,foldername):
	return path.join(
		custom_models.gen_path_str_from_key_str(
    		rif
    	),
    	foldername,
    	normalize_filename(filename.lower(), pass_blank_name=True)
    )

def get_folio_file_path(instance, filename):
    return path.join(
    	custom_models.gen_path_str_from_key_str(
    		instance.lsr_fisico.identificador
    	),
    	'folio',
    	normalize_filename(filename.lower())
    )

def get_comprobante_file_path(instance, filename):
    return path.join(
    	custom_models.gen_path_str_from_key_str(
    		str(instance.numero_comprobante)
    	),
    	'comprobante',
    	normalize_filename(filename.lower())
    )

def get_archivo_file_path(instance, filename):
    return path.join(
    	custom_models.gen_path_str_from_key_str(
    		str(instance.emisor.id)
    	),
    	'adjunto_notificacion',
    	normalize_filename(filename.lower())
    )
