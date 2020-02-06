from __future__ import absolute_import, unicode_literals

import subprocess
import logging
from os import path, listdir
from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import now

logger = logging.getLogger(__name__)


@shared_task
def clear_log_files():
    log_files = [path.join(settings.BASE_DIR, 'log', file) for file in listdir(path.join(settings.BASE_DIR, 'log'))
                 if path.splitext(file)[-1] == '.log']
    for file in log_files:
        if datetime.fromtimestamp(path.getmtime(file)).date() < now().date() - timedelta(days=30):
            try:
                subprocess.call(f'rm {file}', shell=True)
            except (FileNotFoundError, OSError, IOError) as err:
                logger.error(err)
