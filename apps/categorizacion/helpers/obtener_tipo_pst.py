# -*- enconding: utf-8 -*- 

from apps.categorizacion.models import *
from apps.licencias.models import *
from apps.cuentas.models import *
from registro.models import *

def otp_solicitud(solicitud = None):
	try:
		a = SolicitudLicencia.objects.filter(
		    sucursal = solicitud.sucursal,		    
		    tipo_licenciaid__padre= TipoLicencia.objects.get(codigo = 'LIC_ALO_T'),
		    estatus_solicitudid= EstatusSolicitud.objects.get(codigo = 'EST_APROB')
		)
		"""
		TODO: Validar si en esta seccion existira
		una sola licencia asociada del mismo padre.
		(LICENCIAS MODULE)
		"""
		return a.first().tipo_licenciaid if len(a) else None
	except Exception, e:
		raise Exception("Errores encontrados al momento de determinar tipo de prestador de servicio turistico: %s"%(str(e),))


def otp_prestador(pst = None, sucursal = None):
	try:
		a = SolicitudLicencia.objects.filter(
			sucursal_id = sucursal, 
		    tipo_licenciaid__padre = TipoLicencia.objects.get(codigo = 'LIC_ALO_T'),
		    estatus_solicitudid = EstatusSolicitud.objects.get(codigo = 'EST_APROB'),
		    usuario_pst_id =pst.user
		)
		"""
		TODO: Validar si en esta seccion existira
		una sola licencia asociada del mismo padre.
		(LICENCIAS MODULE)
		"""
		return a.first().tipo_licenciaid if len(a) else None
	except Exception, e:
		raise Exception("Errores encontrados al momento de determinar tipo de prestador de servicio turistico: %s"%(str(e),))