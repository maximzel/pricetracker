from __future__ import absolute_import, unicode_literals
import os
import logging
from logging.handlers import SYSLOG_UDP_PORT
from django.utils import timezone
from celery import Celery
from celery.signals import after_setup_logger

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricetracker.settings')

app = Celery('pricetracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = logging.getLogger(__name__)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # FileHandler
    date = timezone.now().date()
    fh = logging.FileHandler('logs' + date.strftime("%Y-%m-%d") + '.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # SysLogHandler
    slh = logging.handlers.SysLogHandler(address=('localhost', SYSLOG_UDP_PORT))
    slh.setFormatter(formatter)
    logger.addHandler(slh)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
