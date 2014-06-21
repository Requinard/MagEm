from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Magazine(models.Model):
	name = models.CharField(max_length=20)

	creator = models.ForeignKey(User)

	moderators = models.ManyToManyField(User, related_name="mods")

	date_created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Article(models.Model):
	hyperlink = models.URLField(max_length=200)

	article_name = models.CharField(max_length=100, default="Lorem Ipsum")

	posted_by = models.ForeignKey(User, null=True)

	magazine_posted = models.ForeignKey(Magazine)
	date_submitted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.article_name


class Subscription(models.Model):
	magazine_subscribed = models.ForeignKey(Magazine)
	subscriber = models.ForeignKey(User)

	date_subscribed = models.DateTimeField(auto_now=True)


class Comment(models.Model):
	article_related = models.ForeignKey(Article)
	posted_by = models.ForeignKey(User)
	post_body = models.CharField(max_length=1024)
	date_created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.post_body


class Vote(models.Model):
	article_related = models.ForeignKey(Article)
	magazine_related = models.ForeignKey(Magazine, null=True)
	user_voted = models.ForeignKey(User)
	is_constructive = models.BooleanField(default=True)
	is_agreed = models.BooleanField(default=True)
	date_submitted = models.DateTimeField(auto_now=True)

	def __str__(self):
		response = self.article_related.article_name
		if self.is_constructive == True:
			response += " Constructive "
		else:
			response += " Destructive "

		if self.is_agreed == True:
			response += "Agree"
		else:
			response += "Disagree"

		response = response.join(" by " + self.user_voted)

		return response