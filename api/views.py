from rest_framework import viewsets

from .serializers import *


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = ()


class MagazineViewSet(viewsets.ModelViewSet):
	queryset = Magazine.objects.all()
	serializer_class = MagazineSerializers
	permission_classes = ()


class VoteViewSet(viewsets.ModelViewSet):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializers
	permission_classes = ()