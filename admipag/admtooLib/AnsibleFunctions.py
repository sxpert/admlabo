# -*- coding: utf-8 -*-

import ansible.runner as ar

#   # créer le répertoire PRIVATE
#   args = "group="+group+" "
#   args+= "mode=700 "
#   args+= "owner="+uid+" "
#   args+= "path=/home/"+uid+"/PRIVATE/ "
#   args+= "state=directory "
#
#   runner = ansible.runner.Runner (
#           pattern=hostname,
#           forks=1,
#           sudo=True,
#           module_name="file",
#           module_args=args,
#           inventory = inv
#       )
#   results = runner.run()

def createDirectory (machine_fqdn, dirname, uid, gid, modes) :
	# get the hostname
	# that is the first bit of the machine fqdn
	p = machine_fqdn.find ('.')
	if p==-1 :
		hostname = machine_fqdn # strange
	else :
		hostname = machine_fqdn[:p]

	import sys
	sys.stderr.write ('hostname \''+hostname+'\'\n')

	return False

	#
	runner = ar.Runner (
		
	)
	results = runner.run ()
	pass

