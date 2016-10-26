# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .. import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
#
# utility functions
#

# format first or last name


#
# form that is displayed when a person is to be 
# declared
#

import math
import re
import datetime
DATE_RE = re.compile('\d{4}-\d{2}-\d{2}')

def date_invalid (strdate) :
	try:
		d = datetime.datetime.strptime(strdate, '%Y-%m-%d')
	except ValueError :
		return True
	return False

def period_duration (start, finish) :
	try: 
		s = datetime.datetime.strptime(start, '%Y-%m-%d')
		f = datetime.datetime.strptime(finish, '%Y-%m-%d')
	except ValueError as e:
		return None
	td = f - s 
	return td.days

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

	other_office_max_length = models.NewUser._meta.get_field('other_office').max_length

	# read form contents
	newuser = {}
	errors = {}

	# check all data contents
	if request.method == 'POST':

		#======================================================================
		#
		
		#
	except ValueError as e:
		return None	manager = request.POST.get('manager')
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
		# test person's age
		else :
			bd = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
			age = datetime.datetime.today() - bd
			year_length = 365.25
			months_per_year = 12
			month_length = year_length / months_per_year
			age_years = age.days / year_length
			age_months = math.fmod (age.days / month_length, months_per_year)
			age_days = math.fmod (age.days,  month_length)
			age_years = int(math.floor(age_years))
			age_months = int(math.floor (age_months))
			age_days = int(math.floor (age_days))
			#errors['birthdate'] = str(age_years)+' '+str(age_months)+' '+str(age_days)
			try :
				min_age = USER_MIN_AGE
			except NameError as e :
				# log warning
				logger.error ('unable to find \'USER_MIN_AGE\' variable in settings, using default value')
				min_age = 18
			if age_years < min_age :
				u = str(request.user) 
				#if u == 'heriquea' :
				#	age_arr = []
				#	if age_years > 0 :
				#		if age_years == 1 :
				#			age_arr.append (str(age_years)+' an')
				#		else :
				#			age_arr.append (str(age_years)+' ans')
				#	if age_months > 0 :
				#		age_arr.append (str(age_months)+' mois')
				#	if age_days > 0 :
				#		if age_days == 1 :
				#			age_arr.append (str(age_days)+' jour')
				#		else :
				#			age_arr.append (str(age_days)+' jours')
				#	if len(age_arr) == 1:
				#		age_str = age_arr[0]
				#	elif len(age_arr) == 2 :
				#		age_str = age_arr[0]+' et '+age_arr[1]
				#	else :
				#		age_str = age_arr[0]+', '+age_arr[1]+' et '+age_arr[2]
				#	errors['birthdate'] = 'Non Alain, ton nouvel arrivant ne peut pas être agé de seulement '+age_str+'. Il doît etre majeur !!'

				errors['birthdate'] = 'la date de naissance est invalide, l\'utilisateur doit être majeur' 
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
		# should not happen
		if len(other_office)>other_office_max_length :
			errors['other_office'] = 'Valeur trop longue, '+str(other_office_max_length)+' maximum'
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
			departure = None
			pass
		# check date format
		elif DATE_RE.match(departure) is None :
			errors['departure'] = 'La date de départ n\'a pas le bon format - yyyy-mm-dd attendu'
		# check date validity
		elif date_invalid (departure) :
			errors['departure'] = 'La date de départ est invalide'
		newuser['departure'] = departure

		#======================================================================
		# building access
	
		obs_a = request.POST.get('obs_a', '').strip()
		if len(obs_a) > 0 and obs_a == 'on' :
			obs_a = True
		else :
			obs_a = False
		newuser['obs_a'] = obs_a

		phy_d = request.POST.get('phy_d', '').strip()
		if len(phy_d) > 0 and phy_d == 'on' :
			phy_d = True
		else :
			phy_d = False
		newuser['phy_d'] = phy_d
	
		osug_d = request.POST.get('osug_d', '').strip()
		if len(osug_d) > 0 and osug_d == 'on' :
			osug_d = True
		else :
			osug_d = False
		newuser['osug_d'] = osug_d
		
		if not ( obs_a or phy_d or osug_d) :
			errors['access'] = 'Au moins une des 3 options doit être sélectionnée'

		#======================================================================
		#

		if (arrival is not None) and (arrival != '') and (departure is not None) and (departure != '') :
			duration = period_duration (arrival, departure)
		else :
			duration = None

		if duration is not None and duration < 21 :

			comp_account = '0'
			os_type = '0'
			specific_os = ''
			os_lang = '0'
			comp_purchase = '0'

		else : 

			#
			comp_account = request.POST.get('comp_account', '').strip()
			# should be "0" or "1"
			if len(comp_account)==0 :
				errors['comp_account'] = 'Une option doit être sélectionnée'

			#
			os_type = request.POST.get('os_type', '').strip()
			if len(os_type) == 0 :
				errors['os_type'] = "Le type de station de travail ne peut être vide"
			try :
				os_type = int(os_type)
			except ValueError as e:
				pass
	
			#
			specific_os = request.POST.get('specific_os', '').strip()

			#
			os_lang = request.POST.get('os_lang', '').strip()
			if len(os_lang) == 0 :
				errors['os_lang'] = "La langue de la station de travail ne peut être vide"
			try :
				os_lang = int(os_lang)
			except ValueError as e :
				pass

			#
			comp_purchase = request.POST.get('comp_purchase', '').strip()
			# should be "0" or "1"
			if comp_account == '0' :
				comp_purchase = '0'
			if len(comp_purchase)==0 :
				errors['comp_purchase'] = 'Une option doit être sélectionnée'

		newuser['comp_account'] = comp_account
		newuser['os_type'] = os_type
		newuser['specific_os'] = specific_os
		newuser['os_lang'] = os_lang
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
			nu.obs_a =          obs_a
			nu.phy_d =          phy_d
			nu.osug_d =         osug_d
			#
			nu.comp_account =   analyze_radio(comp_account)
			nu.os_type =        os_type
			nu.specific_os =    specific_os
			nu.os_lang =        os_lang
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
				user = models.User.objects.get(first_name=first_name, last_name=last_name)
			except models.User.DoesNotExist as e :
				# can't find corresponding new user...
				pass
			except models.User.MultipleObjectsReturned as e:
				# too many answers
				pass
			else :
				# apply automatic matching to the new user 
				nu.user = user
				nu.send_match_mail(request_user=request.user)				

			nu.save ()

			# call send mail controller
			nu.send_arrival_mail (request_user=request.user)	
		
			return redirect ('dashboard')		

	#
	# generate the form
	context = {}
	context['newuser'] = newuser
	context['other_office_max_length'] = other_office_max_length
	context['errors'] = errors
	context['error_count'] = len(errors.keys())
	context['allusers'] = models.User.objects.all()
	context['DEFAULT_COUNTRY'] = settings.DEFAULT_COUNTRY
	context['allcountries'] = models.Country.objects.all().order_by('citizenship')
	context['alluserclasses'] = models.UserClass.objects.filter(active=True).order_by('fr')
	context['allteams'] = models.Group.objects.filter(group_type=models.Group.TEAM_GROUP).order_by('name')
	context['alloffices'] = models.Office.objects.all()
	context['allostypes'] = models.NewUser.NEWUSER_OS_CHOICES
	context['alloslangs'] = models.NewUser.NEWUSER_OS_LANG_CHOICES
	return render(request, 'new-arrival-form.html', context)

