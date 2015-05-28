# -*- coding: utf-8 -*-

from django.conf import settings
import sys, os, stat, errno
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
						self.plugins.append (m)
				finally:
					if f:
						f.close ()
		for p in self.plugins :
			p.admtooPlugin ()
				

plugins = Plugins()
