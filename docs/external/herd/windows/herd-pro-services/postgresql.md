Source: https://herd.laravel.com/docs/windows/herd-pro-services/postgresql.md

# PostgreSQL

# Installing PostgreSQL via Herd Pro

PostgreSQL is a powerful, open-source object-relational database system that is known for its reliability and robustness.
Laravel Herd Pro extends PostgreSQL by providing a number of popular extensions:

* [PostGIS](https://postgis.net/) - adds support for geographic objects to the PostgreSQL database, making it easy to store and query spatial data.
* [pgrouting](https://pgrouting.org/) - adds routing functionality to PostgreSQL, allowing you to calculate the shortest path between two points.
* [pgvector](https://github.com/pgvector/pgvector) - a vector similarity search extension for PostgreSQL, which allows you to search for (among other things) OpenAI embeddings in your database.


## Configuration

Herd uses a common default configuration for your PostgreSQL instance that works seamlessly for most setups, and you can change the port of the service to run it in parallel to existing installations on your machine.

Enabling the autostart option automatically starts a service instance when you start Herd.

If you want to modify the settings of the database, you can right-click the service in the settings and open its data directory. In this data directory, there is a `postgresql.conf` that this specific PostgreSQL instance loads on startup.

Make sure to restart the service if you make changes to this configuration.

## Creating databases

Before you can connect your application to the database service, you need an actual database within the instance of the service. Herd provides a convenient way to open TablePlus or AdminerEvo in case that you don't use TablePlus.

When clicking on the related button for these tools on the right side of the service details, Herd opens a connection to the database in your preferred tool and automatically logs you in.


## Connecting from your Laravel application

To connect it within your application, you can use the credentials that are listed next to the running service in the settings, or you can use the ones below.

```env theme={null}
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=laravel # set this to your project database
DB_USERNAME=root
DB_PASSWORD=
```

## Connecting via CLI

If you want to access your PostgreSQL instance via the command line or use [squashed migrations](https://laravel.com/docs/11.x/migrations#squashing-migrations), you need to add the `psql` binary to your path. The CLI tool it at the following location:

```bash theme={null}
%USERPROFILE%\.config\herd\bin\services\postgresql\<VERSION>\bin
```

This translates to something like this for your user account (replace `sebastian` with your own username and `16` with the version of PostgreSQL you are using):

```bash theme={null}
C:\Users\sebastian\.config\herd\bin\services\postgresql\16\bin
```

You can add the path to the binary to your PATH by running the following commands in Powershell or CMD. Please make sure to restart your terminal session after changing the PATH variable so that the terminal loads the new value.

### Powershell

```ps1 theme={null}
setx PATH "$env:PATH;$env:USERPROFILE\.config\herd\bin\services\postgresql\16\bin" 
```

### Command Prompt (CMD)

```bash theme={null}
setx PATH "%PATH%;%USERPROFILE%\.config\herd\bin\services\postgresql\16\bin"

```

After that, you can connect to the PostgreSQL server running on port 5432 via the following command:

```bash theme={null}
psql -U postgres -h 127.0.0.1 -p 5432
```

## Database service migrations

Whether you set up a newer version of PostgreSQL or migrate from existing instances on your machine, the most comfortable way is to use a database client like [TablePlus](https://tableplus.com/) to export and import the database tables.
