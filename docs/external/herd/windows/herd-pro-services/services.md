Source: https://herd.laravel.com/docs/windows/herd-pro-services/services.md

# Services

# Services

Herd Pro provides an interface that allows you to spin up complementary services to your site easily. These services can be databases, queues and broadcasting systems, but also search engines and storage providers that mimic your production environment.

You can combine these services with a [herd.yml](https://herd.laravel.com/docs/windows/sites/herd-yaml.md) in your project and store the site configuration for a project within the repository. This makes it super easy for others to spin up a development environment with all services in seconds.

## Installing Services

To install a service, go to the settings and select the services tab. In this tab, you can add new services and manage existing ones. When you add a service, Herd suggests a name and a free port, so you can run multiple versions of the same service side by side.


Select a service to see its configuration. You can change its name, port and whether Herd starts it automatically, and Herd saves your changes right away. The details also show the version, the data directory, the environment variables that your application needs to connect to the service, and its latest log output.

Every service has a binary directory where the applications files live and a data directory where the service stores the data and custom configuration. You can access both folders by right-clicking the service and selecting the destination.


## Managing Services

All services have a right click menu with actions for the individual service. These actions always include a force quit option and directory shortcuts but also provide individual actions that are tailored to the service, like copying the connection URL, cloning or updating the service.

If you want to use a service for a specific Laravel application, you can select it in the Applications window and Herd updates the `.env` file for you. Learn more in [Per-Site Services](https://herd.laravel.com/docs/windows/herd-pro-services/per-site-services.md).

## Managing Services via the CLI

You can manage all your services from the command line as well. This is especially useful for automation, scripting, and AI coding agents.

All service commands can be run without specifying a target – Herd will present interactive prompts to let you select the service type, version, or instance.

```powershell theme={null}
# List all installed services and their status
herd services:list

# See which service types are available
herd services:available

# See available versions for a service type
herd services:versions mysql

# Create a new service instance
herd services:create mysql

# Start and stop services
herd services:start mysql
herd services:stop mysql

# Clone an existing service (including data and config)
herd services:clone mysql

# Delete a service and all its data
herd services:delete mysql
```

For the full list of CLI commands, see the [Command Line](https://herd.laravel.com/docs/windows/advanced-usage/command-line.md#services-herd-pro) reference.

## Available Services

Herd Pro ships with the following services:

* [MySQL](https://herd.laravel.com/docs/windows/herd-pro-services/mysql.md)
* [MariaDB](https://herd.laravel.com/docs/windows/herd-pro-services/mariadb.md)
* [PostgreSQL](https://herd.laravel.com/docs/windows/herd-pro-services/postgresql.md)
* [MongoDB](https://herd.laravel.com/docs/windows/herd-pro-services/mongodb.md)
* [Redis](https://herd.laravel.com/docs/windows/herd-pro-services/redis.md)
* [Laravel Reverb](https://herd.laravel.com/docs/windows/herd-pro-services/laravel-reverb.md)
* [Meilisearch](https://herd.laravel.com/docs/windows/herd-pro-services/meilisearch.md)
* [MinIO](https://herd.laravel.com/docs/windows/herd-pro-services/minio.md)
* [RustFS](https://herd.laravel.com/docs/windows/herd-pro-services/rustfs.md)

You can see which versions Herd provides in the [version matrix](https://herd.laravel.com/docs/windows/herd-pro-services/service-versions.md).

## Deleting Services

You can delete services via right-clicking on them in the service manager and selecting delete. You can also delete a service via the CLI:

```powershell theme={null}
herd services:delete mysql
```
