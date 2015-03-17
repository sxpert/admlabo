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

	def doUpdates (self) :
		from AdminToolCore.models.command import Command	
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

	def _UpdateGroup_LDAP (self, command) :
		l = lo.LdapOsug (self.logger)
		c = json.loads(command.data)
		self.log (str(c))
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
		self.log (str(g))
		if g is None :
			# group not found. add the group as new
			return l.group_create (cn, gidNumber, description, memberUid)
		else :
			# group has been modified
			oldcn, oldgidnumber = g
			if (cn is not None) and (oldcn != cn) :
				l.group_rename (oldcn, cn)
			return l.group_update (cn, gidNumber, description, memberUid)

	def verbUpdateGroup (self, command) :
		self.log ('updating group')
		self.log (command.data)
		return self._UpdateGroup_LDAP (command)
		

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		ul = UpdateLauncher ()
		ul.doUpdates ()

