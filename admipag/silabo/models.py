# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class Group (models.Model) :
	NORMAL_GROUP = 0
	TEAM_GROUP = 1
	SERVICE_GROUP = 2

	GROUP_TYPES_CHOICES = (
		( NORMAL_GROUP,  ''),
		( TEAM_GROUP,    'Groupe d\'équipe'),
		( SERVICE_GROUP, 'Groupe de service'),
	)

	gidnumber   = models.IntegerField(primary_key=True)
	name        = models.CharField(max_length=64, unique=True) 
	group_type	= models.IntegerField(choices = GROUP_TYPES_CHOICES, default=NORMAL_GROUP)
	parent      = models.ForeignKey('self', null=True, blank=True)
	description = models.CharField(max_length=256, null=True, blank=True)

	def __str__ (self) :
		return self.name

class MailingList (models.Model) :
	ml_id       = models.CharField(max_length=64, primary_key=True)
	name        = models.CharField(max_length=128, unique=True)
	description = models.CharField(max_length=256)
	parent      = models.ForeignKey('self', null=True, blank=True)
	group       = models.ForeignKey(Group, null=True, blank=True)

	def __str__ (self) :
		return self.name
	

class User (models.Model) :
	uidnumber   = models.IntegerField(primary_key=True)
	login       = models.CharField(max_length=64, unique=True)
	login_shell = models.CharField(max_length=128, null=True, blank=True)
	first_name	= models.CharField(max_length=128, null=True, blank=True)
	last_name   = models.CharField(max_length=128, null=True, blank=True)
	mail        = models.EmailField(null=True, blank=True)
	manager     = models.ForeignKey('self', null=True, blank=True)
	arrival		= models.DateField(null=True, blank=True)
	departure	= models.DateField(null=True, blank=True)
	groups		= models.ManyToManyField(Group, blank=True, related_name='users')
	room		= models.CharField(max_length=32, null=True, blank=True)
	telephone   = models.CharField(max_length=32, null=True, blank=True)

	class Meta :
		ordering = ['login']

	def __init__ (self, *args, **kwargs) :
		super(User, self).__init__(*args, **kwargs)
	
	def __str__ (self) :
		return self.login

	def full_name (self) :
		n = []
		if self.first_name is not None : 
			n.append(self.first_name)
		if self.last_name is not None :
			n.append(self.last_name)
		return ' '.join(n)

	def all_mailinglists (self) :
		mls = []
		# mailing lists for user class
		
		# mailing lists from groups
		gr = self.all_groups ()
		for g in gr :
			try :
				ml = MailingList.objects.get (group = g)
			except MailingList.DoesNotExist as e :
				pass
			else :
				mls.append(ml)
		for ml in mls :
			p = ml
			while True :
				p = p.parent
				if p is not None :
					if p not in mls :				
						mls.append (p)
				else :
					break
		return mls
				
	def change_mailinglists (self, mailinglists) :
		# va savoir ce qu'il faut faire la dedans... 
		# select all mailing lists not attached to a group
		pass

	def _get_parent_group (self, group) :
		gr = []
		pg = group.parent
		if pg not in gr :
			gr.append (pg)
		if pg is not None :
			tg = self._get_parent_group(pg)
			if tg is not None :
				for g in tg :
					if g not in gr :
						gr.append(g)
		else :
			gr = pg
		return gr
	
	def all_groups (self) :
		gr = []
		for g in self.groups.all() :
			if g not in gr :
				gr.append(g)
			tg = self._get_parent_group(g)
			if tg is not None :
				for pg in tg :
					if pg not in gr :
						gr.append(pg)
		return gr

	# la grouplist est un array de gidnumbers
	def change_groups (self, grouplist) :
		changed = False
		i=0
		while i < len(grouplist) :
			grouplist[i] = int(grouplist[i])
			i += 1
		for g in self.groups.all() :
			if g.gidnumber not in grouplist :
				self.groups.remove(g)
				changed = True
		for g in grouplist :
			g = Group.objects.get(gidnumber=g)
			if (g is not None) and (g not in self.groups.all()) :
				self.groups.add (g)
				changed = True
		if changed :
			self.save()

	def manager_of (self) :
		return User.objects.filter(manager = self)

	def change_managed (self, managed_list) :
		for u in User.objects.filter(manager = self) :
			if u.uidnumber not in managed_list :
				u.manager = None
				u.save ()
		for un in managed_list :
			u = User.objects.get(uidnumber = un)
			if (u.manager != self) :
				u.manager = self
				u.save ()

	def machines (self) :
		return Machine.objects.filter(owner = self)
	
	

#==================================================================================================================================
# 
# Management of machines, ip addresses and the like
#



class MachineClass (models.Model) :
	name      = models.CharField (max_length=64, unique=True)
	shortdesc = models.CharField (max_length=128, blank=True)
	longdesc  = models.CharField (max_length=128, blank=True)

	class Meta:
		verbose_name_plural = "MachineClasses"

	def __str__ (self) :
		return self.name
	
def machine_class_client() :
	try :
		return MachineClass.objects.get(name='client')
	except:
		return None

class Machine (models.Model) :
	default_name = models.ForeignKey('DomainName', null=True, blank=True)
	owner = models.ForeignKey (User, blank=True, null=True)
	comment = models.CharField (max_length=256, blank=True, null=True)

	def __str__ (self) :
		return str(self.default_name)

	def interfaces (self) :
		return NetworkIf.objects.filter(machine = self)
	
#==================================================================================================================================
#
# Management of network bits
#

class NetworkIf (models.Model) :
	STATIC_ADDRESSING = 0
	DHCP_STATIC_ADDRESSING = 1	
	DHCP_ADDRESSING = 2
	
	ADDRESSING_CHOICES = (
		(STATIC_ADDRESSING, 'statique',),
		(DHCP_STATIC_ADDRESSING, 'dhcp statique',),
		(DHCP_ADDRESSING, 'dhcp',),
	)

	mac_addr = netfields.MACAddressField (primary_key = True)
	name = models.CharField (max_length=32, null=True, blank=True)
	ips = models.ManyToManyField ('IPAddress', blank=True, related_name='networkinterfaces')
	addressing_type	= models.IntegerField(choices = ADDRESSING_CHOICES, default=DHCP_ADDRESSING)
	machine = models.ForeignKey (Machine, null=True, blank=True, related_name='interfaces')

	def __str__ (self) :
		return str(self.mac_addr)

class DomainName (models.Model) :
	fqdn = models.CharField (max_length=255, unique=True, null=False)
	ips  = models.ManyToManyField ('IPAddress', blank=True, related_name='domainnames')

	def __str__ (self) :
		return str(self.fqdn)

class IPAddress (models.Model) :
	address = netfields.InetAddressField (primary_key=True)
	ptr = models.ForeignKey (DomainName, null=True, blank=True)
	

	def __str__ (self) :
		return str(self.address)

class Vlan (models.Model) :
	vlan_id	 = models.IntegerField (primary_key=True) 
	name     = models.CharField (max_length=64, null=False)
	ip_block = netfields.CidrAddressField (unique=True, null=False)
	gateway  = netfields.InetAddressField (unique=True, null=False)

	def __str__ (self) :
		return str(self.name)
