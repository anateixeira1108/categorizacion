# *-* coding: utf-8 *-*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template import Template
from json import load as json_load
from os import path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SENDER_EMAIL = 'bot@4geeks.co'

TEMPLATES_BASEDIR_PATH = path.join(
    settings.BASE_DIR, 'share', 'templates'
)

TEMPLATES_FILE_PATH = path.join(
    settings.BASE_DIR, 'share', 'emails.json'
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MetaMailMan(type):
    def __getattr__(cls, attr):
        assert path.isfile(TEMPLATES_FILE_PATH)

        with open(TEMPLATES_FILE_PATH, 'r') as fp:
            templates = json_load(fp)

        assert isinstance(templates, dict)
        assert attr in templates

        def wrapper(data_dict, receptor_email):
            for arg in templates[attr]['args']:
                assert arg in data_dict

            template_file_path = path.join(
                TEMPLATES_BASEDIR_PATH, templates[attr]['filename']
            )

            assert path.isfile(template_file_path)

            with file(template_file_path, 'r') as fp:
                template = Template(fp.read())

                cls.send(template.render(Context(data_dict)), receptor_email)

        return wrapper


class MailMan(object):
    __metaclass__ = MetaMailMan

    @classmethod
    def send(cls, body, receptor_email):
        send_mail(
            'Notificación Mintur', body, SENDER_EMAIL, [receptor_email]
        )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
