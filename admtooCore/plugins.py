# -*- coding: utf-8 -*-

from django.conf import settings
import sys, os, stat, errno
from types import MethodType
import copy
import imp

class Plugins (object) :
	def __init__ (self) :
		self.plugins = []
		self.find_plugins ()

	def find_plugins (self) :
		base = settings.BASE_DIR	
		# list directories in BASE_DIR
		files = os.listdir(base)
		dirs = []
		for f in files :
			if f[0] == '.' :
				continue
			path = os.path.join (base, f)
			s = os.stat (path)
			if stat.S_ISDIR(s.st_mode) :
				dirs.append (f)
		for p in dirs :
			try :
				f,fname,desc = imp.find_module (p)
			except ImportError as e :
				# can't import, skip...
				continue
			else :
				try :
					m = imp.load_module (p, f, fname, desc)
					if 'admtooPlugin' in dir(m) :
						self.plugins.append (m.admtooPlugin)
				finally:
					if f:
						f.close ()
		for p in self.plugins :
			p ()

	def __dynamic_call (self, *args, **kwargs) :
		print "dynamic call"
		print self
		print args
		print kwargs

	def __getattribute__ (self, name) :
		if not ( name.startswith('__') and name.endswith('__') and len(name)>=5) :
			if name not in dir(self) :
				print "Plugins.__getattribute__ ", name
				print dir(self)
				call = []
				print "looking for plugins"
				for p in self.plugins :
					print p
					print dir(p)
					if name in dir(p) :
						call.append (p)
				print "checking if we have any valid plugins"
				print call
				if len(call) == 0 :
					raise AttributeError
				def closure () :
					called = name
					return self.__dynamic_call(method_name = called)
				return closure
		try:
			return object.__getattribute__ (self, name)
		except :
			return "Value of %s"% name

plugins = Plugins()
