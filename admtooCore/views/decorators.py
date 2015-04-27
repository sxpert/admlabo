# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test, login_required

admin_perms = user_passes_test(lambda u: u.is_staff)

def admin_login (view_func) :
	decorated_view_func = login_required(admin_perms(view_func))
	return decorated_view_func


