# -*- coding: utf8 -*-

import os, sys, json
import admtooLib.AdminFunctions as af
# twiki config should be in config sub module...
from .config.twiki import *

class TWiki (object) :
	
	def __init__ (self) :
		self._logger = None
	
	def _log (self, message) :
		if self._logger is not None :
			self._logger.error (message)
		else:
			import logging
			logging.error (message)

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

	#==========================================================================
	# generator functions

	def gen_user_name (self, fname, lname) :
		fname = self._format_name (fname)
		lname = self._format_name (lname)
		return fname+lname

	def _copy_file_to_twiki_server (self, s, encoding, basedir, filename) :
		# copy the contents of s to the twiki system, so as to update the contents of the group
		a = af.rem()
		# save to a temporary file
		import tempfile
		f = tempfile.NamedTemporaryFile ()
		f.write (s.encode(encoding))
		f.flush ()
		import os
		# call the remote access file copy
		res = a.copy (TWIKI_SERVER, TWIKI_FILE_OWNER, TWIKI_FILE_GROUP, f.name, 
					  os.path.join(basedir, filename), '0664')
		# destroy the temporary file		
		f.close()
		if not res : 
			return False
		# everything is fine
		return True

	def _gen_group_config (self, gdata) :
		# generate list of users
		self._log ("_gen_group_config")
		members = []
		self._log (gdata.keys())
		if 'appSpecName' in gdata.keys() :
			if gdata['appSpecName'] is None :
				self._log ('appSpecName is None, this groups is not a twiki group')
				# tell the caller that everything is fine, even if we didn't do anything
				return True
			asn = gdata['appSpecName']
			self._log ("asn : "+str(asn))
			if ('twiki' in asn.keys()) and ('members' in gdata.keys()) :
				twiki_group_name = asn['twiki']
				self._log (twiki_group_name)
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
				self._log (s)
			
				# copy the contents of s to the twiki system, so as to update the contents of the group
				a = af.rem()
				# save to a temporary file
				import tempfile
				f = tempfile.NamedTemporaryFile ()
				f.write (s.encode('utf-8'))
				f.flush ()
				import os
				# call the remote access file copy
				res = a.copy (TWIKI_SERVER, TWIKI_FILE_OWNER, TWIKI_FILE_GROUP, f.name, 
							  os.path.join(TWIKI_MAIN, twiki_group_name+'.txt'), '0664')
				# destroy the temporary file		
				f.close()
				if not res : 
					a.log ('FATAL: Impossible to create twiki group '+twiki_group_name+'\nunable to copy file to it\'s destination')
					return False
				# everything is fine
				return True
			else :
				# need to log this better
				self._log('FATAL: missing bits in group data')
				return False
		else :
			self._log('no appSpecName defined')
			return False

	def _gen_kifekoi_table (self) :
		
		pass

	#==========================================================================
	# commands

	def UpdateTWikiGroup (self, *args, **kwargs) :
		_, command = args
		if "logger" in kwargs.keys() :
			logger = kwargs['logger']
			if logger is not None :
				self._log ('setting logger to '+str(logger))
				self._logger = logger
		c = json.loads (command.data)
		return self._gen_group_config (c)
	
	def UpdateGroup (self, *args, **kwargs) :
		from admtooCore.models import command
		import json
		_, cmd = args

		# check if we actually have a twiki information 
		d = json.loads(cmd.data)
		msg = ''
		if 'appSpecName' in d.keys() :
			asn = d['appSpecName']
			if asn is not None :
				if 'twiki' in asn.keys() :
					twiki_name = asn['twiki']
					if twiki_name is not None :
						c = command.Command ()
						c.user = cmd.user
						c.verb = 'UpdateTWikiGroup'
						c.data = cmd.data
						c.in_cron = True
						msg = 'SUCCES: post UpdateTWikiGroup command'
						c.post ()
					else: 
						msg = 'ERROR: twiki_name is present but None'
				else :
					msg = 'ERROR: twiki_name is absent'
			else :
				msg = 'ERROR: appSpecName is None'
		else :
			msg = 'ERROR: appSpecName is absent'
		self._log ('TWiki.UpdateGroup : '+msg)
			
		return True
		
	#
	# launched from crontab
	# 
	def	UpdateKiFeKoi (self, *args, **kwargs) :
		from admtooCore.models import user
		import time

		# gets the contents of the list to generate the kifekoi document with
		kfk = user.User.generate_kifekoi_list ()

		# generate the document		
		# header
		s = u'%META:TOPICINFO{author="adminToolCore-Twiki-module" date="'+str(int(time.time()))+u'"}%\n'
		s+= u'%TABLE{ sort="on" tableborder="1" cellpadding="1" cellspacing="1" headerrows="1" footerrows="0" }%\n'
		s+= u'| * %ICONURL{ipagSecours}%* | * %ICONURL{ipagExtincteur}%* | * %ICONURL{ipagEvacuation}%* '
		s+= u'| * %ICONURL{ipagHS}%* | *NOM* | *Prénom* | *Équipe* | *Tél.* | ** | *Bureau* | *Autres* |\n'

		# content
		for u in kfk :
			f = u['flags']
			# emergency manager
			l = u'| '	
			if 'secours' in f :	
				l+= u'%ICONURL{ipagSecours}% '
			# fire training
			l+= u'| '
			if 'extincteur' in f :
				l+= u'%ICONURL{ipagExtincteur}% '
			# evacuation training
			l+= u'| '
			if 'evacuation' in f :
				l+= u'%ICONURL{ipagEvacuation}% '
			# health and safety
			l+= u'| '
			if 'HS' in f :
				l+= u'%ICONURL{ipagHS}% '
			# user info
			l+= u'| <noautolink>'+u['last_name']+u'</noautolink> '
			l+= u'| <noautolink>'+u['first_name']+u'</noautolink> '
			l+= u'| '
			
			# team
			if 'team' in u.keys() : 
				if u['team'] is not None :
					l+= u'%ICONURL{'+u['team']+'}% '
			
			# telephone
			l+= u'| '
			if u['telephone'] is not None :
				l+= u['telephone'][-5:]+u' '
			# office
			l+= u'| | '
			if u['room'] is not None :
				l+= '%NOP%'+u['room']+u' '
			# other flags
			l+= u'| '
			
			if 'membreCL' in f:
				l+= '%ICONURL{ipagMembreCL}% '
			if 'responsable' in f:
				l+= '%ICONURL{ipagResponsable}% '
			if 'cafet' in f:
				l+= '%ICONURL{ipagCafet}% '
			if 'refthesard' in f:
				l+= '%ICONURL{ipagRefthesard}% '
			if 'coStages' in f:
				l+= '%ICONURL{ipagStages}% '
			if 'coSeminaires' in f:
				l+= '%ICONURL{ipagSeminaires}% '
			if 'coFormation' in f:
				l+= '%ICONURL{ipagFormation}% '
			if 'acmo' in f:
				l+= '%ICONURL{ipagAcmo}% '
			if 'flag_annuaire' in f :
				l+= '%ICONURL{ipagFlag_annuaire}% '
			if 'flag_photo_web' in f :
				l+= '%ICONURL{ipagFlag_photo_web}% '			
	
			# the end
			l+= u'|'

			l+= u'\n'
			
			s+= l
		# footer

		s+= u'---\n'
		s+= u'<small> <font color="#808080">\n'
		s+= u'_Dernière mise à jour : '+time.strftime('%d %B %Y')+u'_\n'
		s+= u'</small>\n'
		s+= u'\n'
		s+= u'<!--\n'
		s+= u'   * Set CACHEABLE = off\n'
		s+= u'-->\n'

		# upload the document to the twiki server
		if self._copy_file_to_twiki_server (s, 'iso-8859-15', TWIKI_DATA, 'Ipag/Intranet/KifekoiTable.txt') :
			# TODO: cleanup all UpdateKiFeKoi commands that are waiting in the list
			return True

		self._log ('FATAL: Unable to install new version of KiFeKoi table in the twiki instance')

		return False
