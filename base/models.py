from django.db import models

# Create your models here.

class PaymentTransaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
