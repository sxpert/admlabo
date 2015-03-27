# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

#
# new users
#

class NewUser (models.Model) :
	OS_OTHER = 0
	OS_LINUX = 1
	OS_MAC = 2
	OS_WINDOWS = 3

	NEWUSER_OS_CHOICES = (
		( OS_OTHER,   'Autre'),
		( OS_LINUX,   'Linux'),
		( OS_MAC,     'Mac OS'),
		( OS_WINDOWS, 'Windows (7)'),
	)

	# basic information
	last_name = models.CharField(max_length=128, null=True, blank=True)

	# information services
	os_type  = models.IntegerField(choices = NEWUSER_OS_CHOICES, default=OS_LINUX)

	class Meta:
		app_label = 'AdminToolCore'
		ordering  = ['last_name']

	def __str__ (self) :
		return self.last_name
		
