#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from ... import plugins

class PluginTest (object) :
	def __init__ (self) :
		pass

	def run (self) :
		pass
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
    def handle (self, *args, **options) :
        pt = PluginTest ()
        pt.run ()
		


