from django.conf.urls import patterns, url

from silabo import views

urlpatterns = patterns( '',
	url(r'^$', views.index, name='dashboard'),
	url(r'^user/(?P<user_id>\d+)/view/$', views.user_view, name='user_view'),
)
