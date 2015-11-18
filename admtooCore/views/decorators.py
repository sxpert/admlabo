# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test, login_required

def is_rh (u) :
	return u.has_perm('admtooCore.do_rh_tasks')

def is_staff (u) :
	return u.is_staff

def is_admin (u) :
	return is_staff(u) or is_rh(u)

admin_perms = user_passes_test(lambda u: is_admin(u)) 

def admin_login (view_func) :
	decorated_view_func = login_required(admin_perms(view_func))
	return decorated_view_func


