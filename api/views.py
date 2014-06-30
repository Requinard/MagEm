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

	def pre_save(self, obj):
		article_id = int(self.request.DATA['article_related'])
		magazine_id = int(self.request.DATA['magazine_related'])

		vote = Vote.objects.filter(user_voted=self.request.user).filter(article_related__id=article_id)

		if len(vote) > 0:
			vote = vote[0]
			tally = vote.article_related.tally

			# Subtract existing votes
			if vote.is_agreed:
				tally.vote_agr -= 1
			else:
				tally.vote_dis -= 1

			if vote.is_constructive:
				tally.vote_con -= 1
			else:
				tally.vote_des -= 1
			tally.save()

			# Set new votes
			vote.is_agreed = True if self.request.DATA['is_agreed'] == "true" else False
			vote.is_constructive = True if self.request.DATA['is_constructive'] == "true" else False

			if vote.is_agreed:
				tally.vote_agr += 1
			else:
				tally.vote_dis += 1

			if vote.is_constructive:
				tally.vote_con += 1
			else:
				tally.vote_des += 1

			tally.save()

			vote.save()

			raise Exception
		else:
			vote = obj
			tally = obj.article_related.tally

			if vote.is_agreed:
				tally.vote_agr += 1
			else:
				tally.vote_dis += 1

			if vote.is_constructive:
				tally.vote_con += 1
			else:
				tally.vote_des += 1

			tally.save()