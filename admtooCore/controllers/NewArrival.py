# -*- coding: utf-8 -*-
from .. import models
import json
import logging
logger=logging.getLogger('django')

def associateUserWith (user, newuser_id, request_user=None, logins=None) :
	# associate nu and self
	nu = models.NewUser.objects.get (pk = newuser_id)
	nu.user = user
	
	# modify nu's names to use the official ones
	if nu.first_name != user.first_name :
		nu.first_name = user.first_name
	if nu.last_name != user.last_name :
		nu.last_name = user.last_name
	nu.save ()
	
	# modify self with infos from nu
	if user.birthdate is None :
		user.birthdate = nu.birthdate
	if user.arrival is None :
		user.arrival = nu.arrival
	if user.departure is None and nu.departure is not None :
		user.departure = nu.departure

	# set the users's class
	if user.userclass is None :
		user.userclass = nu.status
	
	# set office if defined
	if user.room is None or user.room.strip() == '' :
		if nu.office is not None :
			user.room = nu.office.ref
		elif nu.other_office is not None and nu.other_office.strip() != '' :
			user.room = nu.other_office

	# logins
	try :
		appSpecName = json.loads(user.appspecname)
	except ValueError as e :
		appSpecName = {}
	
	logger.error ('appSpecName (before) : '+str(appSpecName))
	
	logger.error ('logins : '+str(logins))
	if logins is not None :
		for k in logins.keys() :
			if appSpecName is None :
				appSpecName = {}
			appSpecName[k] = logins[k]

	user.appspecname = json.dumps(appSpecName)
	logger.error ('appSpecName (after) : '+str(user.appspecname))

	# set self as an active user
	user.user_state = user.NORMAL_USER
	user.save (request_user=request_user)

	# add command to create directories
	models.userdir.generateDirs (user, request_user)
	
