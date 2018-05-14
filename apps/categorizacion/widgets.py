# encode: utf-8 

from django import forms
from django.forms import widgets
from django.forms import MultiWidget
from django.utils.html import format_html
import HTMLParser

EMPTY_VALUES = (None, '', [], (), {})

class RangoWidget(widgets.MultiWidget):
	"""
		Campo con slider para los valores porcentuales de los aspectos fundamentales
	"""
	def __init__(
		self, 
		name = "_rango", 
		_step = 0.1, 
		_min = 0, 
		_max = 100,
		_icon = "fa-star", 
		attrs = None):
		self.min = _min
		self.max = _max
		self.step =  _step
		self.icon = _icon
		self.name = "_rango"
		self.widgets = [forms.NumberInput( attrs={'type':'range', 'step': _step, 'min': _min, 'max': _max, 'id': 'id_peso_porcentual'} )]
		super(RangoWidget, self).__init__(self.widgets, attrs)

	def decompress(self, value):
		try:
			return [float(value)]			
		except Exception, e:
			return []

	def render(self, name, value, attrs=None):
		output = ""
		for e in self.widgets:
			output += e.render(self.name, self.min)
		return format_html( output )


class CustomStarsWidget(widgets.MultiWidget):
	"""
		Campo con tantas estrellas como categorias tenga el 
		tipo de prestador especificado
	"""
	def __init__(
		self, 
		categorias = 0, 
		star_icon = "fa-star", 
		star_name= "star", 
		flag= "check", 
		attrs = None):
		self.categorias = categorias
		self.star_icon = star_icon
		self.star_name = star_name
		if flag == "check":
			self.widgets = [forms.CheckboxInput()] * categorias if categorias else [forms.TextInput()]
		elif flag == "input":
			self.widgets = [forms.NumberInput()] * categorias if categorias else [forms.TextInput()]
		super(CustomStarsWidget, self).__init__(self.widgets, attrs)

	def str_to_bool(self, s):
		if s == 'True':
			return True
		elif s == 'False':
			return False
		else:
			raise ValueError	
		
	def decompress(self, value):
		if value not in EMPTY_VALUES:
			val = []
			if isinstance(value, str):
				for e in value.split(','):
					val.append( self.str_to_bool(e) )					
			elif isinstance(value, dict):
				for k, v in value:
					if isinstance( v, bool ):
						val.append(v)
					else:
						raise ValueError
			elif isinstance(value, tuple):
				for e in value:
					if isinstance( e, bool ):
						val.append(v)
					else:
						raise ValueError
			else:
				return None
			return val
		else:
			return None

	def render(self, name, value, attrs=None):
		star = '<label for = "%s_%s" style="margin-top: 8px;"><span class="text-red"><i class="fa %s"></i></span>&nbsp;</label>'
		table = '<table class="stars_table col-xs-offset-3"> <tbody> %s </tbody> </table>'
		row = '<tr> <td class="%s">%s</td><td class="col-xs-5">%s</td></tr>'
		widget_labels = []

		for e in xrange(self.categorias):
			widget_labels.append( (star % (self.star_name, e, self.star_icon)) * (e+1) )

		if self.is_localized:
			for widget in self.widgets:
				widget.is_localized = self.is_localized

		if not isinstance(value, list):
			value = self.decompress(value)
		
		output = ''
		for i, widget in enumerate(self.widgets):			
			output += row % (self.star_name, widget_labels[i], widget.render('%s_%s' % (self.star_name, i), value[i] if value is not None else None) )
		return format_html( table % (output,) )


