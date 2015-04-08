# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .. import models
from decorators import admin_login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings

#
# utility functions
#

# format first or last name


#
# form that allows validating a new arrival 
#

@admin_login
@csrf_protect
def NewArrivalValidate (request, newuser_id) :
	context = {}
	context['newuser_id'] = newuser_id
	context['nu'] = models.NewUser.objects.get(pk=newuser_id)
	return render(request, 'new-arrival-validate.html', context)

