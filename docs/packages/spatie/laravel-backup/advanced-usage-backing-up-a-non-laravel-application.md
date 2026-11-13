# Spatie - Advanced Usage/Backing Up A Non Laravel Application

Source: https://spatie.be/docs/laravel-backup/v10/advanced-usage/backing-up-a-non-laravel-application

SPATIE

Laravel Backup
==============

spatie.be/open-source

Docs

Laravel-backup

Advanced-usage

Backing up a non-laravel application

Backing up a non-laravel application
====================================

This package is tailor-made for use inside Laravel applications. But with a little bit of good will you can use it to backup non-Laravel applications as well.

To do so install Laravel on the same server where your non-Laravel application runs. In the Laravel app you'll have to install this package using the installation instructions. In the `app/config/backup.php`configuration file specify the paths of the non-laravel application you wish to backup in the `backup.source.files.include` key.

Do not forget to configure the database as well. In `app/config/databases.php` put the credentials of the database used by the non-Laravel application.

When running `php artisan backup:run` on the command line, the application will be backed up.

Adding extra files to a backup

Binary database dumps with PostgreSQL

Help us improve this page