Source: https://herd.laravel.com/docs/windows/getting-started/databases.md

# Databases

# Using databases with Herd

Herd ships with PHP extensions to support for all major databases, so if you're using MySQL, MariaDB, PostgreSQL, MongoDB, Redis or SQLite, we've got you covered. New Laravel applications use SQLite as default, and you don't need an additional database service to get up and running.

If you plan to use MySQL, PostgreSQL, MongoDB or Redis, you can either download the database service from its vendor, use a free tool like DBngin to manage the database service or upgrade to [Herd Pro](https://herd.laravel.com/checkout).

Herd Pro provides a convenient user interface to manage these services and you can get them up and running in seconds:

* **Databases:** [MySQL](https://herd.laravel.com/docs/windows/herd-pro-services/mysql.md), [MariaDB](https://herd.laravel.com/docs/windows/herd-pro-services/mariadb.md), [PostgreSQL](https://herd.laravel.com/docs/windows/herd-pro-services/postgresql.md) and [MongoDB](https://herd.laravel.com/docs/windows/herd-pro-services/mongodb.md)
* **Caches and queues:** [Redis](https://herd.laravel.com/docs/windows/herd-pro-services/redis.md)
* **Broadcasting:** [Laravel Reverb](https://herd.laravel.com/docs/windows/herd-pro-services/laravel-reverb.md)
* **Search:** [Meilisearch](https://herd.laravel.com/docs/windows/herd-pro-services/meilisearch.md)
* **Storage:** [MinIO](https://herd.laravel.com/docs/windows/herd-pro-services/minio.md) and [RustFS](https://herd.laravel.com/docs/windows/herd-pro-services/rustfs.md)

Once you installed a database service, you can switch a Laravel application to it with a single click in the Applications window. Herd updates the `.env` file for you and can create the database right away. Learn more in [Per-Site Services](https://herd.laravel.com/docs/windows/herd-pro-services/per-site-services.md).

When you create a new application in Herd, you can also select the database in the "Advanced" options of the new application window.
