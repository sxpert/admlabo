# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from models import *
import logging
logger=logging.getLogger('django')

# Register your models here.

class UserForm (forms.ModelForm) :
	class Meta:
		model=User
		fields = '__all__'

	def __init__ (self, *args, **kwargs) :
		super (UserForm, self).__init__ (*args, **kwargs)
		self.fields['appspecname'].widget.attrs.update({'style':'font-family: monospace; width: 100em; height: 45ex;'})


class UserAdmin (admin.ModelAdmin) :
	fields = (('uidnumber', 'group', 'user_state'), 
			   'login', 'login_shell', 'first_name', 'last_name', 'room', 'telephone', 'mail', 'manager', 
			   'userclass', 'arrival', 'departure', 'groups', 'flags', 'appspecname')
	list_display = ('last_name', 'first_name', 'mail_link', 'login', 'uidnumber', 'manager_name', 'user_state') 
	# room and telephone are to be modified via biper only
	readonly_fields = ('uidnumber', 'login', 'first_name', 'last_name', 'mail', 'room', 'telephone')
	filter_horizontal = ('groups', 'flags')

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

class UserGroupHistoryAdmin (admin.ModelAdmin) :
	fields = ('created', 'creator', 'user', 'action', 'data')
	readonly_fields = ('created', 'creator', 'user')
	list_display = ('created', 'creator', 'user', 'action')

admin.site.register(UserGroupHistory, UserGroupHistoryAdmin)

admin.site.register(MailAlias)

class GroupForm (forms.ModelForm) :
	users = forms.ModelMultipleChoiceField (
		label = 'Users',
		queryset = User.objects.all(),
		widget = admin.widgets.FilteredSelectMultiple('Users', False),
		required = False,
	)
	class Meta:
		model=Group
		fields = ['users']

	def __init__ (self, *args, **kwargs) :
		super (GroupForm, self).__init__ (*args, **kwargs)
		self.fields['appspecname'].widget.attrs.update({'style': 'font-family: monospace; width: 100em; height: 45ex;'}) 

class GroupAdmin (admin.ModelAdmin) :
	form = GroupForm
	fields = ('gidnumber', 'name', 'group_type', 'description', 'parent', 'users', 'appspecname')
	list_display = ('name', 'gidnumber', 'group_description')

	def get_form (self, request, obj=None, **kwargs) :
		if obj:
			self.form.base_fields['users'].initial = obj.users.all()
		else :
			self.form.base_fields['users'].initial = []
		print self.form.base_fields['users'].initial
		return super(GroupAdmin, self).get_form(request, obj, **kwargs)

	def save_model (self, request, obj, form, change) :
		obj.users.clear()
		for user in form.cleaned_data['users'] :
			obj.users.add(user)
		super(GroupAdmin, self).save_model(request, obj, form, change)

	def group_description (self, obj) :
		if obj.description is None:
			return ''
		return obj.description

admin.site.register(Group, GroupAdmin)
admin.site.register(MailingList)
admin.site.register(MachineClass)

class NetworkIfInline (admin.StackedInline):
	model = NetworkIf
	extra = 0
	readonly_fields = ('mac_addr', 'addressing_type', 'name', 'ips',)

class MachineAdmin (admin.ModelAdmin) :
	fieldsets = [(None, {'fields': ['default_name', 'owner']},)]
	inlines = [ NetworkIfInline ]
	list_display = ('machine_name', 'machine_owner', )
	
	def machine_name (self, obj) :
		n = str(obj.default_name)
		p = n.index('.')
		if p==-1 :
			s = n
		else :
			s = n[0:p]
		return s
	machine_name.admin_order_field = 'default_name__fqdn'

	def machine_owner (self, obj) :
		if obj.owner is None :
			return ''
		else :
			return str(obj.owner.login)
	machine_owner.admin_order_field = 'owner__login'

admin.site.register(Machine, MachineAdmin)

