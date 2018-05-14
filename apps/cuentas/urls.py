from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from apps.cuentas import views


urlpatterns = \
    patterns('',
             url(r'^$',
                 RedirectView.as_view(url=reverse_lazy('cuentas_login'))),

             url(r'^ingresar/$',
                 views.IngresarView.as_view(),
                 name='cuentas_login'),

             url(r'^salir/$',
                 views.SalirView.as_view(),
                 name='cuentas_logout'),


             url(r'^necesita/ayuda/$',
                 views.NecesitaAyudaView.as_view(),
                 name='cuentas_necesita_ayuda'),

             # Reestablecer contrasena
             url(r'^restablecer/contrasena/(?P<reset_password_key>[a-f0-9]{40})/$',
                 views.ResetPasswordView.as_view(),
                 name='cuentas_restablecer_contrasena'),

             # Preguntas secretas
             url(r'^preguntas/secretas/$',
                 views.PreguntasSecretasView.as_view(),
                 name='cuentas_preguntas_secretas'),


             # Crear cuenta de PST
             url(r'^nueva/$',
                 views.NuevaCuentaView.as_view(),
                 name='cuentas_nueva'),

             # Activar cuenta de PST
             url(
                 r'^activar/(?P<activation_key>[a-f0-9]{40})/$',
                 views.ActivarCuentaView.as_view(),
                 name='cuentas_activar_cuenta'
             )


    )
