# -*- coding: utf-8 -*-

import json
from django.db import transaction, IntegrityError
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
			mdata['url'] = reverse ('mailinglist-view', args=(ml.ml_id,)) 
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
			n = g.name
			if g.is_team_group() :
				n = '[T] '+n
			groups[g.gidnumber] = n
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
			gdata['url'] = reverse ('group-view', args=(g.gidnumber,))
			n = g.name
			if g.is_team_group() :
				n = '[T] '+n
			if g.is_status_group():
				n = '[S] '+n
			gdata['value'] = n
			
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
		data['value'] = models.User.USER_STATE_CHOICES[int(u.user_state)][1]
	return data

#----
# main team field 
#

def user_view_main_team_field (request, userid, action) :
	u = models.User.objects.get(uidnumber = userid)
	data = {}
	if action == 'options' :
		teams = {} 
		for g in u.all_teams() :
			teams[g.gidnumber] = g.description
		data['options'] = teams
		if u.main_team is not None :
			data['selected'] = u.main_team.gidnumber
		else:
			data['selected'] = None
	elif action == 'value' :
		if request.method == 'POST' :
			data = json.loads(request.body)
			if 'value' in data.keys() :
				main_team = data['value']
				if main_team is not None :
					u.main_team = models.Group.objects.get(gidnumber = main_team)
				else :
					u.main_team = None
				u.save()
		if u.main_team is None :
			data['value'] = '<i>No main team</i>';
		else :
			data['value'] = u.main_team.description
	return data

#----
# secondary teams field
#
 
def user_view_secondary_teams_field (request, userid, action) :
	u = models.User.objects.get (uidnumber = userid)
	data = {}
	if action == 'value' :
		t = []
		for g in u.all_teams() :
			if (u.main_team is not None) and (u.main_team.gidnumber != g.gidnumber) :
				t.append ('<li>'+g.description+'</li>')
		s = '<ul>'+''.join(t)+'</ul>\n'
		data['value'] = s
	return data

#----
# mail aliases field
#

@transaction.atomic
def user_view_mail_aliases_field (request, userid, action) :
	data = {}
	logger.error (action)
	u = models.User.objects.get(uidnumber=userid)
	if (action == 'value') and (request.method == 'POST') :
		logger.error ('attempt to change mailaliases')
		reqd = json.loads (request.body)
		logger.error (str(reqd))
		errors = []
		ok = True 
		if 'values' in reqd.keys() : 
			values = reqd['values']
			for v in values :
				logger.error (v)
				# find if v is already used by a different user
				try :
					user = models.MailAlias.objects.get(alias=v).user
				except models.MailAlias.DoesNotExist as e :
					# no problem, that's a new alias
					errors.append (None)
				else :
					# mebbe this is not the same user...
					logger.error (type(user.uidnumber))
					logger.error (type(userid))
					logger.error (str(user.uidnumber)+' '+str(userid))
					if user.uidnumber != int(userid) :
						errors.append('déja utilisé par '+str(user.login))
						ok = False
					else :
						errors.append(None)
			if ok :
				logger.error ('all values are ok, proceeding to update the database')
				# first, remove all aliases not in the new list
				for a in u.UserAliases.all() :
					logger.error (a.alias)
					if a.alias not in values :
						logger.error ('deleting entry')
						a.delete(request_user=request.user)
				# add values not there yet
				for v in values :
					try : 
						alias = models.MailAlias.objects.get(alias=v)
					except models.MailAlias.DoesNotExist as e :
						# add a new entry
						logger.error('alias '+v+' not found, adding to user '+u.login)
						a = models.MailAlias()
						a.alias = v
						a.user = u
						a.save(request_user=request.user)
					else :
						logger.error ('alias '+v+' already exists')
				data['values'] = values
				return data
			data['values'] = values
			data['errors'] = errors
			return data
		else :
			pass
		data['values'] = ('alias1', 'alias2', 'alias3',)
		data['errors'] = (None, 'already used for \'user\'', None,)
		return data
	# !(value & POST)
	logger.error (action)
	# list all values for mailalias that are possible
	al = u.UserAliases.all()
	aliases = []
	# add aliases from the al list to the list
	for a in al :
		if a.alias not in aliases :
			aliases.append (a.alias)
	# check if full name from user email is present, add to list
	if u.mail is not None :
		p = u.mail.find('@')
		if p>=0 :
			alias = u.mail[0:p]
			if alias not in aliases :
				# attempt to push in the mailaliases
				a = models.MailAlias()
				a.alias = alias
				a.user = u
				try :
					a.save(request_user=request.user)
				except IntegrityError as e :
					# ok, forget it...
					pass
				else :
					aliases.append (alias)
		else :
			logger.error ('ERROR: user_view_mail_alias_field : user mail record is badly formed for user '+u.login)
	else:
		logger.error ('ERROR: user_view_mail_alias_field : user '+u.login+' has no email assigned')
	# check if user login is in aliases, add if not
	if u.login not in aliases :
		# attempt to add the login as a mail alias
		a = models.MailAlias()
		a.alias = u.login
		a.user = u
		try :
			a.save(request_user=request.user)
		except IntegrityError as e :
			# there's already a mailalias entry for this...
			pass
		else :
			aliases.append (u.login)
	aliases.sort()
	data['values'] = aliases
	if action == 'options' :
		err = []
		while len(err) < len(aliases) :
			err.append(None)
		data['errors'] = err
	logger.error (data)
	return data

