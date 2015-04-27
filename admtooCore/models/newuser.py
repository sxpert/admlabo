# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django.db import models
import logging
logger=logging.getLogger('django')
from django.conf import settings

def birthdate_default () :
	years = 18
	d = date.today()
	try :
		nd = d.replace (year = d.year + years)
	except ValueError as e:	
		nd = d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))	
	return nd

def arrival_default () :
	return date.today()

def citizenship_default () :
	return settings.DEFAULT_COUNTRY	

def status_default () :
	return 9
#
# new users
#

class NewUser (models.Model) :
	OS_OTHER = 0
	OS_LINUX = 1
	OS_MAC = 2
	OS_WINDOWS = 3

	NEWUSER_OS_CHOICES = (
		( OS_OTHER,   'Autre'),
		( OS_LINUX,   'Linux'),
		( OS_MAC,     'Mac OS'),
		( OS_WINDOWS, 'Windows (7)'),
	)
		
	# manager
	manager = models.ForeignKey ('User', null=True, blank=True, related_name='Manager')
	user = models.ForeignKey ('User', null=True, blank=True, related_name='User')
	# basic information
	last_name = models.CharField(max_length=128, null=True, blank=True)
	first_name = models.CharField(max_length=128, null=True, blank=True)
	birthdate = models.DateField(default=birthdate_default)
	external_email = models.EmailField(max_length=254, null=True, blank=True)
	citizenship = models.ForeignKey ('Country', default=citizenship_default)
	status = models.ForeignKey ('UserClass', default=status_default)
	study_level = models.CharField(max_length=128, null=True, blank=True)
	ujf_student = models.BooleanField(default=False)
	team = models.ForeignKey('Group', null=True, blank=True)
	office = models.ForeignKey('Office', null=True, blank=True)
	other_office = models.CharField(max_length=128, null=True, blank=True)
	# dates
	arrival = models.DateField (default=arrival_default)
	departure = models.DateField (null=True, blank=True)
	# computers
	comp_account = models.BooleanField (default=True)
	os_type = models.IntegerField(choices = NEWUSER_OS_CHOICES, default=OS_LINUX)
	specific_os = models.CharField (max_length=128, null=True, blank=True)
	comp_purchase = models.BooleanField (default=False)
	# access
	ir_lab = models.BooleanField(default=False)
	workshop = models.BooleanField(default=False)
	chem_lab = models.BooleanField(default=False)
	# 
	risky_activity = models.BooleanField(default=False)
	#
	comments = models.TextField (null=True, blank=True)

	# information services
	os_type  = models.IntegerField(choices = NEWUSER_OS_CHOICES, default=OS_LINUX)

	class Meta:
		app_label = 'admtooCore'
		ordering  = ['last_name']

	def __str__ (self) :
		return self.last_name.encode('utf-8')
		
