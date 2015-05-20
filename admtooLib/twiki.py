#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, json

class TWiki (object) :
	def __init__ (self, twiki_server, twiki_data_path) :
		self.srv = twiki_server
		self.path = twiki_data_path

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
			print members
	
#if __name__ == '__main__' :
#	t = TWiki ('ipag.osug.fr', '/var/www/twiki/data')
#	twikiname = t.gen_wiki_name ('raphael', 'jacquot-total')
#	print twikiname
