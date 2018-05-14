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
    'registro',
    'apps.configuracion',
    'apps.cuentas',
    'apps.verificacion',
    'apps.fiscalizacion',
    'apps.inteligencia_tributaria',
    'apps.pagos',
    'apps.resoluciones',
    'apps.factibilidad',
    'apps.firmas',
    'widget_tweaks',
    'braces',
    'declaraciones',
    'passwords'
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

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

# Para redireccionar a esta URL cuando el usuario no se encuentra logueado
LOGIN_URL = '/cuentas/ingresar/'

# Media Settings
MEDIA_URL = '/documents/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'documents', 'files')

PDF_ROOT = os.path.join(BASE_DIR, 'templates', 'base_pdf')

# -------------------- START LOCALES CONFIG ---------------------------
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# -------------------- END LOCALES CONFIG -----------------------------

# ---------------------START PASSWORD STRENGH CHECKER -----------------
PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 16

PASSWORD_COMPLEXITY = {
    "UPPER": 1,
    "LOWER": 1,
    "DIGITS": 1
}
# ---------------------END PASSWORD STRENGH CHECKER -------------------
