#-*- encoding: utf-8 -*-

from __future__ import unicode_literals
from apps.categorizacion.models import *
from apps.categorizacion.helpers.obtener_tipo_pst import *
from apps.categorizacion.helpers.validar_flujo import *

"""
	TODO: Completar esta seccion para culminar computo del tabulador
"""
def evaluar_respuesta(subseccion = None, id_valor_respuesta = None):
	try:
		ts = subseccion.subseccion_config.respuesta_config.tipo_respuesta.nombre.lower().replace(" ", "-")
		af = subseccion.subseccion_config.seccion_config.aspecto_config
		n = SubseccionConfig.objects.filter(seccion_config__aspecto_config = af).count()
		af = af.peso_porcentual

		if ts in ["escala", "dual"]:
			"""
				Se debe realizar la evaluacion de acuerdo al puntaje asociado
				a la respuesta
			"""
			res = ValorRespuestaConfig.objects.get(
					id = id_valor_respuesta
				)
			points = 0
			if ts == 'escala' :				
				if res.nombre.lower() == "bueno" :
					points = af/n
				elif res.nombre.lower() == "deficiente" :
					points = af/2*n
				elif res.nombre.lower() == "malo" :
					points =0
			elif ts == 'dual':
				if res.nombre.lower() == "si" :
					points = af/2*n
				elif res.nombre.lower() == "no" :
					points = 0			
			return points

		elif ts in ["rango", "valor-medida"]:
			"""
				Se debe realizar la evaluacion de acuerdo al rango en el cual
				se encuentre las respuesta
			"""
			valor_respuesta = ValorRespuestaConfig.objects.get(
				id = id_valor_respuesta
			)
			if ts == "rango":

				valor_ingresado = ValorRespuesta.objects.get(
					subseccion = subseccion
				)
				
				li = valor_respuesta.limite_inferior
				ls = valor_respuesta.limite_superior

				if valor_ingresado.valor >= li and valor_ingresado.valor <= ls:					
					return af/n
				else:
					return 0
			else:
				valor_ingresado = ValorRespuesta.objects.get(
					subseccion = subseccion
				)
				"""
					Se debe realizar la comparacion con el valor esperado para
					obtener los puntos configurados en esta respuesta
				"""
				"""
					TODO Agregar valores de respuesta esperados para la Tabla Valor respuesta
				"""
				return af/n if valor_ingresado.valor > 0 else 0
		else:
			raise Exception(u"Tipo de respuesta invalido, configuración de sistema erronea")
	except Exception, e:
		raise e


def evaluar_categoria(acumulador = 0, pst = None, sucursal = None):
	"""
		De acuerdo con los valores dados en la evaluacion se realizan
		en esta funcion las validaciones de rango para colocar la categoria
	"""
	try:
		l = Categoria.objects.filter(
			tipo_pst = otp_prestador(pst, sucursal)
			).order_by("tope_porcentual")
		rangos = zip(l,l[1:])
		cached_ls = None
		for li, ls in rangos:
			if acumulador >= li.tope_porcentual and acumulador < ls.tope_porcentual:
				return li
			elif acumulador < li.tope_porcentual:
				return -1
			elif acumulador >= ls.tope_porcentual:
				cached_ls = ls
				continue		
		return cached_ls
	except Exception, e:
		raise e

