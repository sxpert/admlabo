#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

import sys, json
sys.path.append ('/srv/progs/ipag')
import ldaposug as lo


class UpdateLauncher (object) :
	def __init__ (self, logger = None) :
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
		self.log ("do updates")
		commands = Command.objects.filter(done=False).order_by('created')
		for c in commands :
			self.log (str(c.created)+' '+c.verb)
			v = 'verb'+c.verb
			try :
				func = getattr (self, v)
			except AttributeError :
				self.log ('FATAL: '+c.verb+' not found')
				return
			else :
				if (func (c)) :
					self.log ('SUCCESS - marking command done')
					c.done = True
					c.save ()

	#----------------------------------------------------------------------------------------------
	#
	# update scripts
	#
	# these update scripts are designed so that they leave things in a known state.
	# also, they are designed so that they don't change anything if nothing needs be changed
	# this allows restarting an update order at anytime.
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
		return self._UpdateGroup_LDAP (command)
	
	#
	# actual update of user in ldap
	#
	def _UpdateUser_LDAP (self, command) :
		l = lo.LdapOsug (self.logger)
		c = json.loads (command.data)
		self.log (str(c))
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
		if 'manager' in ck :
			d['manager'] = l.user_dn(c['manager'])
		return l.user_update (uid, d)

	#
	# this updates when a user was modified
	def verbUpdateUser (self, command) :
		self.log ('updating user')
		self.log (command.data)
		return self._UpdateUser_LDAP (command)
	
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		ul = UpdateLauncher ()
		ul.doUpdates ()
