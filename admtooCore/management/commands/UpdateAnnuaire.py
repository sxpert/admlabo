# -*- coding: utf-8 -*-

#
# base django command line tool object.
#

class UpdateAnnuaire (object) :
	def __init__ (self) :
		pass

	def run (self) :
		from ...plugins import plugins
		a = plugins.Annuaire
		a.AnnuaireUpdate ()
		t = plugins.TWiki
		t.UpdateKiFeKoi()


from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		ta =  UpdateAnnuaire()
		ta.run()
