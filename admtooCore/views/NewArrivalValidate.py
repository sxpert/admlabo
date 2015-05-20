# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .. import models
from decorators import admin_login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .. import transforms

import logging
logger=logging.getLogger('django')

#
# form that allows validating a new arrival 
#

@admin_login
@csrf_protect
def NewArrivalValidate (request, newuser_id) :
	error = None
	if request.method == 'POST' :
		action = request.POST.get('action', None)
		ldap_user = request.POST.get('ldap_user','')
		logger.error (str(action) + " - " + str(ldap_user))
		if (action is not None) and (action == 'associate') :
			try : 
				ldap_user = int(ldap_user)
			except ValueError as e:
				error = 'Probleme dans la transaction'
				logger.error ('error with ldap_user value \''+ldap_user+'\'')
			else :
				# do stuff with user data
				u = models.User.objects.get(uidnumber = ldap_user)
				# handle the twiki login
				logins = {}
				twiki_account = request.POST.get('twiki-account',None)
				if twiki_account is not None :
					logins['twiki'] = twiki_account
				from .. import controllers
				controllers.associateUserWith(u, newuser_id, request.user, logins)
				# everything went well, redirect to user.
				logger.error ('redirecting to user view '+str(ldap_user))
				return redirect('user-view', user_id=ldap_user)
		# fallthrough if problems with the transaction
	context = {}
	if error is not None :
		context['error'] = error
	context['newuser_id'] = newuser_id
	nu = models.NewUser.objects.get(pk=newuser_id)
	# can we find a corresponding user ?
	logger.error ('looking for matching user')
	if nu.user is None :
		
		try :
			# bilateral transforms only work for django 1.8 or later
			import django
			if (django.VERSION[0] >= 1) and (django.VERSION[1]<8) :
				fn = nu.first_name.upper()
				ln = nu.last_name.upper()
			else:
				fn = nu.first_name
				ln = nu.last_name
			u = models.User.objects.get(first_name__upper=fn, last_name__upper=ln)
		except models.User.DoesNotExist as e :
			logger.error ('unable to find user matching '+str(nu))
			pass
		else :
			nu.user = u
			nu.save ()
			# reload nu after save
			logger.error ('found '+str(nu.user)+' matching '+str(nu))
	else :
		logger.error ('nu.user for '+str(nu)+' is not None')
	# add the new user to the context
	context['nu'] = nu
	context['users'] = models.User.objects.filter(user_state=models.User.NEWIMPORT_USER)
	return render(request, 'new-arrival-validate.html', context)

@admin_login
@csrf_protect
def NewArrivalValidateUserInfo (request, user_id) :
	context = {}
	try :
		context['u'] = models.User.objects.get(uidnumber=user_id)
	except User.DoesNotExist as e :
		context['u'] = None
	return render(request, 'new-arrival-validate-user-info.html', context)
