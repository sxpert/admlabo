# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class MailingList (models.Model) :
	ml_id       = models.CharField(max_length=64, primary_key=True)
	name        = models.CharField(max_length=128, unique=True)
	description = models.CharField(max_length=256)
	parent      = models.ForeignKey('self', null=True, blank=True)
	group       = models.ForeignKey('Group', null=True, blank=True)
	userclass   = models.ForeignKey('UserClass', null=True, blank=True)

	class Meta:
		app_label = 'admtooCore'
		ordering  = ['ml_id']

	def __str__ (self) :
		return self.name

	def get_children (self) :
		return MailingList.objects.filter(parent=self)

	def _ldap (self, verb, user=None) :
		if (self.name is None) or (len(self.name) == 0):
			logger.error ('current ml alias is empty. skip the ldap creation process')
			return
		ma_data = {
			'alias'       : self.name,
			'description' : self.description,
			'mail'        : self.name
		}
		import command, json
		c = command.Command ()
		if user is None :
			c.user = '(unknown)'
		else :
			c.user = str(user)
		c.verb = verb
		c.data = json.dumps(ma_data)
		c.save()

	def save (self, *args, **kwargs) :
		user = None
		if 'request_user' in kwargs.keys() :
			user = kwargs['request_user']
			del kwargs['request_user']
		super (MailingList, self).save(*args, **kwargs)
		self._ldap ('UpdateMailingList', user)

	def rename (self, new_name, request_user=None) :
		if (self.name is None) or (len(self.name) == 0) :
			self.name = new_name
			return self.save (request_user=request_user)
		if new_name != self.name :
			# save the old name
			old_name = self.name
			self.name = new_name
			# save the object
			super (MailingList, self).save()
			# launch the renaming of the object
			data = {
				'old_alias': old_name,
				'new_alias': new_name
			}
			import command, json
			c = command.Command ()
			if request_user is None :
				c.user = '(unknown)'
			else :
				c.user = str(request_user)
			c.verb = 'RenameMailingList'
			c.data = json.dumps (data)
			c.save ()

	def delete (self, *args, **kwargs) :
		user = None
		if 'request_user' in kwargs.keys () :
			user = kwargs['request_user']
			del kwargs['request_user']
		super (MailingList, self).delete(*args, **kwargs)
		self._ldap ('DeleteMailingList', user)

