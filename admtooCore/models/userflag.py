# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

class UserFlag (models.Model) :
	name = models.CharField (max_length=64, null=True, blank=True)

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return str(self.name)
