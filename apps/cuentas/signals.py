# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from utils.generate_sha1 import generate_sha1


def create_new_user_signal(sender, instance, created, **kwargs):
    """ Senal que se activa despues de la creacion de un PST en sistema """
    if created and instance.is_pst() and not instance.is_superuser:
        # se genera el activation_key unico para activar el PST
        activation_key = generate_sha1()
        while sender.objects.filter(activation_key=activation_key):
            activation_key = generate_sha1()

        # Se asigna el token al nuevo usuario creado
        instance.activation_key = activation_key
        instance.is_active = False
        instance.save()

        print "Activation_key Generated: %s, for pst: %s" % (activation_key, instance)

        # Se envia el correo de registro de nuevo PST

        context = {
            'pst': instance,
            'server_uri': settings.SERVER_URI
        }
        asunto = render_to_string(
            'notificaciones_correo_electronico/asunto_activacion_nuevo_pst.txt',
            context
        )

        asunto = ''.join(asunto.splitlines())
        mensaje = render_to_string(
            'notificaciones_correo_electronico/mensaje_activacion_nuevo_pst.txt',
            context
        )

        send_mail(
            asunto,
            mensaje,
            'mintur@mintur.gob.ve',
            [instance.correo_electronico, ],
            fail_silently=False
        )