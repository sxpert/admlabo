# -*- coding: utf-8 -*-

#
# base django command line tool object.
#

import logging
from ...models.user import User
from ...plugins import plugins

class PhotoGrabber (object) :
	def __init__ (self) :
		pass

	def run (self) :
		logging.basicConfig (level=logging.INFO)
		a = plugins.Annuaire
		for u in User.objects.all () :
			logging.debug (u.login)
			if a._fetch_photo (u) :
				logging.info (u'picture obtained for user '+unicode(u.login))
			
			


from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		pg =  PhotoGrabber()
		pg.run()
