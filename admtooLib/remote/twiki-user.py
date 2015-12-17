#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, subprocess, datetime
from ansible.module_utils.basic import *

TWIKI_DATA_DIR   = 'data'
TWIKI_HTPASSWD   = '.htpasswd'

DF_COMMAND       = 'df'
GETENT_COMMAND   = 'getent'
QUOTA_COMMAND    = 'quota'
SETQUOTA_COMMAND = 'setquota'

def is_exe (fpath) :
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def split_line (line) :
	line = line.split(u' ')
	l = []
	for w in line :
		if w != u'' :
			l.append(w)
	return l


# one twiki user
class TWikiUserEntry (object) :
	def __init__ (self, line) :
		self.empty = False
		self.active = True
		self.name = ''
		self.passwd = ''
		self.email = None

		# removes blanks on both ends
		line = line.strip()

		if len(line) == 0 :
			self.empty = True
			return
		
		if line[0] == '#' :
			self.active = False
			line = line[1:]
		
		# get the information bits now
		data = line.split(':')
		if len(data) > 2 :
			self.email = data[2]
		self.name = data[0]
		self.passwd = data[1]

	# generate line representing the user
	def __unicode__ (self) :
		l = u''
		if self.empty :
			return l
		if not self.active :
			l+=u'#'
		l+=self.name
		l+=':'
		l+=self.passwd
		l+=':'
		if self.email is not None :
			l+=self.email
		return l

# list of twiki users
class TWikiUserEntries (object) :
	def __init__ (self) :
		self.users = []

	def append (self, entry) :
		self.users.append (entry)

	def exists (self, name) :
		for u in self.users :
			if u.name == name :
				return u
		return False
	
	def inactive_users (self) :
		l = []
		for u in self.users :
			if not u.active :
				l.append(u.name)
		l.sort()
		return l

	def active_users (self) :
		l = []
		for u in self.users :
			if u.active :
				l.append(u.name)
		l.sort()
		return l

	# generate a unicode representation of this list
	def __unicode__ (self) :
		l = []
		for u in self.inactive_users() :
			l.append(unicode(self.exists(u)))
		for u in self.active_users() :
			l.append(unicode(self.exists(u)))
		return u'\n'.join(l)+u'\n'

"""
	manipulates twiki users
	uses 

	the <twikibase>/data/.htpasswd
"""

class TWikiUser (object) :

	def find_executable (self, fname) :
		if 'PATH' not in os.environ :
			self.module.fail_json (msg=u'Unable to find PATH variable in environment')
		os_path = os.environ['PATH'].split(u':')
		found = False
		for p in os_path :
			cmd = os.path.join(p, fname)
			if is_exe(cmd) :
				found = True
				break
		if not found :
			self.module.fail_json(msg=u'Unable to find '+unicode(fname)+u' command')
		return cmd

	def fail (self, msg) :
		if self.module is not None :
			self.module.fail_json (msg=msg)
		else :
			print (msg)
			sys.exit (1)

	# reads the current .htpasswd file in memory
	def read_htpasswd_file (self) :
		try :
			f = open(self.htpasswd, 'rU')
		except IOError as e :
			self.fail (u'unable to open '+unicode(fname))
		self.twu = TWikiUserEntries ()
		for line in f :
			self.twu.append (TWikiUserEntry (line))
		f.close ()
		return True 

	def is_user_present (self) :
		if not self.read_htpasswd_file () :
			return None
		return self.twu.exists (self.user)

	def __init__ (self) :

		self.module = AnsibleModule (
			argument_spec = dict(
				state     = dict(default='active', choices=['active', 'inactive']),
				user      = dict(required=True),
				twikibase = dict(required=True),
			),
			supports_check_mode=True,
		)

		self.state     = self.module.params['state']
		self.user      = self.module.params['user']
		self.twikibase = self.module.params['twikibase']

		# generate the default htpasswd file name
		self.htpasswd = os.path.join (self.twikibase, TWIKI_DATA_DIR, TWIKI_HTPASSWD)

		msg = ''

		# 1. find if the user is present in the current 
		up = self.is_user_present ()
		if up is None :
			self.module.fail_json(msg=u'error finding user '+unicode(self.user))

		changed = False

		# check and change user state
		if self.state == 'inactive' :
			if up.active :
				changed = True
				up.active = False
		elif self.state == 'active' :
			if not up.active :
				changed = True
				up.active = True

		# when not in check mode, we're in production mode, change stuff
		if not self.module.check_mode :
			# do actual things
			if changed :
				# 1. copy old file to new file
				s = os.stat(self.htpasswd)
				uid = s.st_uid
				gid = s.st_gid
				modes = s.st_mode
				d = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
				htpasswd_backup = self.htpasswd+'.'+d
				shutil.copy2(self.htpasswd,self.htpasswd+'.'+d)
				os.chown(htpasswd_backup, uid, gid) 
				# 2. generate new file
				f = tempfile.NamedTemporaryFile(delete=False)
				tempname = f.name
				f.write(unicode(self.twu))
				f.close()
				os.chown(tempname, uid, gid)
				os.chmod(tempname, modes)
				os.rename(tempname, self.htpasswd)
				

		# exit indicating if there was some change
		if len(msg) > 0 :
			self.module.exit_json(changed=changed, msg=msg, state=self.state)
		self.module.exit_json(changed=changed, state=self.state)

if __name__ == '__main__' :
	q = TWikiUser ()

