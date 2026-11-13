Source: https://laravel.com/cloud/docs/resources/object-storage.md

# Laravel Object Storage

S3-compatible object storage buckets

&#x20;Powered by [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/)

## Introduction

Laravel Cloud lets you create S3-compatible object storage buckets and attach them to your application's environments directly from the Laravel Cloud dashboard. Laravel Cloud offers Object Storage in partnership with Cloudflare R2.

You may use Laravel Cloud Object Storage as an S3-compatible file storage backend for your application. Laravel applications can interact with the bucket through Laravel's [`Storage` facade](https://laravel.com/docs/filesystem), and Symfony applications may use any S3-compatible storage integration.

## Laravel prerequisites

Before using Laravel Object Storage, make sure your application includes the `league/flysystem-aws-s3-v3` package in its `composer.json` dependencies:

```shell theme={null}
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

## Creating buckets


To attach a Laravel Object Storage bucket to an environment, click "Add bucket" on your environment's infrastructure canvas dashboard. Laravel Cloud then prompts you to select an existing bucket to attach or to create a new bucket.

When you create a new bucket, select "Laravel Object Storage" as your bucket type.

After you attach the bucket, redeploy the environment for the changes to take effect.

Visit the [pricing](https://laravel.com/cloud/docs/pricing#laravel-object-storage) docs for information on compute and storage prices.

### Bucket disk names

When you create a bucket, Laravel Cloud also prompts you for a "disk name". You use this name to access the bucket's disk through Laravel's `Storage` facade:

```php theme={null}
return Storage::disk('r2')->get('photo.jpg');
```

You can also make the disk the "default" disk for the Laravel application. When a bucket is the default disk, you do not need to provide its name when you access it through Laravel's `Storage` facade:

```php theme={null}
return Storage::get('photo.jpg');
```

### Bucket location

When you create a bucket, you may choose where its data lives using the "Jurisdiction" and "Location hint" settings:

* **Jurisdiction:** guarantees the broad region your bucket's data stays in. You may choose "Automatic", "European Union", or "United States".
* **Location hint:** asks Cloudflare R2 to place the bucket near a given region. You may choose "Automatic", "Western North America", "Eastern North America", "Western Europe", "Eastern Europe", "Asia-Pacific", or "Oceania". A location hint is a preference, not a guarantee.

You may choose a location hint only when the bucket's jurisdiction is "Automatic". To reduce latency, choose the location hint closest to the region your application runs in. You choose both settings when you create the bucket, and you cannot change them later.

### Bucket file visibility

When you create a bucket, Laravel Cloud prompts you to select the bucket's file visibility. All files in the bucket receive that visibility. Laravel Cloud Object Storage buckets do not support mixed file visibility within a single bucket.

You may change a bucket's visibility later from the bucket's **Edit settings** page. Making a public bucket private removes its public URL. Making a private bucket public again restores one.

* **Private buckets:** all files in the bucket are private and are not publicly accessible on the Internet. However, you may generate temporary public URLs to files in these buckets using the `Storage::temporaryUrl` method [offered by Laravel](https://laravel.com/docs/filesystem#temporary-urls). Private buckets typically hold private assets, like personal documents that your application's users upload.
* **Public buckets:** all files in the bucket are public and accessible on the Internet through a URL that Laravel Cloud provides. Public buckets typically hold publicly viewable assets like user avatars.

> [!NOTE]
>
> Cloudflare R2 manages visibility at the bucket level and does not support per-object ACL headers. Do not set `visibility: 'public'` in your Flysystem storage configuration. R2 rejects the request with a `NotImplemented` error. Bucket-level visibility governs object access.

### Restricted file types

> [!WARNING]
>
> Laravel Object Storage buckets do not accept `.html` or `.htm` files. Any `.html` or `.htm` file uploaded to a bucket is deleted automatically. If your application needs to store `.html` files, [contact support](https://laravel.com/cloud/docs/support) to request an exception.

### CORS policy

Laravel Cloud automatically manages CORS (Cross-Origin Resource Sharing) policies for your object storage buckets, so browsers permit cross-origin requests.

#### Automatic domain inclusion

When you attach a bucket to an environment, Laravel Cloud automatically adds all of the environment's custom and Cloud domains to the bucket's CORS policy. You do not need to configure anything.

#### Custom allowed origins

In addition to your environment's domains, you may allow other origins to access your bucket. Custom origins are useful for:

* Local development environments, such as `http://example.test`
* External domains that need access to your bucket
* Testing from non-production environments

To add custom allowed origins:

1. Navigate to your organization's resources page by clicking **Org > Resources > Object storage** from the main dashboard.
2. Click the "**...**" menu next to the bucket you want to configure.
3. Select "**Edit settings**".
4. In the "**Allowed origins**" field, enter the origins you want to allow, separated by new lines.
5. Prefix each origin with its protocol, `https://` or `http://`.

If you would like to allow requests from every origin, you may enter `*` as an allowed origin. When `*` is present, it replaces your environment domains and any other custom origins in the bucket's CORS policy.


#### Local development

