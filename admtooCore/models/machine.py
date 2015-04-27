# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class Machine (models.Model) :
	default_name = models.ForeignKey('DomainName', null=True, blank=True)
	owner = models.ForeignKey ('User', blank=True, null=True, db_index=True)
	comment = models.CharField (max_length=256, blank=True, null=True)

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return str(self.default_name)

	def interfaces (self) :
		from networkif import NetworkIf
		return NetworkIf.objects.filter(machine = self)
