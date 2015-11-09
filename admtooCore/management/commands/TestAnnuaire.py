# -*- coding: utf-8 -*-

#
# base django command line tool object.
#

class TestAnnuaire (object) :
	def __init__ (self) :
		pass

	def run (self) :
		from ...plugins import plugins
		a = plugins.Annuaire
		a.AnnuaireUpdate ()


from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
	def handle (self, *args, **options) :
		ta =  TestAnnuaire()
		ta.run()
