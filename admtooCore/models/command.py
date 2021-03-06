# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

#
# the command class implements a list of commands that needs to be launched
# This implements the interfacing between the core, and various systems
#

# a command is composed of
# * a timestamp is included to execute them in order
# * a verb, describing what has to be done
# * a data block in json, that includes the relevant data
# furthermore, 
# * user information, so as to blame people ;)
# * a boolean indicating that the command is intended to run within a cron
#   process, as root
# * a boolean indicating that the command has been passed already

class Command (models.Model) :
	created   = models.DateTimeField (auto_now_add=True)
	modified  = models.DateTimeField (auto_now_add=True, null=True)
	user      = models.CharField (max_length=64)
	verb      = models.CharField (max_length=64)
	data      = models.TextField (default='', blank=True) # could be some soft of json field
	in_cron   = models.BooleanField (default=False)
	done      = models.BooleanField (default=False)

	class Meta:
		get_latest_by = 'created'
		ordering  = ['-created']
		app_label = 'admtooCore'

	def __str__ (self) :
		return str(self.created)+' '+self.verb

	def save(self) :
		# attempt to execute command
		super(Command, self).save()
		if not self.done :
			self.execute ()

	# post a new command, don't try to execute more commands, as
	# we are already busy executing commands
	def post (self) :
		super(Command, self).save()

	def execute(self) :
		from ..management.commands import LaunchUpdates as lu
		ul = lu.UpdateLauncher (logger)
		ul.doUpdates()
	
	def subject(self) :
		import json
		try :
			d = json.loads(self.data)
		except ValueError as e :
			# nothing to decode
			return ''
		# user
		if self.verb=='UpdateUser':
			return d['uid']
		elif self.verb == 'UpdatePhoto': 
			return d['uid']
		# groups
		elif self.verb=='UpdateGroup':
			return d['cn']
		elif self.verb=='DestroyGroup':
			if d is not None:
				if (d['cn'] is not None) and (len(d['cn'])>0) :
					return d['cn']
				else :
					return str(d['gidNumber'])
			else:
				return "Group info is None (should not happen)"
		# mail alias
		elif self.verb=='UpdateMailAlias':
			return d['alias']
		# user dirs
		elif self.verb=='CreateUserDir' :
			return d['basedir']+'/'+d['uid']
		elif self.verb=='TWikiUpdateGroup' :
			if 'appSpecName' in d.keys() :
				sp = d['appSpecName']
				if sp is None :
					return "appSpecName undefined"
				if 'twiki' in sp.keys() :
					return sp['twiki']
				else :
					return "can't find twiki group name"
			else:
				return "no appSpecName variable"
		else :
			return ''

	def desc (self) :
		return self.verb+' '+self.subject()

