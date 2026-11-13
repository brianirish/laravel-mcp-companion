Source: https://herd.laravel.com/docs/macos/herd-pro-services/mariadb.md

# MariaDB

# Installing MariaDB via Herd Pro

MariaDB is a drop-in, fully compatible replacement for MySQL, and it's the default database engine for many Linux distributions. Many popular hosting platforms like [Laravel Forge](https://forge.laravel.com) support MariaDB databases out of the box, making the switch from local to production a breeze.


## Configuration

Herd provides a sensible default configuration for your MariaDB instance that works seamlessly for new setups, and you can change the port of the service to run it in parallel to existing installations on your machine.

Enabling the autostart option automatically starts a service instance when you start Herd.

If you want to modify the settings of the database, you can right click the service in the settings and open its data directory. In this data directory, there is a `my.cnf` that this specific MariaDB instance loads on startup.

Make sure to restart the service if you make changes to this configuration.

## Creating databases

While Laravel applications can create a database when running the migrations for the first time, it's a good practice to set up the database within the database instance yourself.

The service details on the right side of the selected service allow you to open TablePlus or AdminerEvo with a single click. Herd automatically detects TablePlus on your machine and provides a connection string to access the database instance. If you don't use TablePlus, it opens AdminerEvo where it inserts the correct login credentials for you.


## Connecting from your Laravel application

To connect your application to the server, you can use the credentials that are listed next to the running service in the settings, or you can use the ones below.

```env theme={null}
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3307
DB_DATABASE=laravel # set this to your project database
DB_USERNAME=root
DB_PASSWORD=
```

## Database service migrations

Whether you set up a newer version of MariaDB or migrate from existing instances on your machine, the most comfortable way is to use a database client like [TablePlus](https://tableplus.com/) to export and import the database tables.

## Connecting via CLI

Herd symlinks the `mariadb` CLI to your PATH, so you can connect to the database via the command line.
As Laravel Herd allows you to start multiple MariaDB servers, you should specify the port to connect to the correct instance.

For example, to connect to the MariaDB server running on port 3306, you can use the following command:

```bash theme={null}
mariadb -u root -h 127.0.0.1 -P 3306 -p
```
