# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class Vlan (models.Model) :
	vlan_id	 = models.IntegerField (primary_key=True) 
	name     = models.CharField (max_length=64, null=False)
	ip_block = netfields.CidrAddressField (unique=True, null=False)
	gateway  = netfields.InetAddressField (unique=True, null=False)

	class Meta:
		app_label = 'AdminToolCore'

	def __str__ (self) :
		return str(self.name)
