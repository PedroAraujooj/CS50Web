from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Category, Comment


def index(request):
    if AuctionListing.objects.all().exists():
        return render(request, "auctions/index.html", {
            "itens": AuctionListing.objects.all().order_by('-id').values(),
        })
    return render(request, "auctions/index.html")


@login_required(login_url="login")
def watchList(request):
    if request.user.watchList.exists():
        return render(request, "auctions/watchList.html", {
            "itens": request.user.watchList.all().order_by('-id').values(),
        })
    return render(request, "auctions/erro.html", {
        "error": "No itens in your watchlist yet"
    })

@login_required(login_url="login")
def categories(request):
    if Category.objects.all().exists():
        return render(request, "auctions/categories.html", {
            "itens": Category.objects.all().order_by('name').values(),
        })
    return render(request, "auctions/erro.html", {
        "error": "No Categories yet",
    })

@login_required(login_url="login")
def categoriesListing(request, categorieId):
    if Category.objects.get(pk=categorieId) and AuctionListing.objects.all().filter(categories=Category.objects.get(pk=categorieId)):
        return render(request, "auctions/categoriesListing.html", {
            "itens": AuctionListing.objects.all().filter(categories=Category.objects.get(pk=categorieId)).order_by('-id').values(),
            "name": Category.objects.get(pk=categorieId).name,
        })
    return render(request, "auctions/erro.html", {
        "error": "No auctions in this category yet",
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def createListining(request):
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        bid = request.POST["bid"]
        imageUrl = request.POST["url"]
        category = request.POST["category"]

        if title and text and bid:
            try:
                getCategory = Category.objects.get(name=category.capitalize())
            except:
                new_category = Category(name=category.capitalize())
                getCategory = new_category
                getCategory.save()
            auction = AuctionListing(title=title, text=text, imageUrl=imageUrl, startingBid=bid)
            auction.save()
            auction.categories.add(getCategory)
            auction.save()
            user = request.user
            user.auctions.add(auction)

            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, "auctions/createListining.html")

    return render(request, "auctions/createListining.html")


@login_required(login_url="login")
def listing(request, listingId):
    if AuctionListing.objects.get(pk=listingId):
        return render(request, "auctions/listing.html", {
            "listing": AuctionListing.objects.get(pk=listingId),
            "bids": AuctionListing.objects.get(pk=listingId).bid.all().order_by('-value')
        })
    return render(request, "auctions/index.html")

@login_required(login_url="login")
def watch(request, listingId):
    user = request.user
    if AuctionListing.objects.get(pk=listingId) in user.watchList.all():
        user.watchList.remove(AuctionListing.objects.get(pk=listingId))
        user.save()
    else:
        user.watchList.add(AuctionListing.objects.get(pk=listingId))
        user.save()
    return HttpResponseRedirect(reverse("listing", args=(listingId,)))

@login_required(login_url="login")
def bid(request, listingId):
    if request.method == "POST":
        bidForm = float(request.POST["bid"])
        auction = AuctionListing.objects.get(pk=listingId)
        if bidForm and auction:
            if auction.bid.all().order_by('-value').first():
                if bidForm > auction.bid.all().order_by('-value').first().value:
                    newBid = Bid(user=request.user, auction=auction, value=bidForm)
                    newBid.save()
                    return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
                else:
                    return render(request, "auctions/erro.html", {
                        "error": "Bid lower than the highest one."
                    })
            else:
                if bidForm > auction.startingBid:
                    newBid = Bid(user=request.user, auction=auction, value=bidForm)
                    newBid.save()
                    return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

                else:
                    return render(request, "auctions/erro.html", {
                        "error": "Bid lower than the minimum."
                    })
        else:
            return render(request, "auctions/erro.html", {
                "error": "Invalid value for bid"
            })

@login_required(login_url="login")
def close(request, listingId):
    user = request.user
    auction = AuctionListing.objects.get(pk=listingId)
    if auction and (auction in user.auctions.all()):
        auction.active = False
        auction.save()
    else:
        return render(request, "auctions/erro.html", {
            "error": "User without permission or non-existent item"
        })
    return HttpResponseRedirect(reverse("listing", args=(listingId,)))

@login_required(login_url="login")
def comment(request, listingId):
    if request.method == "POST":
        commentForm = request.POST["comment"]
        auction = AuctionListing.objects.get(pk=listingId)
        if commentForm and auction:
            newComment = Comment(user=request.user, auction=auction, text=commentForm)
            newComment.save()
            return HttpResponseRedirect(reverse("listing", args=(listingId,)))
        else:
            return render(request, "auctions/erro.html", {
                "error": "Invalid comment"
            })
