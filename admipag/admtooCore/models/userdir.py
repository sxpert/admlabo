# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

#
# the userdir data defines what directories should be present on
# which servers for the users
#

class UserDir (models.Model) :
	machine = models.ForeignKey ('Machine',     null=True, blank=True)
	label   = models.CharField  (max_length=32, null=True, blank=True)
	basedir = models.CharField  (max_length=128,null=True, blank=True)
	modes   = models.CharField  (max_length=4,  null=True, blank=True)

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return str(self.machine)+' '+str(self.basedir)+' ('+str(self.modes)+')'

	def generate (self, user, request_user) :
		import command, json
		from django.conf import settings
		from group import Group
		data = {}
		data['machine'] = self.machine.default_name.fqdn
		data['basedir'] = self.basedir
		data['modes'] = self.modes
		data['uid'] = user.login
		if user.group is None : 
			# should not happen
			data['gidNumber'] = Group.objects.get(name=settings.DEFAULT_USER_GROUP).gidnumber
		else :
			data['gidNumber'] = user.group.gidnumber # default gid
		data['uidNumber'] = user.uidnumber
		c = command.Command ()
		c.user = request_user
		c.verb = "CreateUserDir"
		logger.error (str(data))
		c.data = json.dumps(data)
		# the directories should be created by the cron job, 
		# as it takes forever and requires root access
		c.in_cron = True
		c.save ()

def generateDirs (user, request_user=None) :
	for d in UserDir.objects.all () :
		d.generate (user, request_user)

