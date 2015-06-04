# -*- coding: utf-8 -*-

import sys, json
import admtooLib.AdminFunctions as af
# twiki config should be in config sub module...
from .config.twiki import *

class TWiki (object) :
	
	def __init__ (self) :
		print "initializing TWiki plugin" 
		self._logger = None
		self.srv = settings.TWIKI_SERVER
		self.path = settings.TWIKI_DATA
	
	def _log (self, message) :
		if self._logger is not None :
			self._logger.error (message)
		else:
			sys.stdout.write (str(message)+'\n')
			sys.stdout.flush ()

	def _format_name (self, name) :
		s = ''
		first = True
		for c in name :
			if c in ' -\'' :
				# skip and set first
				first = True
				continue
			else :
				if first :
					c = c.upper()
					first = False
				else :
					c = c.lower()
				s += c
		return s

	def gen_user_name (self, fname, lname) :
		fname = self._format_name (fname)
		lname = self._format_name (lname)
		return fname+lname

	def gen_group_config (self, gdata) :
		# generate list of users
		members = []
		if 'appSpecName' in gdata.keys() and gdata['appSpecName'] is not None :
			asn = gdata['appSpecName']
			if ('twiki' in asn.keys()) and ('members' in gdata.keys()) :
				twiki_group_name = asn['twiki']
				gdm = gdata['members']
				for m in gdm :
					n = None
					if 'appSpecName' in m.keys() :
						asn=m['appSpecName']
						try :
							asn = json.loads(asn)
						except ValueError as e :
							pass
						else :
							if 'twiki' in asn :
								n = asn['twiki']
					if (n is None) and ('first_name' in m.keys()) and ('last_name' in m.keys()) :
						n = self.gen_user_name (m['first_name'], m['last_name'])
					if n is None :
						continue
					members.append(n)
				# sort members
				members.sort()
				# generate members list
				members = ['Main.'+s for s in members]
				twiki_group_members = ', '.join(members)

				import time
				# generate file
				s = u'%META:TOPICINFO{author="adminToolCore-Twiki-module" date="'+str(int(time.time()))+u'"}%\n'
				s+= u'%META:TOPICPARENT{name="TWikiGroups"}%\n'
				s+= u'---+!! <nop>'+twiki_group_name+u'\n'
				s+= u'\n'
				s+= u'   * Member list:\n'
				s+= u'      * Set GROUP = '+twiki_group_members+u'\n'
				s+= u'\n'
				s+= u'   * Persons/group who can change the list:\n'
				s+= u'      * Set ALLOWTOPICCHANGE = '+twiki_group_name+u'\n'
				s+= u'\n'
				s+= u'__%MAKETEXT{"Related Topics:"}%__ %WIKIUSERSTOPIC%, TWikiGroups, %TWIKIWEB%.TWikiAccessControl\n'
				s+= u'---\n'
				s+= u'<small> <font color="#808080">\n'
				s+= u'_Dernière mise à jour : '+time.strftime('%d %B %Y')+u'_\n'
				s+= u'</small>\n'
				s+= u'\n'
				s+= u'<!--\n'
				s+= u'   * Set CACHEABLE = off\n'
				s+= u'-->\n'
				print s
			
				# copy the contents of s to the twiki system, so as to update the contents of the group
				a = af.rem()
				# save to a temporary file
				import tempfile
				f = tempfile.NamedTemporaryFile ()
				f.write (s.encode('utf-8'))
				f.flush ()
				import os
				# call the remote access file copy
				res = a.copy (settings.TWIKI_SERVER, settings.TWIKI_FILE_OWNER, settings.TWIKI_FILE_GROUP,
				              f.name, os.path.join(settings.TWIKI_MAIN, twiki_group_name+'.txt'), '0664')
				# destroy the temporary file		
				f.close()
				if not res : 
					a.log ('FATAL: unable to copy file to it\'s destination')
			else :
				# need to log this better
				print 'FATAL: missing bits in group data'

	def UpdateGroup (self, *args, **kwargs) :
		self._log ("TWiki plugin UpdateGroup")
		self._log ("args    : "+str(args))
		self._log ("kwargs  : "+str(kwargs))
		_, command = args
		self._log ("command : "+str(command))
		self._log ("verb    : "+str(command.verb))
		self._log ("data    : "+str(command.data))
		if "logger" in kwargs.keys() :
			logger = kwargs['logger']
			if logger is not None :
				self._log ('setting logger to '+str(logger))
				self._logger = logger
		
		
