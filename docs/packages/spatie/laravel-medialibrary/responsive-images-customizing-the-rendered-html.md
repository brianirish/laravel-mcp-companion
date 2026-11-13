# Spatie - Responsive Images/Customizing The Rendered Html

Source: https://spatie.be/docs/laravel-medialibrary/v11/responsive-images/customizing-the-rendered-html

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Responsive-images

Customizing the rendered HTML

Customizing the rendered HTML
=============================

Whenever you use a `$media` instance as output in a Blade view the medialibrary will generate a `img` tag with the necessary `src`, `srcset` and `alt` attributes. You can customize the rendered output by publishing the `views` with:

```php
php artisan vendor:publish --provider="Spatie\MediaLibrary\MediaLibraryServiceProvider" --tag="media-library-views"
```
The following files will be published in the `resources/views/vendor/media-library` directory:

* `image.blade.php`: will be used to render media without responsive images
* `responsiveImage.blade.php`: will be used to render media with responsive images without a tiny placeholder
* `responsiveImageWithPlaceholder.blade.php`: will be used to render media with responsive images including a tiny placeholder.

You may modify these published views to your heart's content.

Using your own width calculator

Generating your own tiny placeholder

Help us improve this page