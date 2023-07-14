from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "hello/index.html")
def pedro(request):
    return HttpResponse("Hello, pedro")
def greet(request, name):
    return render(request, "hello/wiki/greet.html", {
        "name": name.capitalize()
    })
