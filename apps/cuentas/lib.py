# -*- coding: utf-8 -*-
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from utils.generate_sha1 import generate_sha1
from apps.cuentas.models import MinturUser


def reset_password_send_email(user):
    reset_password_key = generate_sha1()

    while MinturUser.objects.filter(reset_password_key=reset_password_key):
        reset_password_key = generate_sha1()

    user.reset_password_key = reset_password_key
    user.reset_password_date = datetime.datetime.now()
    user.save()

    print "Reset Password key Generated: %s, for user: %s " % (reset_password_key, user)

    context = {
        'user': user,
        'server_uri': settings.SERVER_URI
    }
    asunto = render_to_string(
        'notificaciones_correo_electronico/asunto_reset_password.txt',
        context
    )

    asunto = ''.join(asunto.splitlines())
    mensaje = render_to_string(
        'notificaciones_correo_electronico/mensaje_reset_password.txt',
        context
    )

    send_mail(
        asunto,
        mensaje,
        'mintur@mintur.gob.ve',
        [user.correo_electronico, ],
        fail_silently=False
    )