from django.conf import settings


def settings_to_template(request):
    ctx = {
        'USE_I18N': settings.USE_I18N,
        'SHOW_LANG_SWITCH': settings.SHOW_LANG_SWITCH,
        'IS_HOME': is_home(request),
    }
    return ctx


def is_home(request):
    if request.path == '/' + request.LANGUAGE_CODE + '/' or request.path == '/':
        return True
    return False
