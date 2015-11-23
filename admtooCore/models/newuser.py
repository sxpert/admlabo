# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django.utils import timezone
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
	from userclass import UserClass
	uc = UserClass.objects.get(defval=True)
	return uc.pk
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
	
	OS_LANG_FR = 0
	OS_LANG_EN = 1

	NEWUSER_OS_LANG_CHOICES = (
		( OS_LANG_FR,	'Français'),
		( OS_LANG_EN,	'Anglais'),
	)

	# creation datetime of the record
	created   = models.DateTimeField (auto_now_add=True, default=timezone.now)
	
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
	other_office = models.CharField(max_length=32, null=True, blank=True)

	# dates
	arrival = models.DateField (default=arrival_default)
	departure = models.DateField (null=True, blank=True)

	# building access
	obs_a = models.BooleanField (default=False)
	phy_d = models.BooleanField (default=False)
	osug_d = models.BooleanField (default=False)
	
	# computers
	comp_account = models.BooleanField (default=True)
	os_type = models.IntegerField(choices = NEWUSER_OS_CHOICES, default=OS_LINUX)
	os_lang = models.IntegerField(choices = NEWUSER_OS_LANG_CHOICES, default=OS_LANG_FR)
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

	class Meta:
		app_label = 'admtooCore'
		ordering  = ['last_name']

	def __str__ (self) :
		return self.last_name.encode('utf-8')

	def os_type_choice(self) :
		return self.NEWUSER_OS_CHOICES[self.os_type][1]

	def os_lang_choice(self) :
		return self.NEWUSER_OS_LANG_CHOICES[self.os_lang][1]

	def serialize (self) :
		data = {}

		if self.user is not None :
			user = {}
			user['login'] = self.user.login
			user['uidnumber'] = self.user.uidnumber
			data['user'] = user

		manager = {}
		manager['last_name'] = self.manager.last_name
		manager['first_name'] = self.manager.first_name
		manager['full_name'] = self.manager.full_name()
		manager['mail'] = self.manager.mail
		data['manager'] = manager
		
		data['last_name'] = self.last_name
		data['first_name'] = self.first_name
		data['birthdate'] = None
		logger.error (self.birthdate)
		if self.birthdate is not None :
			data['birthdate'] = self.birthdate.isoformat()
		data['external_email'] = self.external_email
		data['citizenship'] = { 'citizenship': self.citizenship.citizenship }
		
		status = {}
		status['fr'] = self.status.fr
		status['probie'] = self.status.probie
		data['status'] = status

		data['study_level'] = self.study_level
		data['ujf_student'] = self.ujf_student
		data['team'] = { 'name': self.team.name }
		data['office'] = str(self.office)
		data['other_office'] = self.other_office
		
		data['arrival'] = None
		logger.error (self.arrival)
		logger.error (self.departure)
		if self.arrival is not None :
			data['arrival'] = self.arrival.isoformat()
		data['departure'] = None
		if self.departure is not None :
			data['departure'] = self.departure.isoformat()
	
		data['obs_a'] = self.obs_a
		data['phy_d'] = self.phy_d
		data['osug_d'] = self.osug_d

		data['comp_account'] = self.comp_account
		data['os_type'] = self.os_type
		data['os_type_choice'] = self.os_type_choice()
		data['os_lang_choice'] = self.os_lang_choice()
		data['specific_os'] = self.specific_os
		data['comp_purchase'] = self.comp_purchase		

		data['ir_lab'] = self.ir_lab
		data['workshop'] = self.workshop
		data['chem_lab'] = self.chem_lab
	
		data['risky_activity'] = self.risky_activity

		data['comments'] = self.comments

		return data
	
	def send_arrival_mail (self, request_user=None) :
		maildata = {}	
		nu = NewUser.objects.get (pk=self.pk)
		maildata['newuser'] = nu.serialize()
		causes = ['NewArrival']
		if not self.citizenship.eu_member :
			causes.append ('NewArrivalNotEUMember')
		
		# post sendmail command
		import command, json
		c = command.Command ()
		if request_user is None :
			c.user = "(Unknown)"
		else :
			c.user = str(request_user)
		data = { 'mailconditions': causes, 'maildata': maildata }
		c.verb = 'SendMail'
		c.data = json.dumps (data)
		c.save ()

	def send_match_mail (self, request_user=None) :
		maildata = {}
		try :
			nu = NewUser.objects.get (pk=self.pk)
		except NewUser.DoesNotExist as e :
			logger.error ("FATAL : unable to find user ??? "+self.first_name+" "+self.last_name)
			
			return
		maildata['newuser'] = nu.serialize()
		causes = ['UserMatch']
		
		import command, json
		c = command.Command ()
		if request_user is None :
			c.user = "(Unknown)"
		else :
			c.user = str(request_user)
		data = { 'mailconditions': causes, 'maildata': maildata }
		c.verb = 'SendMail'
		c.data = json.dumps(data)
		c.save()
