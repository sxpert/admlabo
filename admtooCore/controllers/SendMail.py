# -*- coding: utf-8 -*-
import logging
logger=logging.getLogger('django')

from .. import models
from django.conf import settings
from django.template import Context, Template
from django.core.mail import get_connection, send_mail

def _send_mail (subject, message, from_email, recipient_list, 
				fail_silently=False, auth_user=None, auth_password=None,
				connection=None, html_message=None) :
	connection = connection or get_connection(username=auth_user, password=auth_password, fail_silently=fail_silently)
	mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection,
								  headers={'Return-Path': 'support-info.ipag@obs.ujf-grenoble.fr'})
	if html_message :
		mail.attach_alternative (html_message, 'text/html')
	return mail.send()

# send mails for one mailcond
def sendMailForCondition (mailcond, data) :
	if type(mailcond) is str :
		logger.error ('DEBUG : '+str(settings.DEBUG))
		# get mail message
		try :
			m = models.EmailAlertMessage.objects.get(cause=mailcond)
		except models.EmailAlertMessage.DoesNotExist as e :
			logger.error ('sendMailForCondition FATAL: unable to find email message data for mailcondition : \''+str(mailcond)+'\'')
			return False
		# generate subject and content from templates
		t = Template(m.subject)
		c = Context(data)
		subject = t.render(c)
		if settings.DEBUG : 
			subject = '[TESTING] '+subject
		logger.error (subject)
		t = Template(m.msgtext)
		msgtext = t.render(c)
		#logger.error (msgtext)
		t = Template(m.msghtml)
		msghtml = t.render(c)
		#logger.error (msghtml)
		# get list of people
		dest = models.EmailAlert.objects.filter(cause=mailcond)
		l = []
		for u in dest :
			l.append (u.email)
		logger.error (str(l))
		if settings.DEBUG :
			l.append ('raphael.jacquot@obs.ujf-grenoble.fr')
		# send one mail per email address found
		# the email down there should be l
		_send_mail ( subject, msgtext, 'django@admipag.obs.ujf-grenoble.fr', 
				     l, fail_silently=False, html_message=msghtml)
	else :
		logger.error ('sendMailForCondition FATAL: don\'t know what to do with mailcondition = \''+str(mailcond)+'\'')

# sends a mail message to a series of people depending on the mail
# condition(s).
# adds the extra-message to the end of the mail if present
# mailconds : string or array of strings
# data      : python dict / object with the variables
#                 
def sendMail (mailconds, data) :
	if type(mailconds) is list :
		for mc in mailconds :
			sendMailForCondition (mc, data)
	elif type(mailconds) is str :
		sendMailForCondition (mailconds, data)
	else :
		logger.error ('sendMail FATAL: don\'t know what to do with mailconditions = \''+str(mailconds)+'\'')


