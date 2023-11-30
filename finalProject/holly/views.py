import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, User, Location, Religion


# Create your views here.
@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        religionsSelect = request.POST["religionsSelect"]
        city = request.POST["city"]
        print(city)
        neighbourhood = request.POST["neighbourhood"]
        print(neighbourhood)
        user = User.objects.get(pk=request.user.id)

        if not user.isEntity:
            religion = Religion.objects.get(name=religionsSelect)
            locations = Location.objects.all().filter(city=city, neighbourhood=neighbourhood)
            entities = User.objects.all().filter(religions=religion, locations__in=locations)
            print(religion)
            print(locations)
            print(entities.__len__())
            paginator = Paginator(entities, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "holly/resultEntities.html", {
                "entities": page_obj,
                "title": "Result of search"
            })
        else:
            return render(request, "holly/erro.html", {
                "error": "Something went wrong"
            })
    else:
        user = User.objects.get(pk=request.user.id)
        if user.isEntity:
            return profile(request, user.id)
        else:
            return render(request, "holly/index.html")


@login_required(login_url="login")
def following(request):
    user = User.objects.get(pk=request.user.id)
    print(user.following.all())
    print(user.following)
    posts = Post.objects.all().filter(user__in=user.following.all()).order_by('-id')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "holly/following.html", {
        "posts": page_obj
    })


def entities(request):
    entities = User.objects.all().filter(isEntity=True)
    paginator = Paginator(entities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "holly/resultEntities.html", {
        "entities": page_obj,
        "title": "All entities"
    })


@login_required(login_url="login")
def profile(request, userId):
    if request.method == "POST":
        if request.user.id == userId and User.objects.get(pk=userId).isEntity:
            text = request.POST["text"]
            if text:
                post = Post(user=request.user, text=text)
                post.save()
                return HttpResponseRedirect(reverse('profile', args=(userId,)))
            else:
                return render(request, "network/erro.html", {
                    "error": "You need to put a text in the post"
                })
        else:
            return render(request, "holly/erro.html", {
                "error": "Something went wrong"
            })
    else:
        if User.objects.get(pk=userId).isEntity:
            print(f"followers: {User.objects.all().filter(following=User.objects.get(pk=userId))} ")
            print(f"following: {User.objects.get(pk=userId).following} ")
            posts = Post.objects.all().filter(user=User.objects.get(pk=userId)).order_by('-id')
            paginator = Paginator(posts, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "holly/profile.html", {
                "posts": page_obj,
                "profileUser": User.objects.get(pk=userId),
                "followers": User.objects.all().filter(following=User.objects.get(pk=userId))
            })
        else:
            return render(request, "holly/erro.html", {
                "error": "Something went wrong"
            })


@login_required(login_url="login")
def editProfile(request, userId):
    if request.method == "POST":
        if request.user.id == userId and User.objects.get(pk=userId).isEntity:
            user = User.objects.get(pk=userId)

            try:
                religionStr = request.POST["religion"]
                try:
                    user.religions.clear()
                    user.religions.add(Religion.objects.get(name=religionStr))
                except:
                    religion = Religion(name=religionStr)
                    religion.save()
                    user.religions.add(religion)
            finally:
                try:
                    city = request.POST["city"]
                    neighbourhood = request.POST["neighbourhood"]
                    details = request.POST["details"]
                    text = request.POST["text"]
                    if city and neighbourhood and details:
                        location = Location(city=city, neighbourhood=neighbourhood, details=details)
                        location.save()
                        user.locations = location
                    elif details:
                        user.locations.details = details
                        user.locations.save()
                    if text:
                        user.text = text
                finally:
                    user.save()
            return HttpResponseRedirect(reverse('profile', args=(userId,)))
        else:
            return render(request, "holly/erro.html", {
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
            return render(request, "holly/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "holly/login.html")


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
        isEntity = request.POST["isEntity"]
        if password != confirmation:
            return render(request, "holly/register.html", {
                "message": "Passwords must match."
            })
        if isEntity == "True":
            try:
                user = User.objects.create_user(username, email, password)
                user.isEntity = True
                religionStr = request.POST["religion"]
                try:
                    user.religions.add(Religion.objects.get(name=religionStr))
                except:
                    religion = Religion(name=religionStr)
                    religion.save()
                    user.religions.add(religion)

                city = request.POST["city"]
                neighbourhood = request.POST["neighbourhood"]
                details = request.POST["details"]
                location = Location(city=city, neighbourhood=neighbourhood, details=details)
                location.save()

                text = request.POST["text"]
                user.text = text
                user.locations = location

                user.save()
            except IntegrityError:
                return render(request, "holly/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Attempt to create new user
        else:
            try:
                user = User.objects.create_user(username, email, password)
                user.isEntity = False
                user.save()
            except IntegrityError:
                return render(request, "holly/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "holly/register.html")
