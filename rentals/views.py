from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignUpForm


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

@login_required
def account(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'rentals/account.html', {'form': form, 'user': request.user})