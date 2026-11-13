Source: https://laravel.com/cloud/docs/resources/caches/valkey.md

# Laravel Valkey

Fully managed, Redis-compatible cache for your application.

## Introduction

Laravel Valkey is a fully managed, Redis-compatible cache for your application. Laravel Valkey comes in sizes starting at 250MB. It performs better and costs less than industry averages, and it can scale automatically. Flex sizes can also [scale to zero](#scale-to-zero) when idle. All Laravel Valkey instances support up to 10,000 concurrent connections.

Caches can store application data, back queue systems, and manage sessions. You can also access a cache directly through the Redis API. Laravel applications can use Laravel's [cache](https://laravel.com/docs/cache), [queues](https://laravel.com/docs/queues), [sessions](https://laravel.com/docs/session), and [Redis API](https://laravel.com/docs/redis) integrations.

## Creating a Laravel Valkey cache

To attach a Laravel Valkey cache to an environment, click **Cache** on your environment's canvas. Laravel Cloud prompts you to select the cache you would like to attach to the environment or to create a new cache. If you create a new cache, select **Laravel Valkey** as the cache type.


After you attach the cache to an environment, redeploy the environment for the changes to take effect.

Visit the [pricing](https://laravel.com/cloud/docs/pricing#laravel-valkey) docs for information on cache sizes and limits on message sizes.

## Connecting to Laravel Valkey

### From your application

When a cache is attached to an environment, Laravel Cloud automatically injects connection environment variables, including `REDIS_HOST` and `REDIS_PASSWORD`. Laravel applications can also use `CACHE_STORE` with the `Cache` facade. You may view these variables in your environment's General Settings.

### From your local machine

To connect to Laravel Valkey from your local machine, navigate to **Organization > Resources > Caches**, click your cache, and click **View credentials** at the top of the page. From your environment's canvas, you can also open the cache's **...** menu and select **View details** to reach this page.


The cache credentials modal shows the credentials you need to connect to your cache. It also shows a command you can run to connect to your Valkey cache server.

> [!WARNING]
>
> You may connect using a client that supports TLS and SNI. Some cache management tools are incompatible with this connection process.

## Editing and resizing your cache

You may edit and resize a Laravel Valkey cache from your organization's **Resources** page. Navigate to the **Caches** tab and click the **...** icon for the cache you would like to edit or resize. Then, click **Edit settings**.

## Detaching and deleting your cache

If your project no longer needs a cache, you can detach it from your application canvas.


> [!WARNING]
>
> **Detaching a cache does not delete it.** Because many applications can share a cache, you can only detach a cache from your application. You can't delete it from there.
>
> Laravel Cloud bills caches for their availability, regardless of whether an application is using them. To permanently delete a cache, visit your [organization's Resources page](https://laravel.com/to/org/resources/caches).

You may delete a Laravel Valkey cache from your [organization's Resources page](https://laravel.com/to/org/resources/caches). Navigate to the **Caches** tab and click the **...** icon for the cache you would like to delete. Then, click **Delete cache**.

## Picking an eviction policy

When your cache reaches its memory limit, an eviction policy determines which data Valkey removes to make room for new entries. With Laravel Valkey, you can configure this policy based on your application's specific traffic patterns.

By default, we recommend using the `allkeys-lru` policy for most general-purpose use cases. It keeps your most recently accessed data in memory and evicts the items that haven't been touched in a while. That keeps the hit rate high for active users.

If your workload has specific requirements (such as prioritizing keys with expiration timers), you can choose from the following Valkey-native policies:

* `allkeys-lfu`: Evicts the least frequently used keys. Best for workloads where specific "hot" keys stay relevant for long periods.
* `allkeys-random`: Randomly removes keys to make space. Useful for testing or when all data has equal value.
* `volatile-lru`: Evicts the least recently used keys only among those with a TTL set. Best when you want to protect "permanent" keys from eviction.
* `volatile-lfu`: Evicts the least frequently used keys only among those with a TTL set. Best for frequency-based scaling with specific transient data.
* `volatile-random`: Randomly removes keys that have a TTL set. Rarely needed. Minimizes overhead but is unpredictable.
* `volatile-ttl`: Removes keys with a TTL set, starting with the shortest remaining life. Best when you want the "soonest to expire" to go first.
* `noeviction`: Returns an error when the memory limit is reached.

## Scale to zero

Laravel Valkey Flex sizes can scale to zero. A Flex cache sleeps when it's idle, and you aren't billed for compute while it sleeps. Before the cache sleeps, Laravel Cloud snapshots its contents to disk, then restores them transparently when the cache wakes, so you keep your data.

Scale to zero is enabled by default on Flex caches. If you need a cache to stay awake, disable scale to zero in the cache's settings. Larger Pro sizes are always-on and do not scale to zero. Pairing a Flex cache that scales to zero with [application compute that scales to zero](https://laravel.com/cloud/docs/compute#scale-to-zero) helps minimize costs on development environments and side projects.

## Automatic upsizing

Laravel Valkey has hard limits on usage, such as commands per second and message size. When your cache reaches these limits, its performance may degrade or it may stop accepting new requests.

Laravel Cloud offers automatic upsizing for Laravel Valkey, so your cache keeps running smoothly as your usage grows. You can enable or disable this feature at any time.


### How automatic upsizing works

1. **Provisioning and configuration.** When you create or update a cache with automatic upsizing enabled, Laravel Cloud provisions the cache and configures its upsizing settings.
2. **Monitoring.** Laravel Cloud continuously monitors your cache's usage. If your cache approaches its usage limits, Laravel Cloud prepares to upsize it.
3. **Notifications.** When your cache reaches a threshold or an upsize starts, Laravel Cloud sends you an alert [notification](https://laravel.com/cloud/docs/notifications).
4. **Upsizing without downtime.** Laravel Cloud moves your cache to the next available size in the background, with no downtime for your application.

> [!WARNING]
>
> With automatic upsizing enabled, your cache scales automatically **up to your current plan's maximum capacity**. On the Growth plan, you may [contact support](https://laravel.com/cloud/docs/support) to [raise this limit](https://laravel.com/cloud/docs/pricing#raising-plan-limits). On the Starter plan, upgrade to Growth to use larger cache sizes.

After an upsize, Laravel Cloud adjusts your billing to reflect the new cache size. See the [pricing](https://laravel.com/cloud/docs/pricing#laravel-valkey) documentation for details.

## Monitoring cache metrics

To view metrics such as storage usage, throughput, and cache hits and misses for Laravel Valkey, navigate to **Organization > Resources > Caches**, click your cache, and review the **Metrics** section. Use the time range selector to adjust the period shown. You can also select **... > View metrics** on the cache card to jump directly to this section. See [Cache metrics](https://laravel.com/cloud/docs/metrics/caches) for what each chart means.

## Troubleshooting

### Handling transient connection errors

Your cache may restart as part of normal operations, such as feature updates and security updates. A restart may cause transient errors with some PHP clients, such as `Error while reading line from the server` or `read error on connection to tls`.

These errors are expected because a TCP connection cannot survive a server restart.

To handle them, we recommend that your application:

1. Catches transient errors.
2. Automatically reconnects to the cache through a new, healthy connection.

We recommend following the [retry and backoff best practices](https://laravel.com/docs/13.x/redis#retry-and-backoff-configuration) in the Laravel documentation.

### Connection force-closed

For the safety of your cache, we enforce a maximum size for messages sent to your cache. The [Laravel Valkey pricing table](https://laravel.com/cloud/docs/pricing#laravel-valkey) lists the limit for each cache size. If a client sends a message that exceeds this limit, we treat it as a protocol violation and immediately force-close the TCP connection.

Because the server drops the connection, your client won't receive a standard error response. Instead, it registers a low-level network error, such as:

* `Error while reading line from the server` (PHP)
* `Error: read ECONNRESET` (Node.js)
* `Connection reset by peer` (Python and Java)

To fix the error, reduce the message size or upgrade your cache size.
