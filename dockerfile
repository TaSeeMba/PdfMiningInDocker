FROM python:2.7
ADD requirements.txt /app/requirements.txt
ADD ./my_celery/ /app/
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT celery -A  my_celery worker --loglevel=info
#ENTRYPOINT ['celery','-A','my_celery', 'worker', '--loglevel=info']
