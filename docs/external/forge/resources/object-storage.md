Source: https://laravel.com/forge/docs/resources/object-storage.md

# Object Storage

> Learn how to create and manage S3-compatible object storage buckets with Laravel Forge.

&#x20;Powered by [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/)

## Introduction

Laravel Forge allows you to create S3-compatible object storage buckets as organization-level resources from the Forge dashboard. Object storage is offered in partnership with Cloudflare R2.

Buckets are managed independently at the organization level. To use a bucket with a site, retrieve the bucket credentials from the Forge dashboard and configure them as [environment variables](https://forge.laravel.com/docs/sites/environment-variables.md) on the site.

Object storage may be used as your Laravel application's [file storage backend](https://laravel.com/docs/filesystem), allowing you to interact with the bucket via Laravel's `Storage` facade.

## Prerequisites

Before using object storage, you should ensure your application includes the `league/flysystem-aws-s3-v3` package in its `composer.json` dependencies:

```shell theme={null}
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

## Creating buckets

To create a new object storage bucket, navigate to your organization's "Resources" page, open the "Object storage" tab, and click "New bucket."

You can view your current usage and billing history on the organization's "Usage" page.

### Public access

When creating or editing a bucket, you may configure **Public access** by toggling the setting on or off.

When public access is disabled, all files within the bucket are private and are not publicly accessible via the internet. However, temporary public URLs may be generated for files within the bucket using the `Storage::temporaryUrl` method [offered by Laravel](https://laravel.com/docs/filesystem#temporary-urls). This is typically used for private assets like personal documents uploaded by your application's users.

When public access is enabled, all files within the bucket are publicly accessible via the internet through a Forge-provided URL. This is typically used for publicly viewable assets like user avatars.

## Using buckets with your sites

To use a bucket with a Laravel site, retrieve the bucket credentials from the Forge dashboard and add them to the site's environment variables.

### Retrieving bucket credentials

Navigate to your organization's "Resources" page, open the "Object storage" tab, click the "..." icon next to the bucket, and select "View credentials." The credentials modal provides the name, endpoint, access key ID, and access key secret needed to connect to the bucket.

### Configuring environment variables

Navigate to your site's "Settings" panel and open the [Environment](https://forge.laravel.com/docs/sites/environment-variables.md) tab. Add the bucket credentials as environment variables using the values from the credentials modal:

```env theme={null}
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-access-key-secret
AWS_DEFAULT_REGION=auto
AWS_BUCKET=your-bucket-name
AWS_ENDPOINT=your-bucket-endpoint
AWS_USE_PATH_STYLE_ENDPOINT=false
FILESYSTEM_DISK=s3
```

Set `FILESYSTEM_DISK` to the disk name defined in your application's `config/filesystems.php` file. If you are using Laravel's default `s3` disk configuration, set `FILESYSTEM_DISK=s3`.

After saving your environment variables, redeploy the site or run `php artisan config:cache` so your application picks up the new configuration.

### Accessing the bucket in your application

Once configured, you may interact with the bucket via Laravel's `Storage` facade using the disk name defined in your filesystem configuration:

```php theme={null}
return Storage::disk('s3')->get('photo.jpg');
```

If the bucket is configured as your application's default disk, you do not need to provide the disk name:

```php theme={null}
return Storage::get('photo.jpg');
```

## CORS policy

Laravel Forge automatically manages CORS (Cross-Origin Resource Sharing) policies for your object storage buckets to ensure browsers will permit cross-origin requests.

### Allowed origins

If your application uploads files directly from the browser, you should add your site's domains to the bucket's allowed origins. This includes any custom domains and `on-forge.com` vanity domains associated with the site.

You may also specify additional origins that should be allowed to access your bucket. This is particularly useful for:

* Local development environments, such as `http://example.test`
* External domains that need access to your bucket
* Testing from non-production environments

To add allowed origins:

1. Navigate to your organization's "Resources" page and open the "Object storage" tab.
2. Click the "**...**" menu next to the bucket you want to configure.
3. Select "**Edit settings**".
4. In the "**Allowed origins**" field, enter each origin on a separate line. This field is only visible when public access is enabled.
5. Each origin must be prefixed with the protocol (`https://` or `http://`).

### Local development

To connect to your object storage buckets from your local Laravel application, add your local development domain, such as `http://example.test`, to the bucket's allowed origins. This makes it easy to test file uploads and storage operations during development.

### Technical details

The CORS policy applied to your buckets allows the following:

* **Methods:** GET, POST, PUT, DELETE, HEAD
* **Headers:** All headers (`*`) are permitted
* **Origins:** Any origins you have configured for the bucket

## Connecting from your local machine

To connect to your bucket from your local machine using a Cloudflare R2-compatible bucket management client like [Cyberduck](https://cyberduck.io/):

1. Navigate to your organization's "Resources" page and open the "Object storage" tab. Then, click the "..." icon next to the bucket and click "View credentials".

2. The credentials modal provides the name, endpoint, access key ID, and access key secret needed to connect to your bucket.

3. Open Cyberduck, select "+" in the bottom-left corner to create a new bookmark, and select "Cloudflare R2 Storage (S3)" as the connection type. If this is your first time using the Cloudflare R2 Storage connection, you may need to add it from `Settings > Profiles`. For more information, review Cyberduck's [Cloudflare R2 documentation](https://docs.cyberduck.io/protocols/s3/cloudflare/).

4. Enter the `AWS_ENDPOINT` bucket credentials value into the Cyberduck "Server" field.

5. Enter the `AWS_ACCESS_KEY_ID` bucket credentials value into the Cyberduck "Access Key ID" field.

6. Enter the `AWS_SECRET_ACCESS_KEY` bucket credentials value into the Cyberduck "Access Key Secret" field.

7. Enter the `AWS_BUCKET` value into the Cyberduck "Path" field under "More Options". If you do not see "More Options," you likely clicked "Open Connection" instead of creating a new bookmark.

8. Optionally, give your bookmark a nickname.

9. Close the "Open Connection" modal and connect to your bucket.

## Editing buckets

You may edit object storage buckets via your organization's "Resources" page. From the "Resources" page, navigate to the "Object storage" tab and click the "..." icon for the bucket you would like to edit. Then, click "Edit settings".

## Deleting buckets

You may delete an object storage bucket via your organization's "Resources" page. From the "Resources" page, navigate to the "Object storage" tab and click the "..." icon for the bucket you would like to delete. Then, click "Delete bucket".
