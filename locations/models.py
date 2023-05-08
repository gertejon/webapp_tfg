from django.db import models
from django.contrib.postgres.fields import ArrayField
from products.models import Product



class Stock(models.Model):
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.PositiveIntegerField(default=0)
    def __str__(self):
            return f"{self.location.name}_{self.product.name}"

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, through="Stock")

    def __str__(self):
            return self.name
    
