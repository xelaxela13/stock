from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count() * 2 + 1


bind = '0.0.0.0:' + environ.get('PORT', '8002')
max_requests = 1000
worker_class = 'sync'
workers = max_workers()

env = {
    'DJANGO_SETTINGS_MODULE': 'project.settings'
}

reload = True
name = environ.get('COMPOSE_PROJECT_NAME', 'test')
