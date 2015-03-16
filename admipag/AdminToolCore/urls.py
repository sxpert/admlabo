from django.conf.urls import patterns, url
from AdminToolCore import views

urlpatterns = patterns( '',
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^users/', views.users, name='users'),
	url(r'^user/(?P<user_id>\d+)/view/$', views.user_view, name='user_view'),
	url(r'^user/(?P<user_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.user_view_field, name='user_view_field'),
	url(r'^groups/', views.groups, name='groups'),
	url(r'^group/(?P<group_id>\d+)/view/$', views.group_view, name='group_view'),
	url(r'^group/(?P<group_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.group_view_field, name='group_view_field'),
	url(r'^mailinglist/(?P<ml_id>[a-z0-9_]+)/view/$', views.mailinglist_view, name='mailinglist_view'),
)

