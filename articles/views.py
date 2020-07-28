from django.views.generic import DetailView, ListView

from articles.models import Article


class ArticleDetailView(DetailView):
    model = Article

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj and not request.session.get(f'viewed_{obj.pk}'):
            obj.view_count += 1
            obj.save(update_fields=('view_count', ))
            request.session.setdefault(f'viewed_{obj.pk}', True)
        return super().get(request, *args, **kwargs)


class ArticleListView(ListView):
    model = Article
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'half_page': str(self.paginate_by // 2)})
        return context
