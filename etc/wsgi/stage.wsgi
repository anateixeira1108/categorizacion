import os
import sys

ETC_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(ETC_DIR))
BASE_DIR_MINTUR = os.path.abspath(os.path.join(BASE_DIR, 'mintur'))
BASE_DIR_EGG = os.path.abspath(os.path.join(BASE_DIR, '.python-egg'))

sys.path.append(BASE_DIR)
sys.path.append(BASE_DIR_MINTUR)
sys.path.append('/usr/local/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/Django-1.6.4-py2.7.egg')
sys.path.append('/usr/local/lib/python2.7/site-packages/django_jenkins-0.15.0-py2.7.egg')

os.environ['PYTHON_EGG_CACHE'] = BASE_DIR_EGG
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
