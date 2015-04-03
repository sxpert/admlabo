#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap
import sys

from laogconfig import *

#DEBUG = False
#LDAP_URI = 'ldap://masterldaplaog.obs.ujf-grenoble.fr'
#LDAP_BASE = 'ou=laog,dc=obs,dc=ujf-grenoble,dc=fr'
#LDAP_ROOT = 'cn=root-master,'+LDAP_BASE
#LDAP_PASS = 'C1n2r3S4'
#LDAP_OU_GROUP = 'ou=Groups'

class Directory (object) :

	#
	# the ldap connection only needs to be a singleton
	#
	ldap_conn = None
	
	def __init__ (self) :
		self._connect ()
	
	def __del__ (self) :
		if (self is not None) and (self.ldap_conn is not None) :
			self.ldap_conn.unbind_s()
			self.ldap_conn = None

	def _connect (self) :
		
		if self.ldap_conn is not None :
			return
		trace = 0
		if DEBUG :
			trace = 1
		ldap.set_option (ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
		l = ldap.initialize (LAOG_LDAP_URI, trace_level=trace)
		if l is None :
			print "Unable to connect"
			sys.exit (1) 
		l.set_option (ldap.OPT_PROTOCOL_VERSION, 3)
		l.set_option (ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
		l.set_option (ldap.OPT_X_TLS_DEMAND, True)
	
		try :
			l.start_tls_s ()
		except ldap.CONNECT_ERROR as e :
			print "FATAL: starttls impossible"
			sys.exit (1)
		# bind to the ldap
		l.simple_bind_s (LAOG_LDAP_ROOT, LAOG_LDAP_PASS)
		self.ldap_conn = l

	def get_users (self) :
		l = self.ldap_conn
		f = '(objectClass=posixAccount)'
		v = l.search_s (LAOG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		return v

	def get_user_account (self, username) :
		l = self.ldap_conn
		f = '(uid='+username+')'
		v = l.search_s (LAOG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		if len (v) > 1 : 
			print "FATAL: trop de valeurs"
			sys.exit (1)
		return v[0]

	def get_user_groups (self, username) :
		l = self.ldap_conn
		f = '(&(objectClass=posixGroup)(memberUid='+username+'))'
		v = l.search_s (LAOG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		# create the list of groups from that
		g = {}
		for group in v:
			group = group[1]
			cn = group['cn'][0]
			gidNumber=int(group['gidNumber'][0])
			g[cn] = gidNumber
		return g
	
	#
	# groups management
	#
	
	def get_groups (self) :
		l = self.ldap_conn
		f = '(objectClass=posixGroup)'
		v = l.search_s (LAOG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		g = {}
		for group in v :
			group = group[1]
			gidNumber = int(group['gidNumber'][0])
			cn = group['cn'][0]
			g[gidNumber]=cn
		return g

	def get_group (self, groupname) :
		l = self.ldap_conn
		f = '(&(objectClass=posixGroup)(cn='+groupname+'))'
		v = l.search_s (LAOG_LDAP_BASE, ldap.SCOPE_SUBTREE, f)
		# we have a list of arrays with [ dn, { data } ]
		if len(v)!=1 :
			return None
		v = v[0] 
		return v

	def group_dn(self, cn) :
		return 'cn='+cn+','+LAOG_LDAP_OU_GROUP+','+LAOG_LDAP_BASE
		
	def add_group (self, cn, gidNumber, users, desc) :
		l = self.ldap_conn
		add_record = [
				('objectClass', ['posixGroup']),
				('cn', [cn]),
				('gidNumber', [str(gidNumber)]),
				('memberUid', users),
				('description', [desc]),
			]
		l.add_s (self.group_dn(cn), add_record)

	def modify_group (self, dn, modlist) :
		self.ldap_conn.modify_s(dn, modlist)

	def delete_group (self, dn) :
		self.ldap_conn.delete_s(dn)

if __name__=='__main__' :
	d = Directory ()
	print d.get_users ()
