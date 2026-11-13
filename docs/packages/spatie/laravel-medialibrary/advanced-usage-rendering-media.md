# Spatie - Advanced Usage/Rendering Media

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/rendering-media

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Rendering media

Rendering media
===============

### On this page

1. Customizing the views

If your `$media` instance concerns an image, you can render it directly in a Blade view.

```php
Here is the original image: {{ $media }}
```
This will output an `img` tag with a `src` attribute that contains an url to the media.

You can also render an `img` to a conversion.

```php
Here is the converted image: {{ $media->conversion('thumb') }}
```
You can also use this shorthand:

```php
Here is the converted image: {{ $media('thumb') }}
```
You can add extra attributes by calling `attributes`.

```php
Here is the image with some attributes: {{ $media->img()->attributes(['class' => 'my-class']) }}
```
You may also pass an array of classes to the `class` attribute. This way, you can conditionally add classes where the key is the class name and the value is a boolean indicating whether the class should be added. Elements with a numeric key will always be added. Under the hood, this uses Laravel `Arr::toCssClasses()` helper method.

```php
Here is the image with some classes: {{ $media->img()->attributes(['class' => [
    'my-class',
    'my-other-class' => true,
    'my-third-class' => false,
]]) }}
```
You may also pass an array of styles to the `style` attribute. This way, you can conditionally add styles where the key is the style name and the value is a boolean indicating whether the style should be added. Elements with a numeric key will always be added. Under the hood, this uses Laravel `Arr::toCssStyles()` helper method.

```php
Here is the image with some styles: {{ $media->img()->attributes(['style' => [
    'my-style: value',
    'my-other-style: value',
    'my-third-style: value' => true,
]]) }}
```
If you want defer loading offscreen images you can use the `lazy` function.

```php
Lazy loading this one: {{ $media()->lazy() }}
```
##Customizing the views
-----------------------

You can customize the rendered output even further by publishing the `views` with:

```php
php artisan vendor:publish --provider="Spatie\MediaLibrary\MediaLibraryServiceProvider" --tag="media-library-views"
```
The following files will be published in the `resources/views/vendor/media-library` directory:

* `image.blade.php`: will be used to render media without responsive images
* `responsiveImage.blade.php`: will be used to render media with responsive images without a tiny placeholder
* `responsiveImageWithPlaceholder.blade.php`: will be used to render media with responsive images including a tiny placeholder.

You may modify these published views to your heart's content.

Outputting media

Using a custom directory structure

Help us improve this page