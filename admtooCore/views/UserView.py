# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .. import models
from decorators import *

import logging
logger = logging.getLogger('django_auth_ldap')

#==============================================================================
# users management
#

#
# user information form
#
@admin_login
def user_view (request, user_id) :
	u = models.User.objects.get(uidnumber = user_id)
	context = {
		'edited_user' : u,
	}
	return render(request, 'user-view.html', context)

#------------------------------------------------------------------------------
# 
# ajax bits for user edit
#
#

#----
# manager
#
def user_view_manager_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid)
	data = {}
	if action == 'options' :
		# list all possible managers
		managers = {}
		for m in models.User.objects.all() :
			managers[m.uidnumber] = m.first_name+' '+m.last_name
		data['options'] = managers
		# add currently selected manager
		if u.manager is not None :
			data['selected'] = u.manager.uidnumber
		else :
			data['selected'] = None
	if action == 'value' :
		# save manager
		if request.method == 'POST':
			data = json.loads(request.body)
			if 'value' in data.keys() :
				manager = data['value']
				if manager is not None :
					m = models.User.objects.get(uidnumber = manager)
				else :	
					m = None
				u.manager = m
				u.save(request_user=request.user)
		m = u.manager
		if m is not None :
			data['url'] = reverse ('user-view', args=(m.uidnumber,))
			data['value'] = m.first_name+' '+m.last_name
		else :
			data = {}
	return data

#----
# mailing lists
# TODO: just display things, nothing to edit
# 
def user_view_mailinglist_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid)
	data = {}
	if action == 'options' :
		mls = {}
		for ml in models.MailingList.objects.all() :
			mls[ml.ml_id] = ml.name
		data['options'] = mls
		selected = []
		for ml in u.all_mailinglists() :
			selected.append(ml.ml_id)
		data['selected'] = selected
	if action == 'value' :
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'values' in data.keys() :
				values = data['values']
				u.change_mailinglists (values)
		mls = []
		for ml in u.all_mailinglists() :
			mdata = {}
			mdata['url'] = reverse ('mailinglist_view', args=(ml.ml_id,)) 
			mdata['value'] = ml.name
			mls.append(mdata)
		data['values'] = mls
	return data

#----
# group
#
def user_view_group_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid)
	data = {}
	if action == 'options' :
		groups = {}
		for g in models.Group.objects.all() :
			groups[g.gidnumber] = g.name
		data['options'] = groups
		selected = []
		for g in u.all_groups() :
			selected.append(g.gidnumber)
		data['selected'] = selected
	if action == 'value' :
		# save groups
		if request.method == 'POST':
			data = json.loads(request.body)
			if 'values' in data.keys() :
				values = data['values']
				# values come in as strings
				vs = []
				for v in values :
					vs.append(int(v))
				u.change_groups (vs, request.user)
		# get current groups
		groups = []
		for g in u.all_groups() :
			gdata = {}
			gdata['url'] = reverse ('group_view', args=(g.gidnumber,))
			gdata['value'] = g.name
			groups.append(gdata)
		data['values'] = groups
	return data

#----
# managed
#
def user_view_managed_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid)
	data = {}
	if action == 'options' :
		users = {}
		for user in models.User.objects.all () :
			users[user.uidnumber] = user.first_name+' '+user.last_name
		data['options'] = users
		selected = []
		for user in u.manager_of () :
			selected.append (user.uidnumber)
		data['selected'] = selected
	if action == 'value' :
		# save managers
		if request.method == 'POST':
			data = json.loads(request.body)
			if 'values' in data.keys () :
				values = data['values']
				u.change_managed (values, request.user)	
		managed = []
		for user in u.manager_of () :
			udata = {}
			udata['url'] = reverse ('user-view', args=(user.uidnumber,))
			udata['value'] = user.first_name+' '+user.last_name
			managed.append (udata)
		data['values'] = managed
	return data

#----
# loginshell
#

def user_view_loginshell_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid) 
	data = {}
	if action == 'options':
		data['value'] = u.login_shell
	elif action == 'value':
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'value' in data.keys() :
				value = data['value']
				u.login_shell = value
				u.save(request_user=request.user)
		data['value'] = u.login_shell
	return data

#----
# user_state
#

def user_view_user_state_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid)
	data = {}
	if action == 'options' :
		states = {}
		for v, d in models.User.USER_STATE_CHOICES :	
			states[v] = d			
		data['options'] = states
		if u.user_state is not None :
			data['noblank'] = True
			data['selected'] = u.user_state
		else :
			# should not happen !
			data['selected'] = None
	elif action == 'value' :
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'value' in data.keys() :
				user_state = data['value']
				u.user_state = user_state
				u.save(request_user=request.user)
		data['value'] = models.User.USER_STATE_CHOICES[u.user_state][1]
	return data

#----
# 
#

def user_view_main_team_field (request, userid, action) :
	
	pass

#----
# main function
#
@admin_login
@csrf_protect
def user_view_field (request, user_id, action, fieldtype, fieldname) :
	data = {}	

	mapping = {
		"multiselect" : {
			"mailinglists" : user_view_mailinglist_field,
			"groups"       : user_view_group_field,
			"managed"      : user_view_managed_field
		},
		"select" : {
			"manager"      : user_view_manager_field,
			"user_state"   : user_view_user_state_field
		},
		"text" : {
			"loginshell"   : user_view_loginshell_field
		}
	}

	if fieldtype in mapping.keys() :
		fields = mapping[fieldtype]
		if fieldname in fields.keys() :
			func = fields[fieldname]
			data = func (request, user_id, action)	
	
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json')
