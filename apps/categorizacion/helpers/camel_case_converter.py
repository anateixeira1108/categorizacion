# -*- encoding: utf-8 

try:
	import re
except Exception, e:
	print "[!] Error al importar dependencias. Imposible continuar!!!"
	raise e


def convert_to_space_case(s=""):
	return  re.sub("([a-z])([A-Z])","\g<1> \g<2>",s)
