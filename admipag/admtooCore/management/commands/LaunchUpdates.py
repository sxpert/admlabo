#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

import sys, json
from admtooLib import ldaposug as lo


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

	# launches updates that are not done yet in order.
	# stops at the first problematic update (to allow debugging,
	# and to be sure that everything is working properly)
	def doUpdates (self) :
		from ...models.command import Command	
		#self.log ("do updates")
		commands = Command.objects.filter(done=False).order_by('created')
		for c in commands :
			#self.log (str(c.created)+' '+c.verb)
			v = 'verb'+c.verb
			try :
				func = getattr (self, v)
			except AttributeError :
				self.log ('FATAL: '+c.verb+' not found')
				return
			else :
				res = func(c)
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

	#----------------------------------------------------------------------------------------------
	#
	# update scripts
	#
	# these update scripts are designed so that they leave things in a known state.
	# also, they are designed so that they don't change anything if nothing needs be changed
	# this allows restarting an update order at anytime.
	#

	#==============================================================================================
	# 
	# Updating groups 
	#

	#
	# actual update of group in ldap
	#
	def _UpdateGroup_LDAP (self, command) :
		l = lo.LdapOsug (self.logger)
		c = json.loads(command.data)
		ck = c.keys()
		cn = None
		if 'cn' in ck :
			cn = c['cn']
		gidNumber = None		
		if 'gidNumber' in ck :
			gidNumber = c['gidNumber']
		description = None
		if 'description' in ck :
			description = c['description']
		memberUid = None
		if 'memberUid' in ck :
			memberUid = c['memberUid']

		g = l.group_check_exists (cn, gidNumber)
		if g is None :
			# group not found. add the group as new
			return l.group_create (cn, gidNumber, description, memberUid)
		else :
			# group has been modified
			oldcn, oldgidnumber = g
			if (cn is not None) and (oldcn != cn) :
				l.group_rename (oldcn, cn)
			return l.group_update (cn, gidNumber, description, memberUid)

	#
	# this update when a group was modified
	# for now, only changes in the ldap
	# would go around in other things later if needed
	def verbUpdateGroup (self, command) :
		if self._UpdateGroup_LDAP (command) :
			return self.STATE_SUCCESS
		return self.STATE_FAIL
	
	#==============================================================================================
	# 
	# Updating users
	#

	#
	# actual update of user in ldap
	#
	def _UpdateUser_LDAP (self, command) :
		l = lo.LdapOsug (self.logger)
		c = json.loads (command.data)
		#self.log (str(c))
		ck = c.keys()
		uid = None
		if 'uid' in ck :
			uid = c['uid']
		else :
			self.log ('FATAL: _UpdateUser_LDAP unable to find uid in UpdateUser command data')
			return False
		d = {}
		if 'loginShell' in ck :
			d['loginShell'] = c['loginShell']
		if 'gecos' in ck :
			d['gecos'] = c['gecos']
#		if 'manager' in ck :
#			d['manager'] = l.user_dn(c['manager'])
		# room and telephone
#		if 'roomNumber' in ck :
#			d['roomNumber'] = c['roomNumber']
	
		try :
			res = l.user_update (uid, d)
		except lo.UserGone as e :
			print "USER GONE"
			res = True
		return res

	#
	# this updates when a user was modified
	def verbUpdateUser (self, command) :
		if self._UpdateUser_LDAP (command) :
			return self.STATE_SUCCESS
		return self.STATE_FAIL
	
	#==============================================================================================
	# 
	# Creating directories for users
	#
	
	def verbCreateUserDir (self, command) :
		# if we're not in cron
		if command.in_cron and (not self.in_cron) :
			return self.STATE_SKIP

		from admtooLib import AnsibleFunctions as af
		c = json.loads(command.data)
		ck = c.keys()
		if 'machine' not in ck :
			self.log ('missing \'machine\' name')
			return self.STATE_FAIL
		machine = c['machine']
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

