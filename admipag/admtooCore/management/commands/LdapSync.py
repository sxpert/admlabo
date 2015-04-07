#!/usr/bin/python
# -*- coding: utf-8 -*-

from admtooLib import ldaposug as lo
from django.core.exceptions import ObjectDoesNotExist
from ...models.user import User
from ...models.newuser import NewUser

class LdapSync (object) :
	def __init__ (self) :
		pass

	def run (self) :
		l = lo.LdapOsug (None)
		users = l.users_get()
		added_users = 0
		# add new users not yet in the database
		for uidnumber in users.keys() :
			lu = users[uidnumber]
			create = False
			try :
				u = User.objects.get(uidnumber=uidnumber)
				# found the user
			except User.DoesNotExist as e :
				print "CREATE : unable to find user with uidNumber "+str(uidnumber)+" login "+lu['uid']
				# check if we have a user with the login
				try : 
					u = User.objects.get(login=lu['uid'])
				except User.DoesNotExist as e :
					# user is new, must be created
					u = User(uidnumber=uidnumber, user_state=User.NEWIMPORT_USER)
					create = True
				else :
					if u.uidnumber!=uidnumber :
						print "========================================="
						print "WARNING : uidnumber is different current "+str(u.uidnumber)+" new "+str(uidnumber)
						print "========================================="
						# change the user's uidnumber
						u.uidnumber = uidnumber
						u.save ()
			if create :
				#print lu
				u.login = lu['uid']
				u.login_shell = lu['loginShell']
				u.first_name = lu['givenName']
				u.last_name = lu['sn']
				added_users+=1
				u.save ()
			# check if we have already matched that user
			try : 
				nu = NewUser.objects.get(user=u)
			except NewUser.DoesNotExist as e :
				# attempt to find a matching user
				try :
					nu = NewUser.objects.get(first_name=u.first_name, last_name=u.last_name)
				except NewUser.DoesNotExist as e :
					# can't find corresponding new user...
					pass
				else :
					nu.user = u
					nu.save()
		# remove users that can't be found...

		# stats
		print 'ADD '+str(added_users)+' users'
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
    def handle (self, *args, **options) :
        ls = LdapSync ()
        ls.run ()


