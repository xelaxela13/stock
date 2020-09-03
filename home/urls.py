from django.urls import path
from .views import Home, Energy, Solar

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('energy/', Energy.as_view(), name='energy'),
    path('solar/', Solar.as_view(), name='solar')
]
