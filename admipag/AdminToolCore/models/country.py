# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

#
# list of countries
#

class Country (models.Model) :
	iso2 = models.CharField(max_length=2, primary_key=True)
	name = models.CharField(max_length=128)
	citizenship = models.CharField(max_length=128)
	eu_member = models.BooleanField (default = False)

	class Meta:
		app_label = 'AdminToolCore'
		ordering  = ['name']
		verbose_name_plural = 'Countries'

	def __str__ (self) :
		return self.name.encode('utf-8')
		
