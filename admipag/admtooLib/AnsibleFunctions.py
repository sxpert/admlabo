# -*- coding: utf-8 -*-
import os
from django.conf import settings
import ansible 
import ansible.runner as ar


ansible.utils.VERBOSITY=0

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

	def copy (self, fqdn, dirname, uid, gid, src, dest, modes) :
		hostname = self.getHostname (fqdn)

		self.log (settings.ADMIN_FILES_DIR)
		self.log (dirname)
		# assemble args
		args = 'src='+os.path.join(settings.ADMIN_FILES_DIR,src)+' '
		args+= 'dest='+os.path.join(dirname,dest)+' '
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

#==================================================================================================
#
# high level functional bits
#

# this works only when running as root (for now)
# if not running as root, it should somehow have access to
# the ansible user's private key
# note that it sounds like a bad thing for the web server
# to have access to the key in question.
# preferably, this should run in a cron process running as root
def createDirectory (fqdn, dirname, uid, gid, modes, files) :
	a = Ansible()
	if not a.createDirectory (fqdn, dirname, uid, gid, modes) :
		a.log ('FATAL: Unable to create directory \n'+str(results))
		return False
	a.log ('répertoire créé, création des fichiers')
	ok = True
	a.log (files)
	if 'files' in files :
		fls = files['files']
		a.log (fls)
		for f in fls :
			a.log (f)
			if (not (( 'src' in f ) and ( 'dest' in f))) :
				a.log ('can\'t find src AND dest')
				ok = False
				break
			a.log ('lauching template')
			if 'modes' not in f :
				modes = '0600' # default value... only for the user
			else :
				modes = f['modes']
			if not a.copy (fqdn, dirname, uid, gid, f['src'], f['dest'], modes) :
				a.log ('copy fail')
				ok = False
				break
			a.log ('copy success')
	a.log (ok)
	return ok



