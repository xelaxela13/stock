from django.views import View
from django.http import JsonResponse
from stock.models import ProductStock


class GetAvailableProduct(View):

    def get(self, request, *args, **kwargs):
        available = '-'
        if request.is_ajax():
            product_id = request.GET.get('product_id')
            if product_id and product_id.isdigit():
                try:
                    available = ProductStock.objects.get(product=product_id).amount
                except ProductStock.DoesNotExist:
                    pass
        return JsonResponse({'available': available})
