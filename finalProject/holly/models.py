from django.contrib.auth.models import AbstractUser
from django.db import models


class Religion(models.Model):
    name = models.CharField(max_length=999)

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    city = models.CharField(max_length=999)
    neighbourhood = models.CharField(max_length=999)
    details = models.CharField(max_length=999)

    def __str__(self):
        return f"{self.neighbourhood}"


class User(AbstractUser):
    memberOf = models.ManyToManyField('self', blank=True, symmetrical=False)
    isEntity = models.BooleanField(default=False)
    religions = models.ManyToManyField(Religion, blank=True, symmetrical=False)
    locations = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="userEntitys", blank=True, null=True)
    text = models.CharField(max_length=999)


class Announce(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announces")
    text = models.CharField(max_length=999)
    date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "text": self.text,
            "date": self.date,
        }

    def __str__(self):
        return f"{self.text}"
