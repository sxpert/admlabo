# -*- coding: utf-8 -*-
import os, sys
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
		a.log ('FATAL: Unable to create directory')
		return False
	a.log ('répertoire créé, création des fichiers')
	ok = True
	a.log (files)
	if files is not None :
		# handle directory quotas
		if 'quotas' in files :
			q = files['quotas']
			if 'soft' in q :
				soft = int(q['soft'])
			else:
				soft = 0
			if 'hard' in q :
				hard = int(q['hard'])
			else :
				hard = 0
			if (hard!=0) or (soft!=0) :
				# apply quota command
				a.log (u'applying quota command : soft='+unicode(soft)+u', hard='+unicode(hard))
				if not a.applyQuotas (fqdn, uid, dirname, soft, hard) :
					a.log ('FATAL: unable to set quota on directory')
					return False

		# handle files to be copied
		if 'templates' in files :
			fls = files['templates']
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

# 
# 
#
MTYPE_LINUX   = 0
MTYPE_MACOS   = 1
MTYPE_WINDOWS = 2

def setupBackupPc (fqdn, user, mtype) :
	a = rem()
	# plusieurs facons de faire en fonction de l'os de la machine distante
	if mtype == MTYPE_LINUX :
		# TODO
		return False
	elif mtype == MTYPE_MACOS :
		# TODO
		return False
	elif mtype == MTYPE_WINDOWS :
		# 0. generate a complicated password
		passwd = a.generatePassword (16)
		if (type(passwd) is bool) :
			if not passwd :
				return False
			else :
				# should not happen
				a.log ("setupBackupPc : generatePassword returned \'True\' should not happen")
				return False
		# 1. build the backuppc config file
		import tempfile
		fd, fname = tempfile.mkstemp()
		f = os.fdopen(fd, "w")
		f.write('$Conf{RsyncShareName} = [\n'+\
				'  \'Users\'\n'+\
				'];\n'+\
				'$Conf{RsyncdPasswd} = \''+passwd+'\';\n'+\
				'$Conf{RsyncdUserName} = \'backuppc\';\n'+\
				'$Conf{XferMethod} = \'rsyncd\';\n');
		f.flush ()
		# 2. send the file to the backuppc server
		machine = a.getHostname (fqdn)
		dest = '/etc/BackupPC/pc/'+machine+'.pl'
		if not a.copy ( settings.BACKUPPC_SERVER, 
						settings.BACKUPPC_USER, 
						settings.BACKUPPC_GROUP, 
						fname, dest, '0640' ) :
			return False
		# 3. close the temp file
		f.close ()
		os.unlink(fname)
		# 4. add a line in the backuppc hosts file for that machine and user
		if not a.addLineInFile ( settings.BACKUPPC_SERVER, 
								 '/etc/BackupPC/hosts',
								 machine+'\t0\t'+user,
								 '^'+machine+'.*' ) :
			return False
		# done
		return passwd
	# unknown OS
	return False
	
if __name__ == '__main__' :
	#if __package__ is None :
	#	from os import path
	#	sys.path.append (path.dirname(path.dirname(path.abspath(__file__))))
	#	from admtooCore import settings 
	#passwd = setupBackupPc ('gag8131.obs.ujf-grenoble.fr', 'jacquotr', MTYPE_WINDOWS)
	#sys.stderr.write (passwd+'\n')
	#a = rem()
	#print(a.applyQuotas ('ipag-stoc1.obs.ujf-grenoble.fr', 'ansible', '/user/homedir/ansible', 0, 0, True))
	#print(a.applyQuotas ('ipag-stoc1.obs.ujf-grenoble.fr', 'ansible', '/user/homedir/ansible', 10485760, 11534336))
	




	pass
