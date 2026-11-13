# Spatie - Advanced Usage/Generating Custom Urls

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/generating-custom-urls

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Generating custom URLs

Generating custom URLs
======================

When `getUrl` is called, the task of generating that URL is passed to an implementation of `Spatie\MediaLibrary\Support\UrlGenerator\UrlGenerator`.

The package contains a `DefaultUrlGenerator` that can generate URLs for a media library that is stored inside the public path. It can also generate URLs for S3.

If you are storing your media files in a private directory or are using a different filesystem, you can write your own `UrlGenerator`. Your generator must implement the `Spatie\MediaLibrary\Support\UrlGenerator\UrlGenerator` interface.

Attaching media in mails

Overriding default filesystem behavior

Help us improve this page