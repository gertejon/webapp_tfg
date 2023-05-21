from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("TRANSFER", "Transfer"),
        ("BIZUM", "Bizum"),
    )

    ORDER_STATUS = (
        ("PENDING_PAYMENT", "Pending_payment"),
        ("PAYMENT_RECEIVED", "Payment_received")
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(null=True)


    # dates
    pickup_date = models.DateField()
    return_date = models.DateField()
    
    
    payment_method = models.CharField(max_length=9, choices=PAYMENT_METHODS, default='Cash')
    order_status = models.CharField(max_length=17, choices=ORDER_STATUS, default='Pending_payment')



    # products
