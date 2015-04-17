# -*- coding: utf-8 -*-
import os
from django.conf import settings

from remote import Ansible as rem

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
	a = rem()
	if not a.createDirectory (fqdn, dirname, uid, gid, modes) :
		a.log ('FATAL: Unable to create directory \n'+str(results))
		return False
	a.log ('répertoire créé, création des fichiers')
	ok = True
	a.log (files)
	if (files is not None) and ('files' in files) :
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
			# src and dest should be complet file names
			src  = os.path.join(settings.ADMIN_FILES_DIR,f['src'])
			dest = os.path.join(dirname,f['dest'])
			if not a.copy (fqdn, uid, gid, src, dest, modes) :
				a.log ('copy fail')
				ok = False
				break
			a.log ('copy success')
	a.log (ok)
	return ok



