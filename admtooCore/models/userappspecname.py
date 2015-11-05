# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

class UserAppSpecName (models.Model) :
	ref = models.CharField (max_length=64, null=False, blank=False, db_index=True, unique=True)
	name = models.CharField (max_length=64, null=True, blank=True)
	label = models.CharField (max_length=255, null=True, blank=True)

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return str(self.name)
