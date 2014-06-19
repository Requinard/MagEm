from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Magazine(models.Model):
	name = models.CharField(max_length=20)

	creator = models.ForeignKey(User)

	mods = models.ManyToManyField(User, related_name="mods")

	create_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Article(models.Model):
	link = models.URLField(max_length=200)

	name = models.CharField(max_length=100, default="Lorem Ipsum")

	submitted_by = models.ForeignKey(User, null=True)

	submitted_to = models.ForeignKey(Magazine)
	submitted_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Subscription(models.Model):
	subscribed_to = models.ForeignKey(Magazine)
	subscriber = models.ForeignKey(User)

	subscribed_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
	article_on = models.ForeignKey(Article)
	submitted_by = models.ForeignKey(User)
	text = models.CharField(max_length=1024)
	submitted_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text


class Vote(models.Model):
	article = models.ForeignKey(Article)
	mag = models.ForeignKey(Magazine, null=True)
	user = models.ForeignKey(User)
	constructive = models.BooleanField(default=True)
	agree = models.BooleanField(default=True)
	date_submitted = models.DateTimeField(auto_now=True)

	def __str__(self):
		response = self.article.name
		if self.constructive == True:
			response += " Constructive "
		else:
			response += " Destructive "

		if self.agree == True:
			response += "Agree"
		else:
			response += "Disagree"

		response = response.join(" by " + self.user)

		return response