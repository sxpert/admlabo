#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, json

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from ...plugins import plugins

class UpdateLauncher (object) :
	STATE_SUCCESS = 0
	STATE_FAIL    = 1
	STATE_SKIP    = 2	

	def __init__ (self, logger = None) :
		self.in_cron = False
		self.logger = logger

	def log (self, message) :
		if self.logger is not None :
			self.logger.error (message)
		else :
			print message	

	#==============================================================================================
	#
	# check if one of the plugins failed
	# 

	def _CheckFail (self, ret, command) :
		# check if one or more failed 
		fails = []
		for k in  ret.keys() :
			if ret[k] != True :
				fails.append(k)
		if len(fails) >0 :
			self.log ('ERROR while executing')
			self.log (str(command)) 
			for p in fails :
				self.log ('plugin '+str(p)+' failed to execute')
			return self.STATE_FAIL
		return self.STATE_SUCCESS
	
	# launches updates that are not done yet in order.
	# stops at the first problematic update (to allow debugging,
	# and to be sure that everything is working properly)
	#
	# NOTE :
	# this uses a transaction. if anything goes wrong, the 
	# transaction is reversed
	def doUpdates (self) :
		from ...models.command import Command	
		self.log ("do updates")
		with transaction.atomic() :
			try :
				commands = Command.objects.select_for_update(nowait=True).filter(done=False).order_by('created')
			except DatabaseError as e:
				self.log ('FATAL: unable to lock rows, exiting')
				self.log (str(e))
				return
			self.log ("found "+str(len(commands))+" to execute")
			for c in commands :
				try :					
					func = getattr (plugins, c.verb) 
				except AttributeError :				
					self.log ('FATAL: '+c.verb+' not found')
					self.log ('UNABLE TO FIND COMMAND')
					# stop right there !!
					return
				# we should have a plugins closure here
				self.log ('command '+c.verb+' was found in plugins :')
				self.log (func)
				# if the command requires being run while in crontab,
				# and we're not running from cron, skip it
				if c.in_cron and (not self.in_cron) :
					res = self.STATE_SKIP
				else :
					res = self._CheckFail (func(c, logger=self.logger), c)
				if res == self.STATE_SUCCESS :
					#self.log ('SUCCESS - marking command done')
					c.done = True
					c.save ()
				elif res == self.STATE_FAIL :
					self.log ('FATAL: error while running '+c.verb)
					# something bad happened... stop right there !
					return
				elif res == self.STATE_SKIP :
					self.log ('SKIPPING COMMAND '+str(c.desc()))

	#==============================================================================================
	# 
	# Creating directories for users
	#
	
	def verbCreateUserDir (self, command) :
		# if we're not in cron
		if command.in_cron and (not self.in_cron) :
			return self.STATE_SKIP

		c = json.loads(command.data)
		ck = c.keys()
		if 'machine' not in ck :
			self.log ('missing \'machine\' name')
			return self.STATE_FAIL
		machine = c['machine']

		# in debug mode, force the storage server from the settings
		from django.conf import settings
		if settings.DEBUG :
			try :
				settings.STORAGE_SERVER 
			except NameError as e :
				# skip...
				self.log ('FATAL: we are in DEBUG mode and settings.STORAGE_SERVER is not defined')
				return self.STATE_FAIL
			else :
				self.log ('DEBUG MODE :\ndirectories should normally be created on \''+machine+
					'\'\nwill be created on \''+settings.STORAGE_SERVER+'\' instead')
				machine = settings.STORAGE_SERVER

		if ('basedir' not in ck) and ('uid' not in ck) :
			return self.STATE_FAIL
		dirname = c['basedir']+'/'+c['uid']
		if 'uidNumber' not in ck :
			return self.STATE_FAIL
		try :
			uid = int(c['uidNumber'])
		except ValueError as e :
			return self.STATE_FAIL
		if 'gidNumber' not in ck :
			self.log ('missing \'gidNumber\' field')
			return self.STATE_FAIL
		try :
			gid = int(c['gidNumber'])
		except ValueError as e :
			return self.STATE_FAIL
		if 'modes' not in ck :
			return self.STATE_FAIL
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
			self.log ('success')
			return self.STATE_SUCCESS
		self.log ('FAIL')
		return self.STATE_FAIL
	
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		ul = UpdateLauncher ()
		ul.in_cron=True
		ul.doUpdates ()

