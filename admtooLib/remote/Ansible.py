# -*- coding: utf-8 -*-
import os
import subprocess, sys
import ansible 
import ansible.runner as ar

#==================================================================================================
#
# low level drivers
#

class Ansible (object) :
	def __init__ (self, debug=False) :
		self.debug = debug
		ansible.utils.VERBOSITY=0
		self.inventory = ansible.inventory.Inventory ()
		if self.debug :
			self.log ('Ansible initialized')

	#==============================================================================================
	# utility functions

	def log (self, message) :
		if message is None :
			return
		import sys
		sys.stderr.write (str(message)+'\n')

	def getHostname (self, fqdn) :
		if type(fqdn) not in (str, unicode) :
			return False
		p = fqdn.find('.')
		if p==-1 :
			# there's no '.'
			return fqdn
		else :
			return fqdn[:p]


	def generatePassword (self, length) :
		l = str(length)
		try :
			password = subprocess.check_output(['pwgen', '-s', l, '1'])
			if password[-1] == '\n' :
				password=password[0:-1]
		except OSError as e :
			self.log("pwgen command not found")
			return False
		return password

	#=================================================================================================
	# actual ansible modules

	"""
	this module creates a directory
	parameters are :
		fqdn
		dirname
		uid
		gid
		modes
	"""
	def createDirectory (self, fqdn, dirname, uid, gid, modes) :
		hostname = self.getHostname (fqdn)

		# assemble args
		args = 'path='+dirname+' '
		args+= 'state=directory '
		args+= 'owner='+str(uid)+' '
		args+= 'group='+str(gid)+' '
		args+= 'mode='+modes+' '
	
		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'file',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()
		
		# success is demonstrated by several things
		if 'contacted' not in results :
			self.log ('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log ('FATAL: can\'t find '+hostname+' in results')
			return False
		host = contacted[hostname]
		if 'state' not in host :
			return False
		state = host['state']

		# this is the actual value we're looking for
		if state != 'directory' :
			return False

		return True

	def destroyDirectory (self, fqdn, dirname) :
		hostname = self.getHostname (fqdn)

		args = 'path='+dirname+' '
		args+= 'state=absent '
	
		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'file',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()

		if 'contacted' not in results :
			self.log ('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log ('FATAL: can\'t find '+unicode(hostname)+' in results')
			return False
		host = contacted[hostname] 
		if 'state'not in host :
			self.log ('FATAL: can\'t find \'state\' in host')
			self.log (unicode(host))
			return False
		state = host['state']

		if state != 'absent' :
			return False

		return True
	
	
	"""
	use the home-made 'linux-quota' plugin to put quotas in
	"""
	def applyQuotas (self, fqdn, user, dirname, soft=0, hard=0, present=True) :
		hostname = self.getHostname (fqdn)
		
		args = u'user='+unicode(user)+u' '
		# should handle escaping ?
		args+= u'dirname='+unicode(dirname)+u' '

		# special case, both quota values at 0 == no quotas
		if soft==0 and hard==0 :
			present=False

		if present :
			state = u'present'
			args+= u'state='+state+u' '
			args+= u'soft='+unicode(soft)+u' '
			args+= u'hard='+unicode(hard)+u' '
		else :
			state=u'absent'
			args+= u'state='+state+u' '
		
		# add this scripts' directory in the ansible directory list
		import os.path
		path = os.path.dirname(__file__)

		runner = ar.Runner (
			pattern= hostname,
			forks = 1,
			sudo = True,
			module_path = path,
			module_name = 'linux-quota.py',
			module_args = args,
			inventory = self.inventory
		)
		results = runner.run()
		
		#print results
		# error handling
		if 'contacted' not in results :
			self.log (u'FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log (u'FATAL: can\'t find '+unicode(hostname)+u' in results')
			return False
		host = contacted[hostname]
		if 'failed' in host :
			msg = ''
			if 'msg' in host :
				msg = host['msg']
			self.log (u'The plugin encountered an issue : '+unicode(msg))
			return False
		if 'state' not in host :
			self.log (u'FATAL: can\'t find the state in the response')
			self.log (results)
			return False
		tstate = host['state']
		if tstate != state :
			self.log (u'FATAL: the state in the response does not correspond to the requested state')
			return False

		return True

	def copy (self, fqdn, uid, gid, src, dest, modes) :
		ansible.utils.VERBOSITY=4
		hostname = self.getHostname (fqdn)

		# assemble args
		args = 'src='+src+' '
		args+= 'dest='+dest+' '
		args+= 'owner='+str(uid)+' '
		args+= 'group='+str(gid)+' '
		args+= 'mode='+modes+' '

		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'copy',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()

		if 'contacted' not in results :
			self.log ('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log ('FATAL: can\'t find '+hostname+' in results')
			# extract message 
			if 'dark' in results :
				dark = results['dark']
				if hostname in dark :
					host = dark[hostname]
					if 'msg' in host :
						msg = host['msg']
						self.log(msg)
			return False
		host = contacted[hostname]
		if 'changed' not in host :
			if 'msg' in host :
				self.log (host['msg'])
			self.log ('FATAL: unable to find \'changed\' in results')
			return False
		if host['changed'] :
			#self.log ('File copied over')
			pass
		else :
			self.log ('Destination file is identical to source')
	
		return True

	def fetch (self, fqdn, src, dest, fail_on_missing=True) :
		hostname = self.getHostname (fqdn)

		#assemble args
		args = 'src='+src+' '
		args+= 'dest='+dest+' '
		args+= 'fail_on_missing='+('yes' if fail_on_missing else 'no')

		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'fetch',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()

		if 'contacted' not in results :
			self.log ('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log ('FATAL: can\'t find '+hostname+' in results')
			if 'dark' in results :
				dark = results['dark']
				if hostname in dark :
					host = dark[hostname] 
					if 'msg' in host :
						msg = host['msg']
						self.log (msg)
			return False
		host = contacted[hostname]
		if 'changed' not in host :
			if 'msg' in host :
				self.log (host['msg'])
			self.log ('FATAL: unable to find \'changed\' in results')
			return False
		if host['changed'] :
			pass
		else :
			self.log ('Source file is identical to destination')

		return True

	def addLineInFile (self, fqdn, dest, line, regexp) :
		hostname = self.getHostname (fqdn)

		# assemble args
		args = 'dest='+dest+' '
		args+= 'line="'+line+'" '
		args+= 'regexp="'+regexp+'" '
		args+= 'state=present '

		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'lineinfile',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()

		if 'contacted' not in results :
			self.log ('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log ('FATAL: can\'t find '+hostname+' in results')
			return False
		host = contacted[hostname]
		if 'changed' not in host :
			self.log ('FATAL: unable to find \'changed\' in results')
			return False
		if not host['changed'] :
			self.log ('line was already present')
		return True

	def shell (self, fqdn, command) :
		hostname = self.getHostname (fqdn)

		args = command

		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'shell',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()

		if 'contacted' not in results :
			self.log ('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log ('FATAL: can\'t find '+hostname+' in results')
			return False
		host = contacted[hostname] 
		res = {}
		res['rc'] = host['rc']
		res['stdout'] = host['stdout']
		res['stderr'] = host['stderr']
		return res

	#==========================================================================
	#
	# TWiki related plugins
	#

	def twikiUserActive (self, fqdn, twikibase, twikiname) :
		pass

	"""
	Uses the homemade ansible plugin to remove the twiki user from active service
		* copies the .htpasswd file to a 
		* comments the users's line in the <twikibase>/data/.htpasswd file
	"""
	def twikiUserInactive (self, fqdn, twikibase, twikiname) :
		hostname = self.getHostname (fqdn)

		args = u'user='+unicode(twikiname)+u' '
		args+= u'twikibase='+unicode(twikibase)+u' '
		args+= u'state=inactive'

		import os.path
		path = os.path.dirname(__file__)
		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_path = path,
			module_name = 'twiki-user.py',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()
		#self.log(unicode(results))
		if 'contacted' not in results :
			self.log('FATAL: no \'contacted\' in results')
			return False
		contacted = results['contacted']
		if hostname not in contacted :
			self.log (str(results))
			self.log ('FATAL: can\'t find '+unicode(hostname)+' in results')
			return False
		host = contacted[hostname]
		if 'failed' in host :
			self.log ('Failed deactivating user '+unicode(twikiname)+' '+host['msg'])
			return False
		# if we are here, all is ok...
		return True
