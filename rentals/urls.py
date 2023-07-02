from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('categories',views.categories,name="categories"),
    path('accounts/login/', LoginView.as_view(template_name='rentals/registration/login.html'),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('signup/', views.signup, name="signup"),
    path('account/', views.account, name='account'),
    path('orders/', views.orders, name='orders'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('types/<str:category_name>/', views.types, name='types'),
    path('instruments/<str:type_name>/', views.instruments, name='instruments'),
    path('dates/<str:instrument_name>/', views.dates, name='dates'),
    path('locations/<str:instrument_name>/', views.locations, name='locations'),
    path('accessories/<str:instrument_name>/', views.accessories, name='accessories'),
    path('payment/<str:instrument_name>/', views.payment, name='payment'),
    path('overview/<str:instrument_name>/', views.overview, name='overview'),
    path('confirmation/<str:instrument_name>/', views.confirmation, name='confirmation'),
]