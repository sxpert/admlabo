from django.conf.urls import patterns, url
import views

urlpatterns = patterns( '',
# login forms
	url(r'^login$', views.LoginForm, name='login-form'),
	url(r'^logout$', views.LogoutView, name='logout-view'),
# Dashboard
	url(r'^$', views.Dashboard, name='dashboard'),
	url(r'^DBNewArrivals$', views.DBNewArrivals, name='DBNewArrivals'),
# New Arrival form
	url(r'^new-arrival$', views.NewArrivalForm, name='new-arrival-form'),
# Users
	url(r'^users/', views.users, name='users'),
	url(r'^user/(?P<user_id>\d+)/view/$', views.user_view, name='user_view'),
	url(r'^user/(?P<user_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.user_view_field, name='user_view_field'),
# Groups
	url(r'^groups/', views.groups, name='groups'),
	url(r'^group/(?P<group_id>\d+)/view/$', views.group_view, name='group_view'),
	url(r'^group/(?P<group_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.group_view_field, name='group_view_field'),
# Mailing lists
	url(r'^mailinglist/(?P<ml_id>[a-z0-9_]+)/view/$', views.mailinglist_view, name='mailinglist_view'),
)

