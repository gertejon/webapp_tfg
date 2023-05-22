from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from locations.models import Location
from payment_methods.models import PaymentMethod

class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
            return f"{self.order.id}_{self.product.name}"

class Order(models.Model):
    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("TRANSFER", "Transfer"),
        ("BIZUM", "Bizum"),
    )

    ORDER_STATUS = (
        ("PENDING_PAYMENT", "Pending_payment"),
        ("PAYMENT_RECEIVED", "Payment_received"),
        ("CANCELLED", "Cancelled")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(null=True)

    # dates
    pickup_date = models.DateField()
    return_date = models.DateField()

    # locations
    pickup_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, related_name='order_pickup_location')
    return_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, related_name='order_return_location')
    
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=17, choices=ORDER_STATUS, default='Pending_payment')

    products = models.ManyToManyField(Product, through="OrderProduct")

    def __str__(self):
            return f"{self.user.username}_{self.id}"


