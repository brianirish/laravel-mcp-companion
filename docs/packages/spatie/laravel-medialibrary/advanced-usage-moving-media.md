# Spatie - Advanced Usage/Moving Media

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/moving-media

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Moving media

Moving media
============

### On this page

1. Copying media

You can move media from one model to another with the `move` method.

```php
$mediaItem = $model->getMedia()->first();

$movedMediaItem = $mediaItem->move($anotherModel, 'new-collection', 's3');
```
Any conversions defined on `$anotherModel` will be performed. The `name` and the `custom_properties` will be transferred as well.

##Copying media
---------------

You can also copy media from one model with the `copy` method.

```php
$mediaItem = $model->getMedia()->first();

$copiedMediaItem = $mediaItem->copy($anotherModel, 'new-collection', 's3');
```
Using a custom media downloader

Consuming events

Help us improve this page