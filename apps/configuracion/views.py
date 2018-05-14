# ~º~ coding: UTF-8 ~º~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.configuracion import models
from datetime import date
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from utils import views_helpers as helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Vistas (Funciones) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required(login_url=reverse_lazy('cuentas_login'))
def get_fecha_limite(request):
    if 'periodo' not in request.GET:
        return helpers.json_response({
            'error': -1, 'msg': 'Debe proporcionar el periodo.'
        })

    try:
        period = map(int, request.GET['periodo'].split('/'))

    except ValueError:
        return helpers.json_response({
            'error': -2, 'msg': 'Bad value for the period.'
        })

    if not period or len(period) != 3 or period[0] != 1:
        return helpers.json_response({
            'error': -2, 'msg': 'Bad value for the period.'
        })

    result = models.CalendarioLaboral.get_n_siguiente_dia_laborable(
        15, date(*reversed(period))
    ).strftime('%d/%m/%Y')

    return helpers.json_response({'error': 0, 'result': result})
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
