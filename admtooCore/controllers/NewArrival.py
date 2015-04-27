# -*- coding: utf-8 -*-
from .. import models
import logging
logger=logging.getLogger('django')

def associateUserWith (user, newuser_id, request_user=None) :
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
	if user.arrival is None :
		user.arrival = nu.arrival
	if user.departure is None and nu.departure is not None :
		user.departure = nu.departure
	
	# set office if defined
	if user.room is None or user.room.strip() == '' :
		if nu.office is not None :
			user.room = nu.office
		elif nu.other_office is not None and nu.other_office.strip() != '' :
			user.room = nu.other_office
	# set self as an active user
	user.user_state = user.NORMAL_USER
	user.save (request_user=request_user)

	# add command to create directories
	models.userdir.generateDirs (user, request_user)
	
