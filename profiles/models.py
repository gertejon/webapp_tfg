from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    #image = models.ImageField(blank=True, null=True, upload_to="profile_images/")
    user=models.OneToOneField(User, on_delete=models.CASCADE)