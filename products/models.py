from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.JSONField()
    specs = models.ArrayField(
        models.CharField(max_length=255),
        default=list,
    )
    accessories_id = models.ArrayField(
        models.IntegerField(),
        default=list,
    )
    instrument = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
            return self.name