Source: https://laravel.com/cloud/docs/resources/caches/redis.md

# Redis by Upstash (deprecated)

Redis by Upstash is deprecated and isn’t available for new applications. New applications should use Laravel Valkey.

&#x20;Powered by [Upstash](https://upstash.com)

> [!WARNING]
>
> **Redis by Upstash is deprecated.** You can no longer create new Redis by Upstash caches. Laravel Cloud supports existing caches until **August 31, 2027**. After that date, Laravel Cloud deletes any remaining caches.
>
> Existing caches move to [higher monthly prices](https://laravel.com/cloud/docs/pricing#redis-by-upstash) on **November 30, 2026** to align with Upstash's list pricing.
>
> Beginning **October 1, 2026**, Upstash also resumes enforcing monthly data transfer allowances. See [Bandwidth limits and auto-upgrades](#bandwidth-limits-and-auto-upgrades).
>
> We recommend migrating to a [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) cache, which offers Redis API compatibility, better performance, and more precise per-second billing. Our [migration guide](https://laravel.com/cloud/docs/knowledge-base/migrate-upstash-to-valkey) walks through moving your cache, sessions, queues, and Redis data.
>
> If you need a larger cache, Laravel Cloud also offers managed AWS [ElastiCache](https://laravel.com/cloud/docs/private-cloud/elasticache) caches to Enterprise customers. To learn more, [contact sales](https://laravel.com/cloud/contact).

## Introduction

Laravel Cloud offers an alternative cache through a partnership with Upstash. Redis by Upstash caches offer the following features:

* Multiple cache sizes, from 250MB to 500GB.
* Automatic upsizing.
* Metrics and monitoring.

You can use a cache to store application data, back queue systems, and manage sessions, or you can access it directly through the Redis API. Laravel applications can use Laravel's [cache](https://laravel.com/docs/cache), [queues](https://laravel.com/docs/queues), [sessions](https://laravel.com/docs/session), and [Redis API](https://laravel.com/docs/redis) integrations.

## Connecting to Redis by Upstash

### From your application

When you attach a cache to an environment, Laravel Cloud automatically injects connection environment variables, including `REDIS_HOST` and `REDIS_PASSWORD`. Laravel applications can also use `CACHE_STORE` with the `Cache` facade. You may view these variables in your environment's **General Settings**.

### From your local machine

To connect to your Redis by Upstash cache from your local machine, navigate to **Organization > Resources > Caches**, click your cache, and click **View credentials** at the top of the page. From your environment's canvas, you can also open the cache's **...** menu and select **View details** to reach this page.

The cache credentials modal shows the credentials you need to connect to your cache.

## Editing and resizing your cache

You may edit and resize a Redis by Upstash cache from your organization's **Resources** page. Navigate to the **Caches** tab and click the **...** icon for the cache you would like to edit or resize. Then, click **Edit settings**.

## Bandwidth limits and auto-upgrades

Each cache size includes a monthly data transfer allowance, listed on the [pricing page](https://laravel.com/cloud/docs/pricing#redis-by-upstash). Usage is measured per calendar month and resets on the first day of each month. Beginning **October 1, 2026**, Upstash enforces these allowances.

What happens when a cache uses up its allowance depends on its auto-upgrade setting, which you may change from the cache's **Edit settings** dialog:

* **Auto-upgrade enabled**: Upstash moves the cache to the next size, and Laravel Cloud bills the cache at that size from that point forward. Upstash doesn't move the cache back down automatically, so resize it manually if you no longer need the larger size. You will receive an email when a cache auto-upgrades.
* **Auto-upgrade disabled (the default)**: The cache stops accepting connections until the next calendar month begins or you resize it to a larger size. Your application will receive connection errors in the meantime. Laravel Cloud alerts you as a cache approaches its allowance so you can act before this happens.

You may check a cache's data transfer for the current month from its [metrics](#monitoring-cache-metrics). If a cache regularly approaches its allowance, migrating to [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) removes the limit entirely, since Valkey has no data transfer allowance or bandwidth charge.

## Detaching and deleting your cache

If your project no longer needs a cache, you can detach it from your application canvas.

> [!WARNING]
>
> **Detaching a cache does not delete it.** Since many applications can share a cache, you can only detach a cache from your application. You can't delete it there.
>
> Laravel Cloud bills caches for their availability, whether or not an application uses them. To permanently delete a cache, visit your [organization's Resources page](https://laravel.com/to/org/resources/caches).

You may delete a Redis by Upstash cache from your [organization's Resources page](https://laravel.com/to/org/resources/caches). Navigate to the **Caches** tab and click the **...** icon for the cache you would like to delete. Then, click **Delete cache**.

## Monitoring cache metrics

To view metrics such as storage usage, data transfer, throughput, and cache hits and misses for Redis by Upstash, navigate to **Organization > Resources > Caches**, click your cache, and review the **Metrics** section. Use the time range selector to adjust the period shown. You can also select **... > View metrics** on the cache card to jump directly to this section. See [Cache metrics](https://laravel.com/cloud/docs/metrics/caches) for what each chart means.
