# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

# other models used
from group import Group
from machine import Machine

def userclass_default () :
	from userclass import UserClass
	return UserClass.objects.get(probie=True).pk

class User (models.Model) :
	# unix related things
	uidnumber    = models.IntegerField(unique=True, default=None)
	group        = models.ForeignKey('Group', null=True, blank=True)
	login        = models.CharField(max_length=64, unique=True, db_index=True)
	login_shell  = models.CharField(max_length=128, null=True, blank=True)

	# actual user info
	first_name	 = models.CharField(max_length=128, null=True, blank=True)
	last_name    = models.CharField(max_length=128, null=True, blank=True)
	birthdate    = models.DateField(null=True, blank=True)

	# user photo
	photo_path      = models.CharField(max_length=256, null=True, blank=True)
	photo_is_public = models.BooleanField(default = False)

	# organisational info
	mail         = models.EmailField(max_length=254,null=True, blank=True)
	manager      = models.ForeignKey('self', null=True, blank=True)
	userclass    = models.ForeignKey ('UserClass', null=True, blank=True)
	arrival		 = models.DateField(null=True, blank=True)
	departure	 = models.DateField(null=True, blank=True)

	# teams and groups this user is in
	groups		 = models.ManyToManyField(Group, blank=True, related_name='users')
	main_team    = models.ForeignKey ('Group', null=True, blank=True, related_name='team_member')

	# user localisation
	room		 = models.CharField(max_length=32, null=True, blank=True)
	telephone    = models.CharField(max_length=32, null=True, blank=True)

	flags        = models.ManyToManyField('UserFlag', blank=True)

	# user state management
	NORMAL_USER    = 0
	NEWIMPORT_USER = 1
	DELETED_USER   = 2

	USER_STATE_CHOICES = (
		( NORMAL_USER,    'utilisateur actif'),
		( NEWIMPORT_USER, 'utilisateur nouvellement importé'),
		( DELETED_USER,   'utilisateur supprimé'),
	)
	user_state	 = models.IntegerField(choices = USER_STATE_CHOICES, default=NORMAL_USER)

	# accounts in other applications
	appspecname  = models.TextField(default='', blank=True) 



	class Meta :
		app_label = 'admtooCore'
		ordering = ['login']

	def __init__ (self, *args, **kwargs) :
		super(User, self).__init__(*args, **kwargs)

	def __repr__ (self) :
		return self.login
		s = 'uidnumber   '+str(self.uidnumber)+'\n'
		s+= 'login       \''+str(self.login)+'\'\n'
		s+= 'login_shell \''+str(self.login_shell)+'\'\n'
		s+= 'first_name  \''+str(self.first_name)+'\'\n'
		s+= 'last_name   \''+str(self.last_name)+'\'\n'
		s+= 'mail        \''+str(self.mail)+'\'\n'
		s+= 'manager     '
		if self.manager is None :
			s+= 'None'
		else :
			s+= '\''+str(self.manager)+'\''
		s+= '\n'
		s+= 'arrival     '+str(self.arrival)+'\n'
		s+= 'departure   '+str(self.departure)+'\n'
		s+= 'room        \''+str(self.room)+'\'\n'
		s+= 'telephone   \''+str(self.telephone)+'\'\n'
		return s
	
	def __str__ (self) :
		return self.login
	
	#
	# this internal save command only saves the user to the database
	# no sync to the ldap is done
	def _save (self, *args, **kwargs) :
		#logger.error ('saving user '+self.login+' before assigning groups')
		super (User, self).save(*args, **kwargs)

	def _update_ldap (self, user=None) :
		# modify attributes of the person that we can actually modify
		u = {}
		u['uid'] = self.login
		u['gecos'] = self.first_name+' '+self.last_name
		if self.manager is not None :
			u['manager'] = self.manager.login
		u['loginShell'] = self.login_shell
		# should only be modified through biper
		#u['roomNumber'] = self.room
		#u['telephoneNumber'] = self.telephone		

		import command, json
		c = command.Command ()
		if user is None :
			c.user = "(Unknown)"
		else :
			c.user = str(user)
		c.verb = 'UpdateUser'
		c.data = json.dumps (u)
		c.save ()

	#
	# the default save command syncs the user data to the ldap server
	# as soon as the save command is launched
	def save (self, *args, **kwargs) :
		user = None
		if 'request_user' in kwargs.keys () :
			user = kwargs['request_user']
			del kwargs['request_user']
		super (User, self).save(*args, **kwargs)
		if self.user_state != self.DELETED_USER:
			self._update_ldap(user)

	def full_name (self) :
		n = []
		if self.first_name is not None : 
			n.append(self.first_name)
		if self.last_name is not None :
			n.append(self.last_name)
		return ' '.join(n)

	def userclassref (self) :
		if self.userclass is None :
			return ''
		from mailinglist import MailingList
		return MailingList.objects.get(userclass=self.userclass).ml_id

	def all_mailinglists (self) :
		from mailinglist import MailingList
		mls = []
		# mailing lists for user class
		
		# mailing lists from groups
		gr = self.all_groups ()
		for g in gr :
			try :
				ml = MailingList.objects.get (group = g)
			except MailingList.DoesNotExist as e :
				pass
			else :
				mls.append(ml)
		for ml in mls :
			p = ml
			while True :
				p = p.parent
				if p is not None :
					if p not in mls :				
						mls.append (p)
				else :
					break
		return mls
				
	def change_mailinglists (self, mailinglists) :
		# va savoir ce qu'il faut faire la dedans... 
		# select all mailing lists not attached to a group
		pass

	def _get_parent_group (self, group) :
		gr = []
		pg = group.parent
		if pg not in gr :
			gr.append (pg)
		if pg is not None :
			tg = self._get_parent_group(pg)
			if tg is not None :
				for g in tg :
					if g not in gr :
						gr.append(g)
		else :
			gr = pg
		return gr
	
	def all_groups (self) :
		gr = []
		for g in self.groups.all() :
			if g not in gr :
				gr.append(g)
			tg = self._get_parent_group(g)
			if tg is not None :
				for pg in tg :
					if pg not in gr :
						gr.append(pg)
		return gr
	
	def unique_groups (self) :
		agr = self.all_groups()
		# need to identify all groups for which there's a child in the list
		parents = []
		# identify all group histories
		for g in agr :
			gp = []
			p = g
			while p is not None :
				gp.append (p)
				p = p.parent
			parents.append (gp)
		# identify groups with child
		groups_with_child = []
		for gp in parents :
			p = gp[1:]
			for g in p :
				if g not in groups_with_child :
					groups_with_child.append (g)
		# remove the groups with child from the list
		groups = []
		for g in agr: 
			if g not in groups_with_child :
				groups.append (g)
		return groups

	# la grouplist est un array de gidnumbers
	def change_groups (self, grouplist, user=None) :
		changed = False
		i=0
		while i < len(grouplist) :
			grouplist[i] = int(grouplist[i])
			i += 1
		for g in self.groups.all() :
			if g.gidnumber not in grouplist :
				self.groups.remove(g)
				g._update_ldap(user)
		for g in grouplist :
			g = Group.objects.get(gidnumber=g)
			if (g is not None) and (g not in self.groups.all()) :
				self.groups.add (g)
				g._update_ldap(user)
		# remove the main team if not in grouplist anymore
		if self.main_team is not None:
			if self.main_team.gidnumber not in grouplist :
				self.main_team = None
				self.save()

	def all_teams (self) :
		t = []
		for g in self.all_groups() :
			if g.is_team_group() :
				t.append (g)
		return t

	def manager_of (self) :
		return User.objects.filter(manager = self)

	def change_managed (self, managed_list, user=None) :
		for u in User.objects.filter(manager = self) :
			if u.uidnumber not in managed_list :
				u.manager = None
				u.save (request_user=user)
		for un in managed_list :
			u = User.objects.get(uidnumber = un)
			if (u.manager != self) :
				u.manager = self
				u.save (request_user=user)

	def machines (self) :
		return Machine.objects.filter(owner = self)

	#==========================================================================
	# methods used for the user list

	def account_status (self) :
		if self.departure is not None :
			from django.conf import settings
			import datetime
			today = datetime.date.today()
			
			delta = (today - self.departure).days
			#Logger.error (self.login+" "+str(delta))
			if (delta >= settings.USER_DEPARTURE_SOON) and (delta < 0) :
				return "user-departure-soon"
			elif (delta == 0) and (delta <= settings.USER_DEPARTURE_GONE) :
				return "user-departure-purgatory"
			elif (delta > settings.USER_DEPARTURE_GONE) :
				return "user-departure-gone"
		return ""

	def suspend_date (self) :
		if self.departure is not None :
			from django.conf import settings
			import datetime
			return self.departure + datetime.timedelta(settings.USER_DEPARTURE_GONE)
		return ""


	#==========================================================================
	# User declaration related methods
	
	def has_newuser (self) :
		from newuser import NewUser
		nu = NewUser.objects.get(user=self)
		if nu is not None :
			return True
		return False	
	
	def other_account_names (self) :
		import json
		try :
			v = json.loads(self.appspecname)
		except ValueError as e :
			v = {}
		an = []
		for k in v.keys() :
			an.append ((k, v[k],))
		return an
			
	
	def default_twiki_account (self) :
		#from admtooLib.twiki import TWiki
		from ..plugins import plugins
		t = plugins.TWiki
		return t.gen_user_name (self.first_name, self.last_name)

