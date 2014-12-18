from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from silabo.models import User, Group
import sys
sys.path.append ('/srv/progs/ipag')
import directory as l
import xmldb as x 

class Command(BaseCommand) :
	help = 'Synchronizes the database from the LDAP server and the XML database'

	def log(self, message) :
		self.stdout.write (message)

	def group (self, group_data) :
		self.log (repr(group_data))
		if group_data is None :
			self.log ("group_data is None, aborting")
			return
		gidnumber = group_data['gidNumber']
		if gidnumber is None :
			self.log ("gidnumber is None, aborting")
			return
		if not isinstance(gidnumber, list) or len(gidnumber) != 1 : 
			self.log ("gidnumber is not a 1 item list")
			return
		try :
			gidnumber = int(gidnumber[0])
		except :
			self.log ("gidnumber is not an integer")
			return
		
		# find if we already have that group
		changed = False
		try :
			g = Group.objects.get(gidnumber = gidnumber)
		except Group.DoesNotExist as e :
			# group does not exists, add
			self.log ("adding group "+str(gidnumber))
			g = Group(gidnumber = gidnumber)
			changed = True
		else :
			# group already exists, update
			self.log ("updating group "+str(gidnumber))

		if 'cn' not in group_data.keys() :
			self.log ("problem, no name for group")
			return
		name = group_data['cn'][0]
		if g.name != name :
			g.name = name
			changed = True
			
		description = None
		if 'description' in group_data :
			description = group_data['description'][0]
		if g.description != description :
			g.description = description
			changed = True

		if changed :
			g.save ()
		
			


	def user_add (self, user_data, xml_data) :
		# 'uid': ['cotere'], 
		# 'objectClass': ['posixAccount', 'shadowAccount', 'inetOrgPerson'], 
		# 'loginShell': ['/bin/bash'], 
		# 'userPassword': ['{crypt}$1$qmktPDE5$Ct9TwmEpS/RNwhHzIo725.'], 
		# 'uidNumber': ['281869'], 
		# 'l': ['Saint Martin d Heres'], 
		# 'gidNumber': ['3001'], 
		# 'street': ['414 rue de la piscine'], 
		# 'gecos': ['Remi Cote'], 
		# 'sn': ['Cote'], 
		# 'homeDirectory': ['/user/homedir/cotere'], 
		# 'postalCode': ['38400'], 
		# 'mail': ['Remi.Cote@obs.ujf-grenoble.fr'], 
		# 'givenName': ['Remi'], 
		# 'shadowLastChange': ['16405'], 
		# 'shadowExpire': ['16860'], 
		# 'cn': ['Remi Cote']

		u = User(uidnumber = int(user_data['uidNumber'][0]))
		u.login = user_data['uid'][0]
		u.first_name = user_data['givenName'][0]
		u.last_name = user_data['sn'][0]

		# email
		if 'mail' in user_data.keys() :
			u.mail = (user_data['mail'][0]).lower()
		else :
			u.mail = None
		# 
		
		u.save()

	def user_update (self, user_data, xml_data, u) :
		uidnumber = int(user_data['uidNumber'][0])
		changed = False
		if u.uidnumber != uidnumber :
			u.uidnumber = uidnumber
			changed = True

		if 'mail' in user_data.keys() :
			mail = (user_data['mail'][0]).lower()
		else : 
			mail = None
		if u.mail != mail :
			u.mail = mail
			changed = True
		
		if xml_data is not None :
			old_manager = None
			if u.manager is not None :
				old_manager = u.manager.login
			
			new_manager = xml_data['manager']

			if old_manager != new_manager :
				# get manager object
				try :
					m = User.objects.get(login=new_manager)
				except User.DoesNotExist as e :
					self.log ("there's no user with login "+new_manager)
					m = None
				
				if u.manager != m :				
					u.manager = m
					changed = True

		if changed :
			u.save()
		

	def handle (self, *args, **options) :
		self.log('start synchronizing the database with the ldap')
		d = l.Directory ()
	
		# groups
		dgroups = d.get_groups ()
#		xgroups = x.get_groups ()

		self.log(repr(dgroups))
		for group in dgroups.keys() :
			dn, group = d.get_group (dgroups[group])
			self.log (dn)
			self.group (group)
			
			

		# users

		dusers = d.get_users ()
		xusers = x.get_users () 

		for user in dusers :
			dn, data = user
			uidnumber = int(data['uidNumber'][0])
			uid = data['uid'][0]
			if uidnumber in xusers.keys() :
				xu = xusers[uidnumber]
			else :
				# user doesn't exist yet ?
				self.log ("problem, unable to find user with uid "+str(uidnumber)+" in xml database - skipping")
				xu = None

			try :
				u = User.objects.get(uidnumber=uidnumber)
			except User.DoesNotExist as e :
				# checher si un utilisateur avec le meme login existe
				try : 
					u = User.objects.get(login=uid)
				except User.DoesNotExist as e :
					# ajouter l'utilisateur
					self.user_add (data, xu)
				else:
					self.user_update (data, xu, u)
			else:
				self.user_update (data, xu, u)
			
