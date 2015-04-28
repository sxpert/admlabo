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
	o = NewUser.objects.all()[0]
	nu = dict((key, value) for key, value in o.__dict__.iteritems() if not callable(value) and not key.startswith('__'))
	nu['manager'] = o.manager.full_name
	SendMail.sendMail ('NewArrival', nu)
	return redirect('dashboard')

