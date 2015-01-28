from django.shortcuts import render
import models
# Create your views here.

#
# tableau de bord
# 
def index (request) :
	users = models.User.objects.all()
	context = {
		'users': users,
	}
	return render(request, 'index.html', context)



#------------------------------------------------------------------
# gestion des utilisateurs
#

#
# voir les informations d'un utilisateur
#
def user_view (request, user_id) :
	u = models.User.objects.get(uidnumber = user_id)
	m = models.User.objects.filter(manager = u)
	context = {
		'user' : u,
		'managed' : m,
	}
	return render(request, 'user-view.html', context)
