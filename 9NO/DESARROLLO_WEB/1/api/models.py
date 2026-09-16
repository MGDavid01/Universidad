from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class bank(models.Model):
    name = models.CharField(max_length=32, default="Generic Bank Name")
    address = models.CharField(max_length=64, default="Generic Bank Address")
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


CURRENCY_CHOICES = (
    ("MXN", "Peso Mexicano"),
    ("USD", "Dólar Estadounidense"),
    ("EUR", "Euro")
)


class Account(models.Model):
    name = models.CharField(max_length=32, default="Generic Account Name")
    bank = models.ForeignKey(bank, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="MXN")
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
