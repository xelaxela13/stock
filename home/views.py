from django.views.generic import TemplateView
from project.seometa import MyMetadataMixin
from django.utils.translation import gettext_lazy as _
from fileupload.models import Picture


class Index(MyMetadataMixin, TemplateView):
    title = _('Stock')
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pictures'] = Picture.objects.all()
        return context
