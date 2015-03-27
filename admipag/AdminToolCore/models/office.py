# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

class Office (models.Model) :
	ref = models.CharField (max_length=16, null=False)
	desc = models.CharField (max_length=16, null=True, blank=True)

	class Meta:
		app_label = 'AdminToolCore'
		ordering  = ['ref']

	def __str__ (self) :
		if self.desc is not None :
			return self.desc
		return self.ref
