# -*- encoding: utf-8 -*-


def dprint(*args, **kwargs):
	try:
		import datetime		
		print "[DEBUG PRINTING]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		print "Current date: %s" % (datetime.datetime.now().strftime('%d-%m-%Y'))
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		count = 0
		for v in args:
			count += 1
			print "(%d) [args value] => %s" % (count,str(v))	
		for k,v in kwargs.items():
			count += 1
			print "(%d) [%s] => %s" % (count, k, str(v))
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[END]"
	except Exception, e:
		raise e
