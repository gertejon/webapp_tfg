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
]