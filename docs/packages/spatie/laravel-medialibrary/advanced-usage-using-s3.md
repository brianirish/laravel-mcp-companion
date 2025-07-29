# Spatie - Advanced Usage/Using S3

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/using-s3

Docs

Laravel-medialibrary

Introduction

Laravel Media Library
=====================

Associate files with Eloquent models
------------------------------------

A free package that associates files to Eloquent models, generates thumbnails and responsive images, and manages media across file systems.

Repository

Open Issues

29,005,597

5,979

Introduction
------------

### On this page

1. Are you a visual learner?
2. We have badges!

This package can associate all sorts of files with Eloquent models. It provides a simple, fluent API to work with. The Pro version of the package offers Blade, Vue and React components to handle uploads to the media library and to administer the content of a medialibrary collection.

Here are some quick code examples:

```php
$yourModel = YourModel::find(1);
$yourModel->addMedia($pathToFile)->toMediaCollection('images');

```
It can also directly handle your uploads:

```php
$yourModel->addMediaFromRequest('image')->toMediaCollection('images');

```
Want to store some large files on another filesystem? No problem:

```php
$yourModel->addMedia($smallFile)->toMediaCollection('downloads', 'local');
$yourModel->addMedia($bigFile)->toMediaCollection('downloads', 's3');

```
The storage of the files is handled by Laravel's Filesystem, so you can plug in any compatible filesystem.

The package can also generate derived images such as thumbnails for images, videos and PDFs. Once you've set up your model, they're easily accessible:

```php
$yourModel->getMedia('images')->first()->getUrl('thumb');

```
##Are you a visual learner?
---------------------------

We've recorded a video course on how to use this package. It's the best way to get started using media library

![video course](/docs/laravel-medialibrary/v11/images/video-course.jpg)

##We have badges!
-----------------

![Latest Version](https://img.shields.io/github/release/spatie/laravel-medialibrary.svg?style=flat-square)
![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)
![Build Status](https://img.shields.io/travis/spatie/laravel-medialibrary/master.svg?style=flat-square)
![Quality Score](https://img.shields.io/scrutinizer/g/spatie/laravel-medialibrary.svg?style=flat-square)
![Total Downloads](https://img.shields.io/packagist/dt/spatie/laravel-medialibrary.svg?style=flat-square)

About us

Support us

Help us improve this page