from django.urls import path
from .views import RedirectToLogin

urlpatterns = [
    path('', RedirectToLogin.as_view(), name='home'),
]
