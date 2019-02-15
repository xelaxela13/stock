from django.contrib import admin
from django.utils.html import format_html
from stock.models import Product, ProductGroup, Order, Customer, CustomerGroup, OrderItem
from stock.utils import float_format
import pdb


class OrderMixin(admin.ModelAdmin):

    def order_total_discount(self, obj=None):
        if obj:
            return format_html(
                '<span style="color: red;">{}</span>',
                sum(i.sum_discount_price() for i in obj.order_items.all())
            ) or 0

    order_total_discount.short_description = 'Итого с учетом скидки:'

    def calculated_order_discount(self, obj=None):
        if obj:
            return obj.order_total() - sum(i.sum_discount_price() for i in obj.order_items.all())

    calculated_order_discount.short_description = 'Скидка по накладной:'

    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #     field = super().formfield_for_dbfield(db_field, request, **kwargs)
    #     if db_field.name == 'user':
    #         field.initial = request.user
    #     return field

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


@admin.register(Order)
class OrderInAdmin(OrderMixin):
    list_filter = ('date', 'type')
    list_display = ('number', 'date', 'order_item_count', 'order_total', 'order_total_discount', 'type')
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

    def save_model(self, request, obj, form, change):
        if obj:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
