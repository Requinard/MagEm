from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
	'',
	url('^api/', include('api.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^account/', include('account.urls')),
	url(r'^', include('magazine.urls', namespace="magazine")),
)
