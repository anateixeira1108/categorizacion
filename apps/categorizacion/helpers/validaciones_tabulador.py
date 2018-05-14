# -*- encoding: utf-8 -*-

from django.core.exceptions import ValidationError

# Evitar que se agreguen versiones negativas o 0
def validate_non_cero(value):
	if value <= 0:
		raise ValidationError('Este campo debe ser mayor a 0')

def validar_ciclos_subsecciones(sbsc_all, sbsc):
	try:
		l = []
		for e in sbsc_all:			
			f = False
			m = e
			while m is not None:
				if m.subseccion_config_padre == sbsc:
					break
				else:
					m = m.subseccion_config_padre
				if m is None:
					f = True
			if f:
				l.append(e)
		return l
	except Exception, e:
		raise e

	
