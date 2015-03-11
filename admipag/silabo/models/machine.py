# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')
from silabo.models.domainname import DomainName
from silabo.models.networkif import NetworkIf

class Machine (models.Model) :
	default_name = models.ForeignKey(DomainName, null=True, blank=True)
	owner = models.ForeignKey ('User', blank=True, null=True, db_index=True)
	comment = models.CharField (max_length=256, blank=True, null=True)

	class Meta:
		app_label = 'silabo'

	def __str__ (self) :
		return str(self.default_name)

	def interfaces (self) :
		return NetworkIf.objects.filter(machine = self)
