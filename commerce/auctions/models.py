from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return f"{self.id}: {self.name}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=999)
    startingBid = models.FloatField()
    imageUrl = models.CharField(blank=True, max_length=999)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="auctions")

    def __str__(self):
        return f"{self.id}:{self.title} by {self.startingBid}"


class User(AbstractUser):
    auctions = models.ManyToManyField(AuctionListing, blank=True, related_name="users")
    watchList = models.ManyToManyField(AuctionListing, blank=True, related_name="usersWatchs")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid")
    value = models.FloatField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=999)

    def __str__(self):
        return f"{self.user.username}: {self.text}"
