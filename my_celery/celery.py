from __future__ import absolute_import
from celery import Celery

BROKER_URL = 'amqp://admin:mypass@10.211.55.12:5672'
CELERY_RESULT_DBURI = 'postgresql://user:password@localhost/mydatabase'

app = Celery('my_celery',broker=BROKER_URL,backend=CELERY_RESULT_DBURI,include=['my_celery.task'])

