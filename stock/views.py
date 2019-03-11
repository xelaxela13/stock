from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView
from django.http import JsonResponse, Http404
from django.core.cache import cache
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
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
        return Http404


class ClearCache(RedirectView):
    url = reverse_lazy('admin:app_list', kwargs={'app_label': 'stock'})

    def get(self, request, *args, **kwargs):
        cache.clear()
        messages.add_message(request, messages.INFO, _('Cache cleaned'))
        if request.is_ajax():
            return JsonResponse({'message': _('Cache cleaned')})
        return super().get(request, *args, **kwargs)
