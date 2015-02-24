# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')
from silabo.models.group import Group
from silabo.models.mailinglist import MailingList
from silabo.models.machine import Machine

class User (models.Model) :
	uidnumber   = models.IntegerField(primary_key=True)
	login       = models.CharField(max_length=64, unique=True)
	login_shell = models.CharField(max_length=128, null=True, blank=True)
	first_name	= models.CharField(max_length=128, null=True, blank=True)
	last_name   = models.CharField(max_length=128, null=True, blank=True)
	mail        = models.EmailField(null=True, blank=True)
	manager     = models.ForeignKey('self', null=True, blank=True)
	arrival		= models.DateField(null=True, blank=True)
	departure	= models.DateField(null=True, blank=True)
	groups		= models.ManyToManyField(Group, blank=True, related_name='users')
	room		= models.CharField(max_length=32, null=True, blank=True)
	telephone   = models.CharField(max_length=32, null=True, blank=True)

	class Meta :
		ordering = ['login']
		app_label = 'silabo'

	def __init__ (self, *args, **kwargs) :
		super(User, self).__init__(*args, **kwargs)
	
	def __str__ (self) :
		return self.login

	def save (self, *args, **kwargs) :
		logger.error ('saving user '+self.login)
		super (User, self).save(*args, **kwargs)
		# save into the production ldap
		logger.error ('user saved')

	def full_name (self) :
		n = []
		if self.first_name is not None : 
			n.append(self.first_name)
		if self.last_name is not None :
			n.append(self.last_name)
		return ' '.join(n)

	def all_mailinglists (self) :
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

	# la grouplist est un array de gidnumbers
	def change_groups (self, grouplist) :
		changed = False
		i=0
		while i < len(grouplist) :
			grouplist[i] = int(grouplist[i])
			i += 1
		for g in self.groups.all() :
			if g.gidnumber not in grouplist :
				self.groups.remove(g)
				changed = True
		for g in grouplist :
			g = Group.objects.get(gidnumber=g)
			if (g is not None) and (g not in self.groups.all()) :
				self.groups.add (g)
				changed = True
		if changed :
			self.save()

	def manager_of (self) :
		return User.objects.filter(manager = self)

	def change_managed (self, managed_list) :
		for u in User.objects.filter(manager = self) :
			if u.uidnumber not in managed_list :
				u.manager = None
				u.save ()
		for un in managed_list :
			u = User.objects.get(uidnumber = un)
			if (u.manager != self) :
				u.manager = self
				u.save ()

	def machines (self) :
		return Machine.objects.filter(owner = self)
	
	
