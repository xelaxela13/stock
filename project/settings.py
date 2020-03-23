"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from os import path

from celery.schedules import crontab
from decouple import config
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from whitenoise.storage import CompressedManifestStaticFilesStorage

# Build paths inside the project like this: path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))


def rel(*x):
    #  For example: rel('log', 'file.log') will to returned /var/www/stock/log/file.log
    return path.join(BASE_DIR, *x)


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool, default=False)


def log_level():
    return 'INFO' if DEBUG else 'INFO'


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')], default='127.0.0.1')

ADMINS = [('Alex', config('ADMIN_EMAIL', default='dummy@mail.com')), ]

# Application definition
INSTALLED_APPS = [
    # custom dashboard
    'jet.dashboard',  # comment this - migrate and then uncomment and migrate again
    'jet',
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
    'import_export',
    'pipeline',
    'sorl.thumbnail',
    'sortedm2m',
    # local apps
    'project',
    'accounts',
    'home',
    'fileupload',
    'stock',
    'multiplefileupload'
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
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'project.middleware.DefaultLanguageMiddleware',
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
                'project.context_processors.settings_to_template',  # my context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME', default='postgres'),
        'USER': config('DB_USER', default='postgres'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default=5432),
        'PASSWORD': config('DB_PASSWORD', default='test')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = reverse_lazy('panel')
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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

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

USE_L10N = True

USE_TZ = True

SHOW_LANG_SWITCH = False

DEFAULT_LANGUAGE = LANGUAGE_CODE

# Email send
# https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = config('GMAIL_PASSWORD', default='')
EMAIL_HOST_USER = config('GMAIL_USER', default='')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': config('MEMCACHED_HOST', default='127.0.0.1') + ':' + config('MEMCACHED_PORT', default='11211'),
        'TIMEOUT': 60 * 60,  # 1h,
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_FOLDER = 'static_content'
STATIC_URL = '/static/'
STATIC_ROOT = rel(STATIC_FOLDER, 'asset')
STATICFILES_DIRS = [
    rel('asset_dev')
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'pipeline.finders.FileSystemFinder',
    # 'pipeline.finders.AppDirectoriesFinder',
    # 'pipeline.finders.PipelineFinder',
)

# CompressedManifestStaticFilesStorage.manifest_strict = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE = {
    'COMPILERS': ('pipeline.compilers.es6.ES6Compiler', 'pipeline.compilers.sass.SASSCompiler', ),
    # 'BABEL_BINARY': '/usr/lib/node_modules/@babel',
    'BABEL_ARGUMENTS': '--presets /usr/lib/node_modules/@babel/preset-env',
    'JS_COMPRESSOR': None,  # 'pipeline.compressors.jsmin.JSMinCompressor',
    'STYLESHEETS': {
        'styles': {
            'source_filenames': (
                'styles.scss',
                'open-iconic/font/css/open-iconic-bootstrap.scss',
                'magic/magic.min.css'
            ),
            'output_filename': 'styles.css',
            'extra_context': {
                'media': 'screen',
            },
        },
        'admin': {
            'source_filenames': (
                'admin/css/custom.scss',
            ),
            'output_filename': 'admin/css/custom.css',
            'extra_context': {
                'media': 'screen',
            },
        },
    },
    'JAVASCRIPT': {
        'js': {
            'source_filenames': (
                'script.es6',
            ),
            'output_filename': 'script.js',
        }
    }
}

SITE_LOGO_FIRST = path.join(STATIC_URL, 'images/logo.png')
SITE_LOGO_SECOND = path.join(STATIC_URL, 'images/logo.png')

# Media files
# https://docs.djangoproject.com/en/2.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
MEDIA_URL = '/media/'
MEDIA_ROOT = rel(STATIC_FOLDER, 'media')

#  https://ipstack.com/
#  free geo api
IPSTACK_ACCESS_KEY = config('IPSTACK_ACCESS_KEY', default='')

# Activate Django-Heroku, uncomment it when deploy to Heroku
if not DEBUG and config('HEROKU', default=False):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    import django_heroku
    django_heroku.settings(locals())


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
            'filename': rel('log', '{}_django.log'.format(timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'secure_file_log': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_secure.log'.format(timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'request_file_log': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_request.log'.format(timezone.now().strftime('%Y%m%d'))),
            'formatter': 'verbose',
        },
        'celery_file_log': {
            'level': log_level(),
            'class': 'logging.FileHandler',
            'mode': 'w' if DEBUG else 'a',
            'filename': rel('log', '{}_celery.log'.format(timezone.now().strftime('%Y%m%d'))),
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
    PIPELINE['JS_COMPRESSOR'] = None
    from pprint import pprint
    from ipdb import set_trace

    __builtins__["pp"] = pprint
    __builtins__["st"] = set_trace
