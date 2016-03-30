from django.conf.urls import patterns, url
import views

urlpatterns = patterns( '',
# API
	url(r'^API/XmlDB$', views.XmlDB, name='xml-db'),
# login forms
	url(r'^login$', views.LoginForm, name='login-form'),
	url(r'^logout$', views.LogoutView, name='logout-view'),
# Dashboard
	url(r'^$', views.Dashboard, name='dashboard'),
	url(r'^DBNewArrivals$', views.DBNewArrivals, name='DBNewArrivals'),
	url(r'^DBUnknownUsers$', views.DBUnknownUsers, name='DBUnknownUsers'),
	url(r'^DBReclaimMachines$', views.DBReclaimMachines, name='DBReclaimMachines'),

#
# people and human structure management
#

# New Arrival form
	url(r'^new-arrival/form$', views.NewArrivalForm, name='new-arrival-form'),
	url(r'^new-arrival/validate/(?P<newuser_id>\d+)$', views.NewArrivalValidate, name='new-arrival-validate'),
	url(r'^new-arrival/validate/userinfo/(?P<user_id>\d+)$', views.NewArrivalValidateUserInfo, name='new-arrival-validate-user-info'),
# Users
	url(r'^users/', views.users, name='users'),
	url(r'^user/(?P<user_id>\d+)/view/$', views.user_view, name='user-view'),
	url(r'^user/(?P<user_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.user_view_field, name='user_view_field'),
	# photos
	url(r'^user/photos/(?P<user_id>\d+)/(?P<fname>.*)$', views.user_view_photo, name='user-view-photo'),
# Groups
	url(r'^groups/', views.groups, name='groups'),
	url(r'^group/new/$', views.group_new, name='group-new'),
	url(r'^group/(?P<group_id>\d+)/view/$', views.group_view, name='group-view'),
	url(r'^group/(?P<group_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.group_view_field, name='group_view_field'),
# MailingLists
	url(r'^mailinglists/$', views.mailinglist_list, name='mailinglist-list'),
	url(r'^mailinglist/new/$', views.mailinglist_new, name='mailinglist-new'),
	url(r'^mailinglist/(?P<ml_id>[a-z0-9_-]+)/view/$', views.mailinglist_view, name='mailinglist-view'),
	url(r'^mailinglist/(?P<ml_id>[a-z0-9_-]+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.mailinglist_view_field, name='mailinglist_view_field'),
# MailAliases
	url(r'^mailaliases/$', views.mailalias_list, name='mailalias-list'),
	url(r'^mailalias/new/$', views.mailalias_new, name='mailalias-new'),
	url(r'^mailalias/(?P<alias>[a-z0-9_-]+)/view/$', views.mailalias_view, name='mailalias-view'),
	url(r'^mailalias/(?P<alias>[a-z0-9_-]+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.mailalias_view_field, name='mailalias_view_field'),
#
# machines management
#

# Machines
	url(r'^machine/(?P<machine_id>\d+)/view/$', views.machine_view, name='machine-view'),
#
#
# test
	url(r'^test$', views.Test, name='test'),
)

