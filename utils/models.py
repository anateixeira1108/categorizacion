# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.db import models
from errno import EEXIST
from hashlib import sha1
from mintur.settings import MEDIA_ROOT
from os import makedirs
from os import path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ERROR_MSG = (
    'No hay forma de conseguir el usuario para este modelo.'
    '\n¿Está seguro que no prefiere usar la clase Model'
    ' en lugar de esta clase para extender su modelo?'
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CustomFileAllocatorModel(models.Model):
    class Meta:
        abstract = True

    def save(self):
        if u'cedula' in dir(self):
            key_str = self.rif

        elif u'pst' in dir(self):
            key_str = self.pst.rif

        elif u'declaracion' in dir(self):
            key_str = self.declaracion.pst.rif
            
        else:
            raise Exception(ERROR_MSG)

        for field in self._meta.fields:
            if isinstance(field, models.FileField):
                process_file_field(field, key_str)

        super(CustomFileAllocatorModel, self).save()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_directory_if_not_exists(relative_path_str):
    complete_path_str = path.join(MEDIA_ROOT, relative_path_str)

    if not path.exists(complete_path_str):
        try:
            makedirs(complete_path_str)

        except OSError as exception:
            if exception.errno != EEXIST or not path.isdir(path):
                raise exception


def gen_path_str_from_key_str(key_str):
    hash_str = sha1(key_str).hexdigest()
    return path.join(*(hash_str[i:i+4] for i in xrange(0, 40, 4)))


def process_file_field(field, key_str):
    field.upload_to = gen_path_str_from_key_str(key_str)
    create_directory_if_not_exists(field.upload_to)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
