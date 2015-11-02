# -*- coding: utf-8 -*-

from django import template
register = template.Library ()

@register.filter
def is_only_rh(user) :
	if user.is_staff :
		return False
	if user.has_perm('admtooCore.do_rh_tasks') :
		return True
	return False

