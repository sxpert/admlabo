# -*- coding: utf-8 -*-
from django.db import models, IntegrityError
import netfields
import logging
logger=logging.getLogger('django')
from django.conf import settings

# other models used
from group import Group
from machine import Machine
from userclass import UserClass
from usergrouphistory import UserGroupHistory

def userclass_default () :
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
	ERROR_USER     = 3

	USER_STATE_CHOICES = (
		( NORMAL_USER,    'utilisateur actif'),
		( NEWIMPORT_USER, 'utilisateur nouvellement importé'),
		( DELETED_USER,   'utilisateur supprimé'),
		( ERROR_USER,     'utilisateur créé par erreur'),
	)
	user_state	 = models.IntegerField(choices = USER_STATE_CHOICES, default=NORMAL_USER)

	# accounts in other applications
	appspecname  = models.TextField(default='', blank=True) 



	class Meta :
		app_label = 'admtooCore'
		ordering = ['login']
		permissions = (
			('do_rh_tasks', 'can change photos and flags'),
		)

	def __init__ (self, *args, **kwargs) :
		super(User, self).__init__(*args, **kwargs)
		try :
			groups = self.unique_groups ()
		except ValueError as e :
			# do nothing if there's an error obtaining groups
			pass
		else :
			if len(groups) > 0 :
				# search for status groups
				status_groups = []
				for g in groups :
					if g.group_type == g.STATUS_GROUP :
						status_groups.append(g)
				if len (status_groups) == 1 :
					try :
						uc = UserClass.objects.get(group=status_groups[0]) 
					except UserClass.DoesNotExist as e :
						pass
					else :
						if self.userclass is None: 
							self.userclass = uc 
							self._save()
		

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
		user_state = int(self.user_state)
		if user_state not in (self.DELETED_USER, self.ERROR_USER) :
			self._update_ldap(user)
		else : 
			# remove user from all groups it belongs to
			# put those groups in the history table
			logger.error ('>>> removing all groups')
			self.change_groups([],user)

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
		logger.error ('')
		logger.error ('MAILING LISTS :')
		logger.error (mls)
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
		
		# check if user belongs to all listed groups
		# logs an alert otherwise
		not_member = []
		for g in gr :
			if g not in self.groups.all() :
				not_member.append(g)
		if len(not_member)>0 :
			logger.error (unicode(self.login)+u' not member of '+unicode(not_member)+u', fixing') 
			for g in not_member :
				#logger.error (u'adding group '+unicode(g)+u' to user '+unicode(self.login))
				self.add_group(g, None)

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

	"""
	generate user group change entries
	"""
	def add_ugh_entry (self, mode, groups, user=None) :
		import json
		ugh = UserGroupHistory()
		creator = None
		if user is not None :
			creator = User.objects.get (login=user)
		ugh.creator = creator
		ugh.user = self
		ugh.action = mode
		# generate json block
		group_info = {}
		for g in groups :
			group_info[g.gidnumber] = g.name	
		ugh.data = json.dumps(group_info)
		ugh.save()

	"""
	Removes the group from the user only if the user is not a member of a descendant group
	The caller is to update the ldap group
	"""
	def remove_group (self, g, user=None) :
		# get the object for the group
		if type(g) is int :
			try :
				group = Group.objects.get (gidnumber = g)
			except Group.DoesNotExist as e :
				# the group can't be found
				logger.error (u'ERROR: Unable to find group '+unicode(g))
				return False
		elif type(g) is Group :
			group = g
		else :
			logger.error (u'ERROR: invalid value for group, integer or Group expected, got '+unicode(g))
			return False
		
		# step 1 : find if this particular group has descendants
		children = Group.objects.filter (parent=group)
		logger.error (children)
		
		# find if user is a member of any children, if so, bail out
		for g in self.groups.all() :
			if g in children :
				logger.error (u'ERROR: removing group : user '+unicode(self.login)+u' is member of '+unicode(g.name)+u' which is a children of '+unicode(group.name))
				return False
		
		# we can safely remove user from group
		self.groups.remove(group)
		# generate an ugh entry
		self.add_ugh_entry (UserGroupHistory.ACTION_DEL, [group], user)
		return True
		
	"""
	Adds the group for the user, adds all non present parent groups
	The caller is responsible for udating the ldap group
	"""
	def add_group (self, g, user=None) :
		added_groups = []
		if type(g) is int :
			# get the object for the group
			try :
				group = Group.objects.get (gidnumber = g)
			except Group.DoesNotExist as e :
				# can't find the group
				logger.error (u'ERROR: Unable to find group '+unicode(g))
				return False
		elif type(g) is Group :
			group = g
		else :
			logger.error (u'ERROR: invalid value for group, integer or Group expected, got '+unicode(g))
			return False

		# step 0: check if user is already a member
		if group in self.groups.all() :
			return False

		# step 1: find all parents of this group
		parents = self._get_parent_group (group)
		
		if parents is not None :
			# step 2: add the user to parents starting from the last one
			for g in reversed(parents) :
				logger.error (g)
				if g not in self.groups.all() :
					# catch potential exception on fail to add group
					try :
						self.groups.add (g)
					except IntegrityError as e :
						# log that something happened
						logger.error (u'WARNING: user '+unicode(self.login)+u' was already in group '+unicode(g))
					else :
						added_groups.append (g)
					# update group in ldap, whatever happened
					g._update_ldap (user)

		# adds the target group
		logger.error (u'Adding group '+unicode(group)+u' to user '+unicode(self))
		try:
			self.groups.add (group)
		except IntegrityError as e :
			logger.error (u'WARNING: user '+unicode(self.login)+u' was already in group '+unicode(g))
		else :
			added_groups.append (group)

		self.add_ugh_entry (UserGroupHistory.ACTION_ADD, added_groups, user)

		return True

	# la grouplist est un array de gidnumbers
	def change_groups (self, grouplist, user=None) :
		changed = False
		
		# generate newgroups list
		newgroups = []
		for gidnumber in grouplist :
			try :
				g = Group.objects.get(gidnumber=int(gidnumber))
			except Group.DoesNotExist as e :
				logger.error (u'Can\'t find group with gidnumber'+unicode(gidnumber))
			else :
				newgroups.append(g)
		
		# oldgroups are normally sorted by parent-ness (with the most senior at the end)
		oldgroups = self.groups.all()
		logger.error (u'NEWGROUPS : '+unicode(newgroups))
		logger.error (u'OLDGROUPS : '+unicode(oldgroups))
	
		for g in newgroups :
			if g not in oldgroups :
				if self.add_group (g, user) :
					g._update_ldap (user)
		for g in oldgroups :
			if g not in newgroups :
				if self.remove_group (g, user) :
					g._update_ldap (user)

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
			elif (delta >= 0) and (delta <= settings.USER_DEPARTURE_GONE) :
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
			

	#==========================================================================
	# TWiki related
	# 

	
	def default_twiki_account (self) :
		# check if user already has a TWiki name
		import json
		try :
			v = json.loads(self.appspecname)
		except ValueError as e :
			pass
		else :
			if 'twiki' in v :
				return v['twiki']
		#from admtooLib.twiki import TWiki
		from ..plugins import plugins
		t = plugins.TWiki
		return t.gen_user_name (self.first_name, self.last_name)
	
	def disable (self, ru) :
		import command, json
		c = command.Command ()
		if ru is None :
			c.user = "(unknown)"
		else :
			c.user = unicode(ru)
		c.verb = "DisableUser"
		c.in_cron = True
		try :
			asn = json.loads(self.appspecname)
		except ValueError as e:
			asn = None
		c.data = json.dumps ({'first_name': self.first_name, 'last_name': self.last_name, 'appSpecName': asn })
		c.post ()

	#==========================================================================
	# generate a command to update the kifekoi 

	@staticmethod
	def generate_kifekoi_list () :
		import datetime
		today = datetime.date.today()
		data = []
		users = User.objects.filter(user_state=User.NORMAL_USER).order_by ('last_name', 'first_name')
		for u in users :
			# skip user if departure date is passed
			if u.departure is not None :
				if today > u.departure :
					continue
			user = {}
			user['first_name'] = u.first_name
			user['last_name'] = u.last_name
			user['telephone'] = u.telephone
			user['room'] = u.room
			if u.main_team is not None :
				try :
					user['team'] = u.main_team.wiki_teamlogo()
				except AttributeError as e :
					pass
			else :
				# find the team groups within the users's groups
				groups = u.groups.filter(group_type=Group.TEAM_GROUP)
				if len(groups) == 1 :
					user['team'] = groups[0].wiki_teamlogo()
			# flags
			flags = []
			for f in u.flags.all() :
				flags.append (f.name)
			user['flags'] = flags
			# add user to list
			data.append (user)
		return data

	@staticmethod
	def update_kifekoi (request_user=None) :	
		# users list generated, insert the command
		import command, json
		c = command.Command ()
		if request_user is None :
			c.user = "(Unknown)"
		else :
			c.user = unicode(request_user)
		c.verb = 'UpdateKiFeKoi'
		c.in_cron = True
		c.data = ''
		c.post ()

	@staticmethod
	def update_annuaire (request_user=None) :
		import command, json
		c = command.Command()
		if request_user is None :
			c.user = '(unknown)'
		else :
			c.user = unicode(request_user)
		c.verb = 'AnnuaireUpdate'
		c.in_cron = True
		c.data = ''
		c.post ()

	#==========================================================================
	# method for the directory display

	def display_in_directory (self) :
		# is the user active in the lab
		if self.user_state != User.NORMAL_USER :
			return False
		# check if today is later than the departure date
		if self.departure is not None :
			import datetime
			today = datetime.date.today()
			if today > self.departure :
				return False
		# can the user be normally displayed
		if self.userclass and self.userclass.directory :
			return True
		# do we have flag_annuaire
		flags = [f.name for f in self.flags.all()]
		if settings.FLAG_ANNUAIRE in flags :
			return True
		return False
	
