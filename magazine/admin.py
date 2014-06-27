from django.contrib import admin

from .models import Magazine, Article, Subscription, Comment, Vote


class MagazineAdmin(admin.ModelAdmin):
	fieldsets = (
	(
	"Meta", {
	'fields': ("name", "creator")
	}),
	(
	"Moderators", {
	"fields": ("moderators",)
	}),
	)

	list_display = ("id", "name", "creator", "date_created")

	list_filter = ("name", "creator")


class ArticleAdmin(admin.ModelAdmin):
	list_display = ("id", "article_name", "posted_by", "magazine_posted")
	list_filter = ("magazine_posted", "posted_by")
	search_fields = ("magazine_posted__name", "posted_by", "article_name")

	fieldsets = (
	(
	"Meta", {
	'fields': ("magazine_posted", "posted_by")
	}
	),
	(
	"Article Info", {
	"fields": ("hyperlink", "article_name")
	}
	),
	)


class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ("id", "magazine_subscribed", "subscriber")
	list_filter = ("magazine_subscribed", "subscriber")


class CommentAdmin(admin.ModelAdmin):
	readonly_fields = ("tally", )



# Register your models here.
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote)