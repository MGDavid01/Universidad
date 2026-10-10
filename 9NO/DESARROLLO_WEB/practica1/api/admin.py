# admin.py
from django.contrib import admin
from api import models

@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
        "status",
    ]

@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "bank",
        "user",
        "currency",
    ]
