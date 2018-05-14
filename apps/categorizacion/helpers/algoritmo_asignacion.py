# -*- encoding: utf-8 -*-

import random
from random import choice
from django.db.models import Count
from datetime import datetime as time
from apps.categorizacion.models import *
from apps.categorizacion.helpers.debug_printer import dprint

"""
	Plantamos la semilla para permitir la generacion
	de numero aleatorios
"""
random.seed(time.now())

def algoritmo_de_asignacion(tipo='coordinador_ct',quitar= None):
	coordinadores_sin_asig = Funcionario.objects.exclude(
		id__in=Asignacion.objects.distinct('funcionario__id').values('funcionario__id').filter(asignacion_habilitada=True)
		).filter(tiporol__nombre=tipo, habilitado=True)
	dprint(coordinadores_sin_asig= coordinadores_sin_asig)
	x=list(coordinadores_sin_asig)
	for e in x:
	    if e.id == quitar:
	        x.remove(e)

	if len(x) > 0:
		coordinador_ids = choice(x)
		coordinador_id =coordinador_ids.id
	else:
		if quitar:  
			coord_asignacion = Asignacion.objects.filter(funcionario__tiporol__nombre=tipo, 
				funcionario__habilitado=True, asignacion_habilitada=True
				).values_list('funcionario').annotate(dcount=Count('funcionario')
				).order_by('dcount').exclude(funcionario_id=quitar)
		else:
			coord_asignacion = Asignacion.objects.filter(funcionario__tiporol__nombre=tipo, 
				funcionario__habilitado=True, asignacion_habilitada=True
				).values_list('funcionario').annotate(dcount=Count('funcionario')
				).order_by('dcount')
		if coord_asignacion:
			auxiliar = [e[1] for e in coord_asignacion]
			cantidad = auxiliar.count(auxiliar[0])
			if cantidad > 1:
				coord_fecha = coord_asignacion[:cantidad]
				auxiliar1 = [e[0] for e in coord_fecha]

				coordinador_fecha = Asignacion.objects.filter(funcionario_id__in= auxiliar1, 
					asignacion_habilitada=True
				).values_list('funcionario').order_by('fecha_asignacion').first()

				coordinador_id = coordinador_fecha[0]
			else:
				coordinador_id= coord_asignacion[0][0]
		else:
			return None
	return coordinador_id

def asignacion_analista_inspector(tipo='analista'):
	l = Asignacion.objects.filter(
            funcionario__tiporol__nombre=tipo,
            funcionario__habilitado=True,
            asignacion_habilitada=True
        ).values_list('funcionario').annotate(dcount=Count('funcionario')).order_by('dcount')    
	lista_asignacion2 = [f[0] for f in l]
	no_tiene_asignaciones = Funcionario.objects.filter(
    	tiporol__nombre=tipo,habilitado=True
	).exclude(id__in=lista_asignacion2)
	no_tiene = [c.id for c in no_tiene_asignaciones]
	tipos_list = no_tiene+lista_asignacion2

	clauses = ' '.join(['WHEN id = %s THEN %s' % (pk, i) for i, pk in enumerate(tipos_list)])
	ordering = 'CASE %s END' % clauses

	tipos_nombre = Funcionario.objects.filter(
	    pk__in=tipos_list
	).extra(
    	select={'ordering':ordering},
    	order_by = ('ordering',)
	)       
	tipo_list = [(t.id,t.nombre,t.apellido) for t in tipos_nombre]

	return tipo_list

def array_de_funcionarios(array_funcionarios=None, tipo='analista'):
	array = []
	for e in array_funcionarios:
		if e.funcionario.tiporol.nombre ==tipo:
			func = (e.funcionario.id, e.funcionario.nombre+" "+ e.funcionario.apellido )
			if func not in array:
				array.append((e.funcionario.id, e.funcionario.nombre+" "+ e.funcionario.apellido ))
	return array

"""
def asignacion_notif_asig(funcionario, funcionario_nuevo, solicitudes=None, asignaciones=None):
	notificaciones_emisor_viejo = Notificacion.objects.filter(
        emisor=analista.user, solicitud_id__in=solicitudes_analista)
    notificaciones_receptor_viejo = Notificacion.objects.filter(
        receptor = analista.user, solicitud_id__in=solicitudes_analista)

   #moviendo notificaciones del analista viejo al nuevo
    if notificaciones_emisor_viejo:
        for n in notificaciones_emisor_viejo:
            notificacion_nueva = Notificacion(
                emisor=funcionario_nuevo.user, receptor_id=n.receptor_id, 
                solicitud_id=n.solicitud_id, asunto= n.asunto, 
                observacion=n.observacion, fecha_emision= n.fecha_emision, 
                estado_anterior=n.estado_anterior)
            notificacion_nueva.save()
            n.delete()

       	#moviendo notificaciones del analista viejo al nuevo
    if notificaciones_receptor_viejo:
        for n in notificaciones_receptor_viejo:
            notificacion_nueva = Notificacion(
	            emisor_id=n.emisor_id, receptor=funcionario_nuevo.user, 
	            solicitud_id=n.solicitud_id, asunto= n.asunto, 
	            observacion=n.observacion, fecha_emision= n.fecha_emision, 
	            estado_anterior=n.estado_anterior)
            notificacion_nueva.save()
            n.delete()  

        #moviendo asignaciones del analista viejo al nuevo

    if asignaciones:
        tipoasig = TipoAsignacion.objects.get(abreviacion='A')
       	for n in asignaciones:
        	asignacion_nueva = Asignacion(
            	funcionario=funcionario_nuevo, tipo_asignacion=tipoasig,
                solicitud_id=n.solicitud_id, 
              	fecha_asignacion=datetime.datetime.now(),
                asignacion_habilitada=True)
            asignacion_nueva.save()
           	n.asignacion_habilitada=False
            n.save()

        for s in solicitudes:
            if s.funcionario_id == analista.id:
                s.funcionario_id = func_nuevo.id
"""
