from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    username = models.CharField(max_length=150)
    
    REQUIRED_FIELDS = ['username', 'email', 'password1', 'password2']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.user.username