# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import models

#==============================================================================
# application dashboard
# 
def dashboard (request) :
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'dashboard.html', context)



#==============================================================================
# users management
#

#
# complete list of active users
#
def users (request) :
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'users.html', context)

#
# user information form
#
def user_view (request, user_id) :
	u = models.User.objects.get(uidnumber = user_id)
	context = {
		'user' : u,
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
				u.save()
		m = u.manager
		if m is not None :
			data['url'] = reverse ('user_view', args=(m.uidnumber,))
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
				u.change_groups (vs)
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
				u.change_managed (values)	
		managed = []
		for user in u.manager_of () :
			udata = {}
			udata['url'] = reverse ('user_view', args=(user.uidnumber,))
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
	if action == 'value':
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'value' in data.keys() :
				value = data['value']
				u.login_shell = value
				u.save()
		data['value'] = u.login_shell
	return data

#----
# main function
#
@csrf_protect
def user_view_field (request, user_id, action, fieldtype, fieldname) :
	data = {}	
	if fieldtype == 'multiselect' :
		if fieldname == 'mailinglists' : 
			data = user_view_mailinglist_field (request, user_id, action)
		if fieldname == 'groups' :
			data = user_view_group_field (request, user_id, action)
		if fieldname == 'managed' :
			data = user_view_managed_field (request, user_id, action)
	if fieldtype == 'select' :
		if fieldname == 'manager' :
			data = user_view_manager_field (request, user_id, action)
	if fieldtype == 'text' :
		if fieldname == 'loginshell' :
			data = user_view_loginshell_field (request, user_id, action) 
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json')

#==============================================================================
# groups management
#

#
# list of all groups
#
@login_required
def groups (request) :
	groups = models.Group.objects.all()
	context = {
		'groups': groups,
	}
	return render(request, 'groups.html', context)

#
# details of one particular group
#
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
				g.save()
		d = g.name
		if d is None : # should not happen
			d = ''
		data['value'] = d
	return data

def group_view_members_field (request, group_id, action) :
	g = models.Group.objects.get(gidnumber=group_id)
	data = {}
	if action=='value' :
		# get current group members
		members = []
		for u in g.members() :
			udata = {}
			udata['url'] = reverse ('user_view', args=(u.uidnumber,))
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
				g.save()
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
				g.save()
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
				g.save()
		d = g.description
		if d is None :
			d = ''
		data['value'] = d
	return data

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
