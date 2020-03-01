# encoding: utf-8
from django.urls import path
from .views import ImageDetailView

urlpatterns = [
    path('<slug:slug>', ImageDetailView.as_view(), name='image-slug'),
]
