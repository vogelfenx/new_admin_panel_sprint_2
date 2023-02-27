FROM python:3.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

WORKDIR /opt/app

RUN mkdir -p /opt/app/static/ \
    && mkdir -p /opt/app/media/ \
    && apt update; apt install -y \
       netcat \
       gettext \
    && pip install --no-cache-dir --upgrade pip

RUN groupadd -r app && useradd -d /opt/app -r -g app app \
    && chown app:app -R /opt/app



### target: development ###
FROM base as development

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install --no-cache-dir pipenv \
    && pipenv install --dev --system

USER app
COPY . .
ENTRYPOINT ["./docker-entrypoint-dev.sh"]


### target: production ###
FROM base as production

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


USER app

COPY uwsgi/uwsgi.ini uwsgi.ini

COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]
