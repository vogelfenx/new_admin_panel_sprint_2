# Administration web interface and API for the Movies service

This project implements the following features of the Movies service:

- a web administration user interface to manage the content.
- API endpoints to interact with the service via REST.

## Setup

Before running the application, set the required environment in the `movies_admin\.env` file.

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

To run the Movies service and all required components in a production environment, use the provided `docker-compose.yml` schema.

The production environment uses the following components in dedicated containers/services:

- `nginx` as a Nginx web server
- `web-app` as a Movies Service application using `uWSGI` as an application web server
- `postgres_db` as a PostgreSQL database

### Setup

Before running the `docker-compose.yml` file, set the required environment variables in the `.pg_env` file in the project root directory:

```conf
PG_USER = 'postgres_user'
PG_PASSWORD = 'postgres_password'
```

The Movies service application itself uses `movies_admin\Dockerfile` to run the application inside a container.

The `movies_admin\docker-entrypoint.sh` script is the Entrypoint in the `Dockerfile`.
The script collects static files, performs migrations and runs the `uWSGI` as a web server.

The `uWSGI` configuration file is located in the `uwsgi\uwsgi.ini` path.
