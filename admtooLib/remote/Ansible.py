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

	def copy (self, fqdn, uid, gid, src, dest, modes) :
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
			self.log (repr(results))
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


