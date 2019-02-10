from django.forms import ModelForm
from stock.models import OrderItem


class OrderItemModelForm(ModelForm):

    class Meta:
        model = OrderItem
        exclude = ()

