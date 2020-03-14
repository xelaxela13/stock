from django.views.generic.base import TemplateView
from multiplefileupload.models import ImagesGallery


class Home(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for gallery in ('boxes', 'certifications', 'stabilizators'):
            images = ImagesGallery.get_images_from_gallery(gallery)
            context[gallery] = images.values_list('file', flat=True) if images else []
        return context
