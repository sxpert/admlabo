#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ldap, ldap.modlist
import sys
from ldapconfig.osug import *
#from osugconfig import *

class UserGone (Exception) :
	pass

class LdapOsug :
	l = None
		
	def _connect (self) :
		if self.l is not None :
			return
		trace = 0
		if DEBUG :
			trace = 1
		ldap.set_option (ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
#		l = ldap.initialize (OSUG_LDAP_URI, trace_level=trace)
		l = ldap.initialize (OSUG_LDAP_URI)
		if l is None :
			self.log ('LdapOsug: unable to connect to ldap')
			sys.exit (1)
		l.set_option (ldap.OPT_PROTOCOL_VERSION, 3)
		l.set_option (ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
		l.set_option (ldap.OPT_X_TLS_DEMAND, True)
		try :
			l.start_tls_s ()
		except ldap.SERVER_DOWN as e :
			self.log ('LdapOsug Fatal: unable to contact LDAP server')
			sys.exit (1)
		except ldap.CONNECT_ERROR as e :
			self.log ('LdapOsug FATAL: unable to starttls')
			sys.exit (1)
		l.simple_bind_s (OSUG_LDAP_ROOT, OSUG_LDAP_PASS)
		self.l = l

	def __init__ (self, logger = None) :
		self.logger = logger
		self._connect ()

	def log (self, message) :
		if self.logger is not None :
			self.logger.error (message)
		else:
			sys.stdout.write (message+'\n')
			sys.stdout.flush ()

	#==============================================================================================
	#
	# ldap helper functions

	def ldap_clean_record (self, rec) :
		if type(rec) is list :
			if len(rec)==0 :
				self.log ("record empty")
				return None
			if len(rec)>1 :
				# can't happen
				self.log ("problem, found more than one record")
				self.log (str(rec))
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
			self.log ("unexpected data type, expected 'dict', got '"+str(type(d))+"'")
			self.log (str(dn))
			self.log (str(d))
			return None

	def to_ia5(self, s) :
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

	def user_dn (self, uid) :
		return "uid="+uid+","+OSUG_LDAP_IPAG_PEOPLE_OU+","+OSUG_LDAP_IPAG_BASE

	def user_get (self, uid) :
		#self.log ('looking up user '+uid)
		f = '(&(objectClass=inetOrgPerson)(uid='+uid+'))'
		v = self.l.search_s (OSUG_LDAP_IPAG_BASE, ldap.SCOPE_SUBTREE, f)
		u = self.ldap_clean_record (v)
		if u is None :
			self.log ("problem with data for user with uid '"+uid+"'")
			return None
		return u

	# updates the user's data
	def user_update (self, uid, data) :
		dn = self.user_dn (uid)
		# grab the old data
		u = self.user_get (uid)
		if u is None :
			self.log ('unable to find user '+uid) 
			# NOTE: skip when this happens (user was removed from ldap) ?
			# raise exception
			raise UserGone
			return True # skip this entry, it's not going to work anyways
		dn, odata = u
		ok = odata.keys()
		#self.log (str(data))
		#self.log (str(odata))
		# compare the old data with whatever was passed, generating the update list
		ml = []
		for k in data.keys() :
			d = data[k]
			if len(d) == 0 :
				d = None
			if d is not None :
				if k in ('gecos','roomNumber'):
					d = self.to_ia5(d)
				else :
					if type(d) is unicode :
						d = d.encode('utf8')
				if k in ok :
					od = odata[k]
					if od == d :
						self.log ('SKP '+k)
						continue
					self.log ("MOD "+k+" '"+od+"' '"+d+"'")
					# modify
					# TODO: is data an array or just a string ?
					mode = ldap.MOD_REPLACE
				else :
					# create new key
					self.log ("ADD "+k+" '"+d+"'")
					mode = ldap.MOD_ADD
				# the data must be in a list form
				if type(d) is str :
					d = [d]
			else :
				self.log ("DEL "+k)
				mode = ldap.MOD_DELETE
			ml.append ((mode,k,d))
		# update the user record
		try :
			self.log (dn+" "+str(ml))
			res, arr = self.l.modify_s (dn, ml)
		except ldap.INVALID_SYNTAX as e :
			self.log (str(e))
			self.log (str(dn))
			self.log (str(ml))
			import sys
			sys.exit (1)
		if res == 103 :
			return True
		self.log ('problems while attempting to modify')
		self.log (str(arr))
		return False

	def users_get (self) :
		f='(&(objectClass=posixAccount)(objectClass=organizationalPerson))'
		v = self.l.search_s(OSUG_LDAP_IPAG_BASE, ldap.SCOPE_SUBTREE, f)
		users = {}
		for u in v :
			cn, d = self.ldap_clean_record(u)
			uidNumber = d['uidNumber']
			users[uidNumber] = d
		return users
		

	#==============================================================================================
	#
	# group management

	# gets the informations for exactly one group
	def group_get (self, name) :
		dn = self.group_dn (name)
		try:
			v = self.l.search_s(dn, ldap.SCOPE_BASE, '(objectClass=posixGroup)')
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

	def group_dn (self, name) :
		return 'cn='+name+','+OSUG_LDAP_IPAG_GROUP_OU+','+OSUG_LDAP_IPAG_BASE
		
	# returns a tuple with the group cn and gidnumber, or None
	def group_check_exists (self, name, gidnumber=None) :
		# first, attempts to find the group by name
		dn = self.group_dn (name)
		try :
			v = self.l.search_s(dn, ldap.SCOPE_BASE, '(objectClass=posixGroup)')
		except ldap.NO_SUCH_OBJECT :
			# if that fails, tries finding the group by gidnumber
			if gidnumber is not None :
				try :
					f = '(&(objectClass=posixGroup)(gidNumber='+str(gidnumber)+'))'
					v = self.l.search_s(OSUG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
				except ldap.NO_SUCH_OBJECT : 
					v = []
				if len(v) == 0 :
					self.log ('can\'t find it either by gidnumber, aborting')
					return None
			else :
				self.log ('No gidnumber to try, aborting')
				return None
		if len(v) > 1 :
			self.log ('too many values returned, only one expected')
			self.log (str(v))
			return None
		dn, data = v[0]
		cn = data['cn'][0]
		gid = int(data['gidNumber'][0])
		return (cn, gid)

	# creates a new group
	def group_create (self, name, gidNumber, description, members = None) :
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
				self.log ('Problem with members : not a list')
			else :
				m = []
				for u in members :
					if type(u) is unicode :
						u = u.encode('utf8')
					m.append(u)
				ml['memberUid'] = m

		dn = self.group_dn (name)
		self.log ('creating new group '+dn)
		self.log (str(ml))
		ml = ldap.modlist.addModlist (ml)
		res, arr = self.l.add_s (dn, ml)
		if res == 105 :
			self.log ('group successfully added')
			return True
		self.log ('ERROR '+str(res)+' problem while adding group')
		self.log (str(arr))
		return False

	# rename a group
	def group_rename (self, oldname, newname) :
		olddn = self.group_dn(oldname)
		newrdn = 'cn='+newname
		self.log('renaming group from '+olddn+' to '+newrdn)
		# needs catching exceptions, maybe ?
		try:
			self.l.rename_s (olddn, newrdn)
		except :
			self.log('rename_group issue '+str(sys.exc_info()[0]))
			return False
		return True
		
	# updates the informations about a group
	def group_update (self, name, gidNumber, description, members=None) :
		g = self.group_get (name)
		# compare contents, and modify whatever needs modified
		dn = self.group_dn (name)
		self.log ('updating group '+dn)
		ml = []

		if g['gidNumber']!=gidNumber :
			self.log ('update gidnumber from '+str(g['gidNumber'])+' to '+str(gidNumber))
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
				self.log ('problem with members list... not a list\n'+str(members))
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
		self.log ('ADD '+str(add_mem))
		self.log ('DEL '+str(del_mem))
		if len(add_mem) > 0 :
			ml.append ((ldap.MOD_ADD, 'memberUid', add_mem))
		if len(del_mem) > 0 :
			ml.append ((ldap.MOD_DELETE, 'memberUid', del_mem))

		if len(ml)==0 :
			return True
		res, arr = self.l.modify_s (dn, ml)
		if res == 103 :
			return True
		self.log ('problems while attempting to modify')
		self.log (str(arr))
		return False
	
	def groups_get (self) :
		f='(objectClass=posixGroup)'
		v = self.l.search_s(OSUG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		grs = []
		for g in v :
			cn, d = g
			print cn


	# update list of groups for user
	def groups_update (self, user, groups) :

		if type(user) is unicode :
			user = user.encode('utf8')

		# get list of current groups for user
		f='(&(objectClass=posixGroup)(memberUid='+user+'))'
		cg = self.l.search_s(OSUG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		current_groups = []
		for g in cg :
			cn, d = g
			current_groups.append (d['cn'][0])

		self.log ('user           : '+str(user))
		self.log ('new groups     : '+str(groups))
		self.log ('current groups : '+str(current_groups))
		add_gr = []
		rem_gr = []
		for g in groups :
			if g not in current_groups :
				add_gr.append (g)
		for g in current_groups :
			if g not in groups :
				rem_gr.append (g)
		self.log ('groups to add    : '+str(add_gr))
		self.log ('groups to remove : '+str(rem_gr)) 
		
		# add user to groups
		for g in add_gr :
			dn = self.group_dn(g)
			m = [(ldap.MOD_ADD, 'memberUid', [user])]
			self.log (dn+' - '+str(m))
			res, arr = self.l.modify_s(dn, m)
			if res == 103 :
				self.log ('added '+user+' to group '+g)
			else :
				self.log (str(arr))
		# remove user from groups
		for g in rem_gr :
			dn = self.group_dn(g)
			m = [(ldap.MOD_DELETE, 'memberUid', [user])]
			self.log (dn+' - '+str(m))
			res, arr = self.l.modify_s(dn, m)
			if res == 103 :
				self.log ('user '+user+' removed from group '+g)
			else :
				self.log (str(arr))
		

	def test (self) :
		self.log ('error message from LdapOsug object')

if __name__ == '__main__' :
	print ("LDAP OSUG TEST")
	l = LdapOsug ()
	u = l.users_get ()
	l.log (str(u))
