from apps.categorizacion.models import *

def BuildingTree(
	tree, 
	parent=None, 
	ids=[], 
	condicional=None, 
	tipo_pst=None,
	tiporequisito = None,
	deleted = None
	):

	dprint(tree=tree)
	dprint(condicional = condicional, deleted = deleted)

	if tree['type']=="T":
		try:
			tab_basic = Tabulador.objects.get(id=int(tree['id']))
			for e in tree['children']:
				BuildingTree(e,None,ids,None, tipo_pst, tiporequisito, deleted)				
			return ids
		except Exception, e:
			raise e

	elif tree['type']=="AF":

		asp_new = queries(int(tree['id']), tree['type'])
		peso = None

		if tree['extra'].has_key('percent'):
			peso = float(tree['extra']['percent'])

		if tree['extra'].has_key('tipo_aspecto'):
			tipo = int(tree['extra']['tipo_aspecto'])
		else:
			tipo = TipoAspectoFundamental.objects.get(abreviacion = "E").id

		tab = int(tree['parent']['id'])

		if tree['state'] == 'added':
			if  asp_new == None or asp_new.id == tree['id']:
				try:				
					
					asp_new = AspectoFundamentalConfig(
						nombre=tree['name'],
						peso_porcentual=peso,
						tabulador_id=tab,
						tipo_aspecto_id = tipo
					)
					
					asp_new.save()
					
					ids.append({
						'pid': int(tree['id']),
						'nid': asp_new.id,
						'type': 'AF'
					})						

					tree.update( {'id': asp_new.id} )


				except Exception, e:
					raise e
		elif tree['state'] == 'edited':
			try:
				asp_new = AspectoFundamentalConfig.objects.get(id = int(tree['id']))
				asp_new.nombre=tree['name']
				asp_new.peso_porcentual=peso
				asp_new.tabulador_id=tab
				asp_new.tipo_aspecto_id = tipo
				asp_new.save()
			except AspectoFundamentalConfig.DoesNotExist, e:
				raise Exception("Al aspecto fundamental de id %d no existe" % (int(tree['id']),))

		for e in tree['children']:
			# En caso de eliminacion de un elemento que aun no haya sido agregado 
			# su estado es added o edited pero no existe en base de datos
			e['parent'].update({'id': asp_new.id if asp_new is not None else -1})
			if tree['state'] == 'delete':
				BuildingTree(
					e, 
					asp_new.id if asp_new is not None else -1,
					ids,
					None, 
					tipo_pst, 
					tiporequisito, 
					True
				)
			else:
				BuildingTree(
					e, 
					asp_new.id if asp_new is not None else -1,
					ids,
					None, 
					tipo_pst, 
					tiporequisito, 
					False
				)
		
		if tree['state'] == 'delete' and asp_new is not None:
			asp_new.delete()

	elif tree['type']=="S":
		secc_new = queries(int(tree['id']), tree['type'])
		if tree['state'] == 'added' and deleted == False:
			if  secc_new == None or secc_new.id == tree['id']:
				padre = int( tree['parent']['id'] )
				
				secc_new= SeccionConfig(
					nombre = tree['name'],
					seccion_padre_config_id = padre if tree['parent']['type']=="S" else None,
					aspecto_config_id = padre if tree['parent']['type'] == "AF" else parent,
				)
				secc_new.save()

				ids.append({
					'pid': int(tree['id']),
					'nid': secc_new.id,
					'type': 'S'
				})

				tree.update({'id': secc_new.id})
		elif tree['state'] == 'edited':
			try:
				secc_new = SeccionConfig.objects.get(id = int(tree['id']))
				secc_new.nombre=tree['name']
				secc_new.save()
			except SeccionConfig.DoesNotExist, e:
				raise Exception(u"La Seccion de id %d no existe" % (int(tree['id']),))

		for e in tree['children']:
			e['parent'].update({'id': secc_new.id if secc_new is not None else -1})		
			if e['type'] == "SS":
				if tree['state'] == 'delete' or deleted == True:
					BuildingTree(
						e,
						secc_new.id if secc_new is not None else -1,
						ids,
						None, 
						tipo_pst, 
						tiporequisito, 
						True
					)
				elif deleted == False:
					BuildingTree(
						e,
						secc_new.id if secc_new is not None else -1,
						ids,
						None, 
						tipo_pst, 
						tiporequisito, 
						False
					)
			elif e['type'] == 'S':
				if tree['state'] == 'delete' or deleted == True:
					BuildingTree(
						e,
						parent,
						ids,
						None, 
						tipo_pst, 
						tiporequisito, 
						True
					)
				elif deleted == False:
					BuildingTree(
						e,
						parent,
						ids,
						None, 
						tipo_pst, 
						tiporequisito, 
						False
					)

		if tree['state'] == 'delete'and secc_new is not None:
			secc_new.delete()

	elif tree['type']=="SS":
		sub_new = queries(int(tree['id']), tree['type'])
		dprint(deleted = deleted, sub_new = sub_new)

		if (tree['state'] == 'added' or tree['state'] == 'edited') and deleted == False:
			if sub_new == None or sub_new.id == tree['id']:
				if tree.has_key('content'):
					if tree['extra']['subtype'] == 'R':
						ite=0
						flag_rango = False
						cat =Categoria.objects.filter(tipo_pst_id=tipo_pst).order_by('valor')
						for e in cat:
							if tree['content']['relevance_value'][ite]['inf_aplica'] or tree['content']['relevance_value'][ite]['sup_aplica']:
								if tree['state'] == "edited":
									try:
										res_val = RespuestaValorRespuesta.objects.get(
											pregunta_config= sub_new.respuesta_config, 
											respuesta_config__categoria=e
										)
										ValorRespuestaConfig.objects.filter(id=res_val.respuesta_config.id).update(limite_inferior=int(tree['content']['relevance_value'][ite]['inf_star']) if tree['content']['relevance_value'][ite]['inf_aplica'] else None)
										ValorRespuestaConfig.objects.filter(id=res_val.respuesta_config.id).update(limite_superior=int(tree['content']['relevance_value'][ite]['sup_star']) if tree['content']['relevance_value'][ite]['sup_aplica'] else None)										
									except RespuestaValorRespuesta.DoesNotExist:
										val_res= ValorRespuestaConfig(
											nombre= "Rango de Categoria - "+tree['name'],
											limite_inferior=int(tree['content']['relevance_value'][ite]['inf_star']) if tree['content']['relevance_value'][ite]['inf_aplica'] else None,
											limite_superior=int(tree['content']['relevance_value'][ite]['sup_star']) if tree['content']['relevance_value'][ite]['sup_aplica'] else None,
											categoria=e
										)
										val_res.save()

										res_val = RespuestaValorRespuesta(
											pregunta_config= sub_new.respuesta_config, 
											respuesta_config=val_res
										)
										res_val.save()

									RespuestaConfig.objects.filter(id=sub_new.respuesta_config.id).update(tipo_medida=TipoMedida.objects.get(id=int(tree['content']['unit'])))
									sub_new.nombre = tree['name']
									sub_new.save()

									flag_rango = True
								else:
									if flag_rango == False:

										res_conf = RespuestaConfig(
											nombre="Respuesta Rango - "+tree['name'],
											tipo_respuesta= TipoRespuesta.objects.get(codigo="R"),
											tipo_medida_id= int(tree['content']['unit'])
										)
										res_conf.save()

										flag_rango = True
										
									val_res= ValorRespuestaConfig(
										nombre= "Rango de Categoria - "+tree['name'],
										limite_inferior=int(tree['content']['relevance_value'][ite]['inf_star']) if tree['content']['relevance_value'][ite]['inf_aplica'] else None,
										limite_superior=int(tree['content']['relevance_value'][ite]['sup_star']) if tree['content']['relevance_value'][ite]['sup_aplica'] else None,
										categoria=e
									)
									val_res.save()
									
									res_val = RespuestaValorRespuesta(
										pregunta_config= res_conf, respuesta_config= val_res
									)
									res_val.save()
								ite+=1
							else:
								if tree['state'] == 'edited':
									try:
										res_val = RespuestaValorRespuesta.objects.get(
											pregunta_config= sub_new.respuesta_config, 
											respuesta_config__categoria=e
										)

										res_val.respuesta_config.delete()
										res_val.delete()
									except RespuestaValorRespuesta.DoesNotExist:
										pass

						if flag_rango == True:
							val_res = res_val
					elif tree['extra']['subtype'] == 'E' or tree['extra']['subtype'] == 'D':

						if tree['state'] != 'edited':
							print "Creando valores de respuesta"
							res_conf = RespuestaConfig(
								nombre= ( "Respuesta %s - " % ('Dual' if tree['extra']['subtype'] == 'D' else 'Escala') ) + tree['name'],
								tipo_respuesta= TipoRespuesta.objects.get(codigo= 'D' if tree['extra']['subtype'] == 'D' else 'E'),
							)
							res_conf.save()

							for e in tree['content']['options']:
								val_res = RespuestaValorRespuesta(
									pregunta_config= res_conf, respuesta_config_id = int(e)
								)
								val_res.save()
						else:
							sub_new.nombre = tree['name']
							sub_new.save()

							RespuestaValorRespuesta.objects.filter(
								pregunta_config= sub_new.respuesta_config 
							).delete()

							for e in tree['content']['options']:
								val_res = RespuestaValorRespuesta(
									pregunta_config= sub_new.respuesta_config,
									respuesta_config_id = int(e)
								)
								val_res.save()
					elif tree['extra']['subtype'] == 'F':
						formula_elements = tree['content']['formula-elements']
						val_res = None

						if tree['state']=='added':
							res_conf = RespuestaConfig(
								nombre= "Respuesta Formula - " + tree['name'],
								tipo_respuesta= TipoRespuesta.objects.get(codigo = 'F')
							)
							res_conf.save()
						else:
							sub_new.nombre = tree['name']
							sub_new.save()
							res_conf = sub_new.respuesta_config

						ValorIndicador.objects.filter(respuesta_config = res_conf).delete()

						i = 0
						for e in formula_elements:
							local = e
							if local['type'] == 'operando':
								nexte = formula_elements[i+1] if i < len(formula_elements)-1 else None
								preve = formula_elements[i-1] if i > 0 else None
								
								v = ValorIndicador(
									respuesta_config = res_conf,
									indicador_id = int(local['id']),
									operador_derecho_id = int(nexte['id']) if nexte is not None else None,
									operador_izquierdo_id = int(preve['id']) if preve is not None else None,
									orden = i
								)
								v.save()
							i += 1
					elif tree['extra']['subtype'] == "REP":
						val_res = None
						if sub_new == None and tree['state'] == 'added':
							res_conf = RespuestaConfig(
								nombre="Respuesta Repetitiva -"+tree['name'],
								tipo_respuesta=TipoRespuesta.objects.get(codigo='REP')
							)
							res_conf.save()
						else:
							sub_new.nombre = tree['name']
							sub_new.save()					
					else:
						if len(tree['content']['options'])>0:
							if tree['state'] == 'edited' and sub_new != None:
								sub_new.nombre = tree['name']
								sub_new.save()
								res_conf = sub_new.respuesta_config

								RespuestaValorRespuesta.objects.filter(
									pregunta_config= sub_new.respuesta_config 
								).delete()
							else:		
								res_conf= RespuestaConfig(
									nombre="Respuesta Condicional -"+tree['name'],
									tipo_respuesta=TipoRespuesta.objects.get(codigo='C')
								)
								res_conf.save()

								res_val= ValorRespuestaConfig.objects.filter(
									id__in=[ int(o) for o in tree['content']['options']]
								)

								for e in res_val:
									val_res = RespuestaValorRespuesta(
										pregunta_config=res_conf, respuesta_config=	e							
									)
									val_res.save()
								
				if tree.has_key('extra') and tree['state'] != 'edited':

					padre = int(tree['parent']['id'])

					tiposub = TipoSubseccion.objects.filter(
						abreviacion=tiporequisito
					).first() 

					sub_new= SubseccionConfig(
						nombre=tree['name'],
						tipo_subseccion=tiposub, subs_imagen= False,
						respuesta_config_id = val_res.pregunta_config_id if val_res is not None else res_conf.id,
						subseccion_config_padre_id=padre if tree['parent']['type']=="SS" else None,
						seccion_config_id=padre if tree['parent']['type'] == "S" else parent,
						condicion_posneg=condicional
					)

					sub_new.save()
					ids.append({
						'pid': int(tree['id']),
						'nid': sub_new.id,
						'type': 'SS'
					})
					tree.update({'id': sub_new.id})

				if tree.has_key('content'):
					if tree['extra']['subtype'] == "REP":

						cat =Categoria.objects.filter(
							tipo_pst_id=tipo_pst
						).order_by('valor')
						t=0

						dprint(categorias = cat)

						for e in cat:
							dprint(content_repetition=tree['content']['repetition'][t])
							dprint(categoria = e,type=type(e))

							if tree['content']['repetition'][t] !="": 
								if int(tree['content']['repetition'][t])>=0:
									try:
										rel = Relevancia.objects.get(
											categoria=e,
											subseccion_config=sub_new,
										)
										rel.repeticion = int(tree['content']['repetition'][t])
									except Exception, err:
										rel = Relevancia(
											categoria=e,
											subseccion_config=sub_new,
											repeticion= int(tree['content']['repetition'][t])
										)
									rel.save()
							t+=1
					elif tree['extra']['subtype'] in ["R","D","E"] :
						cat =Categoria.objects.filter(
							tipo_pst_id=tipo_pst
						).order_by('valor')
						ite = 0
						for e in cat:
							if (tree['extra']['subtype'] == "R" and (tree['content']['relevance_value'][ite]['inf_aplica'] or tree['content']['relevance_value'][ite]['sup_aplica'])) or (tree['extra']['subtype'] in ["D","E"] and tree['content']['relevance'][ite]):
								if tree['state'] != 'edited':
									rel = Relevancia(
										categoria=e,
										subseccion_config=sub_new
									)
									rel.save()
								else:
									try:
										rel = Relevancia.objects.get(
											categoria=e,
											subseccion_config=sub_new
										)
									except Relevancia.DoesNotExist:
										rel = Relevancia(
											categoria=e,
											subseccion_config=sub_new
										)
										rel.save()
							else:
								if tree['state'] == 'edited':
									# Eliminar la relevancia en caso de conseguir un caso donde no se necesite
									try:
										rel = Relevancia.objects.get(
											categoria=e,
											subseccion_config=sub_new
										)
										rel.delete();
									except Relevancia.DoesNotExist:
										pass
							ite+=1
					elif tree['extra']['subtype'] == "F":
						# Secciones del tipo formula que posean una relevancia por categoria
						# en este caso la relevancia se encuentra acotada por un valor
						# resultante del calculo de la formula			

						if sub_new != None and tree['state'] == 'edited':
							Relevancia.objects.filter(subseccion_config = sub_new).delete()

						categoria =Categoria.objects.filter(tipo_pst_id=tipo_pst).order_by('valor')
						logical_per_category = tree['content']['logical_per_category']						
						t=0

						for cat, log in zip(categoria, logical_per_category):
							rel = Relevancia(
								categoria = cat,
								subseccion_config = sub_new,
								operador_logico_id = int(log)
							)
							rel.save()
		it = 0		
		for e in tree['children']:
			e['parent'].update({'id': sub_new.id if sub_new is not None else -1})
			if e['type']=="SS":
				if tree['extra']['subtype'] == "C":
					if tree['content']['extra'][0]>it:
						if tree['state'] == 'delete':
							BuildingTree(
								e,
								parent,
								ids,
								True, 
								tipo_pst, 
								tiporequisito, 
								True
							)
						elif deleted == False:
							BuildingTree(
								e,
								parent,
								ids,
								True, 
								tipo_pst, 
								tiporequisito, 
								False
							)
					elif tree['content']['extra'][0]+tree['content']['extra'][1] > it:
						if tree['state'] == 'delete':
							BuildingTree(
								e,
								parent,
								ids,
								False, 
								tipo_pst, 
								tiporequisito, 
								True
							)
						elif deleted == False:
							BuildingTree(
								e,
								parent,
								ids,
								False, 
								tipo_pst, 
								tiporequisito, 
								False
							)
					it+=1
				else:
					if tree['state'] == 'delete' or deleted == True:
						BuildingTree(
							e,
							parent,
							ids,
							None, 
							tipo_pst, 
							tiporequisito, 
							True
						)
					elif deleted == False:
						BuildingTree(
							e,
							parent,
							ids,
							None, 
							tipo_pst, 
							tiporequisito, 
							False
						)

		if tree['state'] == 'delete' or deleted == True:
			if sub_new != None:
				sub_new.respuesta_config.delete()
				sub_new.delete()

def queries(idq,tipo):
	if tipo == "AF":
		try:
			return AspectoFundamentalConfig.objects.get(id=idq)
		except AspectoFundamentalConfig.DoesNotExist:
			return None
	elif tipo == "S":
		try:
			return SeccionConfig.objects.get(id=idq)
		except SeccionConfig.DoesNotExist:
			return None
	elif tipo=="SS":
		try:
			return SubseccionConfig.objects.get(id=idq)
		except SubseccionConfig.DoesNotExist:
			return None