def dt_cumpliento_tipo(c = None, s = None, tipo = None):
	"""
		Valida si cumple criterio de aprobacion por tipo de subseccion
	"""
	try:
		#relacion=RespuestaValorRespuesta.objects.filter(pregunta_config=s.subseccion_config.respuesta_config)
		valor=ValorRespuesta.objects.get(subseccion=s)
		try:
			#relevancia=Relevancia.objects.get(categoria=c, subseccion_config=s.subseccion_config)
			#if not s.subseccion_config.subseccion_config_padre or s.subseccion_config.subseccion_config_padre.respuesta_config.tipo_respuesta.codigo == "REP":
			if s.subseccion_config.respuesta_config.tipo_respuesta.codigo == 'D':
				if valor.valor_respuesta.nombre.lower() == 'si':
					return True

				else:
					return False
			elif s.subseccion_config.respuesta_config.tipo_respuesta.codigo == 'E':
				relacion=RespuestaValorRespuesta.objects.filter(pregunta_config=s.subseccion_config.respuesta_config)
				if valor.valor_respuesta.nombre.lower() == 'excelente' or relacion.first().valor_minimo_aceptacion:
					return True

				else:
					return False
			elif s.subseccion_config.respuesta_config.tipo_respuesta.codigo == 'R':
				relacion_rango=RespuestaValorRespuesta.objects.filter(pregunta_config=s.subseccion_config.respuesta_config, respuesta_config__categoria=c)
				limite_inferior=relacion_rango.first().respuesta_config.limite_inferior if relacion_rango.first().respuesta_config.limite_inferior else valor
				limite_superior=relacion_rango.first().respuesta_config.limite_superior if relacion_rango.first().respuesta_config.limite_superior else valor
				if limite_inferior <= valor.valor <= limite_superior:
					return True

				else:
					return False
			elif s.subseccion_config.respuesta_config.tipo_respuesta.codigo == 'F':
				relevancia=Relevancia.objects.get(categoria=c, subseccion_config=s.subseccion_config)
				valores=ValorIndicador.objects.filter(respuesta_config=s.subseccion_config.respuesta_config).order_by('orden')
				formula = ""
				for va in valores:
					v=ValorIndicador.objects.get(indicador=va.indicador, respuesta_config__tipo_respuesta__codigo= 'VE')
					if v.suministrado == True:
						formula = formula + "45"
					else:
						formula = formula + str(ValorCategoria.objects.get(categoria=c, indicador=va.indicador).valor)

					if va.operador_derecho:
						if va.operador_derecho.representacion == "&#43;":
							formula = formula + "+" 
						elif va.operador_derecho.representacion == "&#45;":
							formula = formula + "-" 
						elif va.operador_derecho.representacion == "&#42;":
							formula = formula + "*" 
						elif va.operador_derecho.representacion == "&#47;":
							formula = formula + "/" 
						elif va.operador_derecho.representacion == "&#37;":
							formula = formula + "%" 
				formula=eval(formula)
				resultado=valor.valor
				if relevancia.operador_logico.representacion == "&ge;":
					if resultado >= formula:
						return True

					else:
						return False

				elif relevancia.operador_logico.representacion == "&le;":
					if resultado <= formula:
						return True

					else:
						return False
				elif relevancia.operador_logico.representacion == "&gt;":
					if resultado > formula:
						return True

					else:
						return False
				elif relevancia.operador_logico.representacion == "&lt;":
					if resultado < formula:
						return True

					else:
						return False
					
			elif s.subseccion_config.respuesta_config.tipo_respuesta.codigo == 'C':
				print "Condicional"

				a1=Subseccion.objects.filter(
					tipo_subseccion__abreviacion = tipo,
					respuesta_tabulador__solicitud = solicitud,
					subseccion_config__subseccion_config_padre =  s.subseccion_config,
					subseccion_config__condicion_posneg=True
				)
				x=True if a1 else False


				a2=Subseccion.objects.filter(
					tipo_subseccion__abreviacion = tipo,
					respuesta_tabulador__solicitud = solicitud,
					subseccion_config__subseccion_config_padre =  s.subseccion_config,
					subseccion_config__condicion_posneg=False
				)
				y=True if a2 else False
				for s1 in a1:
					x= x and dt_cumpliento_tipo(c, s1, tipo)

				for s2 in a1:
					y = y and dt_cumpliento_tipo(c, s2, tipo)

				if x or y:
					return True
				else:
					return False
			else:
				print s.id, s.subseccion_config.respuesta_config.tipo_respuesta.codigo, "Este tipo de subseccion es desconocido"
				return False

		except Exception, e:
			print "Error", e
			return False
	except Exception, e:
		print "Error", e
		return False

