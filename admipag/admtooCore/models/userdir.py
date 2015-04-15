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

