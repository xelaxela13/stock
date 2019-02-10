from django.contrib import admin
from stock.models import Product, ProductGroup, OrderIn, OrderOut, Customer, CustomerGroup


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
    list_filter = ('date',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
