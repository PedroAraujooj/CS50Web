from django.urls import path

from hello import views

urlpatterns = [
    path('', views.index, name="index"),
    path('pedro', views.pedro, name="pedro"),
    path('wik<str:name>', views.greet, name="greet"),
]