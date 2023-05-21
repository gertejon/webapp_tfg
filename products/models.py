from django.db import models
from django.contrib.postgres.fields import ArrayField
from categories.models import Category
from product_types.models import Product_Type
from brands.models import Brand


class Product(models.Model):
    QUALITY_CHOICES = (
        ("HIGH-END", "High-end"),
        ("MID-RANGE", "Mid-range"),
        ("BUDGET", "Affordable"),
    )

    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    product_type = models.ForeignKey(Product_Type, null=True, blank=True, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.CASCADE)
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='Mid-range')
    price = models.FloatField(null=True)
    specs = ArrayField(
        models.CharField(max_length=255),
        default=list,
    )
    accessories = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_accessory = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True, upload_to='product_images/')

    def __str__(self):
        return self.name