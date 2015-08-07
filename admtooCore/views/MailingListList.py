# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from .. import models
from decorators import *

import logging
logger = logging.getLogger('django_auth_ldap')

#==============================================================================
# mailing lists management
#

#
# list of all mailing lists 
#
@admin_login
def mailinglist_list (request) :
	mailinglists = models.MailingList.objects.all()
	context = {
		'mailinglists' : mailinglists
	}
	return render(request, 'mailinglist-list.html', context)

