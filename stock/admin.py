from django.contrib import admin
from stock.models import Product, ProductGroup, OrderIn, OrderOut


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(ProductGroup)
class ProductAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(OrderIn)
class OrderInAdmin(admin.ModelAdmin):
    list_filter = ('date',)


@admin.register(OrderOut)
class OrderOutAdmin(admin.ModelAdmin):
    list_filter = ('date', )