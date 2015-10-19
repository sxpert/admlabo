# -*- coding: utf-8 -*-

from django.conf import settings
import sys, os, stat, errno
from types import MethodType
import inspect
import imp

class Plugins (object) :
	def __init__ (self) :
		self.plugins = []
		self.find_plugins ()
	
	def _log (self, message) :
		sys.stdout.write (str(message)+'\n')
		sys.stdout.flush ()

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
						plugin = m.admtooPlugin
						# check if we have an actual object class
						if type(plugin) is type :
							# instanciate object		
							self.plugins.append (plugin())
						else:	
							self._log ('we should have had a type here')
					elif 'admtooPlugins' in dir(m) :
						pluginlist = m.admtooPlugins
						for plugin in pluginlist :
							if type(plugin) is type :
								self.plugins.append (plugin())
				finally:
					if f:
						f.close ()

	def __dynamic_call (self, *args, **kwargs) :
		plugins = kwargs['__dynamic_call_plugins']
		method = kwargs['__dynamic_call_method_name']
		del kwargs['__dynamic_call_plugins']
		del kwargs['__dynamic_call_method_name']
		ret = {}
		for p in plugins :
			m = p.__getattribute__(method)
			ret[p.__class__.__name__] =  m (p, *args, **kwargs)
		return ret

	def __getattribute__ (self, name) :
		if not ((name.startswith('__') and name.endswith('__') and len(name)>=5)
				or (name.startswith('_') and len(name)>=2)) :
			if name not in dir(self) :
				plugins = []
				for p in self.plugins :
					# is it the name of a plugin ?
					pluginclass = p.__class__.__name__
					if name == pluginclass :
						return p
					# is the name within the plugin ?
					members = dir(p)
					# remove all members starting with _
					m = []
					for a in members :
						if not a.startswith('_') :	
							m.append (a)
				
					members = m
					#print pluginclass+" filtered members :\n"+str(members)
					# 
					if name in members :
						plugins.append (p)
						
				if len(plugins) == 0 :
					raise AttributeError ("None of the plugins have methods or attributes called '"+name+"'")
				# check if all are functions
				variables = {}
				method = True
				for p in plugins :
					# no, maybe a variable name within one of the plugins ?
					v = p.__getattribute__(name)
					variables[p.__class__.__name__] = v
					if not inspect.ismethod(v) :
						method = False
				if method :
					def closure (*args, **kwargs) :
						kwargs['__dynamic_call_method_name'] = name
						kwargs['__dynamic_call_plugins'] = plugins
						return self.__dynamic_call(*args, **kwargs)
					return closure
				else :
					# suppose they're all variables
					return variables
		try:
			return object.__getattribute__ (self, name)
		except :
			return "Value of %s"% name

plugins = Plugins()
