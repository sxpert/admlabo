# -*- coding: utf-8 -*-
import logging
logger=logging.getLogger('django')

from .. import models

from django.template import Context, Template
from django.core.mail import send_mail

# send mails for one mailcond
def sendMailForCondition (mailcond, data) :
	if type(mailcond) is str :
		# get mail message
		m = models.EmailAlertMessage.objects.get(cause=mailcond)
		# generate subject and content from templates
		logger.error (m.subject)
		t = Template(m.subject)
		c = Context(data)
		subject = t.render(c)
		logger.error (subject)
		t = Template(m.msgtext)
		msgtext = t.render(c)
		logger.error (msgtext)
		t = Template(m.msghtml)
		msghtml = t.render(c)
		logger.error (msghtml)
		# get list of people
		# send one mail per email address found
		send_mail ( subject, msgtext, 'django@admipag.obs.ujf-grenoble.fr', 
				    ['frederic.roussel@obs.ujf-grenoble.fr'], 
				    fail_silently=False,
					html_message=msghtml)
		pass
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


