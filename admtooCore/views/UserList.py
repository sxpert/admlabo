# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from decorators import *

#
# complete list of active users
#

@admin_login
def users (request) :
	users = models.User.objects.exclude(user_state=models.User.DELETED_USER).order_by('last_name')
	context = {
		'users': users,
	}
	return render(request, 'user-list.html', context)

