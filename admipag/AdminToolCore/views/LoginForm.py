# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .. import models


import logging
logger=logging.getLogger('django')

@csrf_protect
def LoginForm (request) :
	redirect_to = request.GET.get  ('next','')
	username    = request.POST.get ('username', '')
	password    = request.POST.get ('password', '')
	

	logger.error (request.method)
	error = None
	if username!='' and password!='' :
		user = authenticate(username=username, password=password)
		if user is not None :
			if user.is_active :
				login (request, user)
				return redirect(redirect_to)
			else :
				# user supposedly disabled ?
				pass
		else :
			# invalid login
			error='invalid login'	
	context = {}
	context['action_url']  = request.path+'?'+request.META['QUERY_STRING']
	context['error'] = error

	return render(request, 'login-form.html', context)

