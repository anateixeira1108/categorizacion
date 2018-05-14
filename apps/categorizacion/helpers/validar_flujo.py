#-*- enconding: utf-8 -*-

from apps.licencias.models import *
from apps.categorizacion.models import *
from django.core.exceptions import ValidationError
from apps.cuentas.models import ROLE_PST, ROLE_FUNCIONARIO

def validate_requisitos_documentales(solicitud=None):
	"""
		Valida si ya se han registrado todos los requisitos
		documentales y si se han respondido todos los requisitos
		funcionales para pasar a la siguiente fase
	"""
	try:
		if isinstance(solicitud, Solicitud):
			a = Subseccion.objects.filter(
					tipo_subseccion__tipopadre__abreviacion = 'RD', 
					respuesta_tabulador__solicitud = solicitud
				).count()
			b = SubseccionConfig.objects.filter(
				tipo_subseccion__tipopadre__abreviacion = 'RD', 
				seccion_config__aspecto_config__tabulador = solicitud.tabulador
			).count()			
			return a == b
		else:
			raise Exception("Parametro solicitud invalido, debe ser un entero positivo")
	except Exception, e:
		raise e

def validate_valores_especificos(solicitud=None):
	"""
		Valida si ya se han registrado todos los requisitos
		documentales y si se han respondido todos los requisitos
		funcionales para pasar a la siguiente fase
	"""
	try:
		if isinstance(solicitud, Solicitud):
			a = Subseccion.objects.filter(
					tipo_subseccion__abreviacion = 'VE', 
					respuesta_tabulador__solicitud = solicitud
				).count()
			b = SubseccionConfig.objects.filter(
				tipo_subseccion__abreviacion = 'VE', 
				seccion_config__aspecto_config__tabulador = solicitud.tabulador
			).count()			
			return a == b
		else:
			raise Exception("Parametro solicitud invalido, debe ser un entero positivo")
	except Exception, e:
		raise e

def validate_requisitos_principales(solicitud = None, tipo = '*'):
	"""
		Valida si ya se han registrado todos los requisitos
		han respondido todos los requisitos funcionales para 
		pasar a la siguiente fase
	"""
	try:
		if isinstance(solicitud, Solicitud):
			"""
				TODO: Validacion de subsecciones incompletas
			"""

			# # Respuestas suministrados por el prestador
			a= Subseccion.objects.filter(
				Q(tipo_subseccion__abreviacion = tipo),
			 	Q(respuesta_tabulador__solicitud = solicitud),
				Q(subseccion_config__respuesta_config__tipo_respuesta__codigo__in=["E", "D", "R", "F"]),
				Q(subseccion_config__subseccion_config_padre__isnull = True) |
				Q(subseccion_config__subseccion_config_padre__respuesta_config__tipo_respuesta__codigo = "REP")
			).count()

			# # Respuestas configuradas por el administrador del tipo
			# # Escala, Dual, Rango, Formula y Repetitiva
			b = SubseccionConfig.objects.filter(
				Q(tipo_subseccion__abreviacion = tipo),
				Q(seccion_config__aspecto_config__tabulador= solicitud.tabulador),
				Q(respuesta_config__tipo_respuesta__codigo__in=["E", "D", "R", "F"]),
				Q(subseccion_config_padre__isnull = True) |
				Q(subseccion_config_padre__respuesta_config__tipo_respuesta__codigo = "REP")
			).count()


			# # Respuestas configuradas como condicional
			padres = SubseccionConfig.objects.filter(
			 	tipo_subseccion__abreviacion = tipo,
			 	seccion_config__aspecto_config__tabulador= solicitud.tabulador,
			 	respuesta_config__tipo_respuesta__codigo = "C"
			)

			x=True
			for p in padres:
				a1=Subseccion.objects.filter(
					tipo_subseccion__abreviacion = tipo,
					respuesta_tabulador__solicitud = solicitud,
					subseccion_config__subseccion_config_padre = p,
					subseccion_config__condicion_posneg=True
				).count()

				b1=SubseccionConfig.objects.filter(
					tipo_subseccion__abreviacion = tipo,
					seccion_config__aspecto_config__tabulador= solicitud.tabulador,					
					subseccion_config_padre = p,
					condicion_posneg=True
				).count()

				a2=Subseccion.objects.filter(
					tipo_subseccion__abreviacion = tipo,
					respuesta_tabulador__solicitud = solicitud,
					subseccion_config__subseccion_config_padre = p,
					subseccion_config__condicion_posneg=False
				).count()

				b2=SubseccionConfig.objects.filter(
					tipo_subseccion__abreviacion = tipo,
					seccion_config__aspecto_config__tabulador= solicitud.tabulador,					
					subseccion_config_padre = p,
					condicion_posneg=False
				).count()


				x = x and (a1==b1 or a2==b2)

			return x and a==b
		else:
			raise Exception("Parametro solicitud invalido, debe ser un objeto del tipo categorizacion.models.Solicitud")
	except Exception, e:
		raise e

'''
def validate_elementos_valor(solicitud):
	"""
		Valida si ya se han registrado todos los requisitos
		han respondido todos los requisitos funcionales para 
		pasar a la siguiente fase
	"""
	try:
		if isinstance(solicitud, Solicitud):
			return ValorRespuesta.objects.filter(
					subseccion__in = Subseccion.objects.filter(
						tipo_subseccion__abreviacion = "RE", 
						respuesta_tabulador__solicitud = solicitud
					).values("id"),
					valor__isnull = False
				).count() == SubseccionConfig.objects.filter(
					tipo_subseccion__abreviacion = "RE",
					seccion_config__aspecto_config__tabulador= solicitud.tabulador
				).count() 
		else:
			raise Exception("Parametro solicitud invalido, debe ser un objeto del tipo categorizacion.models.Solicitud")
	except Exception, e:
		raise e
'''

