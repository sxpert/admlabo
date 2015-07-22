# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from decorators import *

#
# complete list of active users
#

@admin_login
def users (request) :
	users = models.User.objects.all().order_by('last_name')
	context = {
		'users': users,
	}
	return render(request, 'users.html', context)

