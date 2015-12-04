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
# groups management
#

#
# list of all groups
#
@admin_login
@transaction.atomic
def mailinglist_view (request, ml_id) :
	if request.method == 'POST' :
		logger.error (request.POST)
		action = None
		if 'action' in request.POST :
			action = request.POST['action']
		logger.error (action)
		if action == 'delete' :
			# remove the mailing list in question
			ml = models.MailingList.objects.get(ml_id = ml_id)
			ml.delete (request_user=request.user)
			# return to the mailinglist list
			return redirect ('mailinglist-list')
	ml = models.MailingList.objects.get(ml_id=ml_id)
	context = {
		'ml' : ml
	}
	return render(request, 'mailinglist-view.html', context)

@admin_login
@transaction.atomic
def mailinglist_new (request) :
	ml_id = None
	error = None
	if request.method == 'POST' :
		# find the new ml_id
		if 'ml_id' in request.POST :
			ml_id = request.POST['ml_id']
			if type(ml_id) is unicode :
				pass
			# maybe other types need handled ?
			# try to create the new ml record
			# step 1, check if this ml exists already
			try :
				ml = models.MailingList.objects.get(ml_id=ml_id)
			except models.MailingList.DoesNotExist as e :
				logger.error ('mailing list \''+ml_id+'\' does not exist, creating')
				# step 2 : create new mailing list record
				ml = models.MailingList()
				ml.ml_id = ml_id
				ml.save(request_user=request.user)
				# step 3 : redirect to view mailinglist
				return redirect ('mailinglist-view', ml_id=ml.ml_id)
			else :
				logger.error ('ERROR: ml \''+ml_id+'\' already exists')
				error = 'La mailing list avec ce nom existe déja'
	context = {
		'action' : 'new',
		'error'  : error,  
		'ml'     : {
			'ml_id' : ml_id
		}
	}
	return render(request, 'mailinglist-view.html', context)

#----
# fields functions 

@transaction.atomic
def mailinglist_view_name_field (request, ml_id, action) :
	ml = models.MailingList.objects.get(ml_id=ml_id)
	data = {}
	if ( action == 'value' ) and ( request.method=='POST' ):
		d = json.loads(request.body)
		if 'value' in d.keys() :
			value = d['value']
			ml.rename (value, request_user=request.user)
#			ml.name = value
#			ml.save(request_user=request.user)
	# in all cases, return the contents
	if action in ('value', 'options',) :
		data['value'] = ml.name
	return data

@transaction.atomic
def mailinglist_view_description_field (request, ml_id, action) :
	ml = models.MailingList.objects.get(ml_id=ml_id)
	data = {}
	if ( action == 'value' ) and ( request.method == 'POST' ) :
		d = json.loads(request.body)
		if 'value' in d.keys() :
			value = d['value']
			ml.description = value
			ml.save(request_user=request.user)
	if action in ('value', 'options',) :
		data['value'] = ml.description
	return data

@transaction.atomic
def mailinglist_view_parent_field (request, ml_id, action) :
	ml = models.MailingList.objects.get(ml_id=ml_id)
	data = {}
	if action == 'options' :
		# list all other mailinglists
		mls = {}
		lists = models.MailingList.objects.all ()
		for l in lists :
			mls[l.ml_id] = l.name
		data['options'] = mls
		if ml.parent is not None :
			data['selected'] = ml.parent.ml_id
	elif action == 'value' :
		if request.method == 'POST' :
			d = json.loads(request.body)
			if 'value' in d.keys () :
				value = d['value']
				if value is not None :
					value = models.MailingList.objects.get(ml_id=value)
				ml.parent = value
				ml.save(request_user=request.user)
		if ml.parent is not None :
			data['value'] = ml.parent.name
	return data

@transaction.atomic
def mailinglist_view_group_field (request, ml_id, action) :
	ml = models.MailingList.objects.get(ml_id=ml_id)
	data = {}
	if action == 'options' :
		# list all groups
		gps = {}
		groups = models.Group.objects.all()
		for g in groups :
			gps[g.gidnumber] = g.name
		data['options'] = gps
		if ml.group is not None :
			data['selected'] = ml.group.gidnumber
	elif action == 'value' :
		if request.method == 'POST' :
			d = json.loads (request.body)
			if 'value' in d.keys() :
				value = d['value']
		 		if value is not None :
					value = models.Group.objects.get(gidnumber=value)
				ml.group = value
				ml.save(request_user=request.user)
		if ml.group is not None :
			data['value'] = ml.group.name
	return data	

@transaction.atomic
def mailinglist_view_userclass_field (request, ml_id, action) :
	ml = models.MailingList.objects.get(ml_id=ml_id)
	data = {}
	if action == 'options' :
		# list all userclasses
		uc = {}
		userclasses = models.UserClass.objects.filter(active=True)
		for ucl in userclasses :
			if ucl.fr is None :
				uc[ucl.pk] = ucl.ref
			else :
				uc[ucl.pk] = ucl.fr
		data['options'] = uc
		if ml.userclass is not None :
			data['selected'] = ml.userclass.pk
	elif action == 'value' :
		if request.method == 'POST' :
			d = json.loads (request.body)
			if 'value' in d.keys() :
				value = d['value']
				if value is not None :
					value = models.UserClass.objects.get(pk = value)
				ml.userclass = value
				ml.save(request_user=request.user)
		if ml.userclass is not None :
			if ml.userclass.fr is not None :
				data['value'] = ml.userclass.fr
			else :
				data['value'] = ml.userclass.ref
	return data


#----
# main function
#
@admin_login
@csrf_protect
def mailinglist_view_field (request, ml_id, action, fieldtype, fieldname) :
	data = {}	

	mapping = {
		"select" : {
			"parent"          : mailinglist_view_parent_field,
			"group"           : mailinglist_view_group_field,
			"userclass"       : mailinglist_view_userclass_field,
		},
		"text" : {
			"name"            : mailinglist_view_name_field,
			"description"     : mailinglist_view_description_field,
		},
	}

	if fieldtype in mapping.keys() :
		fields = mapping[fieldtype]
		if fieldname in fields.keys() :
			func = fields[fieldname]
			data = func (request, ml_id, action)	
	
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json')
