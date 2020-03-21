from django.views.generic.base import TemplateView, ContextMixin
from multiplefileupload.models import ImagesGallery


class GalleryContextMixin(ContextMixin):
    galleries_names = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for gallery in self.galleries_names:
            images = ImagesGallery.get_images_from_gallery(gallery)
            if images:
                context[gallery] = images.values_list('file', flat=True)
        return context


class Home(TemplateView, GalleryContextMixin):
    template_name = 'home/home.html'
    galleries_names = {'certifications', 'boxes'}


class Solar(TemplateView, GalleryContextMixin):
    template_name = 'home/solar.html'
    galleries_names = {'solar'}


class Stabilizator(TemplateView, GalleryContextMixin):
    template_name = 'home/stabilizator.html'
    galleries_names = {'stabilizators'}
