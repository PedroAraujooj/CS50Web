from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:userId>", views.profile, name="profile"),
    path("editProfile/<int:userId>", views.editProfile, name="editProfile"),
    path("following", views.following, name="following"),
    path("edit/<postId>", views.edit, name="edit"),
    path("entities", views.entities, name="entities"),
    path("switch/<int:userId>", views.switch, name="switch")
]