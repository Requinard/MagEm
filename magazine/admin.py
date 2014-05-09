from django.contrib import admin

from .models import Magazine, Article, Subscription, Comment

# Register your models here.
admin.site.register(Magazine)
admin.site.register(Article)
admin.site.register(Subscription)
admin.site.register(Comment)