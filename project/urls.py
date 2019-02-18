"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings


def use_i18n(urlpatterns_list):
    if not settings.USE_I18N:
        return urlpatterns_list
    elif not settings.SHOW_LANG_SWITCH:
        return urlpatterns_list
    return i18n_patterns(*urlpatterns_list)


urlpatterns_untranslate = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('admin_tools/', include('admin_tools.urls')),
]
urlpatterns_translate = [
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('upload/', include('fileupload.urls')),
    path('stock/', include('stock.urls'))
]

urlpatterns = staticfiles_urlpatterns() + urlpatterns_untranslate + use_i18n(urlpatterns_translate)

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
