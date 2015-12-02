from django.conf.urls import patterns, include, url
from django.contrib import admin
import root_views 


urlpatterns = patterns('',
	url(r'^$', root_views.MainIndex, name='main-index'), 
	url(r'^API/GetUserInfo/(?P<uid>.+)$', root_views.GetUserInfo, name='get-user-info'),
	url(r'^API/SetupBackupPC', root_views.SetupBackupPC, name='setup-backup-pc'),
    url(r'^admtooCore/', include('admtooCore.admtooCore_urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
