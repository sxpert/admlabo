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
