# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class IPAddress (models.Model) :
	address = netfields.InetAddressField (primary_key=True)
	ptr = models.ForeignKey ('DomainName', null=True, blank=True)
	
	class Meta:
		app_label = 'admtooCore'
		verbose_name_plural = 'IP Addresses'

	def __str__ (self) :
		return str(self.address)

