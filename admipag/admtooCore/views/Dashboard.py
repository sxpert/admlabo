# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .. import models
from django.contrib.auth.decorators import login_required

import logging
logger=logging.getLogger('django')

#==============================================================================
# application dashboard
#
@login_required
def Dashboard (request) :
	logger.error (str(request.user))
	if not request.user.is_staff :
		logger.error ('user is not staff')
		logger.error ('redirecting to new arrival form')
		return redirect ('new-arrival-form')
	logger.error ('user is of staff')
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'dashboard.html', context)

#==============================================================================
# Dashboard bits
# 

from decorators import *

@admin_login
def DBNewArrivals (request) :
	newusers = models.NewUser.objects.all()
	context = {
		'nu' : newusers,
	}
	return render(request, 'DBNewArrivals.html', context)

@admin_login
def DBUnknownUsers (request) :
	users = models.User.objects.filter (user_state=models.User.NEWIMPORT_USER)
	context = {
		'nu' : users,
	}
	return render(request, 'DBUnknownUsers.html', context)
