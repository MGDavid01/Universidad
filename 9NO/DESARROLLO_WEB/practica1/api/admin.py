from django.contrib import admin
from api.models import bank


@admin.register(bank)
class bankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'status', 'timestamp', 'update')
    list_filter = ('status',)
    search_fields = ('name', 'address')
