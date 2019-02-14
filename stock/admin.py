from django.contrib import admin
from stock.models import Product, ProductGroup, Order, Customer, CustomerGroup, OrderItem, OrderType
from stock.utils import float_format


def order_total_discount(obj=None):
    if obj:
        return sum(i.sum_discount_price() for i in obj.order_items.all()) or 0


def calculated_order_discount(obj=None):
    if obj:
        return obj.order_total() - order_total_discount(obj)


class OrderMixin(admin.ModelAdmin):
    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            obj.user = request.user
        return super().get_prepopulated_fields(request, obj)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('product', 'amount', 'price', 'discount', 'discount_type')
        }),
        ('', {
            'fields': ('sum_amount', 'discount_price', 'sum_discount_price')
        }),
    )
    readonly_fields = ('discount_price', 'sum_amount', 'sum_discount_price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name',)
    list_filter = ('group',)


@admin.register(ProductGroup)
class ProductAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(Order)
class OrderInAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    list_display = ('date', 'number', 'order_item_count', 'order_total', 'order_total_discount')
    readonly_fields = ('order_total', 'user', 'order_total_discount', 'calculated_order_discount')
    search_fields = ('order_items__product__name', 'number')
    inlines = [
        OrderItemInline,
    ]
    fieldsets = (
        (None, {
            'fields': (('number', 'date', 'type'), ('customer', 'user')),
        }),
        ('', {
            'fields': (('order_total', 'calculated_order_discount', 'order_total_discount'),),
        })
    )

    def order_total_discount(self, obj=None):
        return float_format(order_total_discount(obj))

    order_total_discount.short_description = 'Итого с учетом скидки:'

    def calculated_order_discount(self, obj=None):
        return float_format(calculated_order_discount(obj))

    calculated_order_discount.short_description = 'Скидка по накладной:'

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            obj.user = request.user
        return super().get_prepopulated_fields(request, obj)


# @admin.register(Order)
# class OrderOutAdmin(admin.ModelAdmin):
#     list_filter = ('date',)
#     list_display = ('date', 'number', 'order_item_count', 'order_total', 'order_total_discount')
#     readonly_fields = ('order_total', 'order_total_discount', 'calculated_order_discount')
#     search_fields = ('order_items__product__name', 'number')
#     inlines = [
#         OrderItemInline,
#     ]
#     fieldsets = (
#         (None, {
#             'fields': (('number', 'date'), ('customer', 'user')),
#         }),
#         ('', {
#             'fields': (('order_total', 'calculated_order_discount', 'order_total_discount'),),
#         })
#     )
#
#     def order_total_discount(self, obj=None):
#         return float_format(order_total_discount(obj))
#
#     order_total_discount.short_description = 'Итого с учетом скидки:'
#
#     def calculated_order_discount(self, obj=None):
#         return float_format(calculated_order_discount(obj))
#
#     calculated_order_discount.short_description = 'Скидка по накладной:'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
