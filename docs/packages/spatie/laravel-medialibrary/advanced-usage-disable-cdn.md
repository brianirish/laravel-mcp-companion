# Spatie - Advanced Usage/Disable Cdn

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/disable-cdn

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Disable CDN

Disable CDN
===========

Media Library Pro uses a CDN to load the Sortable library. Sortable provides the drag-and-drop-ability inside a Media Library Pro component.

If you would like to disable the loading via CDN and want to take care by yourself of including Sortable you will need to add the following option to your `media-library.php` config file.

```php
    ...
    /*
     * When disabling this option, Media Library Pro don't include a script tag to load the Sortable library via a CDN.
     * You have to include the Sortable library by yourself!
     */
    'include_sortable_cdn_script' => false,
    ...
```
You can install Sortable within your project dependencies and include it in your `app.js`.

```php
import Sortable from 'sortablejs'

window.Sortable = Sortable
```
Naming generated files

Customising Database Connections

Help us improve this page