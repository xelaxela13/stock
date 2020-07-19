from django.views.generic import DetailView, ListView

from articles.models import Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'half_page': str(self.paginate_by // 2)})
        return context

