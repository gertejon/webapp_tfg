from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignUpForm
from categories.models import Category
from product_types.models import Product_Type
from products.models import Product
from urllib.parse import unquote


def home(request):
    categories = Category.objects.all()
    return render(request, 'rentals/index.html', {"categories": categories})

def aboutus(request):
    return render(request, 'rentals/aboutus.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'rentals/categories.html', {"categories": categories})

def types(request, category_name):
    category = Category.objects.get(name=category_name)
    types = Product_Type.objects.filter(category=category)
    return render(request, 'rentals/types.html', {'types': types, 'category': category}) 

def instruments(request, type_name):
    if(type_name == 'All instruments'): #viewing all instruments was selected
        instruments = Product.objects.filter(active=True, is_accessory=False)
    else:
        if Product_Type.objects.filter(name=type_name).exists(): # viewing an specific type was selected
            prod_type = Product_Type.objects.get(name=type_name)
            instruments = Product.objects.filter(product_type=prod_type, active=True, is_accessory=False)
        else: # viewing all types from a category was selected
            category = Category.objects.get(name=type_name)
            instruments = Product.objects.filter(category=category, active=True, is_accessory=False)
        
    qualities = instruments.values_list('quality', flat=True).distinct()
    brands = instruments.values_list('brand__name', flat=True).distinct()

    # filters logic
    # getting filters 
    quality = request.GET.get('quality')
    brand = request.GET.get('brand')
    if quality:
        instruments = instruments.filter(quality=quality)
    if brand:
        instruments = instruments.filter(brand__name=brand)
    return render(request, 'rentals/instruments.html', {
        'instruments': instruments, 
        'type': type_name,
        'qualities': qualities,
        'brands': brands,
    })

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