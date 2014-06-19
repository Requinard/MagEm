from rest_framework import serializers

from magazine.models import Article


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article