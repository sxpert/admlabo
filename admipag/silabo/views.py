import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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

@csrf_protect
def user_view_field (request, user_id, action, fieldtype, fieldname) :
	u = models.User.objects.get(uidnumber = user_id)
	data = {}	
	# simple select field type
	if fieldtype == 'select' :
		# manager field
		if fieldname == 'manager' :
			if action == 'options' :
				# list all possible managers
				managers = {}
				for m in models.User.objects.all() :
					managers[m.uidnumber] = m.first_name+' '+m.last_name
				data['options'] = managers
				# add currently selected manager
				data['selected'] = u.manager.uidnumber
			if action == 'value' :
				m = u.manager
				if request.method == 'POST':
					data = json.loads(request.body)
					if 'value' in data.keys() :
						manager = data['value']
						m = models.User.objects.get(uidnumber = manager)
						u.manager = m
						u.save()
				data['url'] = reverse ('user_view', args=(m.uidnumber,))
				data['value'] = m.first_name+' '+m.last_name
	# multiselect field type
	if fieldtype == 'multiselect' :
		# groups
		if fieldname == 'groups' :
			if action == 'options' :
				groups = {}
				for g in models.Group.objects.all() :
					groups[g.gidnumber] = g.name
				data['options'] = groups
				selected = []
				s = u.all_groups()
				for g in s :
					selected.append(g.gidnumber)
				data['selected'] = selected
		# managed
	jsdata = json.dumps(data)
	return HttpResponse(jsdata, content_type='application/json')
