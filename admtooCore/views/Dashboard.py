# -*- coding: utf-8 -*-

from django.db.models import Q
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
	newusers = models.NewUser.objects.filter(Q(user__user_state=models.User.NEWIMPORT_USER)|Q(user__isnull=True)).order_by('arrival')
	context = {
		'nu' : newusers,
	}
	return render(request, 'DBNewArrivals.html', context)

@admin_login
def DBUnknownUsers (request) :
	users = models.User.objects.filter (user_state=models.User.NEWIMPORT_USER)
	sort = request.GET.get('sort', None)

	context = {}

	if sort is not None :
		if sort=='arrival' :
			users = users.order_by('arrival')
			context['sort'] = sort
		if sort=='-arrival' :
			users = users.order_by('-arrival')
			context['sort'] = sort 

	context['nu'] = users
	return render(request, 'DBUnknownUsers.html', context)
