# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
import admtooCore.models as models
from admtooLib import AdminFunctions as af

from dns import resolver, reversename
import logging
logger=logging.getLogger('django')

#==============================================================================
# get user info, used by the installation system
#
def GetUserInfo (request, uid) :
	logger.error (uid)
	
	try :
		u = models.User.objects.get(login=uid)
	except models.User.DoesNotExist as e :
		return HttpResponseNotFound(uid)
	
	data = {}
	data['uid'] = u.login
	data['uidNumber'] = u.uidnumber
	data['gidNumber'] = u.group.gidnumber
	data['gecos'] = u.full_name()
	data['loginShell'] = u.login_shell
	data['email'] = u.mail
	groups = {}
	for g in u.all_groups() :
		groups[g.name] = g.gidnumber
	data['groups'] = groups
	return JsonResponse(data)

#==============================================================================
# application dashboard
#
def SetupBackupPC (request) :
	name = False
	if 'HTTP_X_FORWARDED_FOR' in request.META :
		# one or multiple ips. for now, consider one ip
		ip = request.META['HTTP_X_FORWARDED_FOR']
		logger.error (ip)
		# get the PTR for that ip
		rname = reversename.from_address (ip)
		logger.error (rname)
		name = resolver.query (rname, 'PTR')
		# we should only have 1 object
		l = len(name)
		if l != 1 :
			msg = 'problem, we have '+str(l)+' answers'
			logger.error (msg)
			return HttpResponse ('NOK: '+msg, 'text/plain', 412)

		name = str(name[0])
		if name[-1] == '.':
			name = name[:-1]
		logger.error (name)
	else :
		# other case, ip direcly accessible ?
		pass
	# at this point name should not be False
	if type(name) is bool :
		msg = 'FATAL: we don\'t have a machine name to muck with...'
		logger.error (msg)
		return HttpResponse ('NOK: '+msg, 'text/plain', 412)

	# find user
	m = models.Machine.objects.get (default_name__fqdn=name)
	logger.error (m)
	if m.owner is None :
		# problem with owner
		msg = 'FATAL: unable to find owner for machine '+name
		logger.error (msg)
		return HttpResponse ('NOK: '+msg, 'text/plain', 412)

	user = m.owner.login
	logger.error (user)
	
	os = request.GET.get('os',None)
	if os is not None :
		if os == 'WINDOWS' :
			os = af.MTYPE_WINDOWS
		elif os == 'LINUX' :
			os = af.MTYPE_LINUX
		elif os == 'MACOS' :
			os = af.MTYPE_MACOS
		else :
			msg = 'FATAL: unknown os type, expected one of WINDOWS, LINUX, MACOS'
			logger.error (msg)
			return HttpResponse ('NOK: '+msg, 'text/plain', 412)
	else :
		msg = 'FATAL: os needs to be specified for now, expected one of WINDOWS, LINUX, MACOS'
		logger.error (msg)
		return HttpResponse ('NOK: '+msg, 'text/plain', 412)
	
	logger.error (os)

	passwd = af.setupBackupPc (name, user, os)
	
	if type(passwd) is bool :
		# problem 
		return HttpResponse ('NOK: '+msg, 'text/plain', 412)

	return HttpResponse (passwd, 'text/plain')
