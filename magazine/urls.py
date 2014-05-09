from django.conf.urls import url, patterns

import views

urlpatterns = patterns('',
                       url(r'^m/(?P<mag>\w+)/$', views.magazine, name='magazine'),
                       url(r"^c/(?P<thread>\d+)/$", views.article, name="article"),
                       url(r'^submit/$', views.submit, name='submit'),
                       url(r'^login/$', views.login, name="login"),
                       url(r'^createmag/$', views.createmagazine, name="createmag"),
                       url(r'$', views.index, name="index"),
)