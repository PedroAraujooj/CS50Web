from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("random", views.random, name="random"),
]
