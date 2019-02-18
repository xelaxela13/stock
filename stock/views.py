from django.views import View
from django.http import JsonResponse, Http404
from stock.models import ProductStock


class GetAvailableProduct(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            product_id = request.GET.get('product_id')
            if product_id and product_id.isdigit():
                available = ProductStock.objects.get(product=product_id).amount
                return JsonResponse({'available': available})
        return JsonResponse({'available': '-'})