class CustomStarsWidgetRango(widgets.MultiWidget):
	"""
		Campo con tantas estrellas como categorias tenga el 
		tipo de prestador especificado
	"""
	def __init__(
		self, 
		categorias = 0, 
		star_icon = "fa-star", 
		star_name= "star", 
		name_one="L&iacute;mite Inferior", 
		name_two="L&iacute;mite Superior", 
		attrs = None):
		self.categorias = categorias
		self.star_icon = star_icon
		self.star_name = star_name
		self.name_one = name_one
		self.name_two = name_two
		self.widgets = [forms.NumberInput(attrs={'disabled': 'disabled'}), forms.CheckboxInput()] * 2 * categorias if categorias else [forms.NumberInput()]
		super(CustomStarsWidgetRango, self).__init__(self.widgets, attrs)

	def str_to_bool(self, s):
		if s == 'True':
			return True
		elif s == 'False':
			return False
		else:
			raise ValueError	
		
	def decompress(self, value):
		if value not in EMPTY_VALUES:
			val = []
			if isinstance(value, str):
				for e in value.split(','):
					val.append( self.str_to_bool(e) )					
			elif isinstance(value, dict):
				for k, v in value:
					if isinstance( v, bool ):
						val.append(v)
					else:
						raise ValueError
			elif isinstance(value, tuple):
				for e in value:
					if isinstance( e, bool ):
						val.append(v)
					else:
						raise ValueError
			else:
				return None
			return val
		else:
			return None

	def render(self, name, value, attrs=None):
		first_star = '<td class="%s" style="padding-right:0px;"><i class="fa %s text-red"></i></td>'
		other_star = '<td class="%s" style="padding-right:0px; padding-left:0px;"><i class="fa %s text-red"></i></td>'
		blank_td = '<td style="padding:0px;"></td>'
		padding = ''
		table = '<table class="stars_table table table-striped table-partner"> <thead><tr>'+ blank_td*self.categorias +'<td colspan="2">'+self.name_one+'</td><td colspan="2">'+self.name_two+'</td></tr></thead><tbody> %s </tbody> </table>'
		row = '<tr> %s <td>%s</td><td style="padding: 0;">%s</td><td>%s</td><td>%s</td></tr>'
		widget_labels = []

		for e in xrange(self.categorias):
			widget_labels.append( 
				( first_star % (self.star_name, self.star_icon)) + 
				( other_star % (self.star_name, self.star_icon)) * e + 
				blank_td * ( self.categorias - (e+1) )
			)

		if self.is_localized:
			for widget in self.widgets:
				widget.is_localized = self.is_localized
		
		if not isinstance(value, list):
			value = self.decompress(value)
		
		output = ''
		cont=0		
		for i in xrange(0, len(self.widgets), 4):
			output += row % (				
				widget_labels[cont], 
				self.widgets[i].render('inf_%s_%s' % (self.star_name, cont), value[i] if value is not None else None), 
				self.widgets[i+1].render('inf_aplica_%s' % (cont), value[i+1] if value is not None else None), 
				self.widgets[i+2].render('sup_%s_%s' % (self.star_name, cont), value[i+2] if value is not None else None), 
				self.widgets[i+3].render('sup_aplica_%s' % (cont), value[i+3] if value is not None else None) 
			)
			cont=cont+1
		
		return format_html( table % (output,) )


class CustomStarsLogicalWidget(widgets.MultiWidget):
	def __init__(
		self, 
		categorias = 0, 
		star_icon = "fa-star", 
		star_name= "star",
		logical_options = None,
		attrs = None):
		self.categorias = categorias
		self.star_icon = star_icon
		self.star_name = star_name
		self.widgets = [forms.Select(choices = logical_options)] * self.categorias if categorias else [forms.Select()]
		super(CustomStarsLogicalWidget, self).__init__(self.widgets, attrs)
		
	def decompress(self, value):
		if value not in EMPTY_VALUES:
			val = []
			if isinstance(value, str):
				for e in value.split(','):
					val.append( int(e) )					
			elif isinstance(value, dict):
				for k, v in value:
					if isinstance( v, int ):
						val.append(v)
					else:
						raise ValueError
			elif isinstance(value, tuple):
				for e in value:
					if isinstance( e, int ):
						val.append(v)
					else:
						raise ValueError
			else:
				return None
			return val
		else:
			return None

	def render(self, name, value, attrs=None):
		
		_star = '<i class="%s_icon text-red fa %s"></i>'
		table = '<table class="stars_table col-xs-offset-3 col-xs-6"> <tbody> %s </tbody> </table>'
		row = '<tr> <td class="%s">%s</td><td>%s</td></tr>'
		widget_labels = []
		output = ''

		for e in xrange(self.categorias):
			widget_labels.append( 
				_star % (self.star_name, self.star_icon) * (e+1)
			)

		if self.is_localized:
			for widget in self.widgets:
				widget.is_localized = self.is_localized
		
		if not isinstance(value, list):
			value = self.decompress(value)		
	
		for i in xrange(len(self.widgets)):			
			output += row % (
				self.star_name,
				widget_labels[i],
				self.widgets[i].render('%s_%s' % (self.star_name, i), value[i] if value is not None else None) 
			)
		html_parser = HTMLParser.HTMLParser()
		return html_parser.unescape( format_html( table % (output,) ) )