def edicion_autorizada(user = None, solicitud = None, typeentry = '*'):
	"""
		Valores de retorno
		~~~~~~~~~~~~~~~~~~
		Retorna una tupla con los valores correspondientes
		a (desactivar, valores_asociados) para el proceso de
		generacion del tabulador
	"""
	try:
		if user.role == ROLE_PST:
			if solicitud.estatus.abreviacion.lower() in ['sc','ec'] and solicitud.funcionario == None:
				return (0, 1)
			else:
				return (1, 1)
		elif user.role == ROLE_FUNCIONARIO:
			f = Funcionario.objects.get(user = user)
			rol =f.tiporol.nombre.lower()
			if rol == "administrador":
				return (0, 0)
			elif rol == "inspector" and solicitud.estatus.abreviacion.lower() in ['ei', 'ci']:
				if typeentry == 'RE':
					return (0, 1)
				elif typeentry == 'RB':
					return (0, 1)
			elif rol == "analista" and solicitud.estatus.abreviacion.lower() == 'sai':
				if typeentry == 'RE':
					return (0, 1)
				elif typeentry == 'RB':
					return (1, 1)
			elif rol == 'coordinador_ct' and solicitud.estatus.abreviacion.lower() in  ['vi', 'itg']:
				if typeentry == 'RE':
					return (0, 1)
				elif typeentry == 'RB':
					return (0, 1)
			else:
				return (1, 1)
	except Exception, e:
		Exception("Se han encontrado errores en proceso de validacion de edicion: %s" %(str(e)))
"""
elif rol == 'coordinador_ct' and solicitud.estatus.abreviacion.lower() in  ['vi', 'itg']:
	if typeentry == 'RE':
		return (0, 1)
	elif typeentry == 'RB':
		return (0, 1)
elif rol == 'coordinador_dif' and solicitud.estatus.abreviacion.lower() ==  'ri':
	if typeentry == 'RE':
		return (0, 1)
	elif typeentry == 'RB':
		return (1, 1)
"""

def es_prestador_valido(user=None):
	"""
		Valores de retorno
		~~~~~~~~~~~~~~~~~~
		True: si es un prestador de servicio de alojamiento 
		con licencias, vencidas, vigentes o revocadas

		False: si es un prestador con licencias de alojamiento rechazadas
		o sin ellas.		
	"""
	try:
		if LicenciaAsignada.objects.filter(			
				solicitud_licenciaid__sucursal__pst__user = user,
			    solicitud_licenciaid__tipo_licenciaid__padre__codigo = 'LIC_ALO_T',
			    solicitud_licenciaid__estatus_solicitudid__codigo = 'EST_APROB',
				estatus__in = [1, 2, 3]
			).count():
			return True
		elif LicenciaAsignada.objects.filter(			
				solicitud_licenciaid__sucursal__pst__user = user,
			    solicitud_licenciaid__tipo_licenciaid__padre__codigo = 'LIC_ALO_T',
			    solicitud_licenciaid__estatus_solicitudid__codigo__in =[
			    	'EST_RECHA_ANALIS',
			    	'EST_RECHA_DIRECTOR',
			    	'EST_RECHA_VICE',
			    	'EST_RECHA_MINIST'
				]
			).count():
			return False
		
		return False		
	except Exception, e:
		raise Exception(str(e))

def sucursales_licencia(user = None):
	try:
		s = LicenciaAsignada.objects.filter(
			solicitud_licenciaid__usuario_pst_id = user,
			solicitud_licenciaid__tipo_licenciaid__padre__codigo = 'LIC_ALO_T',
			solicitud_licenciaid__estatus_solicitudid__codigo = 'EST_APROB',
			estatus__in = [1, 2, 3]
		)
		"""
		TODO: Validar si en esta seccion existira
		una sola licencia asociada del mismo padre.
		(LICENCIAS MODULE)
		"""
		return s if len(s) else None
	except Exception, e:
		raise Exception("Errores encontrados al momento de determinar las licencias: %s"%(str(e),))


def dt_licencia(pst = None, sucursal = None):
	try:
		s = LicenciaAsignada.objects.filter(
			solicitud_licenciaid__usuario_pst_id = pst,
			solicitud_licenciaid__sucursal_id = sucursal,
			solicitud_licenciaid__tipo_licenciaid__padre__codigo = 'LIC_ALO_T',
			solicitud_licenciaid__estatus_solicitudid__codigo = 'EST_APROB'
		)
		"""
		TODO: Validar si en esta seccion existira
		una sola licencia asociada del mismo padre.
		(LICENCIAS MODULE)
		"""
		return s.first() if len(s) else None
	except Exception, e:
		raise Exception("Errores encontrados al momento de determinar la licencia: %s"%(str(e),))


def order (a, b):
    return cmp(a['fecha_emision'], b['fecha_emision'])


def validate_fotografias_inspeccion(solicitud):
	"""
		Valida si ya se han registrado todas las fotos
		requeridas en la inspeccion
	"""
	try:
		if isinstance(solicitud, Solicitud):
			return SubseccionArchivoRequisito.objects.filter(
					subseccion__in = Subseccion.objects.filter(
						tipo_subseccion__abreviacion = 'RE', 
						respuesta_tabulador__solicitud = solicitud
					).values("id"),
					requisito_digital__isnull = False
				).count() == SubseccionConfig.objects.filter(
					tipo_subseccion__abreviacion = 'RE',
					seccion_config__aspecto_config__tabulador= solicitud.tabulador,
					subs_imagen=True
				).count() 
		else:
			raise Exception("Parametro solicitud invalido, debe ser un objeto del tipo categorizacion.models.Solicitud")
	except Exception, e:
		raise e





