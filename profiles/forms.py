from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    image = forms.ImageField(help_text='Profile Picture')


    class Meta:
        model = User
        fields = ('username', 'image', 'email', 'password1', 'password2',)