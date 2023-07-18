from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flightId):
    flightItem = Flight.objects.get(pk=flightId)
    return render(request, "flights/flight.html", {
        "flight": flightItem,
        "passengers": flightItem.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flightItem).all()
    })


def book(request, flightId):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flightId)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
