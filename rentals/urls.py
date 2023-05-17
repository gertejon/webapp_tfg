from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('categories',views.categories,name="categories"),
    path('login', LoginView.as_view(template_name='rentals/registration/login.html'),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('signup/', views.signup, name="signup"),
    path('account/', views.account, name='account'),
    path('types/<str:category_name>/', views.types, name='types'),
    path('instruments/<str:type_name>/', views.instruments, name='instruments'),
]