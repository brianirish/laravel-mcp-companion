Source: https://laravel.com/cloud/docs/deploy-guides/python.md

# Python deploy guide

Configure your Django, FastAPI, or Flask application for production on Laravel Cloud.

The [Python quickstart](https://laravel.com/cloud/docs/quickstart#python) walks you through your first deployment to Laravel Cloud. Once your application is up and running, this guide will help you get it ready for production. We'll cover choosing a production server, configuring your framework to run behind Cloud's proxy, and connecting to your databases, caches, and static files.

## Install dependencies

Cloud installs your application's dependencies automatically during the build. To decide how, it looks for the following files in order and uses the first one it finds:

| File | Installation |
| - | - |
| `uv.lock` | Export locked dependencies with uv, then install with pip |
| `poetry.lock` | Export locked dependencies with Poetry, then install with pip |
| `Pipfile.lock` | Export locked dependencies with Pipenv, then install with pip |
| `requirements.txt` | Install with pip, including referenced requirements files |
| `pyproject.toml` | Install the project with pip |

You should list your production server, such as Gunicorn or Uvicorn, among these dependencies. When Cloud exports dependencies from a lockfile, it leaves out your development groups, so it installs only what your application needs in production. Cloud installs packages into a shared Python user directory and adds their executables to your `PATH`, so you can call `gunicorn` or `uvicorn` directly from your start command.

## Run a production server

Django and Flask applications use the Web Server Gateway Interface (WSGI) by default, while FastAPI applications use the Asynchronous Server Gateway Interface (ASGI). Cloud discovers your application's entrypoint and pre-fills a start command using a compatible server from your dependencies. Cloud knows how to generate commands for each of the following servers:

| Server | Application interface |
| - | - |
| Gunicorn | WSGI |
| uWSGI or pyuwsgi | WSGI |
| Waitress | WSGI |
| Granian | WSGI or ASGI |
| Hypercorn | WSGI or ASGI |
| Uvicorn | ASGI |
| Daphne | ASGI |

Cloud also recognizes Django projects that are configured for ASGI, as well as application factories in Flask and FastAPI projects.

If none of these servers appear in your dependencies, Cloud falls back to Gunicorn for WSGI applications or Uvicorn for ASGI applications and pre-fills a `pip install --user` step in your build command to install it. That said, we recommend adding the server to your own dependencies so you stay in control of which version is installed.

Your start command should always use a production server. Django's `runserver`, `flask run`, and reload modes such as `fastapi dev` or `uvicorn --reload` are great for development, but don't use them to run your application in production.

## Bind to the right interface

Your server must listen on the port set by the `PORT` environment variable, which is `3000` by default. It must also accept IPv6 connections, since that is how Cloud's proxy and startup probes reach your application. The pre-filled Gunicorn command already takes care of this with `--bind [::]:$PORT`. If you are using Uvicorn, your start command should look like this:

```sh theme={null}
uvicorn main:app --host :: --port $PORT
```

Replace `main:app` with your own application's entrypoint. If a factory creates your application, be sure to keep the `--factory` flag.

> [!NOTE]
>
> Cloud may pre-fill Uvicorn's host as `--host ''`. When Uvicorn runs multiple workers, it uses an IPv4 socket for this value, which Cloud can't reach. Change it to `--host ::` so your application stays reachable as your worker count grows.

If you are using a different server, make sure your start command still listens on IPv6. Listening only on the loopback interface, or on a hardcoded port, will also prevent Cloud from reaching your application. If your application deploys successfully but still isn't reachable, take a look at the [deployment troubleshooting](https://laravel.com/cloud/docs/deployments#deployment-succeeds-but-serves-no-traffic) guide.

## Worker count

Cloud sets the `WEB_CONCURRENCY` environment variable based on the resources allocated to your app instance. Django and Flask applications receive `(2 × whole CPU cores) + 1` workers, capped so that each worker has a 150 MiB memory budget. FastAPI applications receive one worker per whole CPU core. Either way, your application always receives at least one worker.

Gunicorn and Uvicorn read `WEB_CONCURRENCY` automatically. If you are using another server, you will need to set its worker count option yourself. To change the number of workers, you may override `WEB_CONCURRENCY` in your [environment variables](https://laravel.com/cloud/docs/environments#environment-variables) or pass your server's worker count flag directly. If your application uses a lot of memory per worker, you may want to lower the count.

## Shut down gracefully

When an instance stops, whether during a deployment or while scaling down, Cloud sends a `SIGTERM` signal to your server. Gunicorn and Uvicorn both handle this signal gracefully by letting active requests finish before exiting.

You should keep your server's shutdown deadline shorter than your environment's **graceful shutdown timeout** so the rest of the instance has time to stop cleanly. Gunicorn's `--graceful-timeout` option defaults to 30 seconds, while Uvicorn provides a `--timeout-graceful-shutdown` option. If your requests need more time to complete, adjust both your server's deadline and your environment's timeout.

## Running behind the proxy

Cloud handles TLS for you before forwarding requests to your application, so your server only needs to speak plain HTTP. Cloud's proxy passes the original request scheme in the `X-Forwarded-Proto` header and the client's address chain in the `X-Forwarded-For` header. Before relying on these headers, you should configure your server's or framework's trusted proxy settings.

For Django, add the following to your `settings.py` file so that `request.is_secure()` correctly recognizes HTTPS requests that arrive through Cloud's proxy:

```python theme={null}
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

This setting also allows Django's HTTPS redirects and other secure request checks to use the original scheme. If you also run the same application behind a different proxy, be sure to review Django's [proxy setting documentation](https://docs.djangoproject.com/en/5.2/ref/settings/#secure-proxy-ssl-header) for its trust requirements.

## Django environment variables

New Django environments include a securely generated `SECRET_KEY`, which you are free to edit. If Cloud can discover your settings module in your repository, it will also set `DJANGO_SETTINGS_MODULE` for you.

In addition, Cloud provides `DEBUG=false`, along with comma-separated `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` values based on your environment's active domains. However, Django doesn't read these variables on its own, so you will need to add the following to your `settings.py` file:

```python theme={null}
import os

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
```

These values automatically include any [custom domains](https://laravel.com/cloud/docs/domains) you have added. Note that `ALLOWED_HOSTS` contains plain hostnames, while `CSRF_TRUSTED_ORIGINS` includes the `https://` scheme. You may override any of these variables in your [environment settings](https://laravel.com/cloud/docs/environments#environment-variables), but you should always keep debug mode disabled in production.

## Databases and caches

When you attach a database or cache from the infrastructure canvas, Cloud injects a `DATABASE_URL` (`postgresql://...` or `mysql://...`) or `REDIS_URL` (`rediss://...`) variable into your application's environment. You may read these values from `os.environ`.

Django doesn't read `DATABASE_URL` on its own, but the [dj-database-url](https://github.com/jazzband/dj-database-url) package makes it easy. Add it to your dependencies along with a driver for your database, such as [Psycopg](https://www.psycopg.org/psycopg3/) for Postgres, or [mysqlclient](https://github.com/PyMySQL/mysqlclient) or [PyMySQL](https://github.com/PyMySQL/PyMySQL) for MySQL, then configure your database like so:

```python theme={null}
import dj_database_url

DATABASES = {"default": dj_database_url.config()}
```

If you are using PyMySQL, add `PyMySQL[rsa]` to your dependencies, then register it as Django's MySQL driver at the top of your `settings.py` file:

```python theme={null}
import pymysql

pymysql.install_as_MySQLdb()
```

If you are using SQLAlchemy, you will need to tell it which driver you installed. For example, if you are using Psycopg 3 with a Postgres database:

```python theme={null}
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

url = make_url(os.environ["DATABASE_URL"])
engine = create_engine(url.set(drivername="postgresql+psycopg"))
```

If you are using PyMySQL with a MySQL database, use `mysql+pymysql` as the driver name instead.

For Redis, [redis-py](https://redis.readthedocs.io/en/stable/connections.html) will automatically configure TLS when it sees the `rediss://` scheme:

```python theme={null}
import os

import redis

cache = redis.from_url(os.environ["REDIS_URL"])
```

## Migrations

Database migrations belong in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Cloud runs these commands just before your new deployment goes live. If one of them fails, Cloud cancels the rollout.

New Django environments start with a migration command that is commented out. When you connect a database, Cloud enables it for you automatically, as long as you haven't customized your deploy commands. If you have, add the migration step yourself:

```sh theme={null}
python manage.py migrate
```

If you are using Alembic or Flask-Migrate, your deploy command will be `alembic upgrade head` or `flask db upgrade`, respectively.

## Static files

### Django

Cloud provides the following environment variables to Django applications, both during the build and while your application is running:

```ini theme={null}
STATIC_ROOT=/var/www/html/public/static
STATIC_URL=/static/
```

Since Django doesn't read these variables on its own, you should add the following to your `settings.py` file, using your project's existing `BASE_DIR`:

```python theme={null}
import os

STATIC_ROOT = os.environ.get("STATIC_ROOT", BASE_DIR / "staticfiles")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
```

The fallback values let you use the same settings on your local machine. Next, add the `collectstatic` command to your [build commands](https://laravel.com/cloud/docs/environments#build-commands) so Django collects your assets into `STATIC_ROOT`:

```sh theme={null}
python manage.py collectstatic --noinput
```

Cloud pre-fills this command for you when it detects a Django project with an uncommented `STATIC_ROOT` setting or a WhiteNoise dependency. If your build commands don't include it, add it alongside your existing commands. Running it during the build includes the collected files in your deployment.

With these defaults in place, Cloud's Nginx server serves your collected files under `/static/` on your application's domain, as long as you are using Django's local static file storage. For example, `css/app.css` will be available at `https://your-app.laravel.cloud/static/css/app.css`. There's no need for object storage with this setup.

If you would like to change either value, you may override these variables in your environment's [environment variables](https://laravel.com/cloud/docs/environments#environment-variables). Since Cloud serves files from `/var/www/html/public`, a different URL prefix needs to match the directory layout. For example, you could use `STATIC_ROOT=/var/www/html/public/assets` with `STATIC_URL=/assets/`.

To serve files from outside the public directory, you may configure [WhiteNoise](https://whitenoise.readthedocs.io/en/stable/django.html) to serve them through your application, or use a Django storage backend for [object storage](https://laravel.com/cloud/docs/resources/object-storage). Keep in mind that changing these environment variables won't reconfigure Nginx or upload your files to object storage for you.

### Flask and FastAPI

The environment variables described in the previous section only apply to Django. Flask serves its `static` directory at `/static` by default, while FastAPI requires you to mount a directory using [`StaticFiles`](https://fastapi.tiangolo.com/tutorial/static-files/). Neither framework needs any additional environment variables to serve static files.
