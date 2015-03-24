# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout


import logging
logger=logging.getLogger('django')

def LogoutView (request) :
	logger.error('logging out '+request.user.username)
	logout (request)
	return redirect('dashboard')

