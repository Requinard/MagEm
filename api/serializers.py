from rest_framework import serializers

from magazine.models import Article, Magazine, Vote


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article


class MagazineSerializers(serializers.ModelSerializer):
	class Meta:
		model = Magazine


class VoteSerializers(serializers.ModelSerializer):
	class Meta:
		model = Vote

