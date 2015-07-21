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
# groups management
#

#
# list of all groups
#
@admin_login
def groups (request) :
	groups = models.Group.objects.all()
	context = {
		'groups': groups,
	}
	return render(request, 'groups.html', context)

#
# details of one particular group
#
@admin_login
def group_view (request, group_id) :
	g = models.Group.objects.get(gidnumber = group_id)
	context = {
		'group' : g,
	}
	return render(request, 'group-view.html', context)

#------------------------------------------------------------------------------
# 
# ajax bits for group edit
#
#

def group_view_name_field (request, group_id, action) :
	g = models.Group.objects.get(gidnumber=group_id)
	data = {}
	if action == 'options':
		d = g.name
		if d is None : # should not happen
			d = ''
		data['value'] = d
	if action == 'value' :
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'value' in data.keys() :
				value = data['value']
				g.name = value
				g.save(request_user=request.user)
		d = g.name
		if d is None : # should not happen
			d = ''
		data['value'] = d
	return data

def group_view_members_field (request, group_id, action) :
	g = models.Group.objects.get(gidnumber=group_id)
	data = {}
	if action=='options':
		mem = []
		for u in g.members() :
			mem.append (u.uidnumber)
		data['selected'] = mem
		opt = {}
		for u in models.User.objects.all () :
			opt[u.uidnumber] = u.full_name()
		data['options'] = opt
	if action=='value' :
		# TODO: post action
		if request.method == 'POST': 
			data = json.loads(request.body)
			if 'values' in data.keys() :
				values = data['values']
				g.set_members (values, request.user)
		# get current group members
		members = []
		for u in g.members() :
			udata = {}
			udata['url'] = reverse ('user-view', args=(u.uidnumber,))
			udata['value'] = u.full_name()
			members.append(udata)
		data['values'] = members		
	return data

def group_view_type_field (request, group_id, action) :
	g = models.Group.objects.get(gidnumber=group_id) 
	data = {}
	if action == 'options' :
		data['selected'] = g.group_type
		opt = {}
		for c in g.GROUP_TYPES_CHOICES :
			k, v = c
			opt[k] = v
		data['options'] = opt
		data['noblank'] = True
	if action == 'value' :
		if request.method == 'POST': 
			data = json.loads(request.body)
			if 'value' in data.keys() :
				value = data['value']
				g.group_type = int(value)
				g.save(request_user=request.user)
		data['value'] = g.GROUP_TYPES_CHOICES[g.group_type][1]
	return data

def group_view_parent_field (request, group_id, action) :
	g = models.Group.objects.get(gidnumber=group_id) 
	data = {}
	if action == 'options' :
		if g.parent is not None :
			data['selected'] = g.parent.gidnumber
		else :
			data['selected'] = None
		groups = {}
		for g in models.Group.objects.all () :
			groups[g.gidnumber] = g.name
		data['options'] = groups
	if action == 'value' :
		if request.method == 'POST' :
			# change parent
			data = json.loads(request.body)
			if 'value' in data.keys() :
				value = data['value']
				if value is not None :
					p = models.Group.objects.get(gidnumber=int(value))
				else :	
					p = None
				g.parent = p
				g.save(request_user=request.user)
			pass
		if g.parent is not None :
			d = g.parent.name
			u = reverse ('group_view', args=(g.parent.gidnumber,))
		else :
			d = ''
			u = None
		data['value'] = d
		data['url'] = u
	return data

def group_view_description_field (request, group_id, action) :
	g = models.Group.objects.get(gidnumber=group_id)
	data = {}
	if action == 'options':
		d = g.description
		if d is None :
			d = ''
		data['value'] = d
	if action == 'value' :
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'value' in data.keys() :
				value = data['value']
				g.description = value
				g.save(request_user=request.user)
		d = g.description
		if d is None :
			d = ''
		data['value'] = d
	return data

@admin_login
@csrf_protect
def group_view_field (request, group_id, action, fieldtype, fieldname) :
	data = {}
	if fieldtype == 'multiselect' :
		if fieldname == 'members' :
			data = group_view_members_field (request, group_id, action)
	if fieldtype == 'select' :
		if fieldname == 'group-type': 
			data = group_view_type_field (request, group_id, action)
		if fieldname == 'parent' :
			data = group_view_parent_field (request, group_id, action) 
	if fieldtype == 'text' :
		if fieldname == 'name' :
			data = group_view_name_field (request, group_id, action)
		if fieldname == 'description' :
			data = group_view_description_field (request, group_id, action)
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json') 


#==============================================================================
# mailing lists management
#

def mailinglist_view (request, ml_id) :
	pass
