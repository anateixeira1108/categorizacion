# -*- encoding: utf-8 -*-

from apps.categorizacion.helpers.debug_printer import dprint
from apps.categorizacion.models import *
from django.http import Http404
from django.shortcuts import *

def del_tabulador_session(view):
	"""
		Elimina el elemento -tabulador- de la session
	"""
	def wrapper(s ,request, *args, **kwargs):		
		
		if request.session.has_key('tabulador'):            
		    request.session.__delitem__('tabulador')
		
		return view(s, request, *args, **kwargs)
	
	return wrapper

def admin_only(view):
	"""
		Limita el acceso a funcionalidades del administrador
	"""
	def wrapper(s ,request, *args, **kwargs):		
		try:
			f = Funcionario.objects.get(user = request.user.pk)			
			if f.tiporol.nombre != 'administrador':
				HttpResponseRedirect(
					reverse('bandeja')
				)		
		except Exception, e:
			raise Http404
		
		return view(s, request, *args, **kwargs)
	return wrapper