# -*- encoding: utf-8 -*-

from django import forms
from django.db import models
from apps.categorizacion.models import *
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType


def GenerarFormulario(app_name = 'categorizacion', model_name = None, excludes = None):
	if model_name != None or app_name != None:
		model = get_model(app_name, model_name)
		type_id = ContentType.objects.get_for_model(model).id		
		ctype = ContentType.objects.get(pk=type_id)
		model_class = ctype.model_class()
		class _ObjectForm(forms.ModelForm):
			def __init__(self, *args, **kwargs):
				super(_ObjectForm, self).__init__(*args, **kwargs)
				for k,v in self.fields.items():
					if v.required == True:
						v.widget.attrs={'required': True}
			class Meta:
				model = model_class
				exclude = model_class.exclude
		return _ObjectForm

def GenerarFormularioInstrumento(tabulador_id=None):	
	if tabulador_id is not None:
		class _FormularioInstrumento(forms.Form):
			af = forms.ModelChoiceField(
				label = 'Aspecto Fundamental',
				queryset=AspectoFundamentalConfig.objects.filter(tabulador__id= tabulador_id)
			)
			sec = forms.ModelChoiceField(
				label = 'Sección',
				queryset=AspectoFundamentalConfig.objects.filter(tabulador__id = tabulador_id)
			)
			subsec = forms.ModelChoiceField(
				label = 'Sección',
				queryset=AspectoFundamentalConfig.objects.filter(tabulador__id = tabulador_id)
			)			
		
		return _FormularioInstrumento
