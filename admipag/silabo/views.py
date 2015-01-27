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
	user = models.User.objects.get(uidnumber = user_id)
	context = {
		'user' : user,
	}
	return render(request, 'user-view.html', context)
