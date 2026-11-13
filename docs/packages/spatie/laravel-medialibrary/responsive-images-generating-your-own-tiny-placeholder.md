# Spatie - Responsive Images/Generating Your Own Tiny Placeholder

Source: https://spatie.be/docs/laravel-medialibrary/v11/responsive-images/generating-your-own-tiny-placeholder

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Responsive-images

Generating your own tiny placeholder

Generating your own tiny placeholder
====================================

When generating responsive images, the media library will generate a tiny version of your image which will be used for progressive image loading. By default, this tiny version will be a blurred version of the original.

You can customize how the tiny version of the image should be generated. Maybe you want to just use the dominant color instead of blur. In the `responsive_images.tiny_placeholder_generator` of the `media-library` config file you can specify a class that implements `Spatie\MediaLibrary\ResponsiveImages\TinyPlaceholderGenerator`. This interface only requires you to implement one function:

```php
public function generateTinyPlaceholder(string $sourceImagePath, string $tinyImageDestinationPath);
```
`$sourceImagePath` contains the path of the image where you should generate a tiny representation for. The generated tiny image should be saved at `$tinyImageDestinationPath`. This tiny image should be a `jpg`.

Here's an example implementation that generates a blurred version:

```php
namespace App;

use Spatie\Image\Image;

class Blurred implements TinyPlaceholderGenerator
{
    public function generateTinyPlaceholder(string $sourceImagePath, string $tinyImageDestinationPath)
    {
        $sourceImage = Image::load($sourceImagePath);

        $sourceImage->width(32)->blur(5)->save($tinyImageDestinationPath);
    }
}
```
Customizing the rendered HTML

Responsive images demo

Help us improve this page