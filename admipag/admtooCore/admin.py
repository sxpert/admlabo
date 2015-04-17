# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from models import *
import logging
logger=logging.getLogger('django')

# Register your models here.

class UserAdmin (admin.ModelAdmin) :
	fields = (('uidnumber', 'group', 'user_state'), 
			   'login', 'login_shell', 'first_name', 'last_name', 'room', 'telephone', 'mail', 'manager', 'arrival', 'departure', 'groups')
	list_display = ('last_name', 'first_name', 'mail_link', 'login', 'uidnumber', 'manager_name', 'user_state') 
	readonly_fields = ('uidnumber', 'login', 'first_name', 'last_name', 'mail')
	filter_horizontal = ('groups',)

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

class GroupAdmin (admin.ModelAdmin) :
	form = GroupForm
	fields = ('gidnumber', 'name', 'group_type', 'description', 'parent', 'users', )
	list_display = ('name', 'group_description')

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
admin.site.register(UserClass)
admin.site.register(Office)

class NewUserAdmin (admin.ModelAdmin) :
	fieldsets = (
		( None,                   { 'fields': ( 'manager', 'user', )}),
		( 'État Civil',           { 'fields': ( 'last_name', 'first_name', 'birthdate', 'citizenship', )}),
		( 'Contact',              { 'fields': ( 'external_email', )}),
		( 'Au sein de l\'IPAG',   { 'fields': ( 'status', 'study_level', 'ujf_student', 'team', 'office', 'other_office', )}),
		( 'Dates',                { 'fields': ( 'arrival', 'departure', )}),
		( 'Moyens Informatiques', { 'fields': ( 'comp_account', 'os_type', 'specific_os', 'comp_purchase', )}),
		( 'Autres Accès',         { 'fields': ( 'ir_lab', 'workshop', 'chem_lab', )}),
		( 'Sécurité',             { 'fields': ( 'risky_activity', )}),
		( None,                   { 'fields': ( 'comments', )}),)

admin.site.register(NewUser, NewUserAdmin)
admin.site.register(UserDir)

class EmailAlertAdmin (admin.ModelAdmin) :
	list_display = ('cause', 'email')

admin.site.register(EmailAlert, EmailAlertAdmin)
