#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess
from ansible.module_utils.basic import *

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
 


class SetQuota (object) :

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

	""" uses the getent command to find info about the user """
	def get_user (self, user) :
		try :
			out = subprocess.check_output([self.getent_path, 'passwd', user])
		except subprocess.CalledProcessError as e :
			self.module.fail_json (msg=u'error while trying to get information for user '+unicode(user)+
				u' error:'+unicode(e.returncode)+
				u'\n'+unicode(e.output))
		# here we should have user info in the output
		if out[-1] == u'\n':
			out = out[:-1]
		userdata = out.split(u':')
		return userdata


	""" uses df -P to identify which filesystem a file is located on """
	def get_filesystem (self, dirname) :
		try : 
			out = subprocess.check_output([self.df_path, '-P', dirname])
		except subprocess.CalledProcessError as e:
			self.module.fail_json (msg=u'error while trying to find filesystem information for '+unicode(dirname)+
				u' error:'+unicode(e.returncode)+
				u'\n'+unicode(e.output))
		# split lines and remove the first one
		lines = out.split(u'\n')[1:]
		# drop line 0
		line = split_line(lines[0])
		# the actual filesystem is item 0
		return line[0]

	""" gets the quota information for a particular filesystem for a particular user """
	def get_quota (self, user, fs) :
		# change the locale to C so as to get the default messages
		os.putenv('LANG', 'C')
		try : 
			out = subprocess.check_output([self.quota_path, '-p', '-l', '-w', '-u', user])
		except subprocess.CalledProcessError as e:
			self.module.fail_json (msg=u'error while trying to get quota information for '+unicode(user)+u' on filesystem '+unicode(fs)+
				u' error:'+unicode(e.returncode)+
				u'\n'+unicode(e.output))
		# split lines and remove the 2 first lines
		lines = out.split(u'\n')

		# check if we have some quotas
		l0 = lines[0]
		# find the ':' from the end and look for the next word
		p = l0.rfind(':')
		if p==-1 :
			self.module.fail_json (msg='Fatal: malformed response from '+unicode(QUOTA_COMMAND))
		resp = l0[p+1:].strip()
		if resp == 'none' :
			return None

		# find get the quota lines
		lines = lines[2:]
		for l in lines :
			line = split_line(l)
			try :
				if line[0] == fs :
					# found the line, do something
					q_info = {}
					q_info['filesystem'] = line[0]
					q_info['blocks']     = int(line[1])
					q_info['soft']       = int(line[2])
					q_info['hard']       = int(line[3])
					q_info['grace']      = int(line[4])
					q_info['i_soft']     = int(line[5])
					q_info['i_hard']     = int(line[6])
					q_info['i_grace']    = int(line[7])
					return q_info
			except IndexError as e :
				self.module.fail_json (msg=unicode(e)+'\n'+unicode(lines))
		self.module.fail_json (msg=u'Unable to find quota information for user '+unicode(user)+u' on filesystem '+unicode(fs))

	""" sets the new quota values """
	def set_quota (self, user, filesystem, soft, hard) :
		try :
			out = subprocess.check_output([self.setquota_path, '-u', user, unicode(soft), unicode(hard), '0', '0', filesystem])
		except subprocess.CalledProcessError as e:
			self.module.fail_json (msg=u'error while trying to set quota information for '+unicode(user)+u' on filesystem '+unicode(fs)+
				u' error:'+unicode(e.returncode)+
				u'\n'+unicode(e.output))
		# does not return anything. if we are here, this returned 0, hence everything is ok
		return True

	def __init__ (self) :

		self.module = AnsibleModule (
			argument_spec = dict(
				state   = dict(default='present', choices=['present', 'absent']),
				user    = dict(required=True),
				dirname = dict(required=True),
				soft    = dict(default='0'),
				hard    = dict(default='0'),
			),
			supports_check_mode=True,
		)

		self.state   = self.module.params['state']
		self.user    = self.module.params['user']
		self.dirname = self.module.params['dirname']

		# NOTE: blocks are 1kB 
		s = self.module.params['soft']
		try :
			self.soft    = int(s)
		except ValueError as e :
			self.module.fail_json(msg=u'Unable transform soft quota argument \''+unicode(s)+u'\' from '+unicode(type(s))+u' to integer type')
		s = self.module.params['hard']
		try :
			self.hard    = int(s)
		except ValueError as e :
			self.module.fail_json(msg=u'Unable transform hard quota argument \''+unicode(s)+u'\' from '+unicode(type(s))+u' to integer type')

		self.df_path = self.find_executable(DF_COMMAND)
		self.getent_path = self.find_executable(GETENT_COMMAND)
		self.quota_path = self.find_executable(QUOTA_COMMAND)
		self.setquota_path = self.find_executable(SETQUOTA_COMMAND)

		# find if user exists
		self.userdata = self.get_user(self.user)

		# find if the directory exists
		if not os.path.isdir(self.dirname) :
			self.module.fail_json(msg=u'Unable to find user directory '+unicode(self.dirname))
		
		# get current filesystem
		self.filesystem = self.get_filesystem (self.dirname)

		# get current quotas
		self.current_quota = self.get_quota (self.user, self.filesystem)

		# check if existing quotas are identical to the new ones or not
		changed = False
		msg=None
		if self.current_quota is not None :
			# we had previous quota values
			if self.state == 'present' :
				if self.current_quota['soft'] != self.soft :
					if msg is None :
						msg=u''
					msg+=u'soft '+unicode(self.current_quota['soft'])+u'=>'+unicode(self.soft)
					changed = True
				if msg is not None :
					msg+=u' '
				if self.current_quota['hard'] != self.hard : 
					if msg is None :
						msg=u''
					msg+=u'hard '+unicode(self.current_quota['hard'])+u'=>'+unicode(self.hard)
					changed = True
				if self.soft==0 and self.hard==0 :
					self.state='absent'
			else :
				# remove existing quotas
				self.soft = 0
				self.hard = 0
				changed = True
		else :
			if self.state == 'present' :
				# set some new quotas
				changed = True
			else :
				# nothing to do, there were no quotas, and we don't apply any
				pass

		# when not in check mode, we're in production mode, change stuff
		if not self.module.check_mode :
			# do actual things
			if changed :
				self.set_quota (self.user, self.filesystem, self.soft, self.hard)

		# exit indicating if there was some change
		if msg is not None :
			self.module.exit_json(changed=changed, msg=msg, state=self.state)
		self.module.exit_json(changed=changed, state=self.state)

if __name__ == '__main__' :
	q = SetQuota ()

