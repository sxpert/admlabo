from django.conf.urls import patterns, include, url
from django.contrib import admin
import views 


urlpatterns = patterns('',
	url(r'^$', views.MainIndex, name='main-index'), 
	url(r'^API/SetupBackupPC', views.SetupBackupPC, name='setup-backup-pc'),
    url(r'^admtooCore/', include('admtooCore.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
