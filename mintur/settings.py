"""

Django settings for mintur project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uos)ex^rxt=m3#pidmfzq2%njuo*hez&1$!ph_jqo9bfcp5@5('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'south',
    'venezuela',
    'apps.cuentas',
    'registro',
    'apps.verificacion',
    'apps.fiscalizacion',
    'apps.configuracion',
    'apps.actas',
    'apps.procesos',
    'apps.inteligencia_tributaria',
    'apps.resoluciones',
    'apps.pagos',
    'apps.factibilidad',
    'apps.firmas',
    
    # CGTS DevTeam :: Modulo de Categorizacion y Licencias #
    'apps.licencias',
    'apps.categorizacion',

    'widget_tweaks',
    'braces',
    'declaraciones',
    'passwords',
    'easy_pdf',
    'django_crontab',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mintur.urls'

WSGI_APPLICATION = 'mintur.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tesis',
        'USER': 'ateixeira',
        'PASSWORD': '123456',
        #'HOST': 'pgadmin.cgtscorp.com',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

DATE_INPUT_FORMATS =('%d/%m/%Y')

DATETIME_INPUT_FORMATS =('%d/%m/%y %H:%M:%S')

DATETIME_FORMAT ='d/m/Y H:M:S'

DATE_FORMAT ='d/m/Y'

LANGUAGE_CODE = 'es-ve'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, './static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, './templates'),
)

# Custom User model to authenticate
AUTH_USER_MODEL = 'cuentas.MinturUser'

# Email Backend para desarrollo (No genera salida)
ENABLE_EMAIL=True
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

# SMTP Host config

#############
# CGTS MAIL #
#############

#EMAIL_HOST ='mail.cgtscorp.com'
#EMAIL_USE_TLS = False
#EMAIL_PORT = 25

# Autenticacion
#EMAIL_HOST_USER ='gccdev'
#EMAIL_HOST_PASSWORD='sys64738'

#########
# GMAIL #
#########

EMAIL_HOST ='smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT = 587

# Autenticacion
EMAIL_HOST_USER ='cgts.pruebas@gmail.com'
EMAIL_HOST_PASSWORD='cgts%2014'

# Para redireccionar a esta URL cuando el usuario no se encuentra logueado
LOGIN_URL = '/cuentas/ingresar/'

# Media Settings
MEDIA_URL = '/documents/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'documents', 'files')

PDF_ROOT = os.path.join(BASE_DIR, 'templates', 'base_pdf')

SERVER_URI = u'http://127.0.0.1:8000'

# -------------------- START LOCALES CONFIG ---------------------------
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# -------------------- END LOCALES CONFIG -----------------------------

# -------------------- START DIGITAL SIGNATURES -----------------------

# ruta donde se encontraran las solicitudes de los
# documentos electronicos (documentos no firmados)
DOC_ELECTRONICOS_SOLICITUDES_URL = '/documents/firma_electronica/solicitudes/'

DOC_ELECTRONICOS_SOLICITUDES_ROOT = os.path.join(
    BASE_DIR, 'documents', 'firma_electronica', 'solicitudes')

# ruta donde se encontraran los documentos electronicos (documentos firmados)
# luego de ser firmados por el applet de firmas digitales, es una carpeta
# donde los archivos estaran temporalmente
DOC_ELECTRONICOS_FIRMADOS_TEMP_URL = '/documents/firma_electronica/temporales/'
DOC_ELECTRONICOS_FIRMADOS_TEMP_ROOT = os.path.join(
    BASE_DIR, 'documents', 'firma_electronica', 'temporales')

# ruta donde se consultan los documentos firmados, adicional a la ruta
# se debe colocar el rif y luego el nombre del archivo
# ej: DOC_ELECTRONICOS_FIRMADOS_URL + "pst.rif + "/" + "solicitud_rtn.pdf"
# ej2: 
#//localhost/documents/firma_electronica/firmados/V-12346578-0/solicitud_rtn.pdf
DOC_ELECTRONICOS_FIRMADOS_URL = '/documents/firma_electronica/firmados/'

DOC_ELECTRONICOS_FIRMADOS_ROOT = os.path.join(
    BASE_DIR, 'documents', 'firma_electronica', 'firmados') 

SSH_USER = "amartin"
SSH_PASSWORD = "am092014"
SSH_SERVER = "192.168.7.31"
SSH_PORT = "22"



# -------------------- END DIGITAL SIGNATURES -------------------------



# ----------------------START PASSWORD STRENGH CHECKER -----------------
PASSWORD_MIN_LENGTH = 8

PASSWORD_COMPLEXITY = {
    "UPPER": 1,
    "LOWER": 1,
    "DIGITS": 1
}
# ----------------------END PASSWORD STRENGH CHECKER -------------------

PREFIJO_INICIAL_GENERACION_RTN = 12000

"""
# Memcached
# ----------------- START CACHE CONFIGS -----------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': SERVER_URI,
    }
}
# ----------------- END CACHE CONFIGS -------------------
"""


#crontab jobs
CRONJOBS = [
    #('*/5 * * * *', 'apps.categorizacion.cron.my_scheduled_job'),
    #('*/1 * * * *', 'apps.categorizacion.cron.print_else'),
    #('10 02 * * *', 'apps.categorizacion.cron.requisitos_documentales'),
    #('10 02 * * *', 'apps.categorizacion.cron.reparacion_prorroga'),
    #('10 02 * * sun', 'apps.categorizacion.cron.renovacion'),
    #('10 02 * * *', 'apps.categorizacion.cron.folio'),
    ('10 02 * * *', 'apps.categorizacion.cron.entradas_no_respondidas'),
    ('10 02 * * *', 'apps.categorizacion.cron.requisitos_documentales'),
    ('10 02 * * *', 'apps.categorizacion.cron.reparacion_prorroga'),
    ('10 02 * * sun', 'apps.categorizacion.cron.renovacion'),
    ('10 02 * * *', 'apps.categorizacion.cron.folio'),
    ('10 02 * * *', 'apps.categorizacion.cron.entradas_no_respondidas'),
]
