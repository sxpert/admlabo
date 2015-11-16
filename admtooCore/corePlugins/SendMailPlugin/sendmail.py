#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,json
from django.conf import settings
from django.template import Context, Template
from django.core.mail import get_connection, send_mail, EmailMultiAlternatives
#from django.db import models
from ... import models

class Send_Mail (object) :
	def __init__ (self) :
		self._logger = None

	def _log (self, message) :
		if self._logger is not None :
			self._logger.error (message)
		else :
			
			s = repr(message).encode('utf-8')
			sys.stdout.write (s+u'\n')
			sys.stdout.flush ()

	#
	# sends one mail
	#
	def _send_mail (self, subject, message, from_email, recipient_list, 
					fail_silently=False, auth_user=None, auth_password=None,
					connection=None, html_message=None) :
		connection = connection or get_connection(username=auth_user, password=auth_password, fail_silently=fail_silently)
		mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection,
									  headers={'Return-Path': 'support-info.ipag@obs.ujf-grenoble.fr'})
		if html_message :
			mail.attach_alternative (html_message, 'text/html')
		# should try to catch exceptions
		mail.send()
		self._log ('mail to '+str(recipient_list)+' sent successfully')
		return True

	#
	# send mails for one mailcond
	#
	def _sendMailForCondition (self, mailcond, data) :
		if (type(mailcond) is str) or (type(mailcond) is unicode) :
			self._log ('DEBUG : '+str(settings.DEBUG))
			# get mail message
			try :
				m = models.EmailAlertMessage.objects.get(cause=mailcond)
			except models.EmailAlertMessage.DoesNotExist as e :
				self._log ('sendMailForCondition FATAL: unable to find email message data for mailcondition : \''+str(mailcond)+'\'')
				return False
			# generate data from templates
			c = Context(data)
			# if available, generate sender from template
			sender = m.sender.strip()
			if len(sender) > 0 :
				t = Template(m.sender)
				sender = t.render (c)
			else :
				sender = 'django@admipag.obs.ujf-grenoble.fr' 
			# generate subject from templates
			t = Template(m.subject)
			subject = t.render(c)
			if settings.DEBUG : 
				subject = '[TESTING] '+subject
			self._log (subject)
			# generate content from template
			t = Template(m.msgtext)
			msgtext = t.render(c)
			t = Template(m.msghtml)
			msghtml = t.render(c)
			# get list of people
			dest = models.EmailAlert.objects.filter(cause=mailcond)
			l = []
			for u in dest :
				# should do templates here too
				l.append (u.email)
			self._log (str(l))
			if settings.DEBUG :
				l.append ('raphael.jacquot@obs.ujf-grenoble.fr')
			# send one mail per email address found
			# the email down there should be l
			res = self._send_mail ( subject, msgtext, sender, 
					 		  l, fail_silently=False, html_message=msghtml)
			self._log (res)
			return res
		else :
			self._log ('sendMailForCondition FATAL: don\'t know what to do with mailcondition = \''+str(mailcond)+'\' ('+str(type(mailcond))+')')
			return False

	# sends a mail message to a series of people depending on the mail
	# condition(s).
	# adds the extra-message to the end of the mail if present
	# mailconds : string or array of strings
	# data      : python dict / object with the variables
	#                 
	def SendMail (self, *args, **kwargs) :
		_, command = args
		if 'logger' in kwargs.keys() :
			logger = kwargs['logger']
			if logger is not None :
				self._logger = logger

		c = json.loads(command.data)
		ck = c.keys()

		self._log (str(ck))

		mailconds = c['mailconditions']
		data = c['maildata']
		self._log(type(mailconds))

		if type(mailconds) is list :
			for mc in mailconds :
				# fail if one of the mail sending operation fails
				self._log('sending mail for condition '+mc)
				if not self._sendMailForCondition (mc, data) :
					self._log('send fail for condition '+mc)
					return False
			return True
		elif type(mailconds) is str :
			return self._sendMailForCondition (mailconds, data)
		else :
			self._log ('sendMail FATAL: don\'t know what to do with mailconditions = \''+str(mailconds)+'\' ('+str(type(mailconds))+')')
		return False
		

# -*- coding: utf-8 -*-
#import logging
#logger=logging.getLogger('django')






