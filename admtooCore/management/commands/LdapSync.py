#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from ...plugins import plugins

from ...models.user import User
from ...models.newuser import NewUser

class LdapSync (object) :
	def __init__ (self) :
		pass

	def run (self) :
		l = plugins.Core_LdapOsug
		users = l.GetUsers()
		added_users = 0
		deleted_users = 0
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
				print lu
				u.login = lu['uid']
				u.login_shell = lu['loginShell']
				u.first_name = lu['givenName']
				u.last_name = lu['sn']
				if 'mail' in lu :
					u.mail = lu['mail']
				added_users+=1
				u.save ()
			else :
				# user may have to be modified
				expire = l._get_expire_date (lu)
				if expire is not None :
					#print u.login, u.departure, expire
					pass
				

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
					# apply automatic matching to the new user
					# this does not work and need more thought
					#nu.user = u
					#nu.save()
		#
		# remove users that can't be found...
		for u in User.objects.all() :
			if u.user_state != User.DELETED_USER :
				lu = l.GetUser (u.login)
				if lu is None :
					u.user_state = User.DELETED_USER
					u.save ()
					deleted_users+=1
		# stats
		print 'ADD '+str(added_users)+' users'
		print 'DEL '+str(deleted_users)+' users'
#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
    def handle (self, *args, **options) :
        ls = LdapSync ()
        ls.run ()


