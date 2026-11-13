# Spatie - Requirements

Source: https://spatie.be/docs/laravel-backup/v10/requirements

SPATIE

Laravel Backup
==============

spatie.be/open-source

Docs

Laravel-backup

Requirements

Requirements
============

This backup package requires **PHP 8.4**, with the ZIP module and **Laravel 12 or higher**. It's not compatible with Windows servers.

If you are using an older version of Laravel, take a look at one of the previous versions of this package.

The package needs free disk space where it can create backups. Ensure that you have **at least** as much free space as the total size of the files you want to backup.

Make sure `mysqldump` is installed on your system if you want to backup MySQL databases.

Make sure `pg_dump` is installed on your system if you want to backup PostgreSQL databases.

Make sure `mongodump` is installed on your system if you want to backup Mongo databases.

To send notifications to Slack you'll need to install `laravel/slack-notification-channel`:

```php
composer require laravel/slack-notification-channel
```
Support us

High level overview

Help us improve this page