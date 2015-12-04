# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

class UserClass (models.Model) :
	ref       = models.CharField (max_length=64, null=False)
	defval    = models.BooleanField (default=False)
	fr        = models.CharField (max_length=128, null=True, blank=True)
	en        = models.CharField (max_length=128, null=True, blank=True)
	probie    = models.BooleanField (default=False)
	group     = models.ForeignKey ('Group', null=True, blank=True)
	directory = models.BooleanField (default=True)
	active    = models.BooleanField (default=True)

	class Meta:
		app_label = 'admtooCore'
		ordering  = ['ref']
		verbose_name_plural = 'UserClasses'

	def __str__ (self) :
		return str(self.ref)
