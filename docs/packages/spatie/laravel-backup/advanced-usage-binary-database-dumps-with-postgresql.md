# Spatie - Advanced Usage/Binary Database Dumps With Postgresql

Source: https://spatie.be/docs/laravel-backup/v10/advanced-usage/binary-database-dumps-with-postgresql

SPATIE

Laravel Backup
==============

spatie.be/open-source

Docs

Laravel-backup

Advanced-usage

Binary database dumps with PostgreSQL

Binary database dumps with PostgreSQL
=====================================

PostgreSQL has the ability to produce binary database dumps via the `pg_dump` command, which produce smaller files than the SQL format and are faster to restore. See the full list of `pg_dump` flags.

To take advantage of this, you can set the extra flags for `pg_dump` on the database connection(s) in `app/config/database.php`.

```php
//config/database.php
'connections' => [
	'pgsql' => [
		'driver'    => 'pgsql'
		...,
		'dump' => [
		    ...,
		    'add_extra_option' => '--format=c', // and any other pg_dump flags
		]
	],
```
Additionally, you can change the file extension of the database dump file to signify that it is not a text SQL file.

```php
//config/backup.php
'backup' => [
    ...,
    'database_dump_file_extension' => 'backup', // produces a FILENAME.backup database dump
  ],
```
Backing up a non-laravel application

Encrypt backup archives

Help us improve this page