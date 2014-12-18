from django.db import models
import logging
logger=logging.getLogger('django')

class User (models.Model) :
	uidnumber   = models.IntegerField(primary_key=True)
	login       = models.CharField(max_length=64, unique=True)
	first_name	= models.CharField(max_length=128, null=True, blank=True)
	last_name   = models.CharField(max_length=128, null=True, blank=True)
	mail        = models.EmailField(null=True, blank=True)
	manager     = models.ForeignKey('self', null=True, blank=True)

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

class Group (models.Model) :
	gidnumber   = models.IntegerField(primary_key=True)
	name        = models.CharField(max_length=64, unique=True)
	parent      = models.ForeignKey('self', null=True, blank=True)
	description = models.CharField(max_length=256, null=True, blank=True)

	def __str__ (self) :
		return self.name
