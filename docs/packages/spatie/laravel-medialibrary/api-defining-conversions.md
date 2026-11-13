# Spatie - Api/Defining Conversions

Source: https://spatie.be/docs/laravel-medialibrary/v11/api/defining-conversions

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Api

Defining conversions

Defining conversions
====================

### On this page

1. General methods
2. Image manipulations

A media conversion can be added to your model in the `registerMediaConversions`-function. It should start with a call to `addMediaConversion`. From there on you can use any of the methods available in the API. They are all chainable.

Take a look in the Defining conversions section
for more details.

##General methods
-----------------

### ##addMediaConversion

```php
/*
 * Add a conversion.
 */
public function addMediaConversion(string $name): \Spatie\MediaLibrary\Conversions\Conversion
```
### ##performOnCollections

```php
/*
 * Set the collection names on which this conversion must be performed.
 *
 * @param string $collectionNames,...
 */
public function performOnCollections($collectionNames): self
```
### ##queued

```php
/*
 * Mark this conversion as one that should be queued.
 */
 public function queued(): self
```
### ##nonQueued

```php
/*
 * Mark this conversion as one that should not be queued.
 */
public function nonQueued(): self
```
### ##useLoadingAttributeValue

This is the value that, when this conversation is converted to HTML, will be used in the `loading` attribute. The loading attribute is a standardised attribute that controls lazy loading behaviour of the browser. Possible values are `lazy`, `eager`, `auto` or null if you don't want to set any loading instruction.

You can learn more on native lazy loading in this post on css-tricks.

##Image manipulations
---------------------

You may add any call to one of the manipulation functions available on the spatie/image package.

Adding files

Help us improve this page