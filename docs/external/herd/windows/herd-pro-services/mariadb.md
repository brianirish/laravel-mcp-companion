Source: https://herd.laravel.com/docs/windows/herd-pro-services/mariadb.md

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

Whether you set up a newer version of MariaDB or migrate from existing instances on your machine, the most comfortable way is to use a database client like [TablePlus](https://tableplus.com/windows) to export and import the database tables.

## Connecting via CLI

If you want to access your MariaDB instance via the command line or use [squashed migrations](https://laravel.com/docs/11.x/migrations#squashing-migrations), you need to add the `mariadb` binary to your path. The CLI tool it at the following location:

```bash theme={null}
%USERPROFILE%\.config\herd\bin\services\mariadb\<VERSION>\bin
```

This translates to something like this for your user account:

```bash theme={null}
C:\Users\sebastian\.config\herd\bin\services\mariadb\10.11\bin
```

You can add the path to the binary to your PATH by running the following commands in Powershell or CMD. Please make sure to restart your terminal session after changing the PATH variable so that the terminal loads the new value.

### Powershell

```ps1 theme={null}
setx PATH "$env:PATH;$env:USERPROFILE\.config\herd\bin\services\mariadb\10.11\bin"
```

### Command Prompt (CMD)

```bash theme={null}
setx PATH "%PATH%;%USERPROFILE%\.config\herd\bin\services\mariadb\8.0.36\bin"
```

After that, you can connect to the MariaDB server running on port 3306 via the following command:

```bash theme={null}
mariadb -u root -h 127.0.0.1 -P 3306 -p
```
