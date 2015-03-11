# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')
from silabo.models.ipaddress import IPAddress

class NetworkIf (models.Model) :
	STATIC_ADDRESSING = 0
	DHCP_STATIC_ADDRESSING = 1	
	DHCP_ADDRESSING = 2
	
	ADDRESSING_CHOICES = (
		(STATIC_ADDRESSING, 'statique',),
		(DHCP_STATIC_ADDRESSING, 'dhcp statique',),
		(DHCP_ADDRESSING, 'dhcp',),
	)

	mac_addr = netfields.MACAddressField (primary_key = True)
	name = models.CharField (max_length=32, null=True, blank=True)
	ips = models.ManyToManyField (IPAddress, blank=True, related_name='networkinterfaces', db_index=True)
	addressing_type	= models.IntegerField(choices = ADDRESSING_CHOICES, default=DHCP_ADDRESSING)
	machine = models.ForeignKey ('Machine', null=True, blank=True, related_name='interfaces', db_index=True)

	class Meta:
		app_label = 'silabo'

	def __str__ (self) :
		return str(self.mac_addr)
