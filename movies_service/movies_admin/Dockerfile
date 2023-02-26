FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

WORKDIR /opt/app

COPY docker-entrypoint.sh docker-entrypoint.sh
COPY uwsgi/uwsgi.ini uwsgi.ini
COPY requirements.txt requirements.txt

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && apt update; apt install -y \
                        netcat \
     && pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r app && useradd -d /opt/app -r -g app app \
    && chown app:app -R /opt/app

EXPOSE 8000

USER app

ENTRYPOINT ["./docker-entrypoint.sh"]
