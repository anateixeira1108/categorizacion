#-*- encode: utf-8 -*-
from apps.categorizacion.helpers.debug_printer import dprint
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from utils.forms_helpers import ModelFormBaseClass
from django.db.models.loading import get_model
from apps.categorizacion.models import *
from django.db.models import FileField
from django.db import models
from django import forms
from os import path
import sys


EXTS_CONTENT_TYPE = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'pdf': 'application/pdf',
    'png': 'image/png',
}


def validate_negative(value):
	if value < 0:
		raise ValidationError('Este campo debe ser mayor a 0')

def max_integer(value):
	if value > sys.maxint:
		raise ValidationError('Este valor es demasiado grande')

def max_float(value):
	if value > sys.float_info.max:
		raise ValidationError('Este valor es demasiado grande')


def validator_file(data, rf, content_types, max_upload_size):
	size= rf.size
	content_type= rf.content_type
	dprint("hello")
	fobj = data
	if content_type in content_types:
		if size > max_upload_size:			
			return False
	else:
		return False
	return content_type


def validate_file_type(rf,e, content_types, max_upload_size):
	class ModeloTrap(models.Model):	    
	    archivo_upload = FileField(
	        null = True,
	        blank = True,
	        max_length = 255,
	        upload_to = "/",
	        )

	class Validador(forms.ModelForm):
	    class Meta:
	        model = ModeloTrap

	form = Validador(rf)
	
	if form.is_valid():
		archive = FileField(
			form.fields['archivo_upload'], 
			max_length = 255, upload_to = "/",
		)
		return validator_file(archive,rf[e], content_types, max_upload_size)		
	else:
		return False
