from django.conf.urls import patterns, url
from silabo import views

urlpatterns = patterns( '',
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^users/', views.users, name='users'),
	url(r'^user/(?P<user_id>\d+)/view/$', views.user_view, name='user_view'),
	url(r'^user/(?P<user_id>\d+)/view/(?P<action>[^/]*)/(?P<fieldtype>[^/]*)/(?P<fieldname>[^/]*)$', 
		views.user_view_field, name='user_view_field'),
	url(r'^group/(?P<user_id>\d+)/view/$', views.user_view, name='group_view'),
)

