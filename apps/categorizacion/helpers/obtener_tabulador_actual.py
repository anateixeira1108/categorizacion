# -*- encoding: utf-8 -*-

from apps.categorizacion.models import *

"""
	Criterio
	~~~~~~~~
	Dado un tipo de prestador de servicio se realiza
	el ordenamiento de los tabuladores asociados a este
	retornando siempre la ultima version del mismo
"""

def version_actual(tipo_pst):
	t = None
	try:		
		t = Tabulador.objects.filter(
			tipo_pst = tipo_pst,
			version_actual = True
		)
		if len(t):
			return t.first()
		else:
			raise Exception(u"No existe configurado un tabulador para el tipo de prestador especificado %s" % tipo_pst.nombre)
	except Exception, e:
		raise Exception(u"[version_actual]: %s" % (str(e),))

"""
	Criterio
	~~~~~~~~
	Teniendo un pst se extrae la solicitud abierta mas actual
	para la sucursal suministrada con fecha de clausura nula
"""
def tabulador_asociado(pst, sucursal = None):
# TODO agragar mecanismo de control para las sucursales.
	"""
		Busca dentro de las solicitudes del prestador actual aquellas
		que sea la mas actual y obtiene el tabulador asociado a la 
		misma
	"""
	try:
		"""
			Obtener solicitud abierta para un prestador
			en particular
		"""
		s = Solicitud.objects.filter(
			pst_id = pst,
			fecha_clausura__isnull = True
		)
		if s.exists():
			"""
				Si la solicitud existe entonces se debe retornar
				el tabulador asociado a la solicitud de este prestador
			"""
			return s.first().tabulador
		else:
			raise Exception("Error durante busqueda de tabulador")

	except Exception, e:
		raise e
