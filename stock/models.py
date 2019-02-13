from django.db import models
from django.db.models import Sum, F, Q, Case, When
from accounts.models import User


class ProductGroup(models.Model):
    name = models.CharField(blank=False, max_length=255, verbose_name='Название')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.product_set.count())

    class Meta:
        verbose_name = 'Группа товара'
        verbose_name_plural = 'Группы товаров'


class Product(models.Model):
    name = models.CharField(blank=False, max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    sku = models.CharField(blank=True, max_length=255, verbose_name='Артикул')
    group = models.ManyToManyField(ProductGroup, verbose_name='Гуппы товара')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.sku, self.name)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CustomerGroup(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Группа контрагентов')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.customer_set.count())

    class Meta:
        verbose_name = 'Группа контрагента'
        verbose_name_plural = 'Группы контрагентов'


class Customer(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Контрагент')
    customer_groups = models.ManyToManyField(CustomerGroup, verbose_name='Группы контрагентов')
    description = models.TextField(blank=True, verbose_name='Орисание')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class OrderIn(models.Model):
    number = models.CharField(blank=False, max_length=255, verbose_name='Номер накладной')
    date = models.DateField(verbose_name='Дата накладной')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_payed = models.BooleanField(default=False, verbose_name='Накладная полностью оплачена?')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '№{} ({}) {}'.format(self.number, self.order_items.count(), self.date)

    def order_total(self):
        return self.order_items.all().aggregate(
            total=Sum(F('price') * F('amount'), output_field=models.FloatField()))['total']

    order_total.short_description = 'Сумма накладной без скидки:'

    def order_item_count(self):
        return self.order_items.all().count()

    order_item_count.short_description = 'Товарных позиций в накладной'

    class Meta:
        verbose_name = 'Приходная накладная'
        verbose_name_plural = 'Приходные накладные'


class OrderOut(OrderIn):
    class Meta:
        verbose_name = 'Расходная накладная'
        verbose_name_plural = 'Расходные накладные'


class OrderItem(models.Model):
    DISCOUNT_TYPE = (
        ('amount', 'Грн.'),
        ('percent', '%'),
    )
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена')
    amount = models.PositiveIntegerField(verbose_name='Колличество')
    discount = models.PositiveIntegerField(verbose_name='Скидка', blank=True, default=0)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, default=DISCOUNT_TYPE[1][0],
                                     verbose_name='Тип скидки?')
    order = models.ForeignKey(OrderIn, verbose_name='Накладная', related_name="order_items", on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def discount_price(self):
        if self.price and self.discount > 0:
            if self.discount_type == self.DISCOUNT_TYPE[1][0]:
                return self.price * (1 - (self.discount / 100))
            return self.price - self.discount
        return self.price if self.price else 0

    discount_price.short_description = 'Цена со скидкой'

    def sum_amount(self):
        if self.price:
            return self.price * self.amount

    sum_amount.short_description = 'Сумма'

    def sum_discount_price(self):
        if self.price:
            return self.discount_price() * self.amount

    sum_discount_price.short_description = 'Сумма со скидкой'

    class Meta:
        verbose_name = 'Товарная позиция'
        verbose_name_plural = 'Товары'
