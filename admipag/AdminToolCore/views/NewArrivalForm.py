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
	context['allusers'] = models.User.objects.all()
	context['DEFAULT_COUNTRY'] = settings.DEFAULT_COUNTRY
	context['allcountries'] = models.Country.objects.all().order_by('citizenship')
	context['alluserclasses'] = models.UserClass.objects.all().order_by('fr')
	context['allteams'] = models.Group.objects.filter(group_type=models.Group.TEAM_GROUP).order_by('name')
	context['alloffices'] = models.Office.objects.all()
	context['allostypes'] = models.NewUser.NEWUSER_OS_CHOICES
	return render(request, 'new-arrival-form.html', context)

