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
from locations.models import Location
from urllib.parse import unquote


########################################################### Web content views ###########################################################
def home(request):
    categories = Category.objects.all()
    return render(request, 'rentals/index.html', {"categories": categories})

def aboutus(request):
    return render(request, 'rentals/aboutus.html')


########################################################### instrument browsing views #####################################################
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
    min_price = request.GET.get('min-price-filter')
    max_price = request.GET.get('max-price-filter')
    sort = request.GET.get('sort')
    # applying filters
    if quality:
        instruments = instruments.filter(quality=quality)
    if brand:
        instruments = instruments.filter(brand__name=brand)
    if min_price:
        instruments = instruments.filter(price__gte=min_price)
    if max_price:
        instruments = instruments.filter(price__lte=max_price)
    if sort == 'AZ':
        instruments = instruments.order_by('name')
    elif sort == 'ZA':
        instruments = instruments.order_by('-name')
    return render(request, 'rentals/instruments.html', {
        'instruments': instruments, 
        'type': type_name,
        'qualities': qualities,
        'brands': brands,
    })


############################################################ order creation views ####################################################
@login_required
def rent(request, instrument_name):
    # getting instrument tp render template
    instrument = Product.objects.filter(name=instrument_name)
    # getting locations to check if the instrument can be rented
    pickup_locations = Location.objects.filter(active=True, products__name=instrument_name, stock__units__gt=0).distinct()

    return render(request, 'rentals/rent.html', {'instrument': instrument, 'pickup_locations': pickup_locations})

def locations(request, instrument_name):
    # getting dates from URL
    pickup_date = request.GET.get('pickup_date')
    return_date = request.GET.get('return_date')
    # saving dates in session
    request.session['pickup_date'] = pickup_date
    request.session['return_date'] = return_date
    # getting locations to render template
    pickup_locations = Location.objects.filter(active=True, products__name=instrument_name, stock__units__gt=0).distinct()
    return_locations = Location.objects.filter(active=True)
    # getting instrument to render template
    instrument = Product.objects.filter(name=instrument_name)

    return render(request, 'rentals/locations.html', {
        'instrument': instrument, 
        'pickup_locations': pickup_locations,
        'return_locations': return_locations, 
        'pickup_date': pickup_date,
        'return_date': return_date,
    })

def accessories(request, instrument_name):
    # getting instrument to render template
    instrument = Product.objects.filter(name=instrument_name)
    # getting dates and locations from URL
    pickup_date = request.GET.get('pickup_date')
    return_date = request.GET.get('return_date')
    pickup_loc = request.GET.get('pickup_loc')
    return_loc = request.GET.get('return_loc')
    # saving loactions in session
    request.session['pickup_loc'] = pickup_loc
    request.session['return_loc'] = return_loc
    # getting instrument accessories
    instrumentName = Product.objects.filter(name=instrument_name).first()
    accessories = instrumentName.accessories.all()

    return render(request, 'rentals/accessories.html', {
        'instrument': instrument,
        'pickup_date': pickup_date,
        'return_date': return_date, 
        'pickup_loc': pickup_loc,
        'return_loc': return_loc,
        'accessories': accessories,
    })



########################################################### user management views #######################################################
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