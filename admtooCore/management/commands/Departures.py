# -*- coding: utf-8 -*-

#
# send mails to people that are about to leave the place in DEPARTURE_ALERT_DAYS
#

import logging
import datetime
import json
from ...plugins import plugins
from ... import models
from django.conf import settings

class Departures (object) :
	def __init__ (self) :
		pass

	def run (self) :
		logging.basicConfig (level=logging.INFO)
		dep_date = datetime.date.today()+datetime.timedelta(-settings.USER_DEPARTURE_WARN)
		logging.info (dep_date)
		for u in models.User.objects.filter(departure__isnull=False) :
			if u.departure == dep_date :
				logging.info (unicode(u.login)+u' '+unicode(u.departure))
				# generates one mail per person
				c = models.Command()
				c.user = '(Departures crontab)'
				c.verb = 'SendMail'
				data = {}
				data['mailconditions'] = ['Departure']
				userdata = {}
				userdata['first_name'] = u.first_name
				userdata['last_name'] = u.last_name
				userdata['email'] = u.mail
				userdata['departure'] = u.departure.isoformat()
				userdata['deactivation'] = (u.departure+datetime.timedelta(settings.USER_DEPARTURE_GONE)).isoformat()
				data['maildata'] = userdata
				logging.info (data)
				c.data = json.dumps(data)
				c.save()

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		d =  Departures()
		d.run()
