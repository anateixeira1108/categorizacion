__author__ = 'elio'
# -*- coding: utf-8 -*-
from django import template
from registro.models import TIPOS_PERSONAS_JURIDICA

register = template.Library()


@register.filter(name='tipo_persona_juridica')
def type(value):
	# if value >= 0 and value <= 2 else None
    return TIPOS_PERSONAS_JURIDICA[value][1]