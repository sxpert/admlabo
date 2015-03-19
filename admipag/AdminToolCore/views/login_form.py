# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .. import models

import logging
logger=logging.getLogger('django')

def login_form (request) :
	logger.error (request.method)
	return render(request, 'login-form.html')

