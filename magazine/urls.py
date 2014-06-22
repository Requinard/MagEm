from django.conf.urls import url, patterns

import views

urlpatterns = patterns(
	'',
	url(r'^m/(?P<mag>\w+)/$', views.MagazineView.as_view(), name='magazine'),
	url(r'^m/(?P<mag>\w+)$', views.MagazineView.as_view(), name='magazine'),
	url(r"^a/(?P<thread>\d+)/$", views.ArticleView.as_view(), name="article"),
	url(r'^submit/$', views.SubmitView.as_view(), name='submit'),
	url(r'^createmag/$', views.CreateMagazineView.as_view(), name="createmag"),
	url(r'^subscribe/(?P<mag>\d+)/$', views.SubscribeView.as_view(), name="subscribe"),
	url(r'^', views.IndexView.as_view(), name="index"),
)