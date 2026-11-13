# Spatie - Advanced Usage/Working With Multiple Filesystems

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/working-with-multiple-filesystems

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Working with multiple filesystems

Working with multiple filesystems
=================================

### On this page

1. Storing conversions on a separate disk
2. Are you a visual learner?

By default, all files are stored on the disk specified as the `disk_name` in the config file.

Files can also be stored on any filesystem that is configured in your Laravel app. When adding a file to the media library you can choose on which disk the file should be stored. This is useful when you have a combination of small files that should be stored locally and big files that you want to save on S3.

`toMediaCollection` accepts a disk name as a second parameter:

```php
// Will be stored on a disk named s3
$yourModel->addMedia($pathToAFile)->toMediaCollection('images', 's3');
```
##Storing conversions on a separate disk
----------------------------------------

You can let the media library store your conversions and responsive images on a disk other than the one where you save the original item. Pass the name of the disk where you want conversion to be saved to the `storingConversionsOnDisk` method.

Here's an example where the original file is saved on the local disk and the conversions on S3.

```php
$media = $yourModel
   ->addMedia($pathToImage)
   ->storingConversionsOnDisk('s3')
   ->toMediaCollection('images', 'local');
```
### ##Configuring a default conversions disk

If you want every conversion to land on a particular disk without repeating `storingConversionsOnDisk(...)` for every upload, set the `conversions_disk_name` config value:

```php
// config/media-library.php

return [
    'disk_name' => 's3',
    'conversions_disk_name' => 'public',

    // ...
];
```
With this in place, conversions and responsive images are saved on the `public` disk by default, while the originals still live on `s3`. Anything you set explicitly — either via `->storingConversionsOnDisk(...)` on a `FileAdder` or via `->storeConversionsOnDisk(...)` on a media collection — takes precedence. When the value is `null` (the default), conversions stay on the originals' disk, preserving the historical behavior.

##Are you a visual learner?
---------------------------

Here's a video that shows how to work with multiple filesystems.

Want to see more videos like this? Check out our free video course on how to use Laravel Media Library.

Downloading multiple files

Using custom properties

Help us improve this page