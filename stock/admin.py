from django.contrib import admin
from django.utils.html import format_html
from stock.models import Product, ProductGroup, Order, Customer, CustomerGroup, OrderItem, OrderProxy, ProductStock
from stock import model_choices as mch
from stock.forms.admin_forms import OrderItemInlineForm
from stock.utils import float_format


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInlineForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('product', 'amount', 'available_for_sale', 'price', 'discount', 'discount_type')
        }),
        ('', {
            'fields': ('sum_amount', 'discount_price', 'sum_discount_price')
        }),
    )
    readonly_fields = ('discount_price', 'sum_amount', 'sum_discount_price', 'available_for_sale')

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'product' and self.parent_model.__name__ == 'OrderProxy':
            return db_field.remote_field.model.objects.filter(orderitem__order__type=mch.ORDER_IN).distinct()
        return super().get_field_queryset(db, db_field, request)

    def available_for_sale(self, obj=None):
        if obj:
            try:
                return ProductStock.objects.get(product=obj.product).amount
            except ProductStock.DoesNotExist:
                return '0'

    available_for_sale.short_description = 'Доступно'


class OrderBase(admin.ModelAdmin):
    list_filter = ('date', 'type')
    list_display = ('number', 'date', 'order_item_count', 'order_total', 'order_total_discount', 'colored_type')
    readonly_fields = ('order_total', 'order_total_discount', 'calculated_order_discount')
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

    class Media:
        js = ('/static//admin/js/stock/stock.js',)

    # form = OrderModelForm

    # def get_form(self, request, obj=None, change=False, **kwargs):
    # AdminForm = super().get_form(request, obj, change, **kwargs)
    #
    # class AdminFormWithRequest(AdminForm):
    #     def __new__(cls, *args, **kwargs):
    #         kwargs['request'] = request
    #         return AdminForm(*args, **kwargs)
    #
    # return AdminFormWithRequest

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['user'].initial = request.user
        return form

    def colored_type(self, obj=None, color='black'):
        if obj:
            return format_html('<span style="color: {}">{}</span>', color, mch.ORDER_TYPE[obj.type][1])

    colored_type.short_description = 'Тип накладной'

    def order_total_discount(self, obj=None):
        if obj:
            return format_html(
                '<span style="color: red;">{}</span>',
                float_format(sum(i.sum_discount_price() for i in obj.order_items.all()))
            ) or 0

    order_total_discount.short_description = 'Итого с учетом скидки'

    def calculated_order_discount(self, obj=None):
        if obj:
            return float_format(obj.order_total() - sum(i.sum_discount_price() for i in obj.order_items.all()))

    calculated_order_discount.short_description = 'Скидка по накладной'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'total_order_in', 'total_order_out', 'total_order_in_out')
    list_filter = ('group',)
    filter_horizontal = ('group',)


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    fields = ()


@admin.register(Order)
class OrderInAdmin(OrderBase):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=mch.ORDER_IN)

    def colored_type(self, obj=None, color='green'):
        return super().colored_type(obj, color)

    colored_type.short_description = 'Тип накладной'

    def save_model(self, request, obj, form, change):
        if obj:
            obj.user = request.user
            obj.type = mch.ORDER_IN
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['type'].initial = mch.ORDER_IN
        return form


@admin.register(OrderProxy)
class OrderOutAdmin(OrderBase):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=mch.ORDER_OUT)

    def colored_type(self, obj=None, color='blue'):
        return super().colored_type(obj, color)

    colored_type.short_description = 'Тип накладной'

    def save_model(self, request, obj, form, change):
        if obj:
            obj.type = mch.ORDER_OUT
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['type'].initial = mch.ORDER_OUT
        return form


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    filter_horizontal = ('customer_groups', )


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
