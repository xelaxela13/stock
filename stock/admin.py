from django.contrib import admin
from stock.models import Product, ProductGroup, OrderIn, OrderOut, Customer, CustomerGroup, OrderItem
from stock.forms.admin_forms import OrderItemModelForm


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name',)
    list_filter = ('group',)


@admin.register(ProductGroup)
class ProductAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(OrderIn)
class OrderInAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    list_display = ('date', 'number', 'order_item_count', 'order_total')
    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderOut)
class OrderOutAdmin(admin.ModelAdmin):
    list_filter = ('date',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
