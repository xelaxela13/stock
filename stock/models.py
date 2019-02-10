from django.db import models
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
        return '{} {} {}'.format(self.name, self.sku, self.group)

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

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class OrderItem(models.Model):
    DISCOUNT_TYPE = (
        ('amount', 'Грн.'),
        ('percent', '%'),
    )
    product = models.ManyToManyField(Product, verbose_name='Товар')
    price = models.FloatField(verbose_name='Цена')
    amount = models.PositiveIntegerField(verbose_name='Колличество')
    discount = models.PositiveIntegerField(verbose_name='Скидка')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, default=DISCOUNT_TYPE[1][0])
    create_at = models.DateTimeField(auto_now_add=True)


class OrderIn(models.Model):
    number = models.CharField(blank=False, max_length=255, verbose_name='Номер накладной')
    order_item = models.ManyToManyField(OrderItem, verbose_name='Товар')
    date = models.DateField(verbose_name='Дата накладной')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '№{} ({}) {}'.format(self.number, self.order_item.count(), self.date)

    class Meta:
        verbose_name = 'Приходная накладная'
        verbose_name_plural = 'Приходные накладные'


class OrderOut(OrderIn):

    class Meta:
        verbose_name = 'Расходная накладная'
        verbose_name_plural = 'Расходные накладные'
