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
			try :
				nb_commands = len(commands)
			except Exception as e :
				self.log ('FATAL: error while getting the number of commands to be run')
				self.log (str(e))
				return
			self.log ("found "+str(nb_commands)+" to execute")
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

#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		ul = UpdateLauncher ()
		ul.in_cron=True
		ul.doUpdates ()

