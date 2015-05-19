#!/usr/bin/python
# -*- coding: utf-8 -*-

from admtooLib import ldaposug as lo
from admtooLib.twiki import TWiki
from django.core.exceptions import ObjectDoesNotExist
import json
from ...models.group import Group
from ...models.user import User
from ...models.newuser import NewUser

class TWikiGroups (object) :
	def __init__ (self) :
		pass

	def run (self) :
		for g in Group.objects.all () :
			try :
				j = json.loads (g.appspecname)
			except ValueError as e :
				continue
			print g.name
			if 'twiki' in j :
				print "   "+j['twiki']
		t = TWiki ('','')
		for u in User.objects.filter(user_state=User.NORMAL_USER) :
			print t.gen_user_name (u.first_name, u.last_name)
		for g in Group.objects.all () :
			t.gen_group_config (g.prepare_group_data())
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
    def handle (self, *args, **options) :
        twg = TWikiGroups ()
        twg.run ()
		


