#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess 
from syslog import syslog

REINSTALLED='/srv/reinstalling/'
KNOWN_HOSTS='/root/.ssh/known_hosts'

def remove_key (machine) :
	n = open ('/dev/null', 'w')
	ret = subprocess.call (['ssh-keygen', '-R', machine], stdout=n, stderr=n)
	n.close()
	if ret != 0:
		syslog ("ssh-keygen -R ERROR: failed to remove key for "+machine)

def remove_keys (ip, name) :
	remove_key (name)
	remove_key (ip)
	remove_key (name+','+ip)

def fetch_key (machine) :
	n = open ('/dev/null', 'w')
	f = open (KNOWN_HOSTS, 'a')
	ret = subprocess.call (['ssh-keyscan', '-H', machine], stdout=f, stderr=n)
	f.close ()
	n.close ()
	if ret != 0 :
		syslog ("ssh-keyscan -H ERROR: failed to find key for "+machine)

def fetch_keys (ip, name) :
	fetch_key (name+','+ip)
	fetch_key (ip)
	fetch_key (name)

def refresh_keys (ip, name) :
	# look for a file by the machines ip address in the proper directory
	rfile = REINSTALLED+ip
	try :
		s = os.stat (rfile)
	except OSError as e :
		return
	# if we could stat, the file exists
	# time to refresh the machine's ssh keys
	syslog("refreshing keys for "+ip+" / "+name)
	remove_keys (ip, name)
	fetch_keys (ip, name)
	# remove the file
	os.unlink (rfile)
