# -*- coding: utf-8 -*-
import sys, os

SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.join(SCRIPTS_DIR, '../')

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'mintur'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'mintur.settings'

from apps.cuentas.models import MinturUser
from apps.procesos.models import Proceso, Flujo, FlujoSecuencia
from utils.gluon.storage import Storage
from django.contrib.auth.models import Group

"""Contiene el proceso inicial para las resoluciones"""


flujo = []
fixture = Storage(
    nombre="Resoucion",  
    descripcion="Proceso para generar verificaciones de las solicitudes del pst V: 0.1", 
    activo = True, fecha_desactivacion = None
)

# proceso = Proceso(**fixture)
# proceso.save()

fixtures = [
    Storage(proceso=proceso, grupo=Group.objects.get(name="funcionarios_dggt"), 
            nombre="Revisión y análisis del expediente del contribuyente.", 
            inicio=True, fin=False
    ),
    Storage(proceso=proceso, grupo=Group.objects.get(name="gerente_dggt"), 
            nombre="Negación ó Aprobación de conformidad en el proceso de verificación.", 
            inicio=False, fin=False
    ),
    Storage(proceso=proceso, grupo=Group.objects.get(name="gerente_dggt"), 
            nombre="Aprobado el proyecto de Resolución", inicio=False, fin=True
    ),
    Storage(proceso=proceso, grupo=Group.objects.get(name="gerente_dggt"), 
            nombre="Negado el proyecto de Resolución", inicio=False, fin=True
    )
]

# for data in fixtures:
#     f = Flujo(**data)
#     f.save()
#     flujo.append(f)

fixtures = [
    Storage(actual=flujo[0].id, siguiente=flujo[1].id, proceso=proceso),
    Storage(actual=flujo[1].id, siguiente=flujo[2].id, proceso=proceso),
    Storage(actual=flujo[1].id, siguiente=flujo[3].id, proceso=proceso),
]

# for data in fixtures:
#     fs = FlujoSecuencia(**data)
#     fs.save()