from typing import ClassVar
from django.contrib import admin
from . import models

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product','order','quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','transaction_id')

admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Categories)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.ShippingAddress)
