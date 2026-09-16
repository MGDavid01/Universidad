from django.contrib import admin
from api.models import bank, Account


@admin.register(bank)
class bankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'status', 'timestamp', 'update')
    list_filter = ('status',)
    search_fields = ('name', 'address')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bank', 'user', 'currency', 'balance', 'status')
    list_filter = ('status', 'currency', 'bank')
    search_fields = ('name',)
