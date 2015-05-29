# -*- coding: utf-8 -*-

class Test (object) :
	
	def __init__ (self) :
		print "initializing Test plugin" 
	
	def testcommand (self, *args, **kwargs) :
		_, verb, data = args
		print verb
		print data
		return "test success"
	
