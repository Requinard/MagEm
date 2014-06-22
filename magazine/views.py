from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .models import *


class Functions:
	@staticmethod
	def GetUserSubscriptions(request, context):
		if request.user.is_authenticated():
			subscription = Subscription.objects.filter(subscriber=request.user)
			context['subscriptions'] = subscription
			context['user'] = request.user

	@staticmethod
	def ComputePostScore(request, context, article):
		pass


class IndexView(View):
	def get(self, *args, **kwargs):
		context = {}
		Functions.GetUserSubscriptions(self.request, context)
		return render(self.request, "magazine/index.html", context)


class MagazineView(View):
	def get(self, request, mag):
		context = {}
		Functions.GetUserSubscriptions(self.request, context)

		context['mag'] = get_object_or_404(Magazine, name=mag)
		context['articles'] = Article.objects.filter(magazine_posted=context['mag'])

		return render(self.request, "magazine/magazine.html", context)


class SubmitView(View):
	def get(self, *args, **kwargs):
		context = {}
		Functions.GetUserSubscriptions(self.request, context)
		return render(self.request, "magazine/submit.html", context)

	def post(self, *args, **kwargs):
		post = self.request.POST
		mags = str(post['mags']).split(',')

		for mag in mags:
			a = Article()

			a.magazine_posted = get_object_or_404(Magazine, name=str(mag).replace(" ", ""))
			a.article_name = post['name']
			a.hyperlink = post['link']
			a.posted_by = self.request.user

			a.save()

		return redirect("magazine:magazine", mags[0])


class ArticleView(View):
	def get(self, request, thread):
		context = {}
		Functions.GetUserSubscriptions(request, context)

		context['article'] = Article.objects.get(id=thread)
		context['mag'] = context['article'].magazine_posted
		context['comments'] = Comment.objects.filter(article_related=context['article'])
		return render(request, "magazine/article.html", context)

	def post(self, request, thread):
		comment = Comment()

		comment.posted_by = self.request.user
		comment.post_body = self.request.POST['text']
		comment.article_related = Article.objects.get(id=thread)

		comment.save()

		return redirect("magazine:article", comment.article_related.id)


class CreateMagazineView(View):
	def get(self, *args, **kwargs):
		context = {}
		Functions.GetUserSubscriptions(self.request, context)

		return render(self.request, "magazine/newmagazine.html", context)

	def post(self, *args, **kwargs):
		post = self.request.POST

		# Create magazine
		mag = Magazine()

		mag.name = post['name'].replace(" ", "").lower()
		mag.creator = self.request.user

		mag.save()

		# Subscribe author
		subscription = Subscription()

		subscription.magazine_subscribed = mag
		subscription.subscriber = self.request.user

		subscription.save()

		return redirect("magazine:magazine", mag.name)


class SubscribeView(View):
	def get(self, request, mag):
		print "subscribing"
		sub = Subscription.objects.filter(subscriber=request.user).filter(magazine_subscribed__id=mag)

		if len(sub) != 0:
			print "unsub"
			name = sub[0].magazine_subscribed.name
			print sub[0]
			sub[0].delete()
			return redirect("magazine:magazine", name)

		print "sub"
		sub = Subscription()

		magazine = Magazine.objects.get(id=mag)
		sub.subscriber = request.user
		sub.magazine_subscribed = magazine
		sub.save()

		return redirect("magazine:magazine", sub.magazine_subscribed.name)