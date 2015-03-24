# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from decorators import *

#==============================================================================
# application dashboard
#
@admin_login 
def dashboard (request) :
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'dashboard.html', context)
