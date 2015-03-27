# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from django.contrib.auth.decorators import login_required
from django.conf import settings
#
# form that is displayed when a person is to be 
# declared
#

@login_required
def NewArrivalForm (request) :
	context = {}
	users = models.User.objects.all()
	context['allusers'] = users
	context['DEFAULT_COUNTRY'] = settings.DEFAULT_COUNTRY
	context['allcountries'] = models.Country.objects.all().order_by('citizenship')
	context['alluserclasses'] = models.UserClass.objects.all()
	context['allteams'] = models.Group.objects.filter(group_type=models.Group.TEAM_GROUP).order_by('name')
	offices = []
	for u in users.order_by('room') :
		if u.room is not None  and u.room not in offices :
			offices.append (u.room)
	context['alloffices'] = offices
	return render(request, 'new-arrival-form.html', context)

