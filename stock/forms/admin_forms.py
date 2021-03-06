from django.forms import ModelForm, ValidationError
from stock import model_choices as mch
from stock.models import ProductStock


# class OrderModelForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)

class OrderItemInlineForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['unit', 'price', 'discount']:
            self.fields[field].widget.attrs = {'style': 'width: 80px;'}

    def clean(self):
        cleaned_data = super().clean()

        if self.fields['order'].parent_instance.type == mch.ORDER_OUT:
            try:
                product_stock = ProductStock.objects.get(product=cleaned_data.get('product')).amount
                if self.instance.amount and cleaned_data['amount'] < self.instance.amount:
                    return cleaned_data
                if (self.instance.amount and self.instance.amount < cleaned_data['amount'] and (
                        cleaned_data['amount'] - self.instance.amount) > product_stock) or \
                        (not self.instance.amount and product_stock < cleaned_data['amount']):
                    raise ValidationError('На складе не достаточно товара, доступно: %(value)s',
                                          params={'value': product_stock})
            except ProductStock.DoesNotExist:
                raise ValidationError('Товара нет на складе')
        return cleaned_data
