from django.views.generic.base import TemplateView
from multiplefileupload.models import ImagesGallery


class Home(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery = ImagesGallery.objects.filter(name='boxes').last()
        context['images'] = gallery.image_set.filter(show=True).values_list('file', flat=True) if gallery else []
        return context
