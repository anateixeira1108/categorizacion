# -*- coding: utf-8 -*-

"""
Clase para generar realizar busquedas del pst
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: 4geeks
# contacto: http://www.4geeks.co/contacto
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from registro.models import Pst, Direccion, TipoPst
from registro.models import ESTATUS_REGISTRO_SIN_COMPLETAR
from declaraciones.models import Declaracion
from venezuela.models import Estado, Municipio, Parroquia
from utils.gluon.storage import Storage
from datetime import date, datetime
from django.db.models import F
from django.db.models import Q

MESES = {
    "Enero": 1, "Febrero": 2, "Marzo": 3,
    "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9,
    "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

class BusquedaPst(object):

    def __init__(self, tipo, param):
        """
        Funcion que realiza la busqueda de pst
        parametros
            - cls: objeto Pst
            - tipo (String): tipo de busqueda que desea realizar (basica, avanzada)
            - param (QueryDict): parametros para la busqueda de pst
        retorna
            - cls
        """
        self.tipo = tipo
        self.param = param

    def busqueda(self ):
        list_ids, objs, declaracion, periodo, criterio = [], [], [], [], []
        search_region, search_declaracion, search = dict(), dict(), dict()
        filter = dict()
        region = ['estado', 'municipio', 'parroquia']
        filtro, actividad = int(), int()
        IGUAL_O_MAYOR_QUE = 1
        IGUAL_O_MENOR_QUE = 2
    
        del self.param['busqueda']

        if self.tipo == "basica":
            rif=""
            criterio=["Selección Manual"]
            try:
                rif = self.param['rif']
            except Exception as e:
                pass
            if rif == "":
                objs = Pst.objects.filter(
                            ~Q(estatus=ESTATUS_REGISTRO_SIN_COMPLETAR),
                            numero_contribuyente__isnull=False
                        )
            else:
                objs = Pst.objects.filter(
                            ~Q(estatus=ESTATUS_REGISTRO_SIN_COMPLETAR),
                            numero_contribuyente__isnull=False,
                            rif=rif
                        )

        if self.tipo == "avanzada":
            for key, value in self.param.iteritems():
                if key in region and value:
                    if key == "estado":
                        search['direccion__estado_id']=Estado.objects.get(pk=int(value))
                    if key == "municipio":
                        search['direccion__municipio_id']=Municipio.objects.get(pk=int(value))
                    if key == "parroquia":
                        search['direccion__parroquia_id']=Parroquia.objects.get(pk=int(value))
                    search_region=True

                elif key == 'monto':
                    search_declaracion['monto']=value.encode('utf-8')

                elif key == 'tipo_ingreso':
                    filtro=int(value.encode('utf-8'))

                elif key == 'periodo_desde' or key == 'periodo_hasta': 
                    date_time=self.param['periodo_desde'].split('-')
                    desde=datetime(int(date_time[1]), MESES[str(date_time[0])], 1)
                    date_time = self.param['periodo_hasta'].split('-')
                    hasta=datetime(int(date_time[1]), MESES[str(date_time[0])], 1)
                    search_declaracion['rango_periodo'] = (desde, hasta)
                
                elif key == 'tipo_pst':
                    actividad=TipoPst.objects.get(pk=int(value.encode('utf-8')))
                    search['actividadcomercial__actividad_id']=actividad

                elif key == 'omisiones':
                    search_declaracion['omisiones']=int(value.encode('utf-8'))

                elif key == 'extemp':
                    search_declaracion['extemp']=int(value.encode('utf-8'))
              
            if search_region: 
                criterio.append("Selección por Ubicación geográfica")
            
            for k in search_declaracion:
                if k == 'monto':
                    if filtro == IGUAL_O_MAYOR_QUE:
                        ingreso = "mayores"
                        search['declaracion__total_ventas_territorial__lte']=float(search_declaracion[k])
                    else: 
                        ingreso = "menores"
                        search['declaracion__total_ventas_territorial__gte']=float(search_declaracion[k])

                    m = "Ingresos %s ó iguales a Bs. %s" % (ingreso, search_declaracion[k])
                    criterio.append(m)

                if k == 'rango_periodo':
                    search['declaracion__periodo__range']=(search_declaracion[k][0], search_declaracion[k][1])

                elif key == 'extemp':
                    print search_declaracion[key]

                elif key == 'omisiones':
                    search['declaracion__concepto_pago__pago__fecha_liquidacion']=None
                    search['declaracion__concepto_pago__pago__fecha_vencimiento__lt']=datetime.now()
            print search
            ## Falta la cache en: direccion, declaraciones, acividad comercial
            objs = Pst.objects.filter(~Q(estatus=ESTATUS_REGISTRO_SIN_COMPLETAR), **search)

        return Storage(objects=objs, criterio=criterio)


