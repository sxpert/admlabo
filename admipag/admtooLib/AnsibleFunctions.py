# -*- coding: utf-8 -*-
import ansible 
import ansible.runner as ar

# this works only when running as root (for now)
# if not running as root, it should somehow have access to
# the ansible user's private key
# note that it sounds like a bad thing for the web server
# to have access to the key in question.
# preferably, this should run in a cron process running as root
def createDirectory (machine_fqdn, dirname, uid, gid, modes) :
	p = machine_fqdn.find ('.')
	if p==-1 :
		hostname = machine_fqdn # strange
	else :
		hostname = machine_fqdn[:p]

	import sys
	sys.stderr.write ('hostname \''+hostname+'\'\n')

	args = 'path='+dirname+' '
	args+= 'state=directory '
	args+= 'owner='+str(uid)+' '
	args+= 'group='+str(gid)+' '
	args+= 'mode='+modes+' '

	sys.stderr.write ('args \''+args+'\'\n')
	
	ansible.utils.VERBOSITY=0
	inv = ansible.inventory.Inventory ()

	#
	runner = ar.Runner (
		pattern     = hostname,
		forks       = 1,
		sudo        = True,
		module_name = 'file',
		module_args = args,
		inventory   = inv
	)
	results = runner.run ()
	if 'contacted' in results.keys() :
		contacted = results['contacted']
		if hostname in contacted :
			host = contacted[hostname]
			if 'state' in host.keys() :
				state = host['state']
				sys.stderr.write ('state=\''+state+'\'\n')
				if state == 'directory' :
					return True
	sys.stderr.write ('FATAL: Unable to create directory \n'+str(results))
	return False

