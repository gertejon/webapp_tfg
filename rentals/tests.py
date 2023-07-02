from django.test import TestCase, Client
from django.urls import resolve, reverse
from rentals.views import *
from django.contrib.auth.views import LoginView, LogoutView
import json
from django.conf import settings
from datetime import datetime


class TestUrl(TestCase):
    def test_home(self):
        url = reverse('home')
        view = home
        self.assertEquals(resolve(url).func, view)
        
    def test_aboutus(self):
        url = reverse('aboutus')
        view = aboutus
        self.assertEquals(resolve(url).func, view)

    def test_categories(self):
        url = reverse('categories')
        view = categories
        self.assertEquals(resolve(url).func, view)
    
    def test_login(self):
        url = reverse('login')
        view = LoginView.as_view(template_name='rentals/registration/login.html')
        self.assertEquals(type(resolve(url).func.view_class.as_view()), type(view))

    def test_logout(self):
        url = reverse('logout')
        view = LogoutView.as_view()
        self.assertEquals(type(resolve(url).func.view_class.as_view()), type(view))
    
    def test_signup(self):
        url = reverse('signup')
        view = signup
        self.assertEquals(resolve(url).func, view)
    
    def test_account(self):
        url = reverse('account')
        view = account
        self.assertEquals(resolve(url).func, view)
    
    def test_orders(self):
        url = reverse('orders')
        view = orders
        self.assertEquals(resolve(url).func, view)
    
    def test_order_detail(self):
        order_id_example = 1
        url = reverse('order_detail', args=[order_id_example])
        view = order_detail
        self.assertEquals(resolve(url).func, view)
    
    def test_types(self):
        url = reverse('types', args=['category_example'])
        view = types
        self.assertEquals(resolve(url).func, view)
    
    def test_instruments(self):
        url = reverse('instruments', args=['type_example'])
        view = instruments
        self.assertEquals(resolve(url).func, view)
    
    def test_dates(self):
        url = reverse('dates', args=['instrument_example'])
        view = dates
        self.assertEquals(resolve(url).func, view)
    
    def test_locations(self):
        url = reverse('locations', args=['instrument_example'])
        view = locations
        self.assertEquals(resolve(url).func, view)
    
    def test_accessories(self):
        url = reverse('accessories', args=['instrument_example'])
        view = accessories
        self.assertEquals(resolve(url).func, view)
    
    def test_payment(self):
        url = reverse('payment', args=['instrument_example'])
        view = payment
        self.assertEquals(resolve(url).func, view)

    def test_overview(self):
        url = reverse('overview', args=['instrument_example'])
        view = overview
        self.assertEquals(resolve(url).func, view)
    
    def test_confirmation(self):
        url = reverse('confirmation', args=['instrument_example'])
        view = confirmation
        self.assertEquals(resolve(url).func, view)
    

class TestViews(TestCase):
    def test_example(self):
        print(settings.DATABASES)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(id=100, username='test', password='test')
        self.location = Location.objects.create(
            id=100,
            name='Aribau',
            active=True,
        )
        self.home_url = reverse('home')
        self.aboutus_url = reverse('aboutus')
        self.categories_url = reverse('categories')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.signup_url = reverse('signup')
        self.account_url = reverse('account')
        self.orders_url = reverse('orders')

        self.pickup_date = datetime.strptime('07/12/2023', "%m/%d/%Y").date()
        self.order_example = Order.objects.create(id=100, 
            pickup_date=datetime.strptime('07/12/2023', "%m/%d/%Y").date(),
            return_date=datetime.strptime('09/12/2023', "%m/%d/%Y").date(),
            user_id=100,
        )
        self.order_detail_url = reverse('order_detail', args=[self.order_example.id])
        self.category_example = Category.objects.create(
            id=100,
            name='Guitars',
        )
        self.types_url = reverse('types', args=[self.category_example])
        self.type_example = Product_Type.objects.create(
            id=100,
            name='Electric Guitars',
            category_id=100,
        )
        self.instruments_url = reverse('instruments', args=[self.type_example])
        self.brand = Brand.objects.create(
            id=100,
            name='Guild'
        )
        self.instrument_example = Product.objects.create(
            id=100,
            name='Guild Starfire',
            category_id=100,
            product_type_id=100,
            quality='MID-RANGE',
            price=18,
            specs=['spec1', 'spec2'],
            active=True,
            image=None,
            brand_id=100,
            is_accessory=False,
        )

        self.accessory_example = Product.objects.create(
            id=111,
            name='Jack',
            category_id=100,
            product_type_id=100,
            quality='MID-RANGE',
            price=18,
            specs=['spec1', 'spec2'],
            active=True,
            image=None,
            brand_id=100,
            is_accessory=True,
        )

        self.inst_name = self.instrument_example.name

        self.dates_url = reverse('dates', args=[self.inst_name])
        self.dates_url += f'?pickup_loc={self.location.name}'

        self.locations_url = reverse('locations', args=[self.inst_name])

        self.accessories_url = reverse('accessories', args=[self.inst_name])
        self.pdate = '07/12/2023'
        self.rdate = '07/15/2023'
        self.accessories_url += f'?pickup_date={self.pdate}&return_date={self.rdate}'

        self.payment_url = reverse('payment', args=[self.inst_name])
        self.payment_url += f'?accessories={self.accessory_example.name}'

        self.overview_url = reverse('overview', args=[self.inst_name])
        self.confirmation_url = reverse('confirmation', args=[self.inst_name])


    

    def test_GET_home(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/index.html')

    def test_GET_aboutus(self):
        response = self.client.get(self.aboutus_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/aboutus.html')
    
    def test_GET_categories(self):
        response = self.client.get(self.categories_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/categories.html')

    def test_GET_login(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/registration/login.html')

    def test_GET_logout(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 200)

    def test_GET_signup(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/registration/signup.html')

    def test_GET_account(self):
        # before login
        response = self.client.get(self.account_url)
        self.assertEquals(response.status_code, 302)
        # after login
        self.client.login(username='test', password='test')
        response = self.client.get(self.account_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/account.html')
        self.client.logout()
    
    def test_GET_orders(self):
        # before login
        response = self.client.get(self.orders_url)
        self.assertEquals(response.status_code, 302)
        # after login
        self.client.login(username='test', password='test')
        response = self.client.get(self.orders_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/orders.html')
        self.client.logout()

    def test_GET_order_detail(self):
        # before login
        response = self.client.get(self.order_detail_url)
        self.assertEquals(response.status_code, 302)
        # after login
        self.client.login(username='test', password='test')
        response = self.client.get(self.order_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/order_detail.html')

    def test_GET_types(self):
        response = self.client.get(self.types_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/types.html')

    def test_GET_instruments(self):
        response = self.client.get(self.instruments_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/instruments.html')

    def test_GET_locations(self):
        # before login
        response = self.client.get(self.locations_url)
        self.assertEquals(response.status_code, 302)
        # after login
        self.client.login(username='test', password='test')
        response = self.client.get(self.locations_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/locations.html')

    def test_GET_dates(self):
        # before login
        response = self.client.get(self.dates_url)
        self.assertEquals(response.status_code, 302)
        # after login
        self.client.login(username='test', password='test')
        response = self.client.get(self.dates_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/dates.html')














    