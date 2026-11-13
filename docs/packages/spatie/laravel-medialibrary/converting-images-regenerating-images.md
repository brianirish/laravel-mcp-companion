# Spatie - Converting Images/Regenerating Images

Source: https://spatie.be/docs/laravel-medialibrary/v11/converting-images/regenerating-images

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Converting-images

Regenerating images

Regenerating images
===================

When you change a conversion on your model, all images that were previously generated will not be updated automatically. You can regenerate your images via an artisan command. Note that conversions are often queued, so it might take a while to see the effects of the regeneration in your application.

```php
php artisan media-library:regenerate
```
If you only want to regenerate the images for a single model, you can specify it as a parameter:

```php
php artisan media-library:regenerate "App\Models\Post"
```
When using a morph map, you should use the name of the morph.

```php
php artisan media-library:regenerate "post"
```
If you only want to regenerate images for a few specific media items, you can pass their IDs using the `--ids` option:

```php
php artisan media-library:regenerate --ids=1 --ids=2 --ids=3
```
A comma separated list of id's works too.

```php
php artisan media-library:regenerate --ids=1,2,3
```
If you only want to regenerate images for one or many specific conversions, you can use the `--only` option:

```php
php artisan media-library:regenerate --only=thumb --only=foo
```
If you only want to regenerate missing images, you can use the `--only-missing` option:

```php
php artisan media-library:regenerate --only-missing
```
If you want to force responsive images to be regenerated, you can use the `--with-responsive-images` option:

```php
php artisan media-library:regenerate --with-responsive-images
```
If you want to regenerate images starting at a specific id (inclusive), you can use the `--starting-from-id` option

```php
php artisan media-library:regenerate --starting-from-id=1
```
You can also start after the provided id by also passing the `--exclude-starting-id` or `-X` options

```php
php artisan media-library:regenerate --starting-from-id=1 --exclude-starting-id
php artisan media-library:regenerate --starting-from-id=1 -X
```
The `--starting-from-id` option can also be combined with the `modelType` argument

```php
php artisan media-library:regenerate "App\Models\Post" --starting-from-id=1
```
Optimizing converted images

Getting started with responsive images

Help us improve this page