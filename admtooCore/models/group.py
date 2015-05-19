# -*- coding: utf-8 -*-
from django.db import models
import json
import netfields
import logging
logger=logging.getLogger('django')

class Group (models.Model) :
	NORMAL_GROUP = 0
	TEAM_GROUP = 1
	SERVICE_GROUP = 2

	GROUP_TYPES_CHOICES = (
		( NORMAL_GROUP,  ''),
		( TEAM_GROUP,    'Groupe d\'équipe'),
		( SERVICE_GROUP, 'Groupe de service'),
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
		logger.error ("saving group to ldap, members list : "+str(members))
		
		g = self.prepare_group_data()

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
