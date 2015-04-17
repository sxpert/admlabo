# -*- coding: utf-8 -*-
import os
import ansible 
import ansible.runner as ar

#==================================================================================================
#
# low level drivers
#

class Ansible (object) :
	def __init__ (self) :
		ansible.utils.VERBOSITY=0
		self.inventory = ansible.inventory.Inventory ()

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

		self.log (args)	
		
		runner = ar.Runner (
			pattern     = hostname,
			forks       = 1,
			sudo        = True,
			module_name = 'copy',
			module_args = args,
			inventory   = self.inventory
		)
		results = runner.run ()

		self.log (results)
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
		if host['changed'] :
			self.log ('File copied over')
		else :
			self.log ('Destination file is identical to source')
	
		return True


