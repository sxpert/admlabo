# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.db.models import Max
from django.conf import settings
import json
import netfields
import logging
logger=logging.getLogger('django')

class Group (models.Model) :
	NORMAL_GROUP = 0
	TEAM_GROUP = 1
	SERVICE_GROUP = 2
	STATUS_GROUP = 3

	GROUP_TYPES_CHOICES = (
		( NORMAL_GROUP,  ''),
		( TEAM_GROUP,    'Groupe d\'équipe'),
		( SERVICE_GROUP, 'Groupe de service'),
		( STATUS_GROUP,  'Groupe de statut'),
	)

	gidnumber   = models.IntegerField(primary_key=True)
	name        = models.CharField(max_length=64, unique=True) 
	group_type	= models.IntegerField(choices = GROUP_TYPES_CHOICES, default=NORMAL_GROUP)
	parent      = models.ForeignKey('self', null=True, blank=True)
	description = models.CharField(max_length=256, null=True, blank=True)
	appspecname = models.TextField(default='') 

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return self.name
	
	# 
	# finds an available gidnumber within the permitted range
	@transaction.atomic
	def create_new (self) :
		logger.error ('identifying new group id')
		last_group = Group.objects.all().aggregate(Max('gidnumber'))['gidnumber__max']
		logger.error (type(last_group))
		logger.error ('current max gidnumber '+str(last_group))	
		new_gidnumber = last_group+1
		# check if the new number is within the range
		try :
			ranges = settings.GIDNUMBER_RANGES
		except AttributeError as e :
			# ranges are not defined, assume all are authorized
			return True
		logger.error (type(ranges))
		if type(ranges) is not list :
			logger.error ('ERROR: settings.GIDNUMBER_RANGES should be an array of 2 values arrays')
			# consider things ok though
			return True
		# if no ranges defined, consider everything ok
		if len(ranges) <= 0:
			return True		
		ok = False
		for r in ranges :
			if type(r) is not list :
				logger.error ('ERROR: settings.GIDNUMBER_RANGES should be an array of 2 values arrays')
				# skip this element
				continue
			d, u = r
			if (d <= new_gidnumber) and (new_gidnumber <= u) :
				ok = True
		if ok :
			logger.error ('number is in range')	
		else :
			logger.error ('ERROR: new number is invalid')
		self.gidnumber = new_gidnumber
		# don't involve the external update mechanisms just yet, as nothing is filled in
		super (Group, self).save ()
		return ok

	# 
	# removes a group
	#
	def destroy (self, user=None) :
		# get members list
		g = self.prepare_group_data()
		logger.error ("destroying group : "+str(g['members']))

		import command, json
		c = command.Command ()
		if user is None :
			c.user = "(Unknown)"
		else :
			c.user = user
		c.verb = 'DestroyGroup'
		c.data = json.dumps(g)
		c.save ()
		# remove group from database
		# TODO: keep in history table ?
		self.delete()
	

	#
	# return a group identifier for the group list
	# either the name, if not empty, or the gidnumber
	#
	def identifier (self) :
		#logger.error (type(self.name))
		if (self.name is not None) and (type(self.name) in (str, unicode,)) and (len(self.name)>0) :
			return self.name
		return self.gidnumber

	def prepare_group_data (self) :
		members = self.member_logins()
		g = {}
		g['cn']          = self.name
		g['gidNumber']   = self.gidnumber
		g['description'] = self.description
		g['members']   = members
		try :
			g['appSpecName'] = json.loads(self.appspecname)
		except ValueError as e :
			g['appSpecName'] = None
		return g
	
	# update the group object to the ldap server
	def _update_ldap (self, user=None) :
		# get members list
		g = self.prepare_group_data()
		logger.error ("saving group to ldap, members list : "+str(g['members']))

		import command, json
		c = command.Command ()
		if user is None :
			c.user = "(Unknown)"
		else :
			c.user = user
		c.verb = 'UpdateGroup'
		c.data = json.dumps(g)
		c.save ()
		
	def save (self, *args, **kwargs) :
		user = None
		if 'request_user' in kwargs.keys () :
			user = kwargs['request_user']
			del kwargs['request_user']
		super (Group, self).save (*args, **kwargs)
		self._update_ldap (user)

	def members (self) :
		import user as usermodule
		return usermodule.User.objects.filter(groups__name=self.name)

	def member_logins (self) :
		m = []
		for u in self.members() :
			user = {}
			user['login'] = u.login
			user['first_name'] = u.first_name
			user['last_name'] = u.last_name
			user['appSpecName'] = u.appspecname
			m.append (user)
		return m
	
	def set_members (self, members, user=None) :
		from user import User
		m = []
		for u in members :
			m.append (int(u))
		changed = False
		# remove members not in list
		for u in User.objects.filter(groups__name=self.name) :
			if u.uidnumber not in m :
				u.groups.remove (self)
				changed = True
		# add new members 
		for uidnumber in m :
			try :
				u = User.objects.get(uidnumber=uidnumber,groups__name=self.name)
			except User.DoesNotExist as e :
				try :
					u = User.objects.get(uidnumber=uidnumber)
				except User.DoesNotExist as e :
					# should not happen
					pass
				else :
					u.groups.add(self)
					changed = True
		if changed :
			self._update_ldap(user)
	
	# helper functions used by the xml template
	
	def get_children (self) :
		return Group.objects.filter(parent=self)	
					
	def is_team_group (self) :
		return self.group_type == self.TEAM_GROUP
	
	def is_service_group (self) :
		return self.group_type == self.SERVICE_GROUP

	def is_status_group (self) :
		return self.group_type == self.STATUS_GROUP
