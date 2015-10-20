# -*- coding: utf-8 -*-

from django.db import models
import logging
logger = logging.getLogger('django')

class UserGroupHistory (models.Model) :
	ACTION_ADD = 0
	ACTION_DEL = 1
	ACTION_CHOICES = (
		( ACTION_ADD, 'ADD' ),
		( ACTION_DEL, 'DEL' ),
	)

	created    = models.DateTimeField (auto_now_add=True)
	creator    = models.ForeignKey ('User', null=True, blank=True, related_name = 'ugh_creator')
	user       = models.ForeignKey ('User', null=False, blank=False, related_name = 'ugh_subject')
	action     = models.IntegerField (choices = ACTION_CHOICES, null=False, blank=False)
	# json string with list of groups
	data       = models.TextField (default='', blank=True)

	class Meta :
		get_latest_by = 'created'
		ordering = ['-created']
		app_label = 'admtooCore'
