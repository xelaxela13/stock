from meta.views import Meta, MetadataMixin
from django.conf import settings


class MyMeta(Meta):

    def __init__(self, **kwargs):
        super(MyMeta, self).__init__(**kwargs)
        self.title = settings.META_BASE_TITLE + (' ' + str(self.title) if self.title is not None else '') \
            if getattr(settings, 'META_BASE_TITLE', False) else str(self.title)
        self.description = settings.META_BASE_DESCRIPTION + (' ' + str(self.description) if self.description is not None else '') \
            if getattr(settings, 'META_BASE_DESCRIPTION', False) else str(self.description)


class MyMetadataMixin(MetadataMixin):

    meta_class = MyMeta

