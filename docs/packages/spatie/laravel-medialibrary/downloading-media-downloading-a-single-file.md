# Spatie - Downloading Media/Downloading A Single File

Source: https://spatie.be/docs/laravel-medialibrary/v11/downloading-media/downloading-a-single-file

Docs

Laravel-medialibrary

Downloading-media

Downloading a single file

Downloading a single file
=========================

### On this page

1. Are you a visual learner?

`Media` implements the `Responsable` interface. This means that you can just return a media object to download the associated file in your browser.

```php
use Spatie\MediaLibrary\MediaCollections\Models\Media;

class DownloadMediaController
{
   public function show(Media $mediaItem)
   {
      return $mediaItem;
   }
}

```
If you need more control you could also do the above more verbose:

```php
use Spatie\MediaLibrary\MediaCollections\Models\Media;

class DownloadMediaController
{
   public function show(Media $mediaItem)
   {
       return response()->download($mediaItem->getPath(), $mediaItem->file_name);
   }
}

```
##Are you a visual learner?
---------------------------

Here's a video that shows how to download files.

Want to see more videos like this? Check out our free video course on how to use Laravel Media Library.

Creating a custom image generator

Downloading multiple files

Help us improve this page