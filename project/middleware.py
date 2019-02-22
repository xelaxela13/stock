from django.conf import settings
from django.utils import translation


class DefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(settings, 'DEFAULT_LANGUAGE', None) and settings.DEFAULT_LANGUAGE != translation.get_language():
            language = settings.DEFAULT_LANGUAGE
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
