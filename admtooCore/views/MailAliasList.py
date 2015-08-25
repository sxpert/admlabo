# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from .. import models
from decorators import *

import logging
logger = logging.getLogger('django_auth_ldap')

#==============================================================================
# mail aliases management
#

#
# list of all mail aliases
#
@admin_login
def mailalias_list (request) :
	mailaliases = models.MailAlias.objects.all()
	context = {
		'mailaliases' : mailaliases
	}
	return render(request, 'mailalias-list.html', context)

