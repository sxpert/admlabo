# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

#
# email alerts that are sent in various occasions
#

class EmailAlertMessage (models.Model) :
	cause   = models.CharField(max_length=32, default='Unknown')
	subject = models.TextField(default='')
	message = models.TextField(default='') 

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return self.cause
		
