# Spatie - Converting Images/Defining Conversions

Source: https://spatie.be/docs/laravel-medialibrary/v11/converting-images/defining-conversions

Docs

Laravel-medialibrary

Converting-images

Defining conversions

Defining conversions
====================

### On this page

1. Are you a visual learner?
2. A single conversion
3. Using multiple conversions
4. Performing conversions on specific collections
5. Using a specific disk
6. Queuing conversions
7. Using model properties in a conversion

When adding files to the media library it can automatically create derived versions such as thumbnails and banners.

Media conversions will be executed whenever a `jpg`, `png`, `svg`, `webp`, `avif`, `pdf`, `mp4` , `mov` or `webm` file is added to the media library. By default, the conversions will be saved as a `jpg` files. This can be overwritten using the `format()` or `keepOriginalImageFormat()` methods.

Internally, spatie/image is used to manipulate the images. You can use any manipulation function from that package.

Please check the image generator docs for additional installation requirements when working with PDF, SVG or video formats.

##Are you a visual learner?
---------------------------

Here's a video that shows how to working with conversion.

Want to see more videos like this? Check out our free video course on how to use Laravel Media Library.

##A single conversion
---------------------

You should add a method called `registerMediaConversions` to your model. In that model you can define the media conversion. Here's an example:

```php
use Illuminate\Database\Eloquent\Model;
use Spatie\MediaLibrary\MediaCollections\Models\Media;
use Spatie\MediaLibrary\HasMedia;
use Spatie\MediaLibrary\InteractsWithMedia;

class YourModel extends Model implements HasMedia
{
    use InteractsWithMedia;

    public function registerMediaConversions(?Media $media = null): void
    {
        $this->addMediaConversion('thumb')
              ->width(368)
              ->height(232)
              ->sharpen(10);
    }
}

```
Let's add an image to the media library.

```php
$media = YourModel::first()->addMedia($pathToImage)->toMediaCollection();

```
Besides storing the original item, the media library also has created a derived image.

```php
$media->getPath();  // the path to the where the original image is stored
$media->getPath('thumb'); // the path to the converted image with dimensions 368x232

$media->getUrl();  // the url to the where the original image is stored
$media->getUrl('thumb'); // the url to the converted image with dimensions 368x232

```
##Using multiple conversions
----------------------------

You can register as many media conversions as you want

```php
// in your model
use Spatie\Image\Enums\BorderType;
use Spatie\Image\Enums\CropPosition;

// ...

    public function registerMediaConversions(?Media $media = null): void
    {
        $this->addMediaConversion('thumb')
              ->width(368)
              ->height(232)
              ->sharpen(10);

        $this->addMediaConversion('old-picture')
              ->sepia()
              ->border(10, BorderType::Overlay, 'black');

        $this->addMediaConversion('thumb-cropped')
            ->crop(400, 400, CropPosition::Center); // Trim or crop the image to the center for specified width and height.
    }

```
Use the conversions like this:

```php
$media->getUrl('thumb') // the url to the thumbnail
$media->getUrl('old-picture') // the url to the sepia, bordered version

```
##Performing conversions on specific collections
------------------------------------------------

By default a conversion will be performed on all files regardless of which collection is used. Conversions can also be performed on specific collections by adding a call to `performOnCollections`.

This is how that looks like in the model:

```php
// in your model
public function registerMediaConversions(?Media $media = null): void
{
    $this->addMediaConversion('thumb')
          ->performOnCollections('images', 'downloads')
          ->width(368)
          ->height(232);
}

```
```php
// a thumbnail will be generated for this media item
$media = $yourModel->addMedia($pathToImage)->toMediaCollection('images');
$media->getUrl('thumb') // the url to the thumbnail

//but not for this one
$media = $yourModel->addMedia($pathToImage)->toMediaCollection('other collection');
$media->getUrl('thumb') // returns ''

```
##Using a specific disk
-----------------------

You can ensure that conversions added to a collection are automatically added to a certain disk.

```php
public function registerMediaCollections(): void
{
    $this
        ->addMediaCollection('big-files')
        ->useDisk('s3')
        ->storeConversionsOnDisk('public');
}

```
##Queuing conversions
---------------------

By default, a conversion will be added to the connection and queue that you've specified in the configuration. If you want your image to be created directly (and not on a queue) use `nonQueued` on a conversion.

```php
// in your model
public function registerMediaConversions(?Media $media = null): void
{
    $this->addMediaConversion('thumb')
            ->width(368)
            ->height(232)
            ->nonQueued();
}

```
If you have set `queue_conversions_by_default` in the `media-library` config file to `false`, all conversions will all be generated synchronously. If you want to generate a conversion on a queue, while `queue_conversions_by_default` is set to `false`, use the `queued` method.

```php
// in your model
public function registerMediaConversions(?Media $media = null): void
{
    $this->addMediaConversion('thumb')
            ->width(368)
            ->height(232)
            ->queued();
}

```
The default behaviour is that queued conversions will run **after all database transactions have been committed**.
This prevents unexpected behaviour where the model does not yet exist in the database and the conversion is disregarded.
If you need the conversions to run within your transaction, you can set the `queue_conversions_after_database_commit`
in the `media-library` config file to `false`.

##Using model properties in a conversion
----------------------------------------

When registering conversions inside the `registerMediaConversions` function you won't have access to your model properties by default. If you want to use a property of your model as input for defining a conversion you must set `registerMediaConversionsUsingModelInstance` to  `true` on your model.

```php
// in your model
public $registerMediaConversionsUsingModelInstance = true;

public function registerMediaConversions(?Media $media = null): void
{
    $this->addMediaConversion('thumb')
          ->performOnCollections('images', 'downloads')
          ->width($this->width)
          ->height($this->height);
}

```
Be aware that this can lead to a hit in performance. When processing media the media library has to perform queries to fetch each separate model.

Defining media collections

Retrieving converted images

Help us improve this page