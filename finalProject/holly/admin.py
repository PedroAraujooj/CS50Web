from django.contrib import admin

from holly.models import Announce, User, Religion, Location

# Register your models here.
admin.site.register(User)
admin.site.register(Announce)
admin.site.register(Religion)
admin.site.register(Location)
