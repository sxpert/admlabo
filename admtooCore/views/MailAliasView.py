# -*- coding: utf-8 -*-

import json
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .. import models
from decorators import *

import logging
logger = logging.getLogger('django_auth_ldap')

#==============================================================================
# mail alias
#

#
# list of all mail aliases
#
@admin_login
@transaction.atomic
def mailalias_view (request, alias) :
	if request.method == 'POST' :
		logger.error (request.POST)
		action = None
		if 'action' in request.POST :
			action = request.POST['action']
		logger.error (action)
		if action == 'delete' :
			# remove the mailing list in question
			ma = models.MailAlias.objects.get(alias = alias)
			ma.delete ()
			# return to the mailinglist list
			return redirect ('mailalias-list')
	ma = models.MailAlias.objects.get(alias=alias)
	context = {
		'ma' : ma
	}
	return render(request, 'mailalias-view.html', context)

#
# creation of a new mail alias
#

@admin_login
@transaction.atomic
def mailalias_new (request) :
	alias = None
	error = None
	if request.method == 'POST' :
		# find the new alias
		if 'alias' in request.POST :
			alias = request.POST['alias']
			if type(alias) is unicode :
				pass
			# maybe other types need handled ?
			# try to create the new ma record
			# step 1, check if this ma exists already
			try :
				ma = models.MailAlias.objects.get(alias=alias)
			except models.MailAlias.DoesNotExist as e :
				logger.error ('mail alias \''+alias+'\' does not exist, creating')
				# step 2 : create new mailing list record
				ma = models.MailAlias()
				ma.alias = alias
				ma.save()
				# step 3 : redirect to view mailinglist
				return redirect ('mailalias-view', alias=ma.alias)
			else :
				logger.error ('ERROR: alias \''+alias+'\' already exists')
				error = 'Un alias de mail avec ce nom existe déja'
	context = {
		'action' : 'new',
		'error'  : error,  
		'ma'     : {
			'alias' : alias
		}
	}
	return render(request, 'mailalias-view.html', context)

#----
# fields functions 

@transaction.atomic
def mailalias_view_description_field (request, alias, action) :
	ma = models.MailAlias.objects.get(alias=alias)
	data = {}
	if ( action == 'value' ) and ( request.method == 'POST' ) :
		d = json.loads(request.body)
		if 'value' in d.keys() :
			value = d['value']
			ma.description = value
			ma.save(request_user=request.user)
	if action in ('value', 'options',) :
		if ma.description is None :
			data['value'] = ''
		else :
			data['value'] = ma.description
	return data

@transaction.atomic
def mailalias_view_mail_field (request, alias, action) :
	ma = models.MailAlias.objects.get(alias=alias)
	data = {}
	if ( action == 'value' ) and ( request.method == 'POST' ) :
		d = json.loads(request.body)
		if 'value' in d.keys() :
			value = d['value']
			ma.mail = value
			ma.save(request_user=request.user)
	if action in ('value', 'options',) :
		if ma.mail is None :
			data['value'] = ''
		else :	
			data['value'] = ma.mail
	return data

#----
# main function
#
@admin_login
@csrf_protect
def mailalias_view_field (request, alias, action, fieldtype, fieldname) :
	data = {}	

	mapping = {
		"text" : {
			"description"     : mailalias_view_description_field,
			"mail"            : mailalias_view_mail_field,
		},
	}

	if fieldtype in mapping.keys() :
		fields = mapping[fieldtype]
		if fieldname in fields.keys() :
			func = fields[fieldname]
			data = func (request, alias, action)	
	
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json')
