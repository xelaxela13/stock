from django.urls import path
from .views import Home, Stabilizator, Projects

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('energy/', Stabilizator.as_view(), name='energy'),
    path('projects/', Projects.as_view(), name='projects')
]
