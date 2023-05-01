from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import Rental

def index(request):
    rentals = Rental.objects 
    return render(request, 'rentals/index.html',{'rentals':rentals})