from django.urls import path
from .views import ArticleDetailView, ArticleListView

urlpatterns = [
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('articles/', ArticleListView.as_view(), name='articles'),
]
