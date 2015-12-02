#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import errno
import stat
import subprocess
import time
import xml.etree.ElementTree as et
from syslog import syslog

XMLDB="/srv/data/xmldatabase.xml"
XMLDBUSR="laogtool"
XMLDBSRV="admlaog"
XMLDBSRC="/home/laogtool/laogtool/Production/data/db/default/admtooDatabase.xml"

xmlroot = None

def refresh_database () :
	global xmlroot
	
	xmldblocation=XMLDBUSR+"@"+XMLDBSRV+":"+XMLDBSRC
	subprocess.call(["rsync",xmldblocation,XMLDB])
	xmlroot = load_xmldb()

def check_and_get_database () :
	try :
		s = os.stat (XMLDB)
	except OSError as e :
		if e.errno == errno.ENOENT :
			refresh_database ()
			return
	# database exists, check date
	curt = time.time()
	if (s.st_mtime+60<curt) :
		refresh_database()

def load_xmldb () :
	t = et.parse (XMLDB)
	r = t.getroot()
	return r
		
def find_user_for_machine (machine_name) :
	if xmlroot is None :
		syslog('FATAL: unable to load XML database')
		return None
	for host in xmlroot.iter('host') :
		a = host.attrib
		if "name" in a :	
			name = a["name"]
			if name == machine_name :
				# find an "owner" entry
				o = host.findall('owner')
				if len(o)==1 :
					o = o[0]
					return o.text
				# too many owners, we have a problem
	syslog ("unable to find machine "+machine_name+"in xmldb")
	return None

# récupères la liste des utilisateurs

def get_users () :
	global xmlroot
	if xmlroot is None :
		refresh_database ()
	users = {}
	for user in xmlroot.iter('user') :
		first_name = user.find ('firstName').text
		last_name = user.find ('lastName').text
		login = user.find ('login').text
		agalan_login = user.find ('agalanLogin').text
		if login != agalan_login :
			print "different login '"+login+"' and agalan_login '"+agalan_login+"' for user "
			continue
		
		uid = user.find ('uid').text
		try :
			uid = int(uid)
		except :
			print "problem for user "+login+" uid '"+str(uid)+"' is not a number"
			continue

		birth_date = user.find ('birthDate')
		if birth_date is not None :
			birth_date = birth_date.text

		affiliation = user.find ('affiliation')
		if affiliation is not None :
			a = affiliation.attrib
			if 'idref' in a :
				affiliation = a['idref']
			else :
				affiliation = None
		
		responsible_ref = user.find ('responsibleRef')
		if responsible_ref is not None :
			a = responsible_ref.attrib
			if 'name' in a :
				responsible_ref = a['name']
			else :
				responsible_ref = None

		user_class_ref = user.find ('userClassRef')
		if user_class_ref is not None :
			a = user_class_ref.attrib
			if 'idref' in a :
				user_class_ref = a['idref']
			else :
				user_class_ref = None

		gid = None
		group_refs = user.find ('groupRefs')
		groups = []
		for group in group_refs.iter('groupRef') :
			if group is not None :
				a = group.attrib
				if 'name' in a :
					g = a['name']
					groups.append (g)
					if 'type' in a :
						t = a['type']
						if t == 'effective' :
							gid = g
	
		tags = user.find ('tags')
		t = []		
		if tags is not None :
			for tag in tags.iter('tag') :
				if tag is not None :
					tag = tag.text
					if tag not in t :
						t.append(tag)
		tags = t

		room_number = user.find ('roomNumber')
		if room_number is not None :
			room_number = room_number.text

		telephone_number = user.find ('telephoneNumber')
		if telephone_number is not None :
			telephone_number = telephone_number.text

		arrival_date = user.find ('arrivalDate')
		if arrival_date is not None :
			arrival_date = arrival_date.text

		departure_date = user.find ('departureDate')
		if departure_date is not None :
			departure_date = departure_date.text
	
		user = {}
		user['first_name'] = first_name
		user['last_name'] = last_name
		user['login'] = login
		user['uid'] = uid
		user['gid'] = gid
		user['birth_date'] = birth_date
		user['affiliation'] = affiliation
		user['manager'] = responsible_ref
		user['user_class'] = user_class_ref
		user['groups'] = groups
		user['tags'] = tags
		user['room_number'] = room_number
		user['telephone_number'] = telephone_number
		user['arrival_date'] = arrival_date
		user['departure_date'] = departure_date
		
		users[uid] = user
	
	return users

def parse_groups (parent) :
	groups = {}
	if parent.tag == 'groups' :
		p = None
	else :
		# find id 
		pgid = parent.find('gid')
		if pgid is not None :
			pgid = int(pgid.text)
			p = pgid
		else :
			print "can't find gid for parent group"
			return None

	l = list(parent)
	tg = []
	for i in l :
		if i.tag=='group' :
			tg.append(i)
	
	for g in tg :
		
		if g is None:
			return groups

		gid = g.find('gid')
		if gid is not None :
			gid = int(gid.text)
		
		name = g.find('name')
		if name is not None :
			name = name.text

		description = g.find('description')
		if description is not None :
			description = description.text

		type_group = None
		if g.find('serviceGroup') is not None :
			type_group = 'SERVICE'
		if g.find('teamGroup') is not None :
			type_group = 'TEAM' 

		group = {}
		group['gidNumber'] = gid
		group['gid'] = name
		group['description'] = description
		group['parent'] = p
		group['type'] = type_group

		groups[gid] = group

		cg = parse_groups(g)
		
		for k in cg.keys() :
			groups[k] = cg[k]
		
	return groups


