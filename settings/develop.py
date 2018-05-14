from .common import *

SERVER_URI = u'http://127.0.0.1:8000'

DEBUG = True

# Email Backend para desarrollo (No genera salida)
ENABLE_EMAIL = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'