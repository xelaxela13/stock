from os import path

from celery.schedules import crontab
from decouple import config
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from whitenoise.storage import CompressedManifestStaticFilesStorage
from .utils import rel

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool, default=False)


def log_level():
    return 'INFO' if DEBUG else 'INFO'


ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       cast=lambda v: [s.strip() for s in v.split(',')],
                       default='127.0.0.1')

ADMINS = [('Alex', config('ADMIN_EMAIL', default='dummy@mail.com')), ]

# Application definition
INSTALLED_APPS = [
    # custom dashboard
    # 'jet.dashboard',
    # comment this - migrate and then uncomment and migrate again
    # 'jet',
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # external apps
    'rosetta',
    'django_celery_results',
    'django_celery_beat',
    'sorl.thumbnail',
    'sortedm2m',
    'tinymce',
    # local apps
    'project',
    'accounts',
    'home',
    'multiplefileupload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n
    # Simplified static file serving.
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [rel('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config('DB_NAME', default='sqlite3'),
    }
}

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    rel('locale'),
]
TIME_ZONE = 'Europe/Kiev'

USE_I18N = False

USE_L10N = False

USE_TZ = True

SHOW_LANG_SWITCH = False

DEFAULT_LANGUAGE = LANGUAGE_CODE

# Email send
# https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_PORT = config('EMAIL_PORT', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default='')
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default='')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': config('MEMCACHED_HOST',
                           default='127.0.0.1') + ':' + config(
            'MEMCACHED_PORT', default='11211'),
        'TIMEOUT': 60 * 60,  # 1h,
    }
}
# Static files (CSS, JavaScript, Images)
STATIC_FOLDER = 'static_content'
STATIC_URL = '/static/'
STATIC_ROOT = rel(STATIC_FOLDER, 'asset')
STATICFILES_DIRS = [
    rel('asset_dev')
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CompressedManifestStaticFilesStorage.manifest_strict = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = rel(STATIC_FOLDER, 'media')

# REDIS related settings
CELERY_REDIS_HOST = 'redis'
CELERY_REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + CELERY_REDIS_HOST + ':' + CELERY_REDIS_PORT + '/0'
CELERY_RESULT_BACKEND = 'django_celery_results.backends.database.DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {
    'Clear log files': {
        'task': 'project.tasks.clear_log_files',
        'schedule': crontab(hour=1, day_of_week=0),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'file_log': {
            'level': log_level(),
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_django.log'.format(
                timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'secure_file_log': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_secure.log'.format(
                timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'request_file_log': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_request.log'.format(
                timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'celery_file_log': {
            'level': log_level(),
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_celery.log'.format(
                timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': True,
        },
        'console': {
            'level': log_level(),
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_log', 'console'],
            'propagate': True,
            'level': log_level(),
        },
        'django.request': {
            'handler': ['mail_admins', 'request_file_log'],
            'propagate': True,
            'level': 'WARNING',
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
        },
        'django.security': {
            'handlers': ['mail_admins', 'secure_file_log'],
            'level': 'WARNING',
            'propagate': False,
        },
        'celery': {
            'handlers': ['celery_file_log', 'console'],
            'level': log_level(),
            'propagate': True
        },
    }
}

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }
    LOGGING = False