def get_groups () :
	g = xmlroot.find('groups')
	if g is not None :
		groups = parse_groups (g)	
		return groups
	print "dafuq ?? unable to find groups !"

def parse_mailinglists (parent) :
	lists = {}
	if parent.tag == 'mailingLists' :
		p = None
	else :
		p = parent.attrib['id']

	l = list(parent)
	tml = []
	for i in l :
		if i.tag == 'mailingList':
			tml.append (i)
	for ml in tml :
		if ml is None :
			return lists
		ml_id = ml.attrib['id']
	
		if 'userClass' in ml.attrib :
			userclass = ml.attrib['userClass']
		else :
			userclass = None
	
		name = ml.find ('name')
		if name is not None :
			name = name.text
	
		description = ml.find ('description')
		if description is not None :
			description = description.text

		groupref = ml.find ('groupRef')
		if (groupref is not None) and ('name' in groupref.attrib.keys()) :
			groupref = groupref.attrib['name']
		else :
			groupref = None
		
		ucls = ml.findall('userClassLabel')
		if ucls is not None and len(ucls)>0 :
			ucl={}
			for uc in ucls :
				if 'lang' in uc.attrib :
					lang = uc.attrib['lang']
				else :
					lang = 'fr'
				ucl[lang] = uc.text
		else :
			ucl = None
		print ucl

		mailinglist = {}
		mailinglist['id'] = ml_id
		mailinglist['userclass'] = userclass
		mailinglist['parent'] = p
		mailinglist['name'] = name
		mailinglist['description'] = description
		mailinglist['group'] = groupref		
		mailinglist['ucl'] = ucl

		lists[ml_id] = mailinglist
	
		cml = parse_mailinglists (ml)
		for k in cml.keys() :
			lists[k] = cml[k]
	return lists

def get_mailinglists () :
	ml = xmlroot.find('mailingLists')
	if ml is not None :
		mailinglists = parse_mailinglists (ml)
		return mailinglists
	print "dafuq ?? unable to find mailing lists !"

def get_machine_classes () :
	classes = []
	cls = xmlroot.find('serverClasses')
	if cls is None :
		return None
	for c in cls.iter('serverClass') :
		a = c.attrib
		name = None
		if 'name' in a :
			name = a['name']
		title = c.find('title')
		if title is not None :
			title = title.text
		information = c.find('information')
		if information is not None :
			information = information.text
		
		cl = {}
		cl['name'] = name
		cl['title'] = title
		cl['information'] = information
		classes.append (cl)
		
	return classes

def get_vlans_machines () :
	vlans = []
	machines = []

	global xmlroot
	if xmlroot is None :
		refresh_database ()
	vlans_item = xmlroot.find('vlans')
	for vlan in vlans_item.iter('vlan'):
		# vlans
		a = vlan.attrib

		if 'id' in a :
			id = a['id']
		else :
			print "FATAL: vlan has no id"
			print a
			sys.exit(1)

		if 'name' in a :
			name = a['name']
		else :
			print "problem in vlan, no name found"
			print a		
			sys.exit(1)
	
		if 'lan' in a:
			lan = a['lan']
		else:
			print "problem in vlan, no ip block found"
			print a
			sys.exit(1)

		if 'gateway' in a:
			gateway = a['gateway']
		else :
			print "vlan has no gateway specified"
			print a
			sys.exit (1)

		v = {}
		v['vlan_id'] = id
		v['name'] = name
		v['ip_block'] = lan
		v['gateway'] = gateway
		vlans.append(v)
		
		# machines
		for host in vlan.iter('host') :
			a = host.attrib
			
			if 'name' in a :
				name = a['name']
			else : 
				print "host has no name"
				print a
				sys.exit(1)
		
			aliases = host.find('aliases')
			al = []
			if aliases is not None :
				for alias in list(aliases) :
					al.append(alias.text)
			aliases = al

			classes = host.find('class')
			cl = []
			if classes is not None :
				for c in list(classes) :
					cl.append (c.tag)
			classes = cl
	
			ip = host.find('ip')
			if ip is not None :
				ip = ip.text
			
			mac = host.find('mac')
			if mac is not None :
				mac = mac.text

			addressing = host.find('addressing')
			if addressing is not None :
				ad = addressing.text
				
				adtypes = [ None, 'statique', 'dynamique avec reservation', 'dynamique']
				idx = adtypes.index (ad)
				if idx is None :
					print "problem, unknown addressing type '"+str(ad)+"'"
					sys.exit (1)
				sysadtypes = [ None, 'STATIC', 'DHCP-MAC', 'DHCP']
				addressing = sysadtypes[idx]

			text = host.find('text')
			if text is not None :
				text = text.text

			owner = host.find('owner')
			if owner is not None :
				owner = owner.text

			h = {}
			h['vlan'] = v['vlan_id']
			h['name'] = name
			h['aliases'] = aliases
			h['classes'] = classes
			h['ip'] = ip
			h['mac'] = mac
			h['addrtype'] = addressing
			h['text'] = text
			h['owner'] = owner

#			print h
			machines.append (h)

	return (vlans, machines,)

if __name__ == '__main__' :
	users = get_users ()
	print users
	vlm = get_vlans_machines ()
	print vlm
else :
	print "loading database"
	check_and_get_database ()
