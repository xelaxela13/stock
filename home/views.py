from django.views.generic.base import RedirectView


class RedirectToLogin(RedirectView):
    url = 'admin'
