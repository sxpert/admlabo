# -*- coding: utf-8 -*-
from django.db import models
import logging
logger=logging.getLogger('django')

class MailAlias (models.Model) :
	alias = models.CharField (max_length=254, unique=True)
#	user  = models.ForeignKey ('User', null=True, blank=True, related_name='UserAliases')
	description = models.CharField (max_length=254, null=True, blank=True)
	mail = models.EmailField(max_length=254,null=True, blank=True)

	class Meta:
		verbose_name_plural = "MailAliases"
		app_label = 'admtooCore'

	def __str__ (self) :
		return self.alias

	def _ldap (self, verb, user=None) :
		ma_data = {
			'alias'       : self.alias,
			'description' : self.description,
			'mail'        : self.mail
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
		if 'request_user' in kwargs.keys () :
			user = kwargs['request_user']
			del kwargs['request_user']
		super (MailAlias, self).save(*args, **kwargs)
		if self.mail is not None :
			self._ldap ('UpdateMailAlias', user)

	def delete (self, *args, **kwargs) :
		user = None
		if 'request_user' in kwargs.keys () :
			user = kwargs['request_user']
			del kwargs['request_user']
		super (MailAlias, self).delete(*args, **kwargs)
		self._ldap ('DeleteMailAlias', user)
