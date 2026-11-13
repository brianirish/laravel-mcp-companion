# Spatie - Advanced Usage/Ordering Media

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/ordering-media

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Ordering media

Ordering media
==============

This package has a built-in feature to help you order the media in your project. By default, all inserted media items are arranged in order by their time of creation (from the oldest to the newest) using the `order_column` column of the `media` table.

You can easily reorder a list of media by calling ̀Media::setNewOrder`:

```php
 /**
  * This function reorders the records: the record with the first id in the array
  * will get the starting order (defaults to 1), the record with the second id
  * will get the starting order + 1, and so on.
  *
  * A starting order number can be optionally supplied.
  *
  * @param array $ids
  * @param int $startOrder
  */
Media::setNewOrder([11, 2, 26]);
```
Of course, you can also manually change the value of the `order_column`.

```php
$media->order_column = 10;

$media->save();
```
Using a custom file removal strategy

Using a custom media downloader

Help us improve this page