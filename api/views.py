from rest_framework import viewsets

from .serializers import *


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = ()