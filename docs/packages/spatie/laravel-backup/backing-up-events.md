# Spatie - Backing Up/Events

Source: https://spatie.be/docs/laravel-backup/v9/backing-up/events

Docs

Laravel-backup

Introduction

Laravel Backup
==============

A modern backup solution for Laravel apps
-----------------------------------------

Repository

Open Issues

17,676,447

5,851

Introduction
------------

### On this page

1. We have badges!

This Laravel package creates a backup of your application. The backup is a zipfile that contains all files in the directories you specify along with a dump of your database. The backup can be stored on any of the filesystems you have configured. The package can also notify you via Mail, Slack or any notification provider when something goes wrong with your backups.

Feeling paranoid about backups? Don't be! You can backup your application to multiple filesystems at once.

Once installed, making a backup of your files and databases is very easy. Just run this artisan command:

```php
php artisan backup:run

```
In addition to making the backup, the package can also clean up old backups, monitor the health of the backups, and show an overview of all backups.

If you need to backup multiple servers, take a look at our laravel-backup-server package.

##We have badges!
-----------------

![Latest Version](https://img.shields.io/github/release/spatie/laravel-backup.svg?style=flat-square)
![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)
![Build Status](https://img.shields.io/travis/spatie/laravel-backup/master.svg?style=flat-square)
![Quality Score](https://img.shields.io/scrutinizer/g/spatie/laravel-backup.svg?style=flat-square)
![Total Downloads](https://img.shields.io/packagist/dt/spatie/laravel-backup.svg?style=flat-square)

About us

Support us

Help us improve this page