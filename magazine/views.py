from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import View

from .models import *


class Functions:
	@staticmethod
	def GetUserSubscriptions(request, context):
		if request.user.is_authenticated():
			subscription = Subscription.objects.filter(subscriber=request.user)
			context['subscriptions'] = subscription
			context['user'] = request.user


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
		context['articles'] = Article.objects.filter(submitted_to=context['mag'])

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

			a.submitted_to = get_object_or_404(Magazine, name=str(mag).replace(" ", ""))
			a.name = post['name']
			a.link = post['link']
			a.submitted_by = self.request.user

			a.save()

		return redirect("magazine:magazine", mag[0].name)


class ArticleView(View):
	def get(self, request, thread):
		context = {}
		Functions.GetUserSubscriptions(request, context)

		context['article'] = Article.objects.get(id=thread)
		context['comments'] = Comment.objects.filter(article_on=context['article'])
		return render(request, "magazine/article.html", context)

	def post(self, request, thread):
		comment = Comment()

		comment.submitted_by = self.request.user
		comment.text = self.request.POST['text']
		comment.article_on = Article.objects.get(id=thread)

		comment.save()

		return ("magazine:article", comment.article_on.id)


class LoginView(View):
	def get(self, *args, **kwargs):
		return redirect("magazine:index")

	def post(self, request, *args, **kwargs):
		user = authenticate(username=request.POST['user'], password=request.POST['password'])

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect("magazine:index")
			else:
				return HttpResponse("You were banned!")
		else:
			return HttpResponse("The password or username was incorrect")


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

		subscription.subscribed_to = mag
		subscription.subscriber = self.request.user

		subscription.save()

		return redirect("magazine:magazine", mag.name)