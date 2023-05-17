from django.db import models
from categories.models import Category

class Product_Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_types_images/')

    def __str__(self):
        return self.name