from apps.cuentas.models import ROLE_PST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin
from registro.models import PERSONA_NATURAL
from registro.models import ESTATUS_REGISTRO_SIN_COMPLETAR


class MenuPSTMixin(ContextMixin):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(MenuPSTMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MenuPSTMixin, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated():
            if user.role == ROLE_PST:
                pst = user.pst_set.get()  # Obtenemos el registro PST
                natural = False
                juridica = False

                if pst.tipo_figura == PERSONA_NATURAL:
                    natural = True
                else:
                    juridica = True

            context['pst'] = pst
            context['natural'] = natural
            context['juridica'] = juridica
            context['nuevo_registro'] = (pst.estatus == 1)
            context['mostrar_cambio_perfil'] = (
                pst.emprendedor and pst.estatus != ESTATUS_REGISTRO_SIN_COMPLETAR
            )

        return context
