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
# New Arrival form
	url(r'^new-arrival/form$', views.NewArrivalForm, name='new-arrival-form'),
	url(r'^new-arrival/validate/(?P<newuser_id>\d+)$', views.NewArrivalValidate, name='new-arrival-validate'),
	url(r'^new-arrival/validate/userinfo/(?P<user_id>\d+)$', views.NewArrivalValidateUserInfo, name='new-arrival-validate-user-info'),
# Users
	url(r'^users/', views.users, name='users'),
	url(r'^user/(?P<user_id>\d+)/view/$', views.user_view, name='user-view'),
	url(r'^user/(?P<user_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.user_view_field, name='user_view_field'),
# Groups
	url(r'^groups/', views.groups, name='groups'),
	url(r'^group/(?P<group_id>\d+)/view/$', views.group_view, name='group_view'),
	url(r'^group/(?P<group_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.group_view_field, name='group_view_field'),
# Mailing lists
	url(r'^mailinglist/(?P<ml_id>[a-z0-9_]+)/view/$', views.mailinglist_view, name='mailinglist_view'),
#
#
# test
	url(r'^test$', views.Test, name='test'),

)

