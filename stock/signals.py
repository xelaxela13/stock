from django.db.models.signals import pre_save
from django.dispatch import receiver
from stock.models import ProductStock, OrderItem
from stock import model_choices as mch


@receiver(pre_save, sender=OrderItem)
def save_product_stock_amount(sender, instance, **kwargs):
    product_stock, created = ProductStock.objects.get_or_create(product=instance.product,
                                                                defaults={'amount': instance.amount})
    st()
    if not created:
        old_instance = sender.objects.filter(pk=instance.pk).first()
        if old_instance:
            if old_instance.order.type == mch.ORDER_OUT:
                if (old_instance.amount - instance.amount) < 0:
                    product_stock.amount -= abs(old_instance.amount - instance.amount)
                else:
                    product_stock.amount += (old_instance.amount - instance.amount)
            else:
                product_stock.amount = product_stock.amount - (old_instance.amount - instance.amount)
        else:
            product_stock.amount = product_stock.amount + instance.amount
        print(product_stock.amount)
        # product_stock.save()
