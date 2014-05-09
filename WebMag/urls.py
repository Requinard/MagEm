from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^magazine/', include('magazine.urls', namespace="magazine")),

                       url(r'^admin/', include(admin.site.urls)),
)
