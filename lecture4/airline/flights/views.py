from django.shortcuts import render
from .models import Flight
# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flightId):
    flightItem = Flight.objects.get(pk=flightId)
    return render(request, "flights/flight.html", {
        "flight":flightItem
    })