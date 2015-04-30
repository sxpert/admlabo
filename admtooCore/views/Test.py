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
	from ..controllers import SendMail
	nu={}
	nu['newuser'] = NewUser.objects.all()[0]
	SendMail.sendMail ('NewArrival', nu)
	return redirect('dashboard')

