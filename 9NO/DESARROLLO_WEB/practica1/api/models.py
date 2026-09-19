from django.db import models


class bank(models.Model):
    name = models.CharField(max_length=32, default="Generic Bank Name")
    address = models.CharField(max_length=64, default="Generic Bank Address")
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name
