from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, symmetrical=False)
    # followers = models.ManyToManyField('self', symmetrical=False)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=999)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "text": self.text,
            "date": self.date,
            "likes": self.likes
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=999)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
