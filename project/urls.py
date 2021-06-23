from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings


def use_i18n(urlpatterns_list):
    if not settings.USE_I18N and not settings.SHOW_LANG_SWITCH:
        return urlpatterns_list
    return i18n_patterns(*urlpatterns_list, prefix_default_language=False)


urlpatterns_untranslate = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('tinymce/', include('tinymce.urls')),
]
urlpatterns_translate = [
    path('', include('home.urls')),
]

urlpatterns = staticfiles_urlpatterns() + urlpatterns_untranslate + use_i18n(urlpatterns_translate)

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
