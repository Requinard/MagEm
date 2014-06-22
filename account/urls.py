from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
	'',
	url(r'^login', views.LoginView.as_view(), name="login"),

)