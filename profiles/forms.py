from django import forms
from django.contrib.auth.forms import UserCreationForm
from profiles.models import Profile

class SignUpForm(UserCreationForm):
    image = forms.ImageField(help_text='Profile Picture')


    # class Meta:
    #     model = CustomUser
    #     fields = ('username', 'image', 'email', 'password1', 'password2',)