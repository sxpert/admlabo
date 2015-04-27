# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class DomainName (models.Model) :
	fqdn = models.CharField (max_length=255, unique=True, null=False)
	ips  = models.ManyToManyField ('IPAddress', blank=True, related_name='domainnames')

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return str(self.fqdn)

