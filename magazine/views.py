from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import *


def UserItems(request, context):
    if request.user.is_authenticated():
        subscription = Subscription.objects.filter(subscriber=request.user)
        context['subscriptions'] = subscription

        context['user'] = request.user


# Create your views here.
def index(request):
    context = {}

    UserItems(request, context)

    return render(request, "magazine/index.html", context)


def magazine(request, mag):
    context = {}

    UserItems(request, context)

    mag = get_object_or_404(Magazine, name=mag)
    context['mag'] = mag

    articles = Article.objects.filter(submitted_to=mag)
    context['articles'] = articles

    return render(request, "magazine/magazine.html", context)


def submit(request):
    context = {}

    UserItems(request, context)

    if request.POST:
        post = request.POST

        mags = str(post['mags']).split(',')

        for mag in mags:
            a = Article()

            a.submitted_to = get_object_or_404(Magazine, name=str(mag).replace(" ", ""))
            a.name = post['name']
            a.link = post['link']
            a.submitted_by = request.user

            a.save()

        return redirect("/magazine/m/" + mags[0] + "/")

    return render(request, "magazine/submit.html", context)


def article(request, thread):
    context = {}

    print("getting items")
    UserItems(request, context)

    print ("getting article")
    art = get_object_or_404(Article, id=int(thread))
    context['article'] = art

    if request.POST:
        print "saving comment"
        com = Comment()

        com.submitted_by = request.user
        com.text = request.POST['text']
        com.article_on = art

        com.save()

        print com

    print("getting comment")
    comments = Comment.objects.filter(article_on=art)
    context['comments'] = comments

    return render(request, "magazine/article.html", context)


def login(request):
    if request.user.is_authenticated():
        return redirect("/magazine/")
    else:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/magazine/")
            else:
                return HttpResponse("You were banned!")
        else:
            return HttpResponse("The password or username was incorrect")


def createmagazine(request):
    context = {}

    UserItems(request, context)

    if not request.POST:
        return render(request, 'magazine/newmagazine.html', context)
    else:
        post = request.POST

        mag = Magazine()

        mag.name = post['name']
        mag.creator = request.user

        mag.save()

        return redirect("/magazine/m/" + mag.name + "/")