#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ldap, ldap.modlist
import sys
from .config.osug import *
#from osugconfig import *

class UserGone (Exception) :
	pass

class Core_LdapOsug (object) :
	_l = None
		
	def _connect (self) :
		if self._l is not None :
			return
		trace = 0
		if DEBUG :
			trace = 1
		ldap.set_option (ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
		l = ldap.initialize (OSUG_LDAP_URI)
		if l is None :
			self._log ('LdapOsug: unable to connect to ldap')
			sys.exit (1)
		l.set_option (ldap.OPT_PROTOCOL_VERSION, 3)
		l.set_option (ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
		l.set_option (ldap.OPT_X_TLS_DEMAND, True)
		try :
			l.start_tls_s ()
		except ldap.SERVER_DOWN as e :
			self._log ('LdapOsug Fatal: unable to contact LDAP server')
			sys.exit (1)
		except ldap.CONNECT_ERROR as e :
			self._log ('LdapOsug FATAL: unable to starttls')
			sys.exit (1)
		l.simple_bind_s (OSUG_LDAP_ROOT, OSUG_LDAP_PASS)
		self._l = l

	def __init__ (self, logger = None) :
		self._logger = logger
		#self._log ('initializing LdapOsug plugin')
		self._connect ()

	def _log (self, message) :
		if self._logger is not None :
			self._logger.error (message)
		else:
			sys.stdout.write (str(message)+'\n')
			sys.stdout.flush ()

	#==============================================================================================
	#
	# ldap helper functions

	def _ldap_clean_record (self, rec) :
		if type(rec) is list :
			if len(rec)==0 :
				self._log ("record empty")
				return None
			if len(rec)>1 :
				# can't happen
				self._log ("problem, found more than one record")
				self._log (str(rec))
				return None
			rec = rec[0]
		dn, d = rec
		if type(d) is dict :
			u = {}
			for k in d.keys():
				v = d[k]
				if type(v) is list :
					if len(v)==1 :
						v = v[0]
				u[k] = v
			return [dn, u]
		else :
			self._log ("unexpected data type, expected 'dict', got '"+str(type(d))+"'")
			self._log (str(dn))
			self._log (str(d))
			return None

	def _to_ia5(self, s) :
		if s is None:
			return None
		ns = ''
		for c in s :
			try :
				p = u'ÁÀÂÄÃÉÈÊËẼÍÌÎÏĨÓÒÔÖÕÚÙÛÜŨÝỲŶŸỸáàâäãéèêëẽíìîïĩóòôöõúùûüũýỳŷÿỹçÇ'.index(c)
			except ValueError as e :
				pass
			else :
				c = u'AAAAAEEEEEIIIIIOOOOOUUUUUYYYYYaaaaaeeeeeiiiiiooooouuuuuyyyyycC'[p]
			ns+=c
		return ns.encode('ascii')

	#==============================================================================================
	#
	# user management

	def _user_dn (self, uid) :
		return "uid="+uid+","+OSUG_LDAP_IPAG_PEOPLE_OU+","+OSUG_LDAP_IPAG_BASE

	def _user_get (self, uid) :
		#self._log ('looking up user '+uid)
		f = '(&(objectClass=inetOrgPerson)(uid='+uid+'))'
		v = self._l.search_s (OSUG_LDAP_IPAG_BASE, ldap.SCOPE_SUBTREE, f)
		u = self._ldap_clean_record (v)
		if u is None :
			self._log ("problem with data for user with uid '"+uid+"'")
			return None
		return u

	# updates the user's data
	def _user_update (self, uid, data) :
		dn = self._user_dn (uid)
		# grab the old data
		u = self._user_get (uid)
		if u is None :
			self._log ('unable to find user '+uid) 
			# NOTE: skip when this happens (user was removed from ldap) ?
			# raise exception
			raise UserGone
			return True # skip this entry, it's not going to work anyways
		dn, odata = u
		ok = odata.keys()
		#self._log (str(data))
		#self._log (str(odata))
		# compare the old data with whatever was passed, generating the update list
		ml = []
		for k in data.keys() :
			d = data[k]
			if len(d) == 0 :
				d = None
			if d is not None :
				if k in ('gecos','roomNumber'):
					d = self._to_ia5(d)
				else :
					if type(d) is unicode :
						d = d.encode('utf8')
				if k in ok :
					od = odata[k]
					if od == d :
						self._log ('SKP '+k)
						continue
					self._log ("MOD "+k+" '"+od+"' '"+d+"'")
					# modify
					# TODO: is data an array or just a string ?
					mode = ldap.MOD_REPLACE
				else :
					# create new key
					self._log ("ADD "+k+" '"+d+"'")
					mode = ldap.MOD_ADD
				# the data must be in a list form
				if type(d) is str :
					d = [d]
			else :
				self._log ("DEL "+k)
				mode = ldap.MOD_DELETE
			ml.append ((mode,k,d))
		# update the user record
		try :
			self._log (dn+" "+str(ml))
			res, arr = self._l.modify_s (dn, ml)
		except ldap.INVALID_SYNTAX as e :
			self._log (str(e))
			self._log (str(dn))
			self._log (str(ml))
			import sys
			sys.exit (1)
		if res == 103 :
			return True
		self._log ('problems while attempting to modify')
		self._log (str(arr))
		return False

	def _users_get (self) :
		f='(&(objectClass=posixAccount)(objectClass=organizationalPerson))'
		v = self._l.search_s(OSUG_LDAP_IPAG_BASE, ldap.SCOPE_SUBTREE, f)
		users = {}
		for u in v :
			cn, d = self._ldap_clean_record(u)
			uidNumber = d['uidNumber']
			users[uidNumber] = d
		return users
		

	#==============================================================================================
	#
	# group management

	# gets the informations for exactly one group
	def _group_get (self, name) :
		dn = self._group_dn (name)
		try:
			v = self._l.search_s(dn, ldap.SCOPE_BASE, '(objectClass=posixGroup)')
		except ldap.NO_SUCH_OBJECT :
			return None
		# create a dictionnary with the useful information
		dn, data = v[0]
		g = {}
		g['cn'] = data['cn'][0]
		g['gidNumber'] = int(data['gidNumber'][0])
		if 'description' in data.keys() :
			g['description'] = data['description'][0]
		if 'memberUid' in data.keys() :	
			g['memberUid'] = data['memberUid']
		return g

	def _group_dn (self, name) :
		return 'cn='+name+','+OSUG_LDAP_IPAG_GROUP_OU+','+OSUG_LDAP_IPAG_BASE
		
	# returns a tuple with the group cn and gidnumber, or None
	def _group_check_exists (self, name, gidnumber=None) :
		# first, attempts to find the group by name
		dn = self._group_dn (name)
		try :
			v = self._l.search_s(dn, ldap.SCOPE_BASE, '(objectClass=posixGroup)')
		except ldap.NO_SUCH_OBJECT :
			# if that fails, tries finding the group by gidnumber
			if gidnumber is not None :
				try :
					f = '(&(objectClass=posixGroup)(gidNumber='+str(gidnumber)+'))'
					v = self._l.search_s(OSUG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
				except ldap.NO_SUCH_OBJECT : 
					v = []
				if len(v) == 0 :
					self._log ('can\'t find it either by gidnumber, aborting')
					return None
			else :
				self._log ('No gidnumber to try, aborting')
				return None
		if len(v) > 1 :
			self._log ('too many values returned, only one expected')
			self._log (str(v))
			return None
		dn, data = v[0]
		cn = data['cn'][0]
		gid = int(data['gidNumber'][0])
		return (cn, gid)

	# creates a new group
	def _group_create (self, name, gidNumber, description, members = None) :
		ml = {}

		# check input values
		if name is None :
			raise ValueError("Group name can't be None")
		# cn is a directoryString, encoded as utf8
		if type(name) is unicode :
			name = name.encode('utf8')
		if gidNumber is None :
			raise ValueError("Group gidNumber can't be None")
		if type(gidNumber) is not int:
			raise TypeError("Group gidNumber must be an integer")
	
		ml['cn']          = [name]
		ml['objectClass'] = ['posixGroup']
		ml['gidNumber']   = [str(gidNumber)]
		# description may be None
		if description is not None :
			if type(description) is unicode :
				description = description.encode ('utf8')
			ml['description'] = [description]
		# add users
		if members is not None :
			if type(members) is not list :
				self._log ('Problem with members : not a list')
			else :
				m = []
				for u in members :
					if type(u) is unicode :
						u = u.encode('utf8')
					m.append(u)
				ml['memberUid'] = m

		dn = self._group_dn (name)
		self._log ('creating new group '+dn)
		self._log (str(ml))
		ml = ldap.modlist.addModlist (ml)
		res, arr = self._l.add_s (dn, ml)
		if res == 105 :
			self._log ('group successfully added')
			return True
		self._log ('ERROR '+str(res)+' problem while adding group')
		self._log (str(arr))
		return False
	
	def _group_delete (self, cn, gidNumber) :
		if cn is not None :
			if len(cn)>0 :
				dn = self._group_dn (cn)
				self._log ('deleteing group '+dn)
				try :
					self._l.delete_s (dn)
				except ldap.NO_SUCH_OBJECT as e :
					self._log ('object does not exist in ldap directory')
				# either case, the object is gone from the directory, so all is well
				return True
		self._log ('ERROR : LdapOsug _group_delete: group cn None ou longueur nulle')
		return False


	# rename a group
	def _group_rename (self, oldname, newname) :
		olddn = self._group_dn(oldname)
		newrdn = 'cn='+newname
		self._log('renaming group from '+olddn+' to '+newrdn)
		# needs catching exceptions, maybe ?
		try:
			self._l.rename_s (olddn, newrdn)
		except :
			self._log('rename_group issue '+str(sys.exc_info()[0]))
			return False
		return True
		
	# updates the informations about a group
	def _group_update (self, name, gidNumber, description, members=None) :
		g = self._group_get (name)
		# compare contents, and modify whatever needs modified
		dn = self._group_dn (name)
		self._log ('updating group '+dn)
		ml = []

		if g['gidNumber']!=gidNumber :
			self._log ('update gidnumber from '+str(g['gidNumber'])+' to '+str(gidNumber))
			ml.append ((ldap.MOD_REPLACE, 'gidNumber', [ str(gidNumber) ] ))

		if description is not None :
			if type(description) is unicode :
				description = description.encode('utf8')
		if ('description' in g.keys()) and (g['description']!=description) :
			d = 'None'
			if description is not None:
				d = '\''+description+'\''
				ml.append ((ldap.MOD_REPLACE, 'description', [description]))
			else :
				ml.append ((ldap.MOD_DELETE, 'description', None))
	
		# member lists
		if members is not None :
			if type(members) is not list :
				self._log ('problem with members list... not a list\n'+str(members))
			else :
				# cleanup the members list
				m = []
				for u in members :
					if type(u) is unicode :
						u = u.encode('utf8')
					m.append(u)
				members = m
		add_mem = []
		del_mem = []
		if ('memberUid' in g.keys()) :
			# the list exists and may have changed
			for m in g['memberUid'] :
				if m not in members :
					del_mem.append(m)
			for m in members :
				if m not in g['memberUid']:
					add_mem.append(m)
		else :
			# there is no memberUid record in this object, add the whole list of members
			if len(members)>0 :
				add_mem = members
		self._log ('ADD '+str(add_mem))
		self._log ('DEL '+str(del_mem))
		if len(add_mem) > 0 :
			ml.append ((ldap.MOD_ADD, 'memberUid', add_mem))
		if len(del_mem) > 0 :
			ml.append ((ldap.MOD_DELETE, 'memberUid', del_mem))

		if len(ml)==0 :
			return True
		res, arr = self._l.modify_s (dn, ml)
		if res == 103 :
			return True
		self._log ('problems while attempting to modify')
		self._log (str(arr))
		return False
	
	def _groups_get (self) :
		f='(objectClass=posixGroup)'
		v = self._l.search_s(OSUG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		grs = []
		for g in v :
			cn, d = g
			print cn


	# update list of groups for user
	def _groups_update (self, user, groups) :

		if type(user) is unicode :
			user = user.encode('utf8')

		# get list of current groups for user
		f='(&(objectClass=posixGroup)(memberUid='+user+'))'
		cg = self._l.search_s(OSUG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		current_groups = []
		for g in cg :
			cn, d = g
			current_groups.append (d['cn'][0])

		self._log ('user           : '+str(user))
		self._log ('new groups     : '+str(groups))
		self._log ('current groups : '+str(current_groups))
		add_gr = []
		rem_gr = []
		for g in groups :
			if g not in current_groups :
				add_gr.append (g)
		for g in current_groups :
			if g not in groups :
				rem_gr.append (g)
		self._log ('groups to add    : '+str(add_gr))
		self._log ('groups to remove : '+str(rem_gr)) 
		
		# add user to groups
		for g in add_gr :
			dn = self._group_dn(g)
			m = [(ldap.MOD_ADD, 'memberUid', [user])]
			self._log (dn+' - '+str(m))
			res, arr = self._l.modify_s(dn, m)
			if res == 103 :
				self._log ('added '+user+' to group '+g)
			else :
				self._log (str(arr))
		# remove user from groups
		for g in rem_gr :
			dn = self._group_dn(g)
			m = [(ldap.MOD_DELETE, 'memberUid', [user])]
			self._log (dn+' - '+str(m))
			res, arr = self._l.modify_s(dn, m)
			if res == 103 :
				self._log ('user '+user+' removed from group '+g)
			else :
				self._log (str(arr))
		
	#==============================================================================================
	#
	# Mail alias / mailing list management
	# they do the same things, in different OUs

	# create or update

	def _mail_base (self, ou) :
		return ou+','+OSUG_LDAP_IPAG_BASE

	def _mail_dn (self, ou, cn) :
		return 'cn='+cn+','+self._mail_base(ou)

	def _mail_update (self, ou, mtype, cn, description, mail) :
		self._log ('_mailalias_update')
		if type(cn) is unicode :
			cn = cn.encode('utf-8')
		if type(description) is unicode :
			description = description.encode('utf-8')
		if type(mail) is unicode :
			mail = mail.encode('utf-8')
		# step 1: find if we have an existing alias
		self._log ('step 1 : looking for mail \''+cn+'\' in '+ou)
		f='(&(objectClass=inetOrgPerson)(cn='+cn+'))'
		ca = self._l.search_s(self._mail_base(ou), ldap.SCOPE_SUBTREE, f)
		self._log (ca)
		if len(ca) != 1 :
			self._log ('cn not found, adding')
			dn = self._mail_dn(ou, cn)
			ml = {}
			ml['objectClass'] = ['inetOrgPerson',]
			ml['sn'] = mtype
			ml['cn'] = [cn]
			if (description is not None) and (len(description)>0) :
				ml['description'] = [description]
			ml['mail'] = [mail]
			self._log (ml)
			ml = ldap.modlist.addModlist (ml)
			try :
				res, arr = self._l.add_s (dn, ml)
			except Exception as e :
				self._log (e)
				return False
			if res == 105 :
				self._log ('mail successfully added')
				return True
			self._log ('ERROR '+str(res)+' problem while adding group')
			self._log (str(arr))
			return False
		else :
			dn, ca = self._ldap_clean_record (ca)
			self._log (dn)
			self._log (ca)
			ml = []
			self._log ('mail present, checking if changes needs be made')
			# description is optional
			if 'description' in ca.keys() : 
				if ca['description']!=description :
					if description is not None:
						ml.append ((ldap.MOD_REPLACE, 'description', [description]))
					else :
						ml.append ((ldap.MOD_DELETE, 'description', None))
			else :
				if description is not None :
					ml.append ((ldap.MOD_ADD, 'description', [description]))
			# mail is required
			if 'mail' in ca.keys() :
				if ca['mail']!=mail :
					if mail is not None :
						ml.append ((ldap.MOD_REPLACE, 'mail', [mail]))
			else :
				if mail is None :
					mail = ''
				ml.append ((ldap.MOD_ADD, 'mail', [mail]))

			self._log (ml)
			res, arr = self._l.modify_s (dn, ml)
			if res == 103 :
				self._log ('mail updated')
				return True
			self._log ('problems while attempting to modify')
			self._log (str(arr))
			return False

	# destroy

	def _mail_delete (self, ou, cn) :
		self._log ('deleting mail '+cn+' in '+ou)
		# only interested in the alias here, as we only need the dn
		if type(cn) is unicode :
			cn = cn.encode('utf-8')
		dn = self._mail_dn (ou, cn)
		try :
			res = self._l.delete_s (dn)
		except ldap.NO_SUCH_OBJECT as e :
			return True
		if res[0] == 107 :
			self._log ('mail deleted')
			return True
		self._log (res)
		return False

	#
	# obtain expiration date
	#
	def _get_expire_date (self, user) :
		if 'shadowExpire' in user.keys() :
			expire = int(user['shadowExpire'])
			# expire is number of days since epoch, in utc 
			import datetime
			expire_delta = datetime.timedelta(expire)
			expire_delay = datetime.timedelta(OSUG_LDAP_IPAG_EXPIRE_DATE_DELAY)
			expire_date = datetime.date.fromtimestamp(0) + expire_delta - expire_delay
			return expire_date
		return None
	
	#==============================================================================================
	# 
	# admtoo plugin interface
	#

	def _init_logger (self, **kwargs) :
		self._log ('looking for logger variable')
		if 'logger' in kwargs.keys() :
			self._log ('logger variable found')
			logger = kwargs['logger']
			self._log (logger)
			if logger is not None :
				self._log ('setting logger to '+str(logger))
				self._logger = logger

	def GetUsers (self) :
		return self._users_get()
	
	def GetUser (self, uid) :
		return self._user_get(uid)
	
	def DestroyGroup (self, *args, **kwargs) :
		self._log ('LdapOsug DestroyGroup')
		_, command = args
		self._init_logger(**kwargs)
		import json
		c = json.loads (command.data)
		ck = c.keys ()
		cn = None
		if 'cn' in ck :
			cn = c['cn']
		gidNumber = None
		if 'gidNumber' in ck :
			gidNumber = c['gidNumber']
		self._log (cn)
		self._log (gidNumber)
		return self._group_delete (cn, gidNumber)
		return True

	
	def UpdateGroup (self, *args, **kwargs) :
		self._log ('LdapOsug UpdateGroup command')
		self._log ('args    : '+str(args))
		self._log ('kwargs  : '+str(kwargs))
		_, command = args
		self._log ('command : '+str(command)) 
		self._log ('verb    : '+str(command.verb))
#		self._log ('data    : '+str(command.data))
		self._init_logger (**kwargs)
		import json
		c = json.loads (command.data)
		ck = c.keys ()
		cn = None
		if 'cn' in ck :
			cn = c['cn']
		gidNumber = None
		if 'gidNumber' in ck :
			gidNumber = c['gidNumber']
		description = None
		if 'description' in ck :
			description = c['description']
		memberUid = None
		if 'members' in ck :
			memberUid = []
			for m in c['members'] :
				if 'login' in m.keys() :
					memberUid.append (m['login'])
		self._log (memberUid)
		
		g = self._group_check_exists (cn, gidNumber) 
		if g is None :
			return self._group_create (cn, gidNumber, description, memberUid)
		else :
			oldcn, oldgidnumber = g
			if (cn is not None) and (oldcn != cn) :
				self.group_rename (oldcn, cn)
			return self._group_update (cn, gidNumber, description, memberUid)
	
	def UpdateUser (self, *args, **kwargs) :
		self._log ('LdapOsug UpdateUser command')
		self._log ('args    : '+str(args))
		self._log ('kwargs  : '+str(kwargs))
		_, command = args
		self._log ('command : '+str(command)) 
		self._log ('verb    : '+str(command.verb))
	#	self._log ('data    : '+str(command.data))
		self._init_logger (**kwargs)
		import json
		c = json.loads (command.data)
		ck = c.keys ()
		uid = None
		if 'uid' in ck :
			uid = c['uid']
		else :
			self._log ('FATAL: LdapOsug.UpdateUser unable to find uid in UpdateUser command data')
			return False
		d = {}
		if 'loginShell' in ck :
			d['loginShell'] = c['loginShell']
		if 'gecos' in ck :
			d['gecos'] = c['gecos']
#		if 'manager' in ck :
#			d['manager'] = l.user_dn(c['manager'])
		# room and telephone
#		if 'roomNumber' in ck :
#			d['roomNumber'] = c['roomNumber']

		try :
			res = self._user_update (uid, d)
		except UserGone as e :
			self._log ("USER GONE")
			res = True
		return res

	#---- 
	# Mail objects handling (mail aliases and mailing lists are the same)
	#
	
#	def _RenameMail (self, ou, *args, **kwargs) :

	def _UpdateMail (self, ou, mail_type, *args, **kwargs) :
		self._init_logger (**kwargs)
		_, command = args
		import json
		c = json.loads (command.data)
		ck = c.keys()
		# we should have 2 things in here 

		alias = None
		if 'alias' in ck :
			alias = c['alias']
		else :
			self._log ('FATAL: LdapOsug.UpdateMailAlias unable to find alias value in command data')
			return False

		description = None
		if 'description' in ck :
			description = c['description']

		mail = None
		if 'mail' in ck :
			mail = c['mail']
			if '@' not in mail :
				mail+= '@'+OSUG_LDAP_IPAG_MAILINGLIST_DOMAIN
		else :
			self._log ('FATAL: LdapOsug.UpdateMailAlias unable to find mail value in command data')
			return False
			
		res = self._mail_update (ou, mail_type, alias, description, mail)
		return res

	def _DeleteMail (self, ou, *args, **kwargs) :
		self._init_logger (**kwargs) 
		_, command = args
		import json
		c = json.loads (command.data)
		ck = c.keys()

		alias = None
		if 'alias' in ck :
			alias = c['alias']
		else :
			self._log ('FATAL: LdapOsug.DeleteMailAlias unable to find alias value in command data')
			return False
		
		res = self._mail_delete (ou, alias)
		return res

	def UpdateMailAlias (self, *args, **kwargs) :
		return self._UpdateMail (OSUG_LDAP_IPAG_MAILALIAS_OU, 'mail alias', *args, **kwargs)

	def DeleteMailAlias (self, *args, **kwargs) :
		return self._DeleteMail (OSUG_LDAP_IPAG_MAILALIAS_OU, *args, **kwargs)

	def RenameMailingList (self, *args, **kwargs) :
		# special case, as we need to rename the entry
		self._init_logger (**kwargs)
		_, command = args
		import json
		c = json.loads (command.data)
		ck = c.keys ()
		if ('old_alias' not in ck) or ('new_alias' not in ck) :
			self._log ('FATAL: LdapOsug.RenameMailingList both old_alias and new_alias are required to execute rename function')
			return False

		old_alias = c['old_alias']
		new_alias = c['new_alias']
		
		# calculate the new mail entry
		mail = new_alias+'@'+OSUG_LDAP_IPAG_MAILINGLIST_DOMAIN
		if type(mail) is unicode :
			mail = mail.encode('utf-8')

		# rename entry
		old_dn = self._mail_dn (OSUG_LDAP_IPAG_MAILINGLIST_OU, old_alias)
		new_rdn = 'cn='+new_alias
		self._log ('old_dn  '+old_dn)
		self._log ('new_rdn '+new_rdn)
		try :
			res = self._l.rename_s (old_dn, new_rdn)
		except ldap.NO_SUCH_OBJECT as e :
			# unable to find the thing to rename...
			# for now, all is fine
			return True
		if res[0] != 109 :
			self._log (res)
			return False
		
		# change mail value
		ml = []
		ml.append ((ldap.MOD_REPLACE, 'mail', [mail]))
		new_dn = self._mail_dn (OSUG_LDAP_IPAG_MAILINGLIST_OU, new_alias)
		res, arr = self._l.modify_s (new_dn, ml)
		if res == 103 :
			return True
		self._log ('problems while attempting to modify')
		self._log (str(arr))
		return False
		

	#	return self._RenameMail (OSUG_LDAP_IPAG_MAILINGLIST_OU, *args, **kwargs)
	
	def UpdateMailingList (self, *args, **kwargs) :
		return self._UpdateMail (OSUG_LDAP_IPAG_MAILINGLIST_OU, 'mailing list', *args, **kwargs)

	def DeleteMailingList (self, *args, **kwargs) :
		return self._DeleteMail (OSUG_LDAP_IPAG_MAILINGLIST_OU, *args, **kwargs)

if __name__ == '__main__' :
	print ("LDAP OSUG TEST")
	l = LdapOsug ()
	u = l._users_get ()
	l._log (str(u))
