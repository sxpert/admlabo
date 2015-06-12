# -*- coding: utf-8 -*-

import sys, json

class Core_Storage (object) :
	def __init__ (self) :
		self._logger = None

	def _log (self, message) :
		if self._logger is not None :
			self._logger.error (message)
		else :	
			sys.stdout.write (str(message)+u'\n')
			sys.stdout.flush ()

	def CreateUserDir (self, *args, **kwargs) :
		_, command = args
		if 'logger' in kwargs.keys() :
			logger = kwargs['logger']
			if logger is not None :
				self._logger = logger

		c = json.loads(command.data)
		ck = c.keys()
		if 'machine' not in ck :
			self._log ('missing \'machine\' name')
			return False
		machine = c['machine']

		# in debug mode, force the storage server from the settings
		from django.conf import settings
		if settings.DEBUG :
			try :
				settings.STORAGE_SERVER 
			except NameError as e :
				# skip...
				self._log ('FATAL: we are in DEBUG mode and settings.STORAGE_SERVER is not defined')
				return False
			else :
				self._log ('DEBUG MODE :\ndirectories should normally be created on \''+machine+
					'\'\nwill be created on \''+settings.STORAGE_SERVER+'\' instead')
				machine = settings.STORAGE_SERVER

		if ('basedir' not in ck) and ('uid' not in ck) :
			return False
		dirname = c['basedir']+'/'+c['uid']
		if 'uidNumber' not in ck :
			return False
		try :
			uid = int(c['uidNumber'])
		except ValueError as e :
			return False
		if 'gidNumber' not in ck :
			self._log ('missing \'gidNumber\' field')
			return False
		try :
			gid = int(c['gidNumber'])
		except ValueError as e :
			return False
		if 'modes' not in ck :
			return False
		modes = c['modes']
		if 'files' not in ck :
			files = None
		else :
			files = c['files']

		# NOTE: this is ok when the application server is running as root.
		# the case when it's not needs to be analyzed
		# also, this takes a long time, should be running in a separate
		# process
		from admtooLib import AdminFunctions as af
		created_ok = af.createDirectory (machine, dirname, uid, gid, modes, files)
		if created_ok :
			self._log ('success')
			return True
		self._log ('FAIL')
		return False

