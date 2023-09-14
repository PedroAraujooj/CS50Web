from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import safe
from django.urls import reverse
import json

from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        text = request.POST["text"]
        if text:
            post = Post(user=request.user, text=text, likes=0)
            post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "network/erro.html", {
                "error": "You need to put a text in the post"
            })
    else:
        posts = Post.objects.all().order_by('-id')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj
        })


@login_required(login_url="login")
def following(request):
    user = User.objects.get(pk=request.user.id)
    print(user.following.all())
    print(user.following)
    posts = Post.objects.all().filter(user__in=user.following.all()).order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": page_obj
    })


@login_required(login_url="login")
def profile(request, userId):
    print(f"followers: {User.objects.all().filter(following=User.objects.get(pk=userId))} ")
    print(f"following: {User.objects.get(pk=userId).following} ")
    posts = Post.objects.all().filter(user=User.objects.get(pk=userId)).order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "posts": page_obj,
        "profileUser": User.objects.get(pk=userId),
        "followers": User.objects.all().filter(following=User.objects.get(pk=userId))
    })


def switch(request, userId):
    if request.method == "POST":
        following = request.POST["following"]
        if following == 'true':
            User.objects.get(pk=request.user.id).following.remove(User.objects.get(pk=userId))
            return HttpResponseRedirect(reverse('profile', args=(userId,)))
        elif following == 'false':
            User.objects.get(pk=request.user.id).following.add(User.objects.get(pk=userId))
            return HttpResponseRedirect(reverse('profile', args=(userId,)))
        else:
            return render(request, "network/erro.html", {
                "error": "Something went wrong"
            })


@csrf_exempt
@login_required
def edit(request, postId):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(pk=postId)
        post.text = data.get("text", "")
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=200)
    else:
        post = Post.objects.get(pk=postId)
        if post:
            return JsonResponse(post.serialize(), safe=False)
        else:
            return JsonResponse({"error": "This post doesn't exist"}, status=400)


@csrf_exempt
@login_required
def like(request, postId):
    if request.method == "POST":
        post = Post.objects.get(pk=postId)
        user = User.objects.get(pk=request.user.id)
        print(post.likes.all())
        print(len(post.likes.all()))
        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            print("no")
            print(len(post.likes.all()))
            return JsonResponse({"message": "no"}, status=200)
        else:
            post.likes.add(user)
            post.save()
            print("yes")
            print(len(post.likes.all()))
            return JsonResponse({"message": "yes"}, status=200)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
