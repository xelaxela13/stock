from django.db import models


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


class OrderItem(models.Model):
    DISCOUNT_TYPE = (
        ('amount', 'Грн.'),
        ('percent', '%'),
    )
    product = models.ManyToManyField(Product, verbose_name='Товары')
    price = models.FloatField(verbose_name='Цена')
    discount = models.PositiveSmallIntegerField(verbose_name='Скидка')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, default=DISCOUNT_TYPE[1][0])
    create_at = models.DateTimeField(auto_now_add=True)


class OrderIn(models.Model):
    number = models.CharField(blank=False, max_length=255, verbose_name='Номер накладной')

    date = models.DateField(verbose_name='Дата накладной')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '№{} ({}) {}'.format(self.number, self.product.count(), self.date)

    class Meta:
        verbose_name = 'Приходная накладная'
        verbose_name_plural = 'Приходные накладные'


class OrderOut(models.Model):
    number = models.CharField(blank=False, max_length=255, verbose_name='Номер накладной')
    product = models.ManyToManyField(Product, verbose_name='Товары')
    date = models.DateField(verbose_name='Дата накладной')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '№{} ({}) {}'.format(self.number, self.product.count(), self.date)

    class Meta:
        verbose_name = 'Расходная накладная'
        verbose_name_plural = 'Расходные накладные'
