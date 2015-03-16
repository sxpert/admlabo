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
		app_label = 'silabo'

	def __str__ (self) :
		return self.name
	
	# update the group object to the ldap server
	def _update_ldap (self, l = None) :
		if l is None :
			l = lo.LdapOsug ()
			l.logger = logger
	
		# get members list
		members = self.member_logins()

		g = l.group_check_exists (self.name, self.gidnumber)
		if g is None :
			# can't find group, add it to the ldap server
			l.group_create (self.name, self.gidnumber, self.description, members)
		else :
			# we have a group, attempt to update it
			# 1. check if group needs renaming
			name, gid = g
			if name != self.name :
				l.group_rename (name, self.name)
			# 2. update group info
			l.group_update (self.name, self.gidnumber, self.description, members)

	def save (self, *args, **kwargs) :
		logger.error ("saving group '"+self.name+"'")
		super (Group, self).save (*args, **kwargs)
		self._update_ldap ()

	def members (self) :
		import silabo.models.user as usermodule
		return usermodule.User.objects.filter(groups__name=self.name)

	def member_logins (self) :
		m = []
		for u in self.members() :
			m.append (u.login)
		return m
