# Administration web interface and API for the Movies service

This project implements the following features of the Movies service:

- a web administration user interface to manage the content.
- API endpoints to interact with the service via REST.

## Setup

Before running the application, set the required environment in the `.env` file.

The following environment variables are expected to be set.

Django related configurations:

```conf

DJANGO_SECRET_KEY = 'SOME_DJANGO_SECRET_KEY'
ALLOWED_HOSTS = []
```

Django debug configurations:

```conf
DEBUG = True
INTERNAL_IPS = [] ; when using django-debug-toolbar
```

Postgres related configurations:

```conf
DB_NAME = 'database_name'
DB_USER = 'db_user'
DB_PASSWORD = 'db_passwort'
DB_HOST = 'database_host'
DB_PORT = 'database_port'
```

If you use Swagger, pass the url using that configuration:

```conf
SWAGGER_URL = 'swagger_url_to_pass_cors'
```

## Production environment

Use the provided `Dockerfile` to enroll the application in production.

The `docker-entrypoint.sh`script is the Entrypoint in the `Dockerfile`.
The script collects static files, performs migrations and runs the `uWSGI` as a web server.

The `uWSGI` configuration file is located in the `uwsgi\uwsgi.ini` path.
