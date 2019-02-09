# encoding: utf-8
from django.urls import path
from fileupload.views import (PictureCreateView, PictureDeleteView, PictureListView)

urlpatterns = [
    path('new/', PictureCreateView.as_view(), name='upload-new'),
    path('delete/<int:pk>', PictureDeleteView.as_view(), name='upload-delete'),
    path('view/', PictureListView.as_view(), name='upload-view'),
]
