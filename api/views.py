from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *



# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializers
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MagazineViewSet(viewsets.ModelViewSet):
	queryset = Magazine.objects.all()
	serializer_class = MagazineSerializers
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class VoteViewSet(viewsets.ModelViewSet):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializers
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)