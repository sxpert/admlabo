# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render, redirect
from .. import models
from django.contrib.auth.decorators import login_required
from decorators import *

import logging
logger=logging.getLogger('django')

#==============================================================================
# application dashboard
#
@login_required
def Dashboard (request) :
	admin = is_admin(request.user)
	logger.error (u"DASHBOARD : "+unicode(request.user)+u' '+unicode(admin))
	if not admin :
		logger.error ('user is not staff')
		logger.error ('redirecting to new arrival form')
		return redirect ('new-arrival-form')
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'dashboard.html', context)

#==============================================================================
# Dashboard bits
# 

#
# list of newly declared users not yet taken care of
#
@admin_login
def DBNewArrivals (request) :
	newusers = models.NewUser.objects.filter(Q(user__user_state=models.User.NEWIMPORT_USER)|Q(user__isnull=True)).order_by('arrival')
	context = {
		'nu' : newusers,
	}
	return render(request, 'DBNewArrivals.html', context)

#
# list of users newly imported from Agalan LDAP
#
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

#
# List of machines that have to be reclaimed from users that are gone
# 
@admin_login
def DBReclaimMachines (request) :
	import datetime
	machines = models.Machine.objects.filter(
		Q(owner__user_state=models.User.DELETED_USER)|
		Q(owner__departure__lte=datetime.datetime.today()),
		owner__departure__isnull=False)
	machines = machines.order_by('owner__departure')

	context = {}
	context['m'] = machines
	return render(request, 'DBReclaimMachines.html', context)