To connect to your object storage buckets from your local Laravel application, add your local development domain, such as `http://example.test`, to the bucket's allowed origins. You can then test file uploads and storage operations during development.

#### Technical details

By default, the CORS policy applied to your buckets allows the following:

* **Methods:** GET, POST, PUT, DELETE, HEAD
* **Headers:** All headers (`*`) are permitted
* **Origins:** All domains of every environment the bucket is attached to, plus any custom origins you've configured

You may customize the allowed methods (any of GET, POST, PUT, DELETE, and HEAD), allowed headers, exposed headers, and max age (in seconds) from the bucket's **Edit settings** page. You may also provide these settings in the `cors_settings` field on the API's create and update bucket endpoints. You still manage allowed origins with the **Allowed origins** field.

## Connecting to buckets

### From your application

When you attach a bucket to a Laravel environment, Laravel Cloud configures its filesystem disk automatically. If the bucket is your environment's default disk, Cloud also sets `FILESYSTEM_DISK`.

For non-Laravel environments, Cloud injects S3-compatible connection variables when you attach a bucket as the environment's default disk. These include `AWS_BUCKET`, `AWS_ENDPOINT_URL`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`. You may view these variables in your environment's **General Settings**.

For public buckets, Laravel receives the public base URL automatically through its Cloud-managed filesystem disk configuration. For other stacks, Cloud injects the default bucket's public base URL as `AWS_URL`. Cloud omits `AWS_URL` when the default bucket has no public URL. If you use a custom bucket domain, you may override `AWS_URL` through your environment's custom variables.

The AWS SDK for JavaScript (v3) supports [endpoint configuration through environment variables](https://docs.aws.amazon.com/sdkref/latest/guide/feature-ss-endpoints.html). An endpoint passed directly to the S3 client takes precedence.

> [!WARNING]
>
> The injected `AWS_ENDPOINT_URL`, `AWS_REGION`, and credential variables are global AWS SDK settings rather than S3-specific ones. Clients for other AWS services may read those same values. If your application also talks to other AWS services, define your own `AWS_*` environment variables and configure your bucket's S3 client explicitly. Your own variables take precedence over the injected values.

### Access keys

Each access key is either "Read and write" or "Read only". You choose the permission when you create the key from the bucket's **Access keys** section, and you cannot change it afterward. If you need a key with a different permission, create a new access key.

### From your local machine

To connect to your bucket from your local machine using a Cloudflare R2-compatible bucket management client like [Cyberduck](https://cyberduck.io/):

1. Navigate to **Organization > Resources > Object storage** and click your bucket. In the **Access keys** section, click **...** next to the access key you want to use, then select **View credentials**.


2. The bucket credentials modal shows the name, endpoint, access key ID, and access key secret you need to connect to your bucket.


3. To connect to the bucket with Cyberduck:
   * Open Cyberduck, select "+" in the bottom left-hand corner to create a new bookmark, and select "Cloudflare R2 Storage (S3)" as the connection type. If this is your first time using the Cloudflare R2 Storage connection, you may need to add it from `Settings > Profiles`.  [Learn more](https://docs.cyberduck.io/protocols/s3/cloudflare/)
   * Enter the "AWS\_ENDPOINT" bucket credentials value into the Cyberduck "Server" field
   * Enter the "AWS\_ACCESS\_KEY\_ID" bucket credentials value into the Cyberduck "Access Key ID" field
   * Enter the "AWS\_SECRET\_ACCESS\_KEY" bucket credentials value into the Cyberduck "Access Key Secret" field
   * Enter the "AWS\_BUCKET" value into the Cyberduck "Path" field, under "More Options"
     * If you do not see "More Options", you likely clicked "Open Connection" instead of creating a new bookmark from the first step.
   * Optionally, give your bookmark a "Nickname"
4. When you finish, your new Cyberduck connection should look like the following screenshot. You can now close the "Open connection" modal and connect to your bucket.


## Editing buckets

You may edit Laravel Object Storage buckets from your organization's **Resources** page. Navigate to the **Object storage** tab and click the **...** icon for the bucket you would like to edit. Then, click **Edit settings**.

## Monitoring bucket metrics

To view your bucket's metrics, navigate to **Organization > Resources > Object storage**, click your bucket, and review the **Metrics** section. Use the time range selector to adjust the period shown. You can also view metrics for attached buckets from your environment's **Metrics** tab.

You can monitor the following for each bucket:

* **Operations:** Class A and Class B operation counts. See [Object Storage pricing](https://laravel.com/cloud/docs/pricing#laravel-object-storage) for the operations included in each class.
* **Egress:** The amount of data transferred out of the bucket.
* **Errors:** Aggregate statistics on 4XX and 5XX responses served by R2.

See [Object storage metrics](https://laravel.com/cloud/docs/metrics/object-storage) for more detail on each chart.

## Deleting buckets

You may delete a Laravel Object Storage bucket from your organization's **Resources** page. Navigate to the **Object storage** tab and click the **...** icon for the bucket you would like to delete. Then, click **Delete bucket**.
