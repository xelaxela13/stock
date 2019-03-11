# encoding: utf-8
from django.urls import path
from stock.views import GetAvailableProduct, ClearCache

urlpatterns = [
    path('get-available-product/', GetAvailableProduct.as_view(), name='get-available-product'),
    path('clear-cache/', ClearCache.as_view(), name='clear-cache'),
]
