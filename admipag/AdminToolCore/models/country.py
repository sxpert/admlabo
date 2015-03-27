# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

#
# the command class implements a list of commands that needs to be launched
# This implements the interfacing between the core, and various systems
#

# a command is composed of
# * a timestamp is included to execute them in order
# * a verb, describing what has to be done
# * a data block in json, that includes the relevant data
# furthermore, 
# * user information, so as to blame people ;)
# * a boolean indicating that the command has been passed already

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
		
