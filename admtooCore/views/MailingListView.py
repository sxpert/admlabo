# -*- coding: utf-8 -*-

import json
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
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
def mailinglist_view (request, ml_id) :
	ml = models.MailingList.objects.get(ml_id=ml_id)
	context = {
		'ml' : ml
	}
	return render(request, 'mailinglist-view.html', context)

@admin_login
def mailinglist_new (request) :
	context = {}
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
			ml.name = value
			#ml.save(request_user=request.user)
			ml.save()
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
			#ml.save(request_user=request.user)
			ml.save()
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
				ml.save()
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
				ml.save()
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
		userclasses = models.UserClass.objects.all ()
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
				ml.save()
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
