from django.contrib import admin
from .models import Product,Products

admin.site.register(Product)

class ProductsAdmin(admin.ModelAdmin):
    list_display=['id','name','pdetails','cat','brand','is_active']
    list_filter=['cat','is_active','brand']

admin.site.register(Products,ProductsAdmin)