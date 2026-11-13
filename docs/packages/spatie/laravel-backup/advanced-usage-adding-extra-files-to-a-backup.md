# Spatie - Advanced Usage/Adding Extra Files To A Backup

Source: https://spatie.be/docs/laravel-backup/v10/advanced-usage/adding-extra-files-to-a-backup

SPATIE

Laravel Backup
==============

spatie.be/open-source

Docs

Laravel-backup

Advanced-usage

Adding extra files to a backup

Adding extra files to a backup
==============================

The package ships with a BackupManifestWasCreated event that enables you to add additional files to the backup zip file.

When backup process starts, the package will create a manifest of all file that are selected for backup. Once the manifest has been created, a zip file is made containing all the files in the manifest. The zip file will be copied to the backup destinations you configured.

However, if you have cases where you need to add additional files to a particular backup, you can do so, between the creation of the manifest and the creation of the zip file.

Right after the manifest is created and **before** the zip file is created the `Spatie\Backup\Events\BackupManifestWasCreated` event is fired. This is what is looks like:

```php
namespace Spatie\Backup\Events;

use Spatie\Backup\Tasks\Backup\Manifest;

class BackupManifestWasCreated
{
    /** @var \Spatie\Backup\Tasks\Backup\Manifest */
    public $manifest;

    public function __construct(Manifest $manifest)
    {
        $this->manifest = $manifest;
    }
}
```
You can use that event to add extra files to the manifest as in the example below where the extra files are passed as an array to the addFiles() method.

```php
use Spatie\Backup\Events\BackupManifestWasCreated;

Event::listen(BackupManifestWasCreated::class, function (BackupManifestWasCreated $event) {
   $event->manifest->addFiles([$path1, $path2, ...]);
});
```
Customizing the notifiable

Backing up a non-laravel application

Help us improve this page