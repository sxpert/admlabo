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
		modified_users = 0
		deleted_users = 0
		# add new users not yet in the database
		# in some cases, users exist with no valid uidnumber, those are skipped
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
				modified = False
				# user may have to be modified

				# is user back in play ?
				#if u.user_state == User.DELETED_USER :
				#	u.user_state = User.NORMAL_USER

				# mail
				if 'mail' in lu :
					ldap_mail = lu['mail'].lower()
					if u.mail != ldap_mail :				
						print "mail in ldap '"+str(ldap_mail)+" is different from mail in database "+str(u.mail)
						u.mail = ldap_mail
						modified = True
				else :
					# no mail in ldap
					if u.mail is not None :
						u.mail = None
						modified = True

				# expiration date
				expire = l._get_expire_date (lu)
				update_expire = False
				if expire is not None :
					if u.departure is not None : 
						if expire > u.departure :
							update_expire = True
					else :
						update_expire = True
				# if expire is none the dude is now a permanent fixture ?
				else :
					if u.departure is not None :
						u.departure = None
						update_expire = True

				if update_expire :
					if u.departure is None :
						m = u.login+" setting departure date to "+str(expire)
					else :
						m = u.login+" changing the departure date from "+str(u.departure)+" to "+str(expire)
					print m
					u.departure = expire
					modified = True
				
				# room
				if 'roomNumber' in lu :
					ldap_room = lu['roomNumber']
					if u.room != ldap_room :
						print "room in ldap "+str(ldap_room)+" is different from room in database "+str(u.room)
						u.room = ldap_room
						modified = True
				else :
					if u.room is not None:	
						u.room = None
						modified = True

				#telephone
				if 'telephoneNumber' in lu :
					ldap_phone = lu['telephoneNumber']
					if u.telephone != ldap_phone :
						print "telephone in ldap "+str(ldap_phone)+" is different from telephone in database "+str(u.telephone)
						u.telephone = ldap_phone
						modified = True
				else :
					if u.telephone is not None :
						u.telephone = None
						modified = True

				# the user was modified, save it
				if modified : 
					modified_users+=1
					u.save()
				

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
					nu.user = u
					nu.save()
					# send mail indicating the user has been matched
					nu.send_match_mail ()
			except NewUser.MultipleObjectsReturned as e :
				print (u'UNABLE TO MATCH, multiple newuser instances returned for user '+unicode(u.login))
				nus = NewUser.objects.filter(user=u)
				for nu in nus :
					print (u'    '+unicode(nu.pk)+u' \''+unicode(nu.last_name)+u'\' \''+unicode(nu.first_name)+u'\' \''+unicode(nu.birthdate)+u'\'')
							
					
		#
		# remove users that can't be found...
		for u in User.objects.all() :
			if u.user_state != User.DELETED_USER :
				lu = l.GetUser (u.login)
				if lu is None :
					u.user_state = User.DELETED_USER
					u.save ()
					deleted_users+=1
		
		if modified_users > 0 :
			User.update_kifekoi()

		# skip printing stats if nothing was done
		if ((added_users > 0) or (modified_users > 0) or (deleted_users > 0)) :
			print 'ADD '+str(added_users)+' users'
			print 'MOD '+str(modified_users)+' users'
			print 'DEL '+str(deleted_users)+' users'

#
# base django command line tool object.
#

from django.core.management.base import BaseCommand, CommandError

class Command (BaseCommand) :
    def handle (self, *args, **options) :
        ls = LdapSync ()
        ls.run ()


