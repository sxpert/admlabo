# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from ..models import *

import logging
logger=logging.getLogger('django')

def Test (request) :
	logger.error('testing sendMail')
	nu = NewUser.objects.all()[0]
	nu.send_arrival_mail()
	return redirect('dashboard')

