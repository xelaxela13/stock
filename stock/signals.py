from django.db.models.signals import pre_save
from django.dispatch import receiver
from stock.models import ProductStock, OrderItem


@receiver(pre_save, sender=OrderItem)
def save_product_stock_amount(sender, instance, **kwargs):
    product_stock, created = ProductStock.objects.get_or_create(product=instance.product,
                                                                defaults={'amount': instance.amount})
    if not created:
        try:
            instance_last_amount = sender.objects.get(pk=instance.pk).amount
        except OrderItem.DoesNotExist:
            instance_last_amount = 0
        diff = instance_last_amount - instance.amount
        product_stock.amount = product_stock.amount - diff
        product_stock.save()
