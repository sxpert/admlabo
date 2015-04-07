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
# * a boolean indicating that the command has been passed already

class Command (models.Model) :
	created   = models.DateTimeField (auto_now_add=True)
	modified  = models.DateTimeField (auto_now=True, auto_now_add=True, null=True)
	user      = models.CharField (max_length=64)
	verb      = models.CharField (max_length=64)
	data      = models.TextField () # could be some soft of json field
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

	def execute(self) :
		from ..management.commands import LaunchUpdates as lu
		ul = lu.UpdateLauncher (logger)
		ul.doUpdates()
	
	def subject(self) :
		import json
		d = json.loads(self.data)
		if self.verb=='UpdateUser':
			return d['uid']
		else :
			return ''
