# *~* coding: utf-8 *~*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Autor: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.db import models
from south.modelsinspector import add_introspection_rules
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Clases ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Src: https://gist.github.com/zorainc/5883779
class BigAutoField(models.fields.AutoField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'bigint AUTO_INCREMENT'

        elif 'postgresql' in connection.__class__.__module__:
            return 'bigserial'

        return super(BigAutoField, self).db_type(connection)


# Src: https://gist.github.com/zorainc/5883779
class BigForeignKey(models.ForeignKey):
    def db_type(self, connection):
        """Adds support for foreign keys to big integers as primary keys."""

        rel_field = self.rel.get_related_field()

        override = (
            isinstance(rel_field, BigAutoField) or
            (
                not connection.features.related_fields_match_type and
                isinstance(rel_field, (models.fields.BigIntegerField, ))
            )
        )

        if override:
            return models.fields.BigIntegerField().db_type(
                connection=connection
            )

        return super(BigForeignKey, self).db_type(connection)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Post-configuración ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
add_introspection_rules([], ["^mintur\.fields\.BigAutoField"])
add_introspection_rules([], ["^mintur\.fields\.BigForeignKey"])
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
