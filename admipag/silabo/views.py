from django.shortcuts import render
import models
# Create your views here.

#
# tableau de bord
# 
def dashboard (request) :
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'dashboard.html', context)



#------------------------------------------------------------------
# gestion des utilisateurs
#

#
# liste des utilisateurs 
#
def users (request) :
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'users.html', context)

#
# voir les informations d'un utilisateur
#
def user_view (request, user_id) :
	u = models.User.objects.get(uidnumber = user_id)
	context = {
		'user' : u,
	}
	return render(request, 'user-view.html', context)
