from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path, reverse_lazy
from django import forms
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin
from stock.models import Product, ProductGroup, Order, Customer, CustomerGroup, OrderItem, OrderProxy, ProductStock
from stock import model_choices as mch
from stock.forms.admin_forms import OrderItemInlineForm
from stock.utils import float_format
from stock.resources import ProductResources
from functools import update_wrapper
from random import randint


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInlineForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('product', 'amount', 'available_for_sale', 'unit', 'price', 'discount', 'discount_type')
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
    readonly_fields = ('order_total', 'order_total_discount', 'calculated_order_discount', 'add_many_items')
    search_fields = ('order_items__product__name', 'number')
    inlines = [
        OrderItemInline
    ]
    fieldsets = (
        (None, {
            'fields': (('number', 'date', 'type'), ('customer', 'user'),
                       ('order_total', 'calculated_order_discount', 'order_total_discount')),
        }),
        ('Дополнительно', {
            'fields': (('add_many_items', ), ),
        })
    )

    class Media:
        js = ('/static/admin/js/stock/stock.js',)

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

    def add_many_items(self, obj=None):
        button = f'<a href="add_many_items/?_to_field=1&_popup=1" target="_blank" class="button"> \
                    Добавить несколько товаров</a>'
        return mark_safe(button)

    add_many_items.allow_tags = True

    @staticmethod
    def get_order_url(obj):
        info = obj._meta.app_label, obj._meta.model_name
        return reverse_lazy('admin:%s_%s_change' % info, args=[obj.id])

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            path('<path:object_id>/add_many_items/', wrap(self.add_many_items_view),
                 name='%s_%s_add_many_items' % info),
        ]

        return urlpatterns + urls

    def add_many_items_view(self, request, object_id, **kwargs):
        template = 'admin/stock/order/add_many_items_view/add_many_items.html'
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            key='',
        )
        if request.POST:
            return redirect('..')
        return TemplateResponse(request, template, context)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('sku', 'name', 'total_order_in', 'total_order_out', 'total_in_stock')
    list_filter = ('group',)
    filter_horizontal = ('group',)
    list_select_related = True
    readonly_fields = ('total_in_stock',)
    resource_class = ProductResources

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.price = []
        self.total = []
        self.create_order = None
        self.customer = None
        self.order_number = None
        self.user = None

    def get_import_form(self):
        form = super().get_import_form()
        form.base_fields['create_order'] = forms.BooleanField(required=False, help_text='Создать приходную накладную?')
        form.base_fields['number'] = forms.CharField(max_length=255, required=False)
        return form

    def process_dataset(self, dataset, confirm_form, request, *args, **kwargs):
        # example of dataset
        # {'_data': [['МКН 300х300х200 ір54 з монтажною панеллю',
        #             'Компактна розподільча шафа  MK10 - 300х300х200 IP 54 з монтажною панеллю', '5'],
        #            ['МКН 400х300х200 ір54 з монтажною панеллю',
        #             'Компактна розподільча шафа  MK10 - 400х300х200 IP 54 з монтажною панеллю', '5']],
        #  '_Dataset__headers': ['name', 'description', 'total_in_stock'], '_separators': [], '_formatters': [],
        #  'title': None}
        if dataset and confirm_form.is_valid() and self.create_order:
            total = []
            price = []
            headers = dataset._Dataset__headers
            data = dataset._data
            if data and headers:
                if 'total' in headers:
                    total_in_stock_index = headers.index('total')
                    [total.append(d[total_in_stock_index]) for d in data]
                if 'price' in headers:
                    price_index = headers.index('price')
                    [price.append(d[price_index]) for d in data]
                self.total = total
                self.price = price
        return super().process_dataset(dataset, confirm_form, request, *args, **kwargs)

    def process_result(self, result, request):
        if result and self.create_order:
            order_data = {
                'number': self.order_number or randint(10000, 99999),
                'date': timezone.now(),
                'customer_id': Customer.objects.get_or_create(name='Import')[0].id,
                'user': self.user,
                'type': mch.ORDER_IN,
                'create_at': timezone.now()
            }
            order = Order.objects.create(**order_data)
            if order:
                for i, row in enumerate(result.rows):
                    order_item_data = {
                        'product_id': row.object_id,
                        'price': float(self.price[i]) if self.price and self.price[i].isdigit() else 0,
                        'amount': int(self.total[i]) if self.total and self.total[i].isdigit() else 0,
                        'order_id': order.id,
                        'create_at': timezone.now()
                    }
                    OrderItem.objects.create(**order_item_data)
                url = OrderBase.get_order_url(order)
                mess = f'Накладная № <a href="{url}">{order.number}</a> успешно созданна.'
                messages.add_message(request, messages.INFO, mark_safe(mess))
        return super().process_result(result, request)

    def import_action(self, request, *args, **kwargs):
        if request.POST:
            self.create_order = request.POST.get('create_order')
            self.order_number = request.POST.get('number')
            self.user = request.user
        return super().import_action(request, *args, **kwargs)


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
    filter_horizontal = ('customer_groups',)


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    fields = ()
