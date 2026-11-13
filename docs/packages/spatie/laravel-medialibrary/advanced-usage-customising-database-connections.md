# Spatie - Advanced Usage/Customising Database Connections

Source: https://spatie.be/docs/laravel-medialibrary/v11/advanced-usage/customising-database-connections

SPATIE

Laravel Media Library
=====================

spatie.be/open-source

Docs

Laravel-medialibrary

Advanced-usage

Customising Database Connections

Customising Database Connections
================================

### ##Media model connection

The built-in model (`Spatie\MediaLibrary\MediaCollections\Models\Media`) will use the default database connection set for your application.

If you need to change this database connection, you can create a custom model and set the `$connection` property (https://laravel.com/docs/10.x/eloquent#database-connections). See Using your own model for more information.

```php
<?php

namespace App\Models;

use Spatie\MediaLibrary\MediaCollections\Models\Media as BaseMedia;

class Media extends BaseMedia {

    protected $connection = 'tenant';

}
```
### ##Parent model connection

The `Spatie\MediaLibrary\InteractsWithMedia` trait defines a `MorphMany` relationship to the media model. Eloquent automatically uses the database connection of your parent model when querying the database. In the example below, the user media results will use the `tenant` database connection rather than the application's default connection.

```php
<?php

namespace App\Models;

use Spatie\MediaLibrary\HasMedia;
use Illuminate\Database\Eloquent\Model;
use Spatie\MediaLibrary\InteractsWithMedia;

class User extends Model implements HasMedia {

    use InteractsWithMedia;

    protected $connection = 'tenant';

}
```
When you save files using the code below, the `Spatie\MediaLibrary\MediaCollections\FileAdder` will also automatically use the parent model's database connection if that is set.

```php
$model
    ->addMedia($path)
    ->toMediaCollection();
```
If you need to customise the database connection further before fetching or adding media, use you can do `$model->setConnection('landlord')`.

Disable CDN

Adding files

Help us improve this page