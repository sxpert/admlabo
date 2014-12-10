from django.db import models

# Create your models here.

class User (models.Model) :
	uidnumber = models.IntegerField(primary_key=True)
	login     = models.CharField(max_length=64, unique=True)
	manager   = models.ForeignKey('self')
