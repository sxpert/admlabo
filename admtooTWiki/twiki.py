# -*- coding: utf-8 -*-

class TWiki (object) :
	
	def __init__ (self) :
		print "initializing TWiki plugin" 
		self.a = "string a"
	
	def runcommand (self, *args, **kwargs) :
		_, verb, data = args
		print verb
		print data
		return "twiki return"
	
