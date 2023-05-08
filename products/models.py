from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='')
    product_type = models.CharField(max_length=100, default='')
    manufacturer = models.CharField(max_length=100, default='')
    quality = models.CharField(max_length=100, default='')
    price = models.FloatField()
    #stock = models.JSONField()
    specs = ArrayField(
        models.CharField(max_length=255),
        default=list,
    )
    accessories_id = ArrayField(
        models.IntegerField(),
        default=list,
    )
    instrument = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
            return self.name