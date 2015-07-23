# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from .. import models
from decorators import *

import logging
logger = logging.getLogger('django_auth_ldap')

#==============================================================================
# groups management
#

#
# list of all groups
#
@admin_login
def mailinglist_view (request) :
	context = {}
	return render(request, 'mailinglist-view.html', context)

