from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from ...models import *
import sys, hashlib
from admtooLib import ldaplaog as l, xmldb as x

class Command(BaseCommand) :
	group_map = [
		# team groups
		('ipagsite',            'ipag-pos-site'),
		('perm',                'ipag-pos-permanent'),
		('admin',               'ipag-pos-administratif'),
		('chercheur',           'ipag-pos-chercheur'), 
		('ingetech',            'ipag-pos-groupetechnique'),
		('thesard',             'ipag-pos-doctorant'),
		('invites',             'ipag-pos-invite'),
		('postdoc',             'ipag-pos-postdoctorant'),
		('stage',               'ipag-pos-stagiaire'),
		('master2',             'ipag-pos-etudiant'),
		('astromol',            'ipag-pos-astromol'),
		('cristal',             'ipag-pos-cristal'),
		('planeto',             'ipag-pos-planeto'),
		('sherpas',             'ipag-pos-sherpas'),
		('chercheuraffilie',    'ipag-pos-affilie'),
	
		('aero',                'ipag-pos-aero'),
		('amber',               'ipag-pos-amber'),
		('consert',             'ipag-pos-consert'),
		('direction',           'ipag-pos-direction'),
		('electronique',        'ipag-pos-electronique'),
		('exoplanetes',         'ipag-pos-exoplanetes'),
		('extra',               'ipag-pos-extra'),	
		('fost',                'ipag-pos-fost'),
		('gravity',             'ipag-pos-gravity'),
		('informatique',        'ipag-pos-informatique'),
		('jmmc',                'ipag-pos-jmmc'),
		('marsis',              'ipag-pos-marsis'),
		('neat',                'ipag-pos-neat'),
		('odyssey',             'ipag-pos-odyssey'),
		('pionier',             'ipag-pos-pionier'),
		('radar',               'ipag-pos-radar'),
		('safir',               'ipag-pos-safir'),
		('services',            'ipag-pos-services'),
		('sharad',              'ipag-pos-sharad'),
		('spectro',             'ipag-pos-spectro'),
		('sphere',              'ipag-pos-sphere'),
		('virtis',              'ipag-pos-virtis'),
		('xlabuser',            'ipag-pos-xlabuser'),

		# machine related groups
		('dmz98',               'ipag-ssh-dmz98'),
		('extra-blue',          'ipag-ssh-extra-blue'),
		('guepard',             'ipag-ssh-guepard'),
		('maui',                'ipag-ssh-maui'),
		('picsou',              'ipag-ssh-picsou'),

		# web site related groups
		('web-anr-chaos',       'ipag-web-anr-chaos'),
		('web-asa',             'ipag-web-asa'),	
		('web-benchmarks',      'ipag-web-benchmarks'),
		('web-chemical-cosmos', 'ipag-web-chemical-cosmos'),
		('web-desc',            'ipag-web-desc'),
		('web-exochemistry',    'ipag-web-exochemistry'),
		('web-focus',           'ipag-web-focus'),
		('web-hydrides',        'ipag-web-hydrides'),
		('web-nika2',           'ipag-web-nika2'),
		('web-rt13',            'ipag-web-rt13'),
		('web-stflorent',       'ipag-web-stflorent')
	]

	help = 'Synchronizes the database from the LDAP server and the XML database'

	def log(self, message) :
		sys.stdout.write ("\n"+message)
		sys.stdout.flush ()

	def dot(self) :
		sys.stdout.write ('.')
		sys.stdout.flush ()

	def map_group_name (self, name) :
		for g in self.group_map :
			o, n = g
			if name == o :
				name = n
				break
		return name

	def group (self, gd) :
		if gd is None :
			self.log ("group_data is None, aborting")
			return
		gidnumber = gd['gidNumber']
		if gidnumber is None :
			self.log ("gidnumber is None, aborting")
			return
		if not isinstance(gidnumber, list) or len(gidnumber) != 1 : 
			self.log ("gidnumber is not a 1 item list")
			return
		try :
			gidnumber = int(gidnumber[0])
		except :
			self.log ("gidnumber is not an integer")
			return
		
		# find if we already have that group
		changed = False
		mode = ''
		try :
			g = Group.objects.get(gidnumber = gidnumber)
		except Group.DoesNotExist as e :
			# group does not exists, add
			g = Group(gidnumber = gidnumber)
			mode = 'create'
			changed = True
		else: 
			mode = 'update'

		if 'cn' not in gd.keys() :
			self.log ("problem, no name for group")
			return
		name = gd['cn'][0]
		
		name = self.map_group_name (name)
		if g.name != name :
			g.name = name
			changed = True
			
		description = None
		if 'description' in gd :
			description = gd['description'][0]
		if g.description != description :
			g.description = description
			changed = True

		old_parent = None
		if 'parent' in gd :
			new_parent = gd['parent']
			if g.parent is not None :
				old_parent = g.parent.gidnumber
			
			if old_parent != new_parent :
				p = None
				try : 
					p = Group.objects.get (gidnumber=new_parent)
				except Group.DoesNotExist as e :
					self.log("There is no group with gidnumber "+str(new_parent))
					
				if g.parent != p :
					g.parent = p
					changed = True

		group_type = g.NORMAL_GROUP
		if 'type' in gd :
			if gd['type'] == 'SERVICE' :
				group_type = g.SERVICE_GROUP
			if gd['type'] == 'TEAM' :
				group_type = g.TEAM_GROUP
		if g.group_type != group_type :
			g.group_type = group_type
			changed = True

		if changed :
			if mode == 'create':
				self.log ('adding group '+g.name+' with id '+str(g.gidnumber))
			else : 
				self.log ('updating group '+g.name+' with id '+str(g.gidnumber))
		# save in all cases...
		g.save ()

	# 'description': u"Liste de diffusion de l'\xe9quipe Fost", 
	# 'group': None, 
	# 'id': 'ml_fost_ipag', 
	# 'parent': None, 
	# 'name': 'fost.ipag'
	def mailinglist (self, ml) :
		changed = False
		try :
			m = MailingList.objects.get(ml_id = ml['id'])
		except MailingList.DoesNotExist as e :
			m = MailingList(ml_id = ml['id'])
			changed = True
	
		print m.ml_id
	
		name = None
		if 'name' in ml :
			name = ml['name']
		if name != m.name :
			m.name = name
			changed = True
	
		if 'userclass' in ml :
			userclass = ml['userclass']
		else :
			userclass = None
	
		description = None
		if 'description' in ml :
			description = ml['description']
		if description != m.description :
			m.description = description
			changed = True

		parent = None
		if 'parent' in ml :
			parent = ml['parent']
		if parent is not None :
			try :
				newparent = MailingList.objects.get(ml_id = parent)
			except MailingList.DoesNotExist as e:
				newparent = None
		else :
			newparent = None
		if newparent != m.parent :
			m.parent = newparent
			changed = True

		group = None
		if 'group' in ml :
			group = ml['group']
		if group is not None :
			# map group
			group = self.map_group_name(group) 
			try :
				newgroup = Group.objects.get(name = group)
			except Group.DoesNotExist as e :
				newgroup = None
		else :
			newgroup = None
		if newgroup != m.group :
			m.group = newgroup
			changed = True

		if changed :
			self.log('saving mailing list '+m.name)
			m.save ()

		# do u user class label
		if userclass is not None :
			changed = False
			try :
				u = UserClass.objects.get(ref=userclass)
				print u
			except UserClass.DoesNotExist as e :
				u = UserClass()
				u.ref = userclass
				changed = True

			if 'ucl' in ml :
				ucl = ml['ucl'] 
				if ucl is not None and type(ucl) is dict :
					ks = ucl.keys()
					for k in ks :
						o = getattr (u, k)
						if o != ucl[k]:
							setattr (u, k, ucl[k])
							changed = True
			if changed :
				u.save()

	# 'uid': ['cotere'], 
	# 'objectClass': ['posixAccount', 'shadowAccount', 'inetOrgPerson'], 
	# 'loginShell': ['/bin/bash'], 
	# 'userPassword': ['{crypt}$1$qmktPDE5$Ct9TwmEpS/RNwhHzIo725.'], 
	# 'uidNumber': ['281869'], 
	# 'l': ['Saint Martin d Heres'], 
	# 'gidNumber': ['3001'], 
	# 'street': ['414 rue de la piscine'], 
	# 'gecos': ['Remi Cote'], 
	# 'sn': ['Cote'], 
	# 'homeDirectory': ['/user/homedir/cotere'], 
	# 'postalCode': ['38400'], 
	# 'mail': ['Remi.Cote@obs.ujf-grenoble.fr'], 
	# 'givenName': ['Remi'], 
	# 'shadowLastChange': ['16405'], 
	# 'shadowExpire': ['16860'], 
	# 'cn': ['Remi Cote']

	def user (self, ud, xud, groups) :
		mode = ''
		changing=[]
		uidnumber = int(ud['uidNumber'][0])
		uid = ud['uid'][0]
		# try to find user
		changed = False
		try :
			u = User.objects.get(uidnumber=uidnumber)
		except User.DoesNotExist as e :
			# checher si un utilisateur avec le meme login existe
			try : 
				u = User.objects.get(login=uid)
			except User.DoesNotExist as e :
				# this is a new user entirely
				u = User(uidnumber = int(ud['uidNumber'][0]))
				mode = 'create'
				changed = True
			else:
				# user has changed uid
				u.uidnumber = ud['uidNumber'][0]
				mode = 'update'
				changed = true	
		else:
			mode = 'update'

		if 'uid' in ud.keys() :
			login = ud['uid'][0]
		else :
			self.log ('ERROR: can\'t find login for user\n'+str(ud)+'\n')
			sys.exit(1)			
		if login != u.login :
			u.login = login

		if 'givenName' in ud.keys() :
			first_name = ud['givenName'][0]
		else :
			self.log ('ERROR: can\'t find first name for user\n'+str(ud)+'\n')
			sys.exit(1)
		if first_name != u.first_name :
			u.first_name = first_name

		if 'sn' in ud.keys() :
			last_name = ud['sn'][0]
		else :
			self.log ('ERROR: can\'t find last name for user\n'+str(ud)+'\n')
			sys.exit (1)
		if last_name != u.last_name :
			u.last_name = last_name

		if 'mail' in ud.keys() :
			mail = (ud['mail'][0]).lower()
		else : 
			mail = None
		if u.mail != mail :
			u.mail = mail
			changing.append(('mail',mail))
			changed = True
	
		if 'loginShell' in ud.keys() :
			nls = ud['loginShell'][0];
			if u.login_shell != nls :
				u.login_shell = nls
				changing.append(('login_shell', nls))
				changed = True
	
		if xud is not None :
			# manager
			old_manager = None
			if u.manager is not None :
				old_manager = u.manager.login
			
			new_manager = xud['manager']

			if old_manager != new_manager :
				# get manager object
				if new_manager is not None :
					try :
						m = User.objects.get(login=new_manager)
					except User.DoesNotExist as e :
						self.log ("there's no user with login "+str(new_manager)+'\n')
						m = None
				else :
					m = None
				
				if u.manager != m :				
					u.manager = m
					changing.append(('manager',str(m)))
					changed = True

			# arrival date
			if 'arrival_date' in xud.keys() :
				arr = None
				if u.arrival is not None :
					arr = u.arrival.isoformat() 
				if arr != xud['arrival_date'] :
					u.arrival = xud['arrival_date']
					changing.append(('arr_date',u.arrival))
					changed = True
			# departure date
			if 'departure_date' in xud.keys() :
				dep = None
				if u.departure is not None :
					dep = u.departure.isoformat()
				if dep != xud['departure_date'] :
					u.departure = xud['departure_date']
					changing.append(('dep_date',u.departure))
					changed = True
			
			if 'room_number' in xud.keys() :
				if u.room != xud['room_number'] :
					u.room = xud['room_number']
					changing.append(('room',u.room))
					changed = True

			if 'telephone_number' in xud.keys() :
				if u.telephone != xud['telephone_number'] :
					u.telephone = xud['telephone_number']
					changing.append(('phone',u.telephone))
					changed = True

		# if create, user has to be saved before changing groups
		# we don't want to update the ldap server just yet
		if mode == 'create' :
			#self.log ('creating user'+u.login)
			u._save ()

		# setup groups
		# remove old groups
		for g in u.groups.all() :
			# not implemented yet
			pass	 

		# add new groups
		for g in groups :			
			gr = Group.objects.get (gidnumber = g)
			ngr=[]
			if (gr is not None) and (gr not in u.groups.all()) :
				u.groups.add (gr)
				ngr.append(gr)
				changed = True
			if len(ngr)>0 :
				changing.append(('new_groups',repr(ngr)))

		# user has been modified, save
		if changed :
			#self.log(mode+' user '+u.login+' '+str(changing))
			try :
				u.save()
			except :
				self.log(repr(u))
				sys.exit (1)
	

	#=============================================================================
	#
	# main functions

	def do_groups (self, dgroups, xgroups) :
		for group in dgroups.keys() :
			dn, group = self.d.get_group (dgroups[group])
			gid = int(group['gidNumber'][0])
			if gid in xgroups.keys() :
				xgroup = xgroups[gid]
				group['parent'] = xgroup['parent']
				group['type'] = xgroup['type']
			else :
				self.log("ERROR: group "+str(gid)+" not found in XML database")
			self.group (group)				

	def do_mailinglists (self, xmls) :
		names = []
		mls = []
		# step 1 : those without parent
		for k in xmls.keys() :
			ml = xmls[k]
			if ml['parent'] is None :
				names.append(k)
				mls.append(ml)
				del xmls[k]
		# step 2 : go around until everything is in...		
		while len(xmls.keys()) > 0 :
			i = 0
			# find the next possible item to add
			while True :
				k = xmls.keys()[i]
				ml = xmls[k]
				p = ml['parent']
				if p in names :
					names.append(k)
					mls.append(ml)
					del xmls[k]
					break
				else :
					i = i+1
		for ml in mls :
			self.mailinglist (ml)

	def do_users (self, dusers, xusers, dgroups) :
		self.log ('Users\n')
		for user in dusers :
			dn, data = user
			uidnumber = int(data['uidNumber'][0])
			uid = data['uid'][0]
			if uidnumber in xusers.keys() :
				xu = xusers[uidnumber]
			else :
				# user doesn't exist yet ?
				xu = None
	
			groups = []
			for group in dgroups.keys() :
				dn, group = self.d.get_group(dgroups[group])
				if 'memberUid' in group :
					members = group['memberUid']	
					if uid in members :
						gidnumber = int(group['gidNumber'][0])
						groups.append(gidnumber)
			self.user (data, xu, groups)
			self.dot()
		self.log ('\n')

	def update_groups (self) :
		for g in Group.objects.all() :
			self.log ("Updating group "+g.name+'\n')
			g.save ()

	def do_machine_classes (self, xclasses) :
		for cls in xclasses :	
			changed = False
			try:
				c = MachineClass.objects.get(name=cls['name'])
			except MachineClass.DoesNotExist as e:
				c = MachineClass(name=cls['name'])
				changed = True
			if c.shortdesc != cls['title'] :
				c.shortdesc = cls['title']
				changed = True
			if c.longdesc != cls['information'] :
				c.longdesc = cls['information']
				changed = True
			if changed : 
				c.save()	

	def do_vlans (self, xvlans) :
		for vlan in xvlans :
			changed = False
			try :
				v = Vlan.objects.get(vlan_id=vlan['vlan_id'])
			except Vlan.DoesNotExist as e:
				v = Vlan(vlan_id=vlan['vlan_id'])
				changed = True
			if v.name != vlan['name'] :
				v.name = vlan['name']
				changed = True
			if v.ip_block != vlan['ip_block'] :
				v.ip_block = vlan['ip_block']
				changed = True
			if v.gateway != vlan['gateway'] :
				v.gateway = vlan['gateway']
				changed = True
			if changed :
				v.save()


	def do_machines (self, xmachines) :
		for m in xmachines :
			#
			# insert domain names
			#
			default_name = None
			names = m['aliases']
			names.append(m['name'])
			domain_names = []
			for n in names :
				p = n.find('.')
				name = n
				if p==-1 :
					name = n+'.obs.ujf-grenoble.fr'
				changed = False
				try :
					d = DomainName.objects.get(fqdn=name)
				except DomainName.DoesNotExist as e:
					d = DomainName(fqdn=name)
					changed = True
				if changed :
					d.save()
				domain_names.append (d)
				if n == m['name'] :
					default_name = d
			
			# 
			# insert IP address and link to default domain name
			#	
			if default_name is None :
				self.log("problem, unable to define default domain name for "+str(names))
				sys.exit(1)
			# the XML database only allows one IP address per machine.
			# those servers with multiple interfaces will need to be tackled some other way
			changed = False
			try :
				ip = IPAddress.objects.get(address=m['ip'])
			except IPAddress.DoesNotExist as e:	
				ip = IPAddress(address=m['ip'])
				changed = True
			if ip.ptr != default_name :
				ip.ptr = default_name
				changed = True
			if changed :
				ip.save ()
			
			for n in domain_names :
				if ip not in n.ips.all() :
					n.ips.add (ip)
		
			# do the interface

			if m['mac'] is None :
				# generate bogus mac from name
				# c0:00:00:xx:xx:xx
				h = hashlib.sha1()
				h.update (m['name'])
				h = h.hexdigest()
				mac = 'c0:00:00:'+h[0:2]+':'+h[2:4]+':'+h[4:6]
				
			else:
				mac = m['mac']
				
			# need to create machine first
			changed = False
			try: 
				mach = Machine.objects.get (default_name = default_name)
			except Machine.DoesNotExist as e :
				mach = Machine(default_name = default_name)	
				changed = True
			# owner
			if m['owner'] is not None :
				old_owner = mach.owner
				try:
					new_owner = User.objects.get(login=m['owner'])
				except User.DoesNotExist as e:
					self.log(m)
					self.log("user "+str(m['owner'])+" not found")
				else :
					if old_owner != new_owner :
						mach.owner = new_owner
						changed = True

			if mach.comment != m['text'] :
				mach.comment = m['text']
				changed = True

			if changed :
				mach.save()

			# generate interface entry
			# by default, interface name is 'eth0'
			changed = False
			try:
				nif = NetworkIf.objects.get(mac_addr = mac)
			except NetworkIf.DoesNotExist as e:
				nif = NetworkIf (mac_addr = mac)
				# sets the name only the first time around
				nif.name = 'eth0'
				changed = True
			# set the machine	
			if nif.machine != mach :
				nif.machine = mach
				changed = True

			if (m['addrtype'] == None) or (m['addrtype'] == 'DHCP'):
				new_addressing = NetworkIf.DHCP_ADDRESSING
			if m['addrtype'] == 'DHCP-MAC' :
				new_addressing = NetworkIf.DHCP_STATIC_ADDRESSING
			if m['addrtype'] == 'STATIC' :
				new_addressing = NetworkIf.STATIC_ADDRESSING
			if new_addressing!=nif.addressing_type :
				nif.addressing_type = new_addressing
				changed = True

			if changed : 
				nif.save ()
	
			# add ip address
			if ip not in nif.ips.all() :
				nif.ips.add (ip)
		

	def handle (self, *args, **options) :
		self.d = l.Directory ()
		x.refresh_database()
		self.log('start synchronizing the database with the ldap')
	
		dgroups = self.d.get_groups ()
		xgroups = x.get_groups ()
		xmls = x.get_mailinglists()
		dusers = self.d.get_users ()
		xusers = x.get_users () 
		xclasses = x.get_machine_classes() 
		xvlans, xmachines = x.get_vlans_machines ()
	
		self.do_groups (dgroups, xgroups)
		self.do_mailinglists (xmls)
		self.do_users (dusers, xusers, dgroups)
		self.update_groups()
		self.do_machine_classes(xclasses)	
		self.do_vlans (xvlans)
		self.do_machines (xmachines)
		
		#self.d.close()
		self.log("end of procedure\n")
