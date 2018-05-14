# encode: utf-8

from apps.categorizacion.widgets import CustomStarsWidget, CustomStarsWidgetRango, RangoWidget, CustomStarsLogicalWidget
from django.forms import Field


class RangoField(Field):
	"""
		Campo de estrellas para porcentajes por aspecto fundamental
	"""
	default_error_messages = {	        
	        'required': u"Este campo es obligatorio",
	        'invalid': u"Valor colocado invalido"
		}	

	def __init__(
			self, 
			required = True, 
			label = "", 
			initial = None,
			help_text = "",
			error_messages = "", 
			show_hidden_initial = None, 
			validators = [],
			localize = False,
			_step = 1,
			_min = 1,
			_max = 100,			
			*args, **kwargs
		):
		self.widget = RangoWidget(_step = _step, _min = _min, _max = _max)
		super(RangoField, self).__init__(*args, **kwargs)


class StarsField(Field):
	"""
		Campo de estrellas para formularios del tabulador
	"""
	default_error_messages = {	        
	        'required': u"Este campo es obligatorio",
	        'invalid': u"Valor colocado invalido"
		}	

	def __init__(
			self, 
			required = True, 
			label = "", 
			initial = None,
			help_text = "",
			error_messages = "", 
			show_hidden_initial = None, 
			validators = [],
			localize = False,
			categorias = 0,
			flag="check",
			star_icon = "fa-star",
			*args, **kwargs
		):
		self.widget = CustomStarsWidget(categorias = categorias, flag=flag, star_icon = star_icon)
		super(StarsField, self).__init__(*args, **kwargs)


class StarsFieldRango(Field):
	"""
		Campo de estrellas para respuesta Rango
	"""
	default_error_messages = {	        
	        'required': u"Este campo es obligatorio",
	        'invalid': u"Valor colocado invalido"
		}	

	def __init__(
			self, 
			required = True, 
			label = "", 
			initial = None,
			help_text = "",
			error_messages = "", 
			show_hidden_initial = None, 
			validators = [],
			localize = False,
			categorias = 0, 
			star_icon = "fa-star",
			*args, **kwargs
		):
		self.widget = CustomStarsWidgetRango(categorias = categorias, star_icon = star_icon)		
		super(StarsFieldRango, self).__init__(*args, **kwargs)		


class StarsFieldLogical(Field):
	"""
		Campo de estrellas para respuesta formula
	"""
	default_error_messages = {	        
	        'required': u"Este campo es obligatorio",
	        'invalid': u"Valor colocado invalido"
		}	

	def __init__(
			self, 
			required = True, 
			label = "", 
			initial = None,
			help_text = "",
			error_messages = "", 
			show_hidden_initial = None, 
			validators = [],
			localize = False,
			categorias = 0, 
			star_icon = "fa-star",
			lo = None,
			*args, **kwargs
		):
		self.widget = CustomStarsLogicalWidget(categorias = categorias, logical_options = lo,  star_icon = star_icon)
		super(StarsFieldLogical, self).__init__(*args, **kwargs)