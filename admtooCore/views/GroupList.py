# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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
def groups (request) :
	groups = models.Group.objects.all()
	context = {
		'groups': groups,
	}
	return render(request, 'groups.html', context)

