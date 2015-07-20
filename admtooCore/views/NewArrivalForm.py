# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
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

def analyze_radio (radio) :
	if len(radio)==0 :
		return None
	if radio=='0':
		return False
	if radio=='1':
		return True
	return None

@login_required
@csrf_protect
def NewArrivalForm (request) :
	# read form contents
	newuser = {}
	errors = {}

	# check all data contents
	if request.method == 'POST':

		#======================================================================
		#
		
		#
		manager = request.POST.get('manager')
		if manager is not None :
			manager = int(manager)
		newuser['manager'] = manager

		#======================================================================
		#
		
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
		external_email = request.POST.get('external_email', '').strip()
		if len(external_email) == 0 :
			errors['external_email'] = 'L\'email externe ne peut être vide'
		elif external_email.count('@') != 1 :
			errors['external_email'] = 'L\'email externe ne peut contenir qu\'une fois le symbole \'@\''
		# on peut tester si le domaine existe...
		newuser['external_email'] = external_email
		
		#
		citizenship = request.POST.get('citizenship', '').strip()
		if len(citizenship) == 0 :
			errors['citizenship'] = 'La nationalité ne peut être vide'
		# on peut vérifier l'existence du code pays dans la table idoine
		newuser['citizenship'] = citizenship
	
		#
		status = request.POST.get('status', '').strip()
		if len(status) == 0 : # can't happen
			errors['status'] = 'Le statut au sein de l\'IPAG ne peut être vide'
		# on peut vérifier qu'on a un entier
		try :
			status = int(status)
		except ValueError as e:
			pass
		newuser['status'] = status
	
		# 
		study_level = request.POST.get('study_level', '').strip()
		# check if status is probie
		if models.UserClass.objects.get(pk=status).probie :
			if len(study_level) == 0:
				errors['study_level'] = 'Le niveau d\'étude ne peut être vide pour un stagiaire'
		newuser['study_level'] = study_level
	
		#
		ujf_student = request.POST.get('ujf_student', '').strip()
		# default to false
		if ujf_student == '' :
			ujf_student = '0'
		# should be "0" or "1"
		newuser['ujf_student'] = ujf_student

		#
		team = request.POST.get('team', '').strip()
		# should be a number < 2^32 
		try:
			team = int(team)
		except ValueError as e:
			pass
		newuser['team'] = team
	
		#
		office = request.POST.get('office', '').strip()
		# should get a valid office reference
		newuser['office'] = office
	
		#
		other_office = request.POST.get('other_office', '').strip()
		if len(office)==0 and len(other_office)==0 :
			errors['other_office'] = 'Ce champ ne peut être vide quand le bureau sélectionné est \'Autre\''
		newuser['other_office'] = other_office

		#======================================================================
		#

		#
		arrival = request.POST.get('arrival', '').strip()
		if len(arrival)==0 :
			errors['arrival'] = 'La date d\'arrivée ne peut être vide'
		# check date format
		elif DATE_RE.match(arrival) is None :
			errors['arrival'] = 'La date d\'arrivée n\'a pas le bon format - yyyy-mm-dd attendu'
		# check date validity
		elif date_invalid (arrival) :
			errors['arrival'] = 'La date d\'arrivée est invalide'
		newuser['arrival'] = arrival
		
		#
		departure = request.POST.get('departure', '').strip()
		if len(departure)==0 :
			pass
		# check date format
		elif DATE_RE.match(departure) is None :
			errors['departure'] = 'La date de départ n\'a pas le bon format - yyyy-mm-dd attendu'
		# check date validity
		elif date_invalid (departure) :
			errors['departure'] = 'La date de départ est invalide'
		newuser['departure'] = departure

		#======================================================================
		#
		
		#
		comp_account = request.POST.get('comp_account', '').strip()
		# should be "0" or "1"
		if len(comp_account)==0 :
			errors['comp_account'] = 'Une option doit être sélectionnée'
		newuser['comp_account'] = comp_account

		#
		os_type = request.POST.get('os_type', '').strip()
		if len(os_type) == 0 :
			errors['os_type'] = "Le type de station de travail ne peut être vide"
		try :
			os_type = int(os_type)
		except ValueError as e:
			pass
		newuser['os_type'] = os_type
	
		#
		specific_os = request.POST.get('specific_os', '').strip()
		newuser['specific_os'] = specific_os

		#
		comp_purchase = request.POST.get('comp_purchase', '').strip()
		# should be "0" or "1"
		if comp_account == '0' :
			comp_purchase = '0'
		if len(comp_purchase)==0 :
			errors['comp_purchase'] = 'Une option doit être sélectionnée'
		newuser['comp_purchase'] = comp_purchase

		#======================================================================
		#
		
		#
		ir_lab = request.POST.get('ir_lab', '').strip()
		# should be "0" or "1"
		if len(ir_lab)==0 :
			errors['ir_lab'] = 'Une option doit être sélectionnée'
		newuser['ir_lab'] = ir_lab

		#
		workshop = request.POST.get('workshop', '').strip()
		# should be "0" or "1"
		if len(workshop)==0 :
			errors['workshop'] = 'Une option doit être sélectionnée'
		newuser['workshop'] = workshop

		#
		chem_lab = request.POST.get('chem_lab', '').strip()
		# should be "0" or "1"
		if len(chem_lab)==0 :
			errors['chem_lab'] = 'Une option doit être sélectionnée'
		newuser['chem_lab'] = chem_lab

		#======================================================================
		#
		
		#
		risky_activity = request.POST.get('risky_activity', '').strip()
		# should be "0" or "1"
		if len(risky_activity)==0 :
			errors['risky_activity'] = 'Une option doit être sélectionnée'
		newuser['risky_activity'] = risky_activity
		
		#======================================================================
		#
		
		# 
		comments = request.POST.get('comments', '').strip()
		newuser['comments'] = comments

		if len(errors.keys()) == 0 :
			nu = models.NewUser ()
			#
			nu.manager =        models.User.objects.get(uidnumber = manager)
			#
			nu.last_name =      last_name
			nu.first_name =     first_name
			nu.birthdate =      birthdate
			nu.external_email = external_email
			nu.citizenship =    models.Country.objects.get(iso2 = citizenship)
			nu.status =         models.UserClass.objects.get(pk = status)
			nu.study_level =    study_level
			nu.ujf_student =    analyze_radio(ujf_student)
			nu.team =           models.Group.objects.get(gidnumber = team)
			try :
				officeref = models.Office.objects.get(ref = office)
			except models.Office.DoesNotExist as e:
				officeref = None
			nu.office =         officeref         
			nu.other_office =   other_office
			#
			nu.arrival =        arrival
			nu.departure =      departure
			#
			nu.comp_account =   analyze_radio(comp_account)
			nu.os_type =        os_type
			nu.specific_os =    specific_os
			nu.comp_purchase =  analyze_radio(comp_purchase)
			#
			nu.ir_lab =         analyze_radio(ir_lab)
			nu.workshop =       analyze_radio(workshop)
			nu.chem_lab =       analyze_radio(chem_lab)
			#
			nu.risky_activity = analyze_radio(risky_activity)
			#
			nu.comments =       comments

			try :
				u = User.objects.get(first_name=nu.first_name, last_name=nu.last_name)
			except User.DoesNotExist as e :
				# can't find corresponding new user...
				pass
			except User.MultipleObjectsReturned as e:
				# too many answers
				pass
			else :
				# apply automatic matching to the new user 
				nu.user = u

			nu.save ()

			# call send mail controller
			nu.send_arrival_mail ()	
			return redirect ('dashboard')		

	#
	# generate the form
	context = {}
	context['newuser'] = newuser
	context['errors'] = errors
	context['error_count'] = len(errors.keys())
	context['allusers'] = models.User.objects.all()
	context['DEFAULT_COUNTRY'] = settings.DEFAULT_COUNTRY
	context['allcountries'] = models.Country.objects.all().order_by('citizenship')
	context['alluserclasses'] = models.UserClass.objects.all().order_by('fr')
	context['allteams'] = models.Group.objects.filter(group_type=models.Group.TEAM_GROUP).order_by('name')
	context['alloffices'] = models.Office.objects.all()
	context['allostypes'] = models.NewUser.NEWUSER_OS_CHOICES
	return render(request, 'new-arrival-form.html', context)

