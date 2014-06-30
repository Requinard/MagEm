from math import log, sqrt

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.timezone import now


# Create your models here.
class Tally(models.Model):
	vote_agr = models.IntegerField(default=1)
	vote_dis = models.IntegerField(default=0)
	vote_con = models.IntegerField(default=1)
	vote_des = models.IntegerField(default=0)
	date_created = models.DateTimeField()

	def _hot(self):
		"""
		Will sort by hot ranking
		:return: Returns score of tally
		"""
		print "starting hot"

		score_agr = self.vote_agr - self.vote_dis
		score_con = self.vote_con - self.vote_des

		total = 0

		sign_agr = 1 if score_agr > 0 else -1 if score_agr < 0 else 0
		sign_con = 1 if score_agr > 0 else -1 if score_con < 0 else 0
		seconds = (now() - self.date_created).total_seconds()

		log_agr = log(max(abs(score_agr), 1), 10)
		log_con = log(max(abs(score_con), 1), 10)

		total += round(log_agr + sign_agr * seconds / 45000, 7)
		total += round(log_con + sign_con * seconds / 45000, 7)

		return total / 2

	def _best(self):
		print "starting best"
		total_agr = self.vote_agr + self.vote_dis
		total_con = self.vote_con + self.vote_des
		total = 0

		if total_agr == 0 or total_con == 0:
			print "a value is 0"
			return 0

		z = 1.0
		perc_agr = float(self.vote_agr) / total_agr
		perc_con = float(self.vote_agr) / total_con

		total += sqrt(perc_agr + z * z / (2 * total_agr) - z * (
		(total_agr * (1 - total_agr) + z * z / (4 * total_agr)) / total_agr)) / (1 + z * z / total_agr)

		total += sqrt(perc_con + z * z / (2 * total_con) - z * (
		(total_con * (1 - total_con) + z * z / (4 * total_con)) / total_con)) / (1 + z * z / total_con)

		return total / 2

	def sort(self, sort_type = "hot"):
		print sort_type
		if sort_type == "hot":
			return self._hot()
		if sort_type == "best":
			return self._best()


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

	tally = models.ForeignKey('Tally', null=True, default=None)

	def __str__(self):
		return self.article_name


class Subscription(models.Model):
	magazine_subscribed = models.ForeignKey(Magazine)
	subscriber = models.ForeignKey(User)

	date_subscribed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.subscriber.username.join(self.magazine_subscribed.name)

	class Meta:
		ordering = ("magazine_subscribed__name",)


class Comment(models.Model):
	article_related = models.ForeignKey(Article)
	posted_by = models.ForeignKey(User)
	post_body = models.CharField(max_length=1024)
	date_created = models.DateTimeField(auto_now=True)

	tally = models.ForeignKey(Tally, null=True, default=None)

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

		response = response.join(" by " + self.user_voted.username)

		return response


def extraInit(**kwargs):
	instance = kwargs.get('instance')
	tal = Tally()
	tal.save()
	instance.tally = tal


pre_save.connect(extraInit, Article)
pre_save.connect(extraInit, Comment)