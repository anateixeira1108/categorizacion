
from django.template.loader import get_template
from django.utils.six import BytesIO
from django.template import Context
from xhtml2pdf import pisa
from StringIO import StringIO 
import os

#context debe ser de tipo Storage

def generar_pdf(context=None,ruta_template=None,ruta_documento=None,nombre_documento=None):
	try:
		template = get_template(ruta_template)
		html = template.render(Context({'data':context}))
		if not os.path.exists(ruta_documento):
			os.makedirs(ruta_documento)
		documento = os.path.join(
            ruta_documento,
            nombre_documento + '.pdf'
        )
		f = open(documento,"w")
		pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=f, encoding='UTF-8')
		f.close()
		return ruta_documento + nombre_documento + '.pdf'
	except Exception, e:
		raise e