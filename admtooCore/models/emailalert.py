# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

#
# email alerts that are sent in various occasions
#

class EmailAlert (models.Model) :
	cause = models.CharField(max_length=32, default='Unknown')
	email = models.CharField(max_length=254, default='user@example.com')

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return self.cause
		