#----
# user class field
#

@transaction.atomic
def user_view_userclass_field (request, userid, action) :
	data = {}
	u = models.User.objects.get(uidnumber=userid)
	if action == 'options' :
		# list all options available
		classes = {}
		for uc in models.UserClass.objects.all() :	
			n = uc.ref
			if uc.fr is not None :
				n = uc.fr
			classes[uc.pk] = n
		data['options'] = classes
		data['noblank'] = True
		if u.userclass is not None :
			data['selected'] = u.userclass.pk
	elif action == 'value' :
		# change the value
		if request.method == 'POST' :
			uc_gidn = None
			if (u.userclass is not None) and (u.userclass.group is not None) :
				uc_gidn = u.userclass.group.gidnumber
			groups = []
			for g in u.unique_groups() :
				# do not add the current userclass to the list
				if uc_gidn != g.gidnumber :	
					groups.append (g.gidnumber)
			reqd = json.loads(request.body)
			# set the new userclass
			if 'value' in reqd :
				uc = models.UserClass.objects.get(pk=int(reqd['value']))
				u.userclass = uc
				if uc.group is not None :
					groups.append(uc.group.gidnumber)
					u.change_groups (groups, request.user)
				u.save(request_user=request.user)
		# get the value
		value = ''
		if u.userclass is not None :
			if u.userclass.fr is not None :
				value = u.userclass.fr
			else:
				value = u.userclass.ref
		data['value'] = value
	else :
		logger.error ("unknown action "+action)
	return data

#----
# main function
#
@admin_login
@csrf_protect
def user_view_field (request, user_id, action, fieldtype, fieldname) :
	data = {}	

	mapping = {
		"multiselect" : {
			"mailinglists"    : user_view_mailinglist_field,
			"groups"          : user_view_group_field,
			"managed"         : user_view_managed_field
		},
		"select" : {
			"userclass"       : user_view_userclass_field,
			"manager"         : user_view_manager_field,
			"user_state"      : user_view_user_state_field,
			"main-team"       : user_view_main_team_field
		},
		"text" : {
			"loginshell"      : user_view_loginshell_field
		},
		"multitext" : {
			"mailaliases"     : user_view_mail_aliases_field
		},
		"display" : {
			"secondary-teams" : user_view_secondary_teams_field
		}
	}

	if fieldtype in mapping.keys() :
		fields = mapping[fieldtype]
		if fieldname in fields.keys() :
			func = fields[fieldname]
			data = func (request, user_id, action)	
	
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json')
