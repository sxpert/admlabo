#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from ...plugins import plugins

class PluginTest (object) :
	def __init__ (self) :
		pass

	def run (self) :
		ret = plugins.path
		print ret
		try :
			ret = plugins.runcommand("command",{"data":["test","data"]})
		except AttributeError as e:
			print e
		else: 
			print ret
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
    def handle (self, *args, **options) :
        pt = PluginTest ()
        pt.run ()
		


