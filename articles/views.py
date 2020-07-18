from django.views.generic import DetailView, ListView

from articles.models import Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
    paginate_by = 6
