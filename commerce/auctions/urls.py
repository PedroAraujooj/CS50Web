from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListining", views.createListining, name="createListining"),
    path("listing/<int:listingId>", views.listing, name="listing"),
    path("watch/<int:listingId>", views.watch, name="watch"),
    path("bid/<int:listingId>", views.bid, name="bid"),
    path("close/<int:listingId>", views.close, name="close"),
    path("comment/<int:listingId>", views.comment, name="comment"),
    path("watchList", views.watchList, name="watchList"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:categorieId>", views.categoriesListing, name="categoriesListing"),

]
