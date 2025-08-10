# Spatie - Installation Laravel

Source: https://spatie.be/docs/laravel-permission/v6/installation-laravel

Docs

Laravel-permission

Installation in Laravel

Installation in Laravel
=======================

### On this page

1. Laravel Version Compatibility
2. Installing
3. Default config file contents

##Laravel Version Compatibility
-------------------------------

See the "Prerequisites" documentation page for compatibility details.

##Installing
------------

1. Consult the **Prerequisites** page for important considerations regarding your **User** models!
2. This package **publishes a `config/permission.php` file**. If you already have a file by that name, you must rename or remove it.
3. You can **install the package via composer**:

   ```php
    composer require spatie/laravel-permission
   ```
4. The Service Provider will automatically be registered; however, if you wish to manually register it, you can manually add the `Spatie\Permission\PermissionServiceProvider::class` service provider to the array in `bootstrap/providers.php` (`config/app.php` in Laravel 10 or older).
5. **You should publish** the migration and the `config/permission.php` config file with:

   ```php
   php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"
   ```
6. BEFORE RUNNING MIGRATIONS

   * **If you are using UUIDs**, see the Advanced section of the docs on UUID steps, before you continue. It explains some changes you may want to make to the migrations and config file before continuing. It also mentions important considerations after extending this package's models for UUID capability.
   * **If you are going to use the TEAMS features** you must update your `config/permission.php` config file:

     + must set `'teams' => true,`
     + and (optional) you may set `team_foreign_key` name in the config file if you want to use a custom foreign key in your database for teams
   * **If you are using MySQL 8+**, look at the migration files for notes about MySQL 8+ to set/limit the index key length, and edit accordingly. If you get `ERROR: 1071 Specified key was too long` then you need to do this.
   * **If you are using CACHE\_STORE=database**, be sure to install Laravel's cache migration, else you will encounter cache errors.
7. **Clear your config cache**. This package requires access to the `permission` config settings in order to run migrations. If you've been caching configurations locally, clear your config cache with either of these commands:

   ```php
    php artisan optimize:clear
    # or
    php artisan config:clear
   ```
8. **Run the migrations**: After the config and migration have been published and configured, you can create the tables for this package by running:

   ```php
    php artisan migrate
   ```
9. **Add the necessary trait to your User model**:

   ```php
    // The User model requires this trait
    use HasRoles;
   ```
10. Consult the **Basic Usage** section of the docs to get started using the features of this package.

.

##Default config file contents
------------------------------

You can view the default config file contents at:

https://github.com/spatie/laravel-permission/blob/main/config/permission.php

Prerequisites

Installation in Lumen

Help us improve this page