from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignUpForm

# Create your views here.



def home(request):
    return render(request, 'rentals/index.html')

def aboutus(request):
    return render(request, 'rentals/aboutus.html')

def categories(request):
    return render(request, 'rentals/categories.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'rentals/registration/signup.html', {'form': form})