class NetworkIfAdmin (admin.ModelAdmin) :
	filter_horizontal = ('ips',)
	list_display = ('mac_addr', 'addressing_type', 'ip_address_list') 
	
	def ip_address_list (self, obj) :
		l = []
		for ip in obj.ips.all() :
			f = str(ip.ptr.fqdn)
			p = f.index('.')
			if p!=-1 :
				f = f[0:p]
			a = str(ip.address)
			if len(f)>0 :
				s = '<b>'+f+'</b>'+' ('+a+')'
			else :
				s = a
			l.append(s)
		return '<br/>'.join(l)
	ip_address_list.allow_tags = True
	ip_address_list.short_description = "list of IP addresses"
	

admin.site.register(NetworkIf,NetworkIfAdmin)

class DomainNameAdmin (admin.ModelAdmin) :
	filter_horizontal = ('ips',)

admin.site.register(DomainName, DomainNameAdmin)
admin.site.register(IPAddress)
admin.site.register(Vlan)

class CommandAdmin (admin.ModelAdmin) :
	fields = ('created', 'modified', 'user', 'verb', 'data', ('done', 'in_cron',),)
	readonly_fields = ('created', 'modified', 'user',)
	list_display = ('user', 'verb', 'done', 'in_cron', 'created', 'subject')

admin.site.register(Command, CommandAdmin)

class CountryAdmin (admin.ModelAdmin) :
	list_display = ('iso2', 'name', 'citizenship', 'eu_member')

admin.site.register(Country, CountryAdmin)

class UserClassAdmin (admin.ModelAdmin) :
	list_display = ('ref', 'defval', 'fr', 'en', 'probie', 'group')

admin.site.register(UserClass, UserClassAdmin)
admin.site.register(Office)

class NewUserAdmin (admin.ModelAdmin) :
	fieldsets = (
		( None,                   { 'fields': ( 'manager', 'user', )}),
		( 'État Civil',           { 'fields': ( 'last_name', 'first_name', 'birthdate', 'citizenship', )}),
		( 'Contact',              { 'fields': ( 'external_email', )}),
		( 'Au sein de l\'IPAG',   { 'fields': ( 'status', 'study_level', 'ujf_student', 'team', 'office', 'other_office', )}),
		( 'Dates',                { 'fields': ( 'arrival', 'departure', )}),
		( 'Moyens Informatiques', { 'fields': ( 'comp_account', 'os_type', 'specific_os', 'os_lang', 'comp_purchase', )}),
		( 'Autres Accès',         { 'fields': ( 'ir_lab', 'workshop', 'chem_lab', )}),
		( 'Sécurité',             { 'fields': ( 'risky_activity', )}),
		( None,                   { 'fields': ( 'comments', )}),)

admin.site.register(NewUser, NewUserAdmin)
admin.site.register(UserDir)

class EmailAlertAdmin (admin.ModelAdmin) :
	list_display = ('cause', 'email')

admin.site.register(EmailAlert, EmailAlertAdmin)

class EmailAlertMessageForm (forms.ModelForm) :
	class Meta:
		model = EmailAlertMessage
		fields = '__all__'

	def __init__ (self, *args, **kwargs) :
		super (EmailAlertMessageForm, self).__init__ (*args, **kwargs)
		self.fields['subject'].widget.attrs.update({'style': 'font-family: monospace; width: 100em; height: 10ex;'}) 
		self.fields['msgtext'].widget.attrs.update({'style': 'font-family: monospace; width: 100em; height: 45ex;'}) 
		self.fields['msghtml'].widget.attrs.update({'style': 'font-family: monospace; width: 100em; height: 45ex;'}) 

class EmailAlertMessageAdmin (admin.ModelAdmin) :
	form = EmailAlertMessageForm

admin.site.register(EmailAlertMessage, EmailAlertMessageAdmin)
admin.site.register(UserFlag)
