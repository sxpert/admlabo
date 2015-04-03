#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import SOAPpy

import socket
import struct

#wsdlFile = 'https://ipam.ujf-grenoble.fr/interfaces/wsdl_eip_full.wsdl'
wsdlFile = '/srv/progs/ipag/wsdl_eip_full.wsdl'

class Ipam (object) :
	def __init__ (self, login, passwd) :
		self.login = login
		self.passwd = passwd
		self.server = SOAPpy.WSDL.Proxy (wsdlFile)

	def ip_address_list (self) :
		address_list = self.server.ip_address_list ({'auth_login':self.login,'auth_password':self.passwd})
		l = address_list['item']
		ips = []
		for ip in l :
			addr = socket.inet_ntoa(struct.pack("<L", int(ip.ip_addr,16)))
			id  = ip.ip_id
			ips.append({'addr':addr,'id':id})
		return ips

if __name__ == '__main__' :
	ipam = Ipam ('jacquotr', 'hok123')
	
	l = ipam.ip_address_list ()
	print l

	
