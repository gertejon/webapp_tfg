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
from locations.models import Stock
from payment_methods.models import PaymentMethod
from orders.models import Order
from orders.models import OrderProduct
from urllib.parse import unquote
from datetime import datetime


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
    # applying filters if requested
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

@login_required
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

@login_required
def accessories(request, instrument_name):
    # getting instrument to render template
    instrument = Product.objects.filter(name=instrument_name)
    # getting dates and locations from URL
    pickup_date = request.session['pickup_date']
    return_date = request.session['return_date']
    pickup_loc = request.GET.get('pickup_loc')
    return_loc = request.GET.get('return_loc')
    # saving locations in session
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

@login_required
def payment(request, instrument_name):
    # getting instrument and payment methods to render template
    instrument = Product.objects.filter(name=instrument_name)
    payment_methods = PaymentMethod.objects.all()
    # getting dates, locations and accessories from URL
    pickup_date = request.session['pickup_date']
    return_date = request.session['return_date']
    pickup_loc = request.session['pickup_loc']
    return_loc = request.session['return_loc']
    accessories = request.GET.getlist('accessories')
    # saving accessories in session
    request.session['accessories'] = accessories

    return render(request, 'rentals/payment.html', {
        'instrument': instrument,
        'payment_methods': payment_methods,
        'pickup_date': pickup_date,
        'return_date': return_date, 
        'pickup_loc': pickup_loc,
        'return_loc': return_loc,
        'accessories': accessories,
    })

@login_required
def overview(request, instrument_name):
    # getting instrument to render template
    instrument = Product.objects.filter(name=instrument_name)
    # getting dates, locations, accessories and payment method from URL
    pickup_date = request.session['pickup_date']
    return_date = request.session['return_date']
    pickup_loc = request.session['pickup_loc']
    return_loc = request.session['return_loc']
    accessories = request.session['accessories']
    payment_method = request.GET.get('payment_method')
    # saving payment method in session
    request.session['payment_method'] = payment_method

    date1 = datetime.strptime(pickup_date, "%m/%d/%Y").date()
    date2 = datetime.strptime(return_date, "%m/%d/%Y").date()
    Ndays = date2 - date1
    days = Ndays.days
    instrumentObj = Product.objects.get(name=instrument_name)
    instrumentPrice = days * instrumentObj.price

    accessory_list = []
    accessories_price = 0.0
    for accessory_name in accessories:
        acc = Product.objects.get(name=accessory_name)
        accessory_list.append(acc)
        accessories_price = accessories_price + acc.price
    totalPrice = instrumentPrice + accessories_price
    request.session['totalPrice'] = totalPrice

    return render(request, 'rentals/overview.html', {
        'instrument': instrument,
        'pickup_date': pickup_date,
        'return_date': return_date, 
        'pickup_loc': pickup_loc,
        'return_loc': return_loc,
        'accessory_list': accessory_list,
        'payment_method': payment_method,
        'days': days,
        'instrumentPrice': instrumentPrice,
        'totalPrice': totalPrice,
    })

@login_required
def confirmation(request, instrument_name):
    
    # page was refreshed and order is already processed
    if not request.session.get('pickup_date'):
        return render(request, 'rentals/index.html')
    
    # creating order
    pickup_date = request.session['pickup_date']
    return_date = request.session['return_date']
    order_pickup_date = datetime.strptime(pickup_date, "%m/%d/%Y").date()
    order_return_date = datetime.strptime(return_date, "%m/%d/%Y").date()
    pickup_loc = Location.objects.get(name=request.session['pickup_loc'])
    return_loc = Location.objects.get(name=request.session['return_loc'])
    pay_method = PaymentMethod.objects.get(name=request.session['payment_method'])
    new_order = Order(
        user = request.user,
        total_price = request.session['totalPrice'],
        pickup_date = order_pickup_date,
        return_date = order_return_date,
        pickup_location = pickup_loc,
        return_location = return_loc,
        payment_method = pay_method,
    )

    # save order (products will be added after saving)
    new_order.save()

    # getting accessories from session
    accessories = request.session['accessories']
    accessory_list = []
    for accessory_name in accessories:
        acc = Product.objects.get(name=accessory_name)
        accessory_list.append(acc)
    # getting instrument object
    instrument = Product.objects.get(name=instrument_name)
    # adding products to order (instruments + accessories) (Through OrderProduct)
    orderproduct = OrderProduct(order = new_order, product = instrument) # instrument
    orderproduct.save()
    for accessory in accessory_list:
        orderproduct = OrderProduct(order = new_order, product = accessory)
        orderproduct.save()

    # stock update
    # stock = Stock.objects.get(location=pickup_loc, product=instrument)
    # stock.units = stock.units - 1
    # stock.save()
    
    del request.session['pickup_date']
    del request.session['return_date']
    del request.session['pickup_loc']
    del request.session['return_loc']
    del request.session['accessories']
    del request.session['totalPrice']
    del request.session['payment_method']

    return render(request, 'rentals/confirmation.html', {
        'order': new_order,
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

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user.id)
    orderProducts = OrderProduct.objects.all()
    orders_id = []
    for order in user_orders:
        orders_id.append(order.id)
    return render(request, 'rentals/orders.html', {
        'user_orders': user_orders,
        'orders_id': orders_id,
        'orderProducts': orderProducts,

    })

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    orderProducts = OrderProduct.objects.all()
    accessory_list = []
    accessories_price = 0


    for op in orderProducts:
        if op.order == order:
            if op.product.is_accessory == False:
                instrument = op.product
                instrument_price = op.product.price
            else:
                accessory_list.append(op.product)
                accessories_price = accessories_price + op.product.price

    Ndays = order.return_date - order.pickup_date
    days = Ndays.days
    instrument_total_price = instrument_price * days
    totalPrice = instrument_total_price + accessories_price


    return render(request, 'rentals/order_detail.html', {
        'order': order,
        'instrument': instrument,
        'accessory_list': accessory_list,
        'totalPrice': totalPrice,
        'instrument_total_price': instrument_total_price,
        'days': days,
    })