# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

# ldap access
import sys
sys.path.append ('/srv/progs')
import ipag.ldaposug as lo

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

	class Meta:
		app_label = 'admtooCore'

	def __str__ (self) :
		return self.name
	
	# update the group object to the ldap server
	def _update_ldap (self) :
		# get members list
		members = self.member_logins()
		logger.error ("saving group to ldap, members list : "+str(members))

		g = {}
		g['cn']          = self.name
		g['gidNumber']   = self.gidnumber
		g['description'] = self.description
		g['memberUid']   = members

		import command, json
		c = command.Command ()
		c.verb = 'UpdateGroup'
		c.data = json.dumps(g)
		c.save ()
		
	def save (self, *args, **kwargs) :
		super (Group, self).save (*args, **kwargs)
		self._update_ldap ()

	def members (self) :
		import user as usermodule
		return usermodule.User.objects.filter(groups__name=self.name)

	def member_logins (self) :
		m = []
		for u in self.members() :
			m.append (u.login)
		return m
