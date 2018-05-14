#from apps.categorizacion.models import *
from apps.categorizacion.helpers.debug_printer import dprint
import shutil
import os

#
################## SCRIPTS #####################
#
def copiar_antes_firma(src_file, dest_dir, documento):
	#se copia el archivo al directorio destino con el nombre del documento cambiado
	try:
		dprint(src_file=src_file)
		dprint(dest_dir=dest_dir)
		shutil.copy(src_file,dest_dir)
		nomb = cambio_nombre_doc(documento)
		aux = dest_dir+'/'+str(documento.nombre)+'.'+str(documento.extension)
		aux1 = dest_dir+'/'+nomb+'.'+str(documento.extension)
		cond = cambio_nombre_file(aux,aux1)
		if cond:
			return nomb
		else:
			dprint("conderror")
			return None
	except IOError:
		dprint("ioerror")
		return None

def eliminar_antes_firma(src_dir,documento):
	try:
		nomb = cambio_nombre_doc(documento)
		aux = src_dir+'/'+nomb+'.'+str(documento.extension)
		dprint(aux=aux)
		os.remove(aux)
		return True
	except OSError:
		return False

def cambio_nombre_file(src_file,dest_file):
	try:
		os.rename(src_file,dest_file)
		return True
	except OSError:
		return False

def mover_file(src_file,dest_dir):
	try:
		shutil.move(src_file,dest_dir)
		return True
	except IOError:
		return False

def eliminar_file(src_file):
	try:
		os.remove(src_file)
		return True
	except OSError:
		return False	

def copiar_file(src_file, dest_dir):
	#se copia el archivo al directorio destino con el nombre del documento cambiado
	try:
		shutil.copy(src_file,dest_dir)
		return True
	except IOError:
		return False
#	
################## FUNCIONES ########################
#


def cambio_nombre_doc(documento):
	#Cambia el nombre colocandole el hash al final al documento a nivel de django
	rut_doc = str(documento.ruta_documento)
	rut_doc = rut_doc.replace('/documents/','')
	rut_doc = rut_doc.split('/')
	rut_doc.pop()
	rut_doc.pop()
	rut_doc = ''.join(rut_doc)
	return str(documento.nombre)+'_'+rut_doc


def obtener_hash_doc(documento):
	doc = documento.split('.')
	doc.pop()
	doc = ''.join(doc)
	doc = doc.split('_')
	doc = doc.pop()
	return doc
