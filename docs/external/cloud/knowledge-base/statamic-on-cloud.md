Source: https://laravel.com/cloud/docs/knowledge-base/statamic-on-cloud.md

# Deploy Statamic on Laravel Cloud

Deploy a Statamic site on Laravel Cloud, keep content and assets persistent, and serve pages from Statamic's static cache.

> [!NOTE]
>
> This guide is for Laravel applications that use Statamic.

[Statamic](https://statamic.com) is a content management system built on Laravel, so it deploys to Laravel Cloud like any other Laravel application. However, Statamic stores its content as flat files by default, and Cloud environments have an [ephemeral filesystem](https://laravel.com/cloud/docs/environments#filesystem). This guide covers the choices to make before going live so your content, assets, and cache behave as expected.

## Decide where your content lives

Each deployment resets your environment's filesystem, and each replica of your App cluster has its own filesystem. If you save an entry, global, navigation, or user to disk through the Statamic control panel in production, the next deployment erases it. Other replicas never see it.

You have two options:

* **Edit content locally.** Treat production as read-only. Your team edits content on their local machines, commits the flat files to your repository, and pushes to deploy. Your content stays in version control, and this approach works well for sites that change infrequently.
* **Store content in a database.** If your team edits content through the control panel in production, store it in a [Laravel MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) or [Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) database using Statamic's [Eloquent driver](https://statamic.dev/tips/storing-content-in-a-database).

To use the Eloquent driver, install it locally and follow the prompts to choose which repositories (such as entries, globals, and navigation) should move to the database:

```bash theme={null}
composer require statamic/eloquent-driver
php please install:eloquent-driver
```

Commit the generated migrations and configuration, attach a database to your environment, and add `php artisan migrate --force` to your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands).

> [!TIP]
>
> Statamic stores users as files by default as well. If anyone signs in to the control panel in production, [store your users in the database](https://statamic.dev/tips/storing-users-in-a-database) so accounts and password changes persist.

## Store assets in object storage

Statamic writes files uploaded to an asset container to the container's filesystem disk. To keep uploads across deployments and replicas, create a [Laravel Object Storage](https://laravel.com/cloud/docs/resources/object-storage) bucket and attach it to your environment. Cloud injects the S3-compatible connection variables for the bucket's disk automatically.

Next, point your asset container at the bucket's [disk name](https://laravel.com/cloud/docs/resources/object-storage#bucket-disk-names). For example, if you named the disk `assets`, update your container's YAML file:

```yaml content/assets/assets.yaml theme={null}
title: Assets
disk: assets
```

If you use a public bucket, copy its `AWS_URL` from the bucket settings page into your environment variables so Statamic can generate public URLs for your assets.

## Refresh the Stache on deploy

Statamic indexes your content in a cache called the Stache. If your content lives in your repository, refresh the Stache after each deployment so Statamic picks up new and changed files:

```bash theme={null}
php please stache:refresh
```

Add this command to your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Deploy commands don't persist filesystem changes, so attach a [cache](https://laravel.com/cloud/docs/resources/caches/valkey) to your environment and use it as your application's cache store. Statamic then stores the Stache in the cache, where every replica can read it.

## Enable static caching

Statamic's [static caching](https://statamic.dev/static-caching) serves pre-rendered pages instead of building each page on every request. Statamic offers two strategies, and the right one depends on how you scale your App cluster.

### Half measure

The half measure strategy stores rendered pages in your application's cache store. Requests still reach PHP, but Statamic returns the cached response without rendering the page. When your cache store is a Cloud [cache](https://laravel.com/cloud/docs/resources/caches/valkey), every replica shares the same cached pages, so this strategy works with [autoscaling](https://laravel.com/cloud/docs/compute#autoscaling).

Set the following environment variable and deploy:

```bash theme={null}
STATAMIC_STATIC_CACHING_STRATEGY=half
```

### Full measure

The full measure strategy writes each page as an HTML file to `public/static`. When your application requires `statamic/cms`, Cloud detects it at deploy time and configures NGINX to serve those files directly, so requests for cached pages never reach PHP. Form submissions and live previews continue to route to your application. You don't need to write any custom NGINX configuration.

Set the following environment variable and deploy:

```bash theme={null}
STATAMIC_STATIC_CACHING_STRATEGY=full
```

> [!WARNING]
>
> The full measure cache lives on each instance's local filesystem, and each deployment clears it. Statamic invalidates the cache only on the instance that handled a content change, so additional replicas would keep serving stale pages. When using the full measure strategy, set your App cluster's [autoscaling strategy](https://laravel.com/cloud/docs/compute#autoscaling) to **None** and scale vertically by choosing a larger instance size instead of adding replicas.

If your site needs to scale horizontally, use the [half measure](#half-measure) strategy instead.

## Monitor your site

Once your site is live, [Laravel Nightwatch](https://nightwatch.laravel.com) shows you slow requests, exceptions, queued jobs, and cache hit rates. Use it to confirm that static caching is doing its job. You can [connect Nightwatch to your environment](https://laravel.com/cloud/docs/environments#nightwatch-integration) directly from the Cloud dashboard.

## Frequently asked questions

**Do I need Statamic Pro to deploy on Cloud?**

No. Statamic Solo and Pro both run on Cloud. Check [Statamic's pricing page](https://statamic.com/pricing) for features, such as multiple control panel users, that require a Pro license.

**Why did my control panel changes disappear after a deployment?**

Statamic writes content saved as flat files in production to the ephemeral filesystem, and each deployment resets that filesystem. Edit content locally and commit it, or [store content in a database](#decide-where-your-content-lives).

**Why are some visitors seeing outdated pages?**

If you use the full measure strategy with more than one replica, only the instance that handled a content change clears its cache. Set your App cluster's autoscaling strategy to **None**, or switch to the [half measure](#half-measure) strategy.

**Does static caching affect applications that don't use Statamic?**

No. Cloud configures NGINX for static caching only when your application requires `statamic/cms`.
