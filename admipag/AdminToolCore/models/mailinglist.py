# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')
from AdminToolCore.models.group import Group

class MailingList (models.Model) :
	ml_id       = models.CharField(max_length=64, primary_key=True)
	name        = models.CharField(max_length=128, unique=True)
	description = models.CharField(max_length=256)
	parent      = models.ForeignKey('self', null=True, blank=True)
	group       = models.ForeignKey(Group, null=True, blank=True)

	class Meta:
		app_label = 'AdminToolCore'

	def __str__ (self) :
		return self.name
