from django.contrib.auth.views import LoginView


class RedirectToLogin(LoginView):
    template_name = 'accounts/registration/login.html'
