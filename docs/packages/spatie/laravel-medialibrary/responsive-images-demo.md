# Spatie - Responsive Images/Demo

Source: https://spatie.be/docs/laravel-medialibrary/v11/responsive-images/demo

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Responsive-images

Responsive images demo

Responsive images demo
======================


The example above demonstrates the responsive images technique used in the Laravel MediaLibrary.

### Try this:

* Throttle your network in Chrome and disable the cache to see this in full effect
* Start with a small browser and reload this page
* Make your browser larger to start loading bigger versions

### What happens?

* We start with an image that has `srcset` values, rendered by the Laravel MediaLibrary
* An initial `sizes="1px"` attribute is used to render an inline base64-encoded SVG placeholder first
* Once the page is loaded, JavaScript sets the `sizes` to the actual width of the image in the layout
* Since we use a `vw` value for this width, a bigger image will be loaded when you upscale the browser

Generating your own tiny placeholder

Using image generators

Help us improve this page