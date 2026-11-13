Source: https://laravel.com/cloud/docs/knowledge-base/migrating-object-storage.md

# Migrating Object Storage to Laravel Cloud

Learn how to move files from another storage provider to Laravel Cloud Object Storage using Laravel's read-through fallback disk.

If you're moving an existing application to Laravel Cloud, you likely already have files sitting in another provider's bucket. Copying everything before you cut over can be slow and can force downtime. Laravel's read-through filesystem driver lets you cut over immediately instead. When a file is missing from your new Laravel Cloud Object Storage bucket, Laravel reads it from your old provider and copies it into the new bucket for next time. Your files move over as your application accesses them.

## Before you start

> [!NOTE]
>
> The read-through driver requires Laravel 13.26.0 or later. Run `composer update laravel/framework` before continuing. If your old provider is S3-compatible, you'll also need `league/flysystem-aws-s3-v3`. See the [Object Storage prerequisites](https://laravel.com/cloud/docs/resources/object-storage#prerequisites).

The read-through driver works with any two Flysystem-compatible disks, including ones that aren't S3-compatible. You can also use it to move off local disk storage or another provider's driver.

## Step 1: Create your Laravel Object Storage bucket

If you haven't already, [create a Laravel Object Storage bucket](https://laravel.com/cloud/docs/resources/object-storage#creating-buckets) and attach it to your environment. Note its disk name (for example, `r2`). Laravel Cloud automatically injects the `AWS_*` credentials your application needs to reach it.

Leave your old provider's credentials in place. You'll need them for the fallback disk in the next step.

## Step 2: Configure your old provider as a fallback disk

In `config/filesystems.php`, add a disk entry for your old provider using whatever credentials it requires:

```php theme={null}
'disks' => [

    // ...

    'legacy' => [
        'driver' => 's3',
        'key' => env('LEGACY_AWS_ACCESS_KEY_ID'),
        'secret' => env('LEGACY_AWS_SECRET_ACCESS_KEY'),
        'region' => env('LEGACY_AWS_DEFAULT_REGION'),
        'bucket' => env('LEGACY_AWS_BUCKET'),
        'endpoint' => env('LEGACY_AWS_ENDPOINT'), // omit for AWS S3; required for R2, Spaces, B2, etc.
    ],

],
```

Laravel Cloud injects credentials only for the bucket attached to your environment, so add your old provider's credentials as custom environment variables under your environment's settings.

## Step 3: Add a read-through disk

Combine your new Laravel Cloud bucket (`primary`) and your old provider (`fallback`) into a single read-through disk:

```php theme={null}
'disks' => [

    // ...

    'assets' => [
        'driver' => 'read-through',
        'primary' => 'r2',
        'fallback' => 'legacy',
    ],

],
```

Reads check the new bucket first. If the file isn't there yet, Laravel reads it from the old provider, copies it into the new bucket, and returns it within the same request. Writes and directory listings always go to the new bucket, so anything your application saves after cutover lands directly on Laravel Cloud. Existence and metadata checks, such as `Storage::exists` and `Storage::size`, consult either disk without triggering a copy.

> [!TIP]
>
> By default, a failed promotion doesn't fail the read. For example, if the new bucket is briefly unreachable, Laravel returns the file from the fallback disk. If you'd rather the read throw an exception, set `'throw_on_promotion_failure' => true` on the disk. Either way, watch your logs during the migration window. [Laravel Nightwatch](https://laravel.com/cloud/docs/knowledge-base/nightwatch-on-cloud) reports exceptions like these in real time, so you can catch credential or permission issues with either disk early.

## Step 4: Point your application at the read-through disk

Update `FILESYSTEM_DISK` to your new read-through disk, and redeploy:

```
FILESYSTEM_DISK=assets
```

From this point on, every file read through `Storage::disk('assets')` or the default `Storage` facade comes from whichever bucket has the file. If the file is still on your old provider, Laravel copies it to Laravel Cloud as part of the read.

## Step 5: Speed up the migration (optional)

Waiting for real traffic to touch every file can leave rarely accessed files on your old provider indefinitely. To migrate everything up front instead, loop over the fallback disk's contents and read each file through the read-through disk:

```php theme={null}
use Illuminate\Support\Facades\Storage;

$legacy = Storage::disk('legacy');
$assets = Storage::disk('assets');

foreach ($legacy->allFiles() as $path) {
    $assets->get($path);
}
```

> [!NOTE]
>
> For large buckets, dispatch a queued job per file or per batch of files instead of running the loop inline.

## Step 6: Retire the old provider

Once every object in your old bucket exists in Laravel Cloud, remove the fallback. To confirm the migration is complete, use your storage provider's inventory or compare the object keys in both buckets. Then follow these steps:

1. Set `FILESYSTEM_DISK` back to your bucket's disk name (`r2`).
2. Remove the `legacy` and `assets` disk entries from `config/filesystems.php`.
3. Redeploy.
4. Cancel or delete the bucket with your old provider.
