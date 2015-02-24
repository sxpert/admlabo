# -*- coding: utf-8 -*-
from django.db import models
import netfields
import logging
logger=logging.getLogger('django')

class MachineClass (models.Model) :
	name      = models.CharField (max_length=64, unique=True)
	shortdesc = models.CharField (max_length=128, blank=True)
	longdesc  = models.CharField (max_length=128, blank=True)

	class Meta:
		verbose_name_plural = "MachineClasses"
		app_label = 'silabo'

	def __str__ (self) :
		return self.name
	
def machine_class_client() :
	try :
		return MachineClass.objects.get(name='client')
	except:
		return None
