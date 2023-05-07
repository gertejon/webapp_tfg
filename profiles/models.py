from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    username = models.CharField(max_length=150)
    
    REQUIRED_FIELDS = ['email', 'password1', 'password2']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username