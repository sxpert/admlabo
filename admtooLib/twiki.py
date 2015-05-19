#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

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
				s += c
		return s

	def gen_wiki_name (self, fname, lname) :
		fname = self._format_name (fname)
		lname = self._format_name (lname)
		return fname+lname

if __name__ == '__main__' :
	t = TWiki ('ipag.osug.fr', '/var/www/twiki/data')
	twikiname = t.gen_wiki_name ('raphael', 'jacquot-total')
	print twikiname
