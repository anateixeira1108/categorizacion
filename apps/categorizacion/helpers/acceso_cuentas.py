# -*- encoding: utf-8 -*-

from apps.categorizacion.models import *

def obtener_template(u=None):
	redirect = None
	if u is not None:
		try:
			f = Funcionario.objects.filter(user = u).first()			
			if f.habilitado == True :
				#USA DIRECCIONFUNCIONARIOTIPOROL
				#r = DireccionFuncionarioTiporol.objects.filter(funcionario = f).first()
				if f.tiporol.nombre == 'administrador':				
					redirect = 'home_panel_administrativo'
				else:
					redirect = 'bandeja'
			else:
				redirect = False

			return redirect
		except Exception, e:
			print "[apps.categorizacion.helper.acceso_cuentas] \
					Se han encontrado errores al momento de validar los roles de usuario"
			return False
