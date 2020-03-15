from django.urls import path
from .views import Home, Solar, Stabilizator

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('solar', Solar.as_view(), name='solar'),
    path('stabilizators', Stabilizator.as_view(), name='stabilizator'),
]