def dt_cumplimiento_total(tipo = "RB", af=None, mantenimiento=False, solicitud=None, c=None):
	"""
		Determina total de cumplimiento por categoria
	"""
	sub=Subseccion.objects.filter(
		Q(tipo_subseccion__abreviacion = tipo),
	 	Q(respuesta_tabulador__solicitud = solicitud),
		Q(subseccion_config__respuesta_config__tipo_respuesta__codigo__in=["E", "D", "R", "F"]),
		Q(subseccion_config__subseccion_config_padre__isnull = True) |
		Q(subseccion_config__subseccion_config_padre__respuesta_config__tipo_respuesta__codigo = "REP")
	)
	if af:
		sub=sub.filter(
			subseccion_config__seccion_config__aspecto_config=af
		)
	elif mantenimiento:
		sub=sub.filter(
			subseccion_config__seccion_config__aspecto_config__tipo_aspecto__abreviacion="M"
		)
	padres = SubseccionConfig.objects.filter(
	 	tipo_subseccion__abreviacion = tipo,
	 	seccion_config__aspecto_config__tabulador= solicitud.tabulador,
	 	respuesta_config__tipo_respuesta__codigo = "C",
	 	subseccion_config_padre__isnull = True
	)


	cumple=0
	nocumple=[]
	total=0

	for p in padres:
		a1=Subseccion.objects.filter(
			tipo_subseccion__abreviacion = tipo,
			respuesta_tabulador__solicitud = solicitud,
			subseccion_config__subseccion_config_padre = p,
			subseccion_config__condicion_posneg=True
		)


		a2=Subseccion.objects.filter(
			tipo_subseccion__abreviacion = tipo,
			respuesta_tabulador__solicitud = solicitud,
			subseccion_config__subseccion_config_padre = p,
			subseccion_config__condicion_posneg=False
		)

		#for c in categorias:
		relevancia=Relevancia.objects.filter(categoria=c, subseccion_config=p).first()
		if relevancia:
			x=True if a1 else False
			for s in a1:
				x= x and dt_cumpliento_tipo(c, s, tipo)
			y=True if a2 else False
			for s in a2:
				y= y and dt_cumpliento_tipo(c, s, tipo)

			if y or x:
				cumple = cumple + 1
			else:
				nocumple.append((p.nombre))
			total = total + 1
	for s in sub:
		#for c in categorias:
		relevancia=Relevancia.objects.filter(categoria=c, subseccion_config=s.subseccion_config).first()
		if relevancia:
			if dt_cumpliento_tipo(c, s, tipo) == True:
				cumple = cumple + 1
			else:
				nocumple.append((s.subseccion_config.nombre))
			total = total + 1
	return total, cumple, nocumple

def dt_categoria(solicitud=None):
	#if validate_requisitos_principales(solicitud, 'RB') and validate_requisitos_principales(solicitud, 'RM'):
	categoria=None
	if validate_requisitos_principales(solicitud, 'RB'):
		for c in Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor'):
			x=dt_cumplimiento_total("RB", None, False, solicitud, c)
			if x[0] == x[1]:
			#y=dt_cumplimiento_total("RM", None, False, solicitud, c)
			#if x[0] == x[1] and y[0] == y[1]:
				if validate_requisitos_principales(solicitud, 'RE'):
					porcentaje_cumplimiento=0
					for af in AspectoFundamentalConfig.objects.filter(tabulador=solicitud.tabulador, tipo_aspecto__abreviacion = 'E'):
						x=dt_cumplimiento_total("RE", af, False, solicitud, c)
						print af.nombre, x[0], x[1], x[2]
						if x[0] == 0:
							porcentaje_cumplimiento = porcentaje_cumplimiento + af.peso_porcentual
						else:
							porcentaje_cumplimiento= porcentaje_cumplimiento + x[1]*af.peso_porcentual/x[0]
						print porcentaje_cumplimiento, c.valor
					#porcentaje_cumplimiento se le debe sumar o restar Gestion ambiental
					if porcentaje_cumplimiento == 100:
						categoria=c
	return categoria 

def dt_tablas_it(solicitud=None):
	categorias={}
	cuadro_incumplimiento={}
	cuadro_incumplimiento_mya={}
	for c in Categoria.objects.filter(tipo_pst = otp_prestador(solicitud.pst, solicitud.sucursal)).order_by('valor'):
		porcentaje_cumplimiento=0
		for af in AspectoFundamentalConfig.objects.filter(tabulador=solicitud.tabulador, tipo_aspecto__abreviacion = 'E'):
			x=dt_cumplimiento_total("RE", af, False, solicitud, c)
			#print af.nombre, x[0], x[1], x[2]
			if x[0] == 0:
				porcentaje_cumplimiento = porcentaje_cumplimiento + af.peso_porcentual
			else:
				porcentaje_cumplimiento= porcentaje_cumplimiento + x[1]*af.peso_porcentual/x[0]
			for sub in x[2]:
				if not cuadro_incumplimiento.has_key(sub):
					cuadro_incumplimiento.update({sub:[]})
				cuadro_incumplimiento[sub].append(
					{
						c.id:True
					}
				)
		#for af in AspectoFundamentalConfig.objects.filter(tabulador=solicitud.tabulador, tipo_aspecto__abreviacion = 'M'):
		x=dt_cumplimiento_total("RB", None, True, solicitud, c)
		#print af.nombre, x[0], x[1], x[2]
		for sub in x[2]:
			if not cuadro_incumplimiento_mya.has_key(sub):
				cuadro_incumplimiento_mya.update({sub:[]})
			cuadro_incumplimiento_mya[sub].append(
				{
					c.id:True
				}
			)
			#print porcentaje_cumplimiento, c.valor
		#porcentaje_cumplimiento se le debe sumar o restar Gestion ambiental
		categorias.update({c.id : str(porcentaje_cumplimiento) + "%"})
	return categorias, cuadro_incumplimiento, cuadro_incumplimiento_mya