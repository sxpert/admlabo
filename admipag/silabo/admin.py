from django.contrib import admin
from silabo.models import User, Group

# Register your models here.

class UserAdmin (admin.ModelAdmin) :
	fields = ('uidnumber', 'login', 'first_name', 'last_name', 'manager')
	list_display = ('last_name', 'first_name', 'mail_link', 'login', 'uidnumber', 'manager_name') 
	readonly_fields = ('uidnumber', 'login', 'first_name', 'last_name')

	def manager_name (self, obj) :
		if obj.manager is None :
			return ''
		return obj.manager.full_name()

	def mail_link (self, obj) :
		if obj.mail is None :
			return ''
		return '<a href="mailto:'+obj.mail+'">'+\
			'<img src="/static/enveloppe.png"/></a>'
	mail_link.allow_tags = True


admin.site.register(User, UserAdmin)

class GroupAdmin (admin.ModelAdmin) :
	fields = ('gidnumber', 'name', 'parent')

admin.site.register(Group, GroupAdmin)
