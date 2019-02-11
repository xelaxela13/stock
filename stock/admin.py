from django.contrib import admin
from stock.models import Product, ProductGroup, OrderIn, OrderOut, Customer, CustomerGroup, OrderItem


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


@admin.register(OrderIn)
class OrderInAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    list_display = ('date', 'number', 'order_item_count', 'order_total')
    readonly_fields = ('order_total', 'user', 'sum_total_order')
    search_fields = ('order_items__product__name', 'number')
    inlines = [
        OrderItemInline,
    ]
    fieldsets = (
        (None, {
            'fields': (('number', 'date', 'sum_total_order', 'order_total'), ('customer', 'user')),
        }),
        # ('', {
        #     'fields': (OrderItemInline,),
        # })
    )

    def sum_total_order(self, obj=None):
        return sum(i.sum_discount_price() for i in obj.order_items.all())

    sum_total_order.short_description = 'Всего:'

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            obj.user = request.user
        return super().get_prepopulated_fields(request, obj)


@admin.register(OrderOut)
class OrderOutAdmin(admin.ModelAdmin):
    list_filter = ('date',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
