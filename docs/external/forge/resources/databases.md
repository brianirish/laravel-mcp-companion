Source: https://laravel.com/forge/docs/resources/databases.md

# Databases

> Learn how to manage databases on your Laravel Forge server.

## Introduction

When provisioning a new Laravel Forge server that requires a database, you can choose between installing an [app server](https://forge.laravel.com/docs/servers/types.md#app-servers) or a dedicated [database server](https://forge.laravel.com/docs/servers/types.md#database-servers). The Forge dashboard provides comprehensive tools for managing databases, users, and permissions across your infrastructure.

## Creating servers with databases

During server creation, you can select from several supported database servers:

* MySQL (8.0, 8.4, 9.x)
* MariaDB (10.11, 11.4)
* PostgreSQL (13, 14, 15, 16, 17, 18)

Laravel Forge automatically handles the installation process, creating a default `forge` database and user with a securely generated password. Both the database and root passwords are displayed upon server creation for your reference.

> [!NOTE]
>
> MySQL 9.x is an [Innovation](https://dev.mysql.com/doc/refman/en/mysql-releases.html) release, designed for developers and teams who want access to the latest MySQL features and improvements. Innovation releases are production-ready, but each version is only supported until the next Innovation release ships.
>
> Laravel VPS servers are limited to the latest MySQL LTS and PostgreSQL versions only.

### Installing databases later

If you need to add database functionality to an existing server, you can install one through the server's "Databases" management tab. Once installed, you'll have full database management capabilities through the Laravel Forge interface.

> [!NOTE]
>
> If the server already has a database installed (MySQL, MariaDB, or PostgreSQL), Forge will not allow installing a different database type on the same server.

> [!WARNING]
>
> If you created a "Web Server", database installation is not supported. Web servers include only the essential software needed for PHP applications. For combined web and database functionality, provision an "App Server" instead.

## Managing database passwords

You can reset both `root` and `forge` database user passwords using the password reset feature in Laravel Forge's "Databases" management tab.

> [!WARNING]
>
> Never change `root` or `forge` database passwords manually or outside the Laravel Forge dashboard. This will break Forge's ability to connect to and manage your database.

## Connecting to databases via database clients

Database connections require SSH key authentication by default and don't support password-only access. When using GUI database clients to connect to your Laravel Forge database, you'll need SSH authentication with your **private SSH key**.

For example, when configuring [TablePlus](https://tableplus.com):


### Using database connection URLs

Some clients like TablePlus support connection URLs for simplified setup. Laravel Forge automatically generates these URLs for you, though you'll need to enter your password manually since it's not included in the URL for security purposes.

Forge also provides a convenient button to launch your preferred database client directly.

## Connecting to external databases

You can connect your application to a database hosted on another Laravel Forge server using [Laravel Forge's server network feature](https://forge.laravel.com/docs/resources/network.md#server-network).

When both servers [meet the network requirements](https://forge.laravel.com/docs/resources/network.md#server-network), follow these steps:

1. **Configure server network access:**

* Navigate to your application server's "Network" settings
* Enable the connection to your database server under the "Server Network" section

2. **Update application configuration:**

* Access your site's environment page
* Set the database host to the external server's private IP address
* Update database credentials to match the external database

## Managing databases

Laravel Forge provides advanced database management capabilities for MySQL, MariaDB, and PostgreSQL servers.

### Creating databases

Create new databases through the server's "Storage" > "Database" tab. You only need to provide the database name—the `forge` user automatically receives access permissions.

### Syncing databases

While we recommend managing databases through Laravel Forge for consistency, you can sync externally created databases using the "Sync Databases" button.

Note that system-reserved database names are excluded from syncing:

* `mysql`, `information_schema`, `performance_schema`, `sys`
* `postgres`, `template0`, `template1`

### Creating database users

The database panel allows you to create additional users by specifying the username, password, and accessible databases. You can also designate users as read-only, restricting them to select operations while preventing insert, update, or delete actions.

## Database upgrades

Laravel Forge doesn't provide automatic database server upgrades. If you need to upgrade your database software, you'll need to handle this process manually.
