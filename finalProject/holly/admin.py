from django.contrib import admin

from holly.models import Post, User, Religion, Location

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Religion)
admin.site.register(Location)
