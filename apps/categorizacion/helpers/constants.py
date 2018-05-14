# -*- encoding: utf-8 -*-

"""
	constants.py
	~~~~~~~~~~~~

	Archivo de definicion de constantes

"""

ELEMENTO_POR_PAGINA = 10
CUENTA_EMAIL = 'user@domain.com'

TIPO_SUBSECCIONES = {
	'req_doc': 'RD',
	'cont_serv': 'CS',
	'otrs': 'O',
	'req_func': 'RF',
	'elem_val_agregado': 'EVA',
	'req_mant': 'RM',
}

COORDENADAS_DOCUMENTOS = {
    "categorizacion": {
        "oficio_disposicion_mejora":{
            "coletilla":{'x': "center",'y': 170, "pagina": 1},
            "firma_electronica":{ 'pX': 250,'pY': 345,'pW': 390,'pH': 395,"pagina": 2}
        },
        "oficio_aprobacion_prorroga":{
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 250,'pY': 170,'pW': 390,'pH': 220,"pagina": 1}
        },
        "oficio_aprobacion_categorizacion":{  #Oficio de aprobacion de categoria por primera vez sin reparacion
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        },
        "oficio_incumplimiento_disposicion":{
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        },
        "oficio_otorgamiento_disposicion":{ #Oficio de aprobacion de categoria luego de una reparacion
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        },
        "oficio_credencial":{ #Listo
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 250,'pY': 160,'pW': 390,'pH': 210,"pagina": 1}
        }
    },
    "lsr": {
        "oficio_respuesta_folios": {
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        } 
    },
    "placa":{
        "alojamiento_sin_tabulador": {
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        },
        "alojamiento_para_elaborarla": {
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        },
        "pst_sin_diseno": {
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        },
        "licencia_vencida": {
            "coletilla":{'x': "center",'y': 170,"pagina": 1},
            "firma_electronica":{ 'pX': 360,'pY': 220,'pW': 580,'pH': 270,"pagina": 1}
        }
    }
}

OFICIOS_FIRMAS = [
	'ODM', #Oficio de Disposiciones de Mejora 
	'ORSP', #Oficio Respuesta de Solicitud de Prórroga
	'OOC1V', #Oficio de Otorgamiento de Categoría 1 vez
	#'OPLV', #Oficio Placa con Licencia Vencida
	#'OPSL', #Oficio Placa Sin Licencia
	'OCPPI', #Oficio Cierre del Procedimiento por Incumplimento
	'OCCDM', #Oficio de Otorgamiento de Categoría por cumplimiento de Disposiciones de Mejora
	'OR', #Oficio de Respuesta
	#'OP', #Oficio Placa
	'C', #Credenciales
	#'OPPT', #Oficio Placa Para Transporte
]

OPCIONES = {
	'SC': [],
	'PAA': [u'Solicitar Análisis', 'Proponer No Procedencia'],	
	'EC': [],
	'SAR': ['Devolver con Observaciones', u'Proponer Aprobación',  'Proponer No Procedencia'],
	'EAP': [u'Aprobar Prórroga', u'Negar Prórroga'],
	'SEAR': ['Devolver con Observaciones', u'Solicitar Inspección', 'Proponer No Procedencia'],
	#'EAR': ['Devolver con Observaciones', 'Proponer No Procedencia', 'Aprobar Reparaciones'],
	'ER': [],
	'EANP': ['Devolver con Observaciones', 'Proponer No Procedencia'],
	'EA': ['Devolver con Observaciones', u'Proponer Aprobación', 'Proponer No Procedencia'],
	'EP': [],
	'VI': ['Devolver con Observaciones', 'Proponer No Procedencia', u'Generar Informe Técnico'],
	'RI': ['Devolver con Observaciones', u'Aprobar Inspección'],
	#'EN':['Devolver con Observaciones', 'Proponer No Procedencia',  u'Incumplimiento de Disposiciones'],
	'PAI': [u'Cancelar Inspección', 'Otorgar Credenciales'],
	'EI': ['Devolver con Observaciones', u'Enviar Inspección'],
	'CI': [u'Enviar Inspección'],
	'ITG':['Devolver con Observaciones', 'Proponer No Procedencia', u'Generar Informe Técnico'],
	'NPI':[],
	'EN': ['Devolver con Observaciones', u'Proponer Incumplimiento'],
	'SN':[],
	'SAI':['Devolver con Observaciones', 'Proponer No Procedencia', u'Solicitar Edición de Requisitos', u'Aprobar Inspección'],
	'A':[],
	'RS':[u'Aprobar Reconsideración', u'Negar Reconsideración'],
	'ECI':['Devolver con Observaciones', u'Cancelar Inspección'],
	'DMG':['Devolver con Observaciones', 'Firmar'],
	'CG': ['Devolver con Observaciones', 'Firmar'],
	'RPG': ['Devolver con Observaciones', 'Firmar']
	#'RS':[u'Solicitar Inspección',u'Proponer Aprobación de Reconsideración'],
}

ESTATUS_PST = {
	u'Análisis':['PAA', 'SAR','SEAR','EANP','EA','VI','RI','PAI','CI', 'EN', 'ITG', 'SAI', 'SAI', 'RS', 'ECI', 'DMG', 'CG', 'RPG', 'EAP'],
	'Negada':['SN'],
	'Negada Por Incumplimiento':['NPI'],
	'Aprobada':['A'],
	'Creada': ['SC'],
	u'En Corrección': ['EC'],
	'En Reparaciones': ['ER'],
	u'En Prórroga': ['EP'],
	u'En Inspección': ['EI'],

}

INT = 0
FLOAT = 1
STRING = 2
DICT = 3
LIST = 4
TUPLE = 5
COLLECTION =  6

TIPO_DATO = (
	(INT, 'Entero'),
	(FLOAT, 'Real'),
	(STRING, 'String'),
	(DICT, 'Diccionario'),
	(LIST, 'Lista'),
	(TUPLE, 'Tupla'),
	(COLLECTION, 'Coleccion'),
	)

SECRET_TAB_KEY = u"tVW7I-@_jWloKPlA@\59TtqT%$UeQF1LM"
