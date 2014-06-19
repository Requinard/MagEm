from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter

import views


router = DefaultRouter()
router.register(r'article', views.ArticleViewSet)
router.register(r'magazine', views.MagazineViewSet)
router.register(r'vote', views.VoteViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)