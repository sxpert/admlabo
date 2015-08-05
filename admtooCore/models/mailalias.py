# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

class MailAlias (models.Model) :
	alias = models.CharField (max_length=254, unique=True)
	user  = models.ForeignKey ('User', null=True, blank=True, related_name='UserAliases')

	class Meta:
		verbose_name_plural = "MailAliases"
		app_label = 'admtooCore'

	def __str__ (self) :
		return self.alias

