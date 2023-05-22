from django.db import models


class PaymentMethod(models.Model):
    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("TRANSFER", "Transfer"),
        ("BIZUM", "Bizum"),
    )
    
    name = models.CharField(max_length=9, choices=PAYMENT_METHODS, default='Cash')
    instructions = models.CharField(max_length=200, unique=True)

    def __str__(self):
            return self.name