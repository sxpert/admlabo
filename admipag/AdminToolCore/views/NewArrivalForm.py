# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from django.contrib.auth.decorators import login_required

#
# form that is displayed when a person is to be 
# declared
#

@login_required
def NewArrivalForm (request) :
	context = {}
	context['allusers'] = models.User.objects.all()
	context['allcountries'] = models.Country.objects.all()
	context['alluserclasses'] = models.UserClass.objects.all()
	return render(request, 'new-arrival-form.html', context)

