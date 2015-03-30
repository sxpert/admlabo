# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings

#
# utility functions
#

# format first or last name


#
# form that is displayed when a person is to be 
# declared
#

import re
DATE_RE = re.compile('\d{4}-\d{2}-\d{2}')

def date_invalid (strdate) :
	try:
		import datetime
		d = datetime.datetime.strptime(strdate, '%Y-%m-%d')
	except ValueError :
		return True
	return False

@login_required
@csrf_protect
def NewArrivalForm (request) :
	# read form contents
	newuser = {}
	errors = {}

	# check all data contents

	#
	manager = request.POST.get('manager')
	if manager is not None :
		manager = int(manager)
	newuser['manager'] = manager

	#
	last_name = request.POST.get('last_name', '').strip()
	if len(last_name) == 0 :
		errors['last_name'] = 'Le nom de famille ne peut être vide'
	newuser['last_name'] = last_name

	#
	first_name = request.POST.get('first_name','').strip()
	if len(first_name) == 0 :
		errors['first_name'] = 'Le prénom ne peut être vide'
	newuser['first_name'] = first_name

	#
	birthdate = request.POST.get('birthdate','').strip()
	if len(birthdate) == 0 :
		errors['birthdate'] = 'La date de naissance ne peut être vide'
	# check date format
	elif DATE_RE.match(birthdate) is None :
		errors['birthdate'] = 'La date de naissance n\'a pas le bon format - yyyy-mm-dd attendu'
	# check date validity
	elif date_invalid (birthdate) :
		errors['birthdate'] = 'La date de naissance est invalide'
	newuser['birthdate'] = birthdate

	#
	

	#
	# generate the form
	context = {}
	context['newuser'] = newuser
	context['errors'] = errors
	context['allusers'] = models.User.objects.all()
	context['DEFAULT_COUNTRY'] = settings.DEFAULT_COUNTRY
	context['allcountries'] = models.Country.objects.all().order_by('citizenship')
	context['alluserclasses'] = models.UserClass.objects.all().order_by('fr')
	context['allteams'] = models.Group.objects.filter(group_type=models.Group.TEAM_GROUP).order_by('name')
	context['alloffices'] = models.Office.objects.all()
	context['allostypes'] = models.NewUser.NEWUSER_OS_CHOICES
	return render(request, 'new-arrival-form.html', context)

