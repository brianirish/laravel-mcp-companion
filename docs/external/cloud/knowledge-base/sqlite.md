Source: https://laravel.com/cloud/docs/knowledge-base/sqlite.md

# SQLite Support

Learn why SQLite is not supported on Laravel Cloud, which databases we recommend, and how to migrate from SQLite to PostgreSQL or MySQL.

While SQLite is a popular option for development and lightweight applications, **it is not supported in Laravel Cloud production environments**. Laravel Cloud environments are [ephemeral](../environments#filesystem), so the filesystem resets across deployments, reboots, and infrastructure migrations. SQLite stores data in a single file on disk, often `*.sqlite`, `*.db`, or a path you configure in `DB_DATABASE`. You lose any changes to that file whenever your application redeploys, sleeps and wakes, or moves between hosts.

> [!TIP]
>
> We recommend [**Laravel Serverless Postgres**](https://laravel.com/cloud/docs/resources/databases/postgres) or [**Laravel MySQL**](https://laravel.com/cloud/docs/resources/databases/laravel-mysql). Both keep your data across deployments, and Serverless Postgres and Laravel MySQL Flex sizes scale to zero when idle.

## Migrating from SQLite to PostgreSQL or MySQL

When you deploy to Laravel Cloud, you need a hosted database such as [Laravel Serverless Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) (Neon) or [Laravel MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql). If your app currently uses SQLite, migrate your schema and data using one of the following paths.

### SQLite to PostgreSQL

You can move your data to Laravel Serverless Postgres with [pgloader](https://pgloader.io/) or with `psql`. pgloader converts and loads your SQLite file in a single step, so it is the simpler option. Before you start, check pgloader's release notes to confirm it supports your database's Postgres version. If it doesn't, [dump and import with psql](#with-psql) instead.

Both options need your database's connection details. To find them, navigate to your organization's **Resources** page, click the **...** icon next to your database, and click **View credentials**. Serverless Postgres requires SSL, so every connection string must include `sslmode=require`.

#### With pgloader

**1. Load your SQLite database**

Run pgloader with the absolute path to your SQLite file and your Serverless Postgres connection string. pgloader creates the tables, converts SQLite's column types to Postgres types, and copies your data:

```bash theme={null}
pgloader sqlite:///absolute/path/to/database.sqlite "postgresql://user:password@ep-example-123456.us-east-2.pg.laravel.cloud/dbname?sslmode=require"
```

See [pgloader's SQLite reference](https://pgloader.readthedocs.io/en/latest/ref/sqlite.html) for additional options.

**2. Verify the migration**

Confirm that row counts match across all tables, that foreign keys and unique constraints behave as expected, and that your application runs against the new database without query errors.

#### With psql

**1. Export your SQLite data**

From your project directory, dump the database to SQL:

```bash theme={null}
sqlite3 database.sqlite .dump > dump.sql
```

**2. Clean up the dump**

PostgreSQL uses different syntax than SQLite. Edit `dump.sql` as needed:

* Remove or replace `BEGIN TRANSACTION` and `COMMIT`.
* Replace `INTEGER PRIMARY KEY AUTOINCREMENT` with `SERIAL PRIMARY KEY` or `BIGSERIAL PRIMARY KEY`.
* Replace `BLOB` with `BYTEA`.
* Remove all `PRAGMA` statements.
* Replace `TEXT` columns that store dates with `TIMESTAMP` if you want PostgreSQL-native date handling.

**3. Import the dump**

```bash theme={null}
psql "postgresql://user:password@ep-example-123456.us-east-2.pg.laravel.cloud/dbname?sslmode=require" < dump.sql
```

**4. Verify the migration**

Confirm that row counts match across all tables, that foreign keys and unique constraints behave as expected, and that your application runs against the new database without query errors.

### SQLite to MySQL 8.4

**1. Export your SQLite data**

```bash theme={null}
sqlite3 your_database.db .dump > dump.sql
```

**2. Clean up the dump**

Edit `dump.sql` for MySQL compatibility:

* Translate SQLite's `INTEGER PRIMARY KEY AUTOINCREMENT` pattern into a MySQL integer primary key column that uses `AUTO_INCREMENT`.
* Replace `TEXT` with `LONGTEXT` or `VARCHAR(n)` as appropriate for your columns.
* Remove all `PRAGMA` statements.
* Change double-quoted identifiers (for example, `"column"`) to backticks (for example, `` `column` ``).
* Replace `BEGIN TRANSACTION` with `START TRANSACTION`.
* Keep `BLOB` as `BLOB`.
* SQLite stores booleans as `0` and `1` integers, and MySQL's `TINYINT(1)` behaves the same way.
* `utf8mb4` is the default character set for new databases on MySQL 8.4 in most configurations, so you often do not need to set it explicitly.

**3. Import into MySQL**

```bash theme={null}
mysql -u user -p target_db < dump.sql
```

**4. Verify the migration**

Confirm that row counts match across all tables, that foreign keys and unique constraints behave as expected, and that your application runs against the new database without query errors.

### Before you go live

* Run through the migration on a **staging** environment first.
* For MySQL, the [`sqlite3-to-mysql`](https://pypi.org/project/sqlite3-to-mysql/) package (`pip install sqlite3-to-mysql`) can automate dialect conversion instead of editing `dump.sql` by hand.
* SQLite is permissive about types. PostgreSQL and MySQL are stricter, so invalid data may surface only after you migrate.
* Foreign keys are not always enforced in SQLite (for example, when `PRAGMA foreign_keys` is off). Your target database enforces them, so the migration can reveal existing data integrity problems.
