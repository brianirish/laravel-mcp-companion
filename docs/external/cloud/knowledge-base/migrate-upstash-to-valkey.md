Source: https://laravel.com/cloud/docs/knowledge-base/migrate-upstash-to-valkey.md

# Migrate from Redis by Upstash to Laravel Valkey

Learn how to migrate your application's cache, sessions, queues, and Redis data from Redis by Upstash to Laravel Valkey.

[Redis by Upstash](https://laravel.com/cloud/docs/resources/caches/redis) is deprecated and scheduled to be sunset. Its replacement is [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey), a fully managed, Redis-compatible cache with better performance and per-second billing. This guide walks through moving an environment from an Upstash cache to a Valkey cache.

> [!WARNING]
>
> Beginning **October 1, 2026**, Upstash will resume enforcing the monthly data transfer allowance included with each cache size. Depending on your auto-upgrade settings, Upstash may upgrade your cache to the next size up or disable your connections for the rest of the month. See [Bandwidth limits and auto-upgrades](https://laravel.com/cloud/docs/resources/caches/redis#bandwidth-limits-and-auto-upgrades) for details, and check your cache's metrics to see how close it is to its allowance.
>
> Redis by Upstash pricing also increases on **November 30, 2026** to align with Upstash's list pricing. Eligible customers who migrate to [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) and delete their Upstash cache before that date will receive a Cloud credit based on two months of the cache's monthly price. See the [pricing page](https://laravel.com/cloud/docs/pricing#redis-by-upstash) for the current and upcoming prices.
>
> Existing Redis by Upstash caches remain available under the higher pricing and bandwidth limits until **August 31, 2027**. After that date, any remaining caches will be deleted.

Valkey is compatible with the Redis API your application already uses, so your application code does not need to change. Migrating comes down to two decisions. You point your environment at the new store, and you decide what, if anything, must happen to the data in the old one.

[Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) is the right destination for most applications. Enterprise customers on [Private Cloud](https://laravel.com/cloud/docs/private-cloud) may instead migrate to a managed AWS [ElastiCache](https://laravel.com/cloud/docs/private-cloud/elasticache) cache. ElastiCache is available with both Valkey and Redis OSS engines and adds automatic failover and multi-AZ deployments. Either way, the destination is a Redis-compatible store, so every path in this guide applies unchanged. To provision ElastiCache, [contact us](https://laravel.com/enterprise).

## Before you start

An environment has one attached cache at a time. Replacing it updates the injected `REDIS_*` environment variables on the next deployment. Detaching a cache does not delete it, so your Upstash cache remains available and billable until you delete it from your organization's Resources page. Its credentials remain valid, so you can run both caches side by side during the migration.

The `UPSTASH_*` and `VALKEY_*` variables in this guide are temporary, and only the migration tooling uses them. Remove them when the migration is complete.

First, work out what your application keeps in its cache. The answer determines how careful you need to be:

| Setting | What you are storing |
| - | - |
| `CACHE_STORE=redis` | Application cache, plus cache-based rate limiters and atomic locks |
| `SESSION_DRIVER=redis` | User sessions |
| `QUEUE_CONNECTION=redis` | Queued jobs, including delayed jobs and pending retries |
| `Redis` facade usage in your code | Anything your application writes to Redis directly |

Then pick your path:

| Path | Use when | Downtime |
| - | - | - |
| 1. [Start fresh](#start-fresh) | Cache only, or you can tolerate losing sessions and pending jobs | None |
| 2. [Drain your queues](#drain-your-queues) | You must not lose queued jobs or sessions | None |
| 3. [Copy the data](#copy-the-data) | Long-lived data you cannot lose or wait out | Maintenance window |

## Start fresh

If Upstash backs only your application's cache, there is no data worth moving. Caches rebuild themselves.

**1. Attach a Valkey cache**

On your environment's canvas, open the **...** menu on the cache card and choose **Replace**. Then select a [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) cache, or create one if needed. Replacing only re-points the environment at the new cache. Nothing changes for your running application until the next deployment.

**2. Deploy**

Redeploy the environment. The injected `REDIS_*` variables now point at Valkey.

**3. Clean up**

Once you have verified the application, delete the Upstash cache from your organization's Resources page. Laravel Cloud bills detached caches until you delete them.

The new cache starts empty, so cache reads miss until it rebuilds. On high-traffic applications, deploy during a low-traffic window to limit the temporary increase in database load. Redis-backed sessions reset, so users must sign in again. Forms submitted across the cutover may receive a `419 Page Expired` response. Use the [session drain](#keeping-users-signed-in) if that is unacceptable. Atomic locks and rate limiters also reset, so a `withoutOverlapping` scheduled task or a `ShouldBeUnique` job could run twice during the deployment.

> [!WARNING]
>
> If `QUEUE_CONNECTION=redis`, your workers never process the jobs still in the old store after the swap, including delayed jobs. Before you cut over, run `php artisan queue:monitor redis:default` from the **Commands** tab and list each queue name you dispatch to. If the count is not zero and those jobs matter, use [Path 2](#drain-your-queues) instead.

## Drain your queues

Queue data changes while your application runs, so do not copy it between stores. Run both stores side by side instead. New jobs dispatch to Valkey while a worker drains the jobs that remain on Upstash.

**1. Save the Upstash credentials**

Before swapping the cache, copy the current values of `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, and `REDIS_SCHEME` from your environment's variables into new custom variables: `UPSTASH_REDIS_HOST`, `UPSTASH_REDIS_PORT`, `UPSTASH_REDIS_PASSWORD`, and `UPSTASH_REDIS_SCHEME`. These variables mirror the values your application connects with today, so they are already in the right format.

**2. Define the drain connections**

Add a Redis connection for the old store in `config/database.php`:

```php theme={null}
// config/database.php, inside the 'redis' array...

'upstash' => [
    'host' => env('UPSTASH_REDIS_HOST'),
    'password' => env('UPSTASH_REDIS_PASSWORD'),
    'port' => env('UPSTASH_REDIS_PORT', '6379'),
    'scheme' => env('UPSTASH_REDIS_SCHEME', 'tls'),
    'database' => env('REDIS_DB', '0'),
],
```

Then add a queue connection that uses it in `config/queue.php`:

```php theme={null}
// config/queue.php, inside the 'connections' array...

'upstash' => [
    'driver' => 'redis',
    'connection' => 'upstash',
    'queue' => env('REDIS_QUEUE', 'default'),
    'retry_after' => (int) env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```

Commit these changes.

**3. Swap the cache and deploy**

Attach the Valkey cache to the environment and deploy. From this moment, every `dispatch()` lands on Valkey because the default Redis connection now resolves to the new store. Your cache and sessions cut over in the same deployment, so the expectations from [Path 1](#start-fresh) apply to them here.

**4. Run a drain worker**

Add a [background process](https://laravel.com/cloud/docs/workers#app-cluster-background-processes) running `php artisan queue:work upstash` and deploy. If you dispatch to multiple queues, list them: `php artisan queue:work upstash --queue=default,emails`. For a small backlog with no delayed jobs, a one-off run of `php artisan queue:work upstash --stop-when-empty` from the **Commands** tab is enough.

**5. Watch until empty**

Check progress from the **Commands** tab with `php artisan queue:monitor upstash:default`, again listing each queue name. The reported size includes delayed and reserved jobs, so zero means the drain is done.

Don't rely on `--stop-when-empty` as your completion signal. It exits as soon as no job is ready right now, even if delayed jobs are still scheduled for the future. `queue:monitor` is the source of truth.

**6. Tear down**

Retry or delete failed jobs before you remove the old connection. Laravel re-dispatches a retried job onto the connection recorded on the failed job. Then remove the drain worker, the two config blocks, and the `UPSTASH_*` variables. Deploy, and delete the Upstash cache from the Resources page.

If you run Horizon, keep it pointed at the default connection and drain the old store with a plain `queue:work` background process. Horizon's internal state lives in Redis, so its dashboard metrics reset at the swap. For job-level visibility that survives the migration, [Laravel Nightwatch](https://nightwatch.laravel.com) traces queue jobs independently of which store backs them.

> [!TIP]
>
> If you are rethinking your queue setup anyway, consider draining to [managed queues](https://laravel.com/cloud/docs/queues#managed-queues) instead of Valkey. The pattern is identical. Create the managed queue so new jobs dispatch to the `cloud` connection, then drain the old Redis store with the same worker and monitor commands.

## Keeping users signed in

By default, sessions reset at the swap and users sign in again. That may be unacceptable if you have long-lived logins, carts kept in the session, or an active admin panel. In that case, you can drain sessions like queues. A temporary read-through session handler checks the new store first and falls back to the old one.

Laravel saves the session at the end of every request. After cutover, the first request from a returning visitor reads their session from Upstash through the fallback and writes it to Valkey. Redis-backed sessions expire `SESSION_LIFETIME` minutes (120 by default) after the user's last request, so keep the fallback in place for one session lifetime after cutover. Any session that remains on Upstash after that period has expired normally.

Reusing the `upstash` Redis connection from the [drain](#drain-your-queues) setup, define a cache store for it in `config/cache.php`:

```php theme={null}
// config/cache.php, inside the 'stores' array...

'upstash-sessions' => [
    'driver' => 'redis',
    'connection' => 'upstash',
],
```

Create the handler:

```php theme={null}
<?php

namespace App\Sessions;

use SessionHandlerInterface;

class DrainingSessionHandler implements SessionHandlerInterface
{
    public function __construct(
        protected SessionHandlerInterface $new,
        protected SessionHandlerInterface $old,
    ) {}

    public function read($id): string|false
    {
        return $this->new->read($id) ?: $this->old->read($id);
    }

    public function write($id, $data): bool
    {
        return $this->new->write($id, $data);
    }

    public function destroy($id): bool
    {
        $this->new->destroy($id);
        $this->old->destroy($id);

        return true;
    }

    public function open($path, $name): bool
    {
        return true;
    }

    public function close(): bool
    {
        return true;
    }

    public function gc($max_lifetime): int
    {
        return 0; // Expiry is handled by the cache TTLs...
    }
}
```

Register it as a session driver in the `boot` method of `app/Providers/AppServiceProvider.php`:

```php theme={null}
use App\Sessions\DrainingSessionHandler;
use Illuminate\Session\CacheBasedSessionHandler;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Session;

Session::extend('drain', function ($app) {
    $minutes = $app['config']['session.lifetime'];

    return new DrainingSessionHandler(
        new CacheBasedSessionHandler(Cache::store('redis'), $minutes),
        new CacheBasedSessionHandler(Cache::store('upstash-sessions'), $minutes),
    );
});
```

Set `SESSION_DRIVER=drain` so the new driver deploys together with the cache swap. The `destroy` method clears both stores, so the fallback can't undo a sign-out. Rolling back mid-window takes only an environment variable change. On Laravel Cloud, the injected configuration points the `default` and `cache` Redis connections at the same store and database, so the keys written here line up with the built-in `redis` session driver.

Once one session lifetime has passed after cutover, set `SESSION_DRIVER` back to `redis` and redeploy before you delete the Upstash cache. With the driver reverted, remove the handler, cache store, and connection with the rest of the drain teardown. If your application has very long session lifetimes, keep in mind that the old cache must stay alive, and keep billing, for the whole window.

## Copy the data

Sometimes the data itself must survive. Your application may store long-lived values through the `Redis` facade, sessions you cannot invalidate, cache entries too expensive to rebuild, or delayed jobs scheduled further out than you can reasonably drain.

Upstash does not expose Redis replication commands (`REPLICAOF`, `PSYNC`) to clients, so a live, zero-downtime replication into Valkey is not possible. You can't restore an Upstash backup either. Upstash runs Redis 8.x, and Valkey, which is Redis 7.2-compatible, cannot load its export format. `DUMP` and `RESTORE` fail for the same reason. The reliable path is a client-side copy that reads each key with its type's native commands and writes it to the new store. The [migration command](#the-migration-command) in this guide does exactly that.

A copy like this is point-in-time. Anything your application writes to the old store after the copy reaches that key is silently lost, so you must freeze writes for the duration. **This path requires a maintenance window** roughly the length of the copy plus a deployment.

**1. Prepare (no downtime yet)**

Create the Valkey cache but do not attach it. Navigate to **Organization > Resources > Caches**, click the cache, and click **View credentials** at the top of the page. Add the connection details as custom environment variables: `VALKEY_REDIS_HOST`, `VALKEY_REDIS_PORT`, `VALKEY_REDIS_USERNAME`, and `VALKEY_REDIS_PASSWORD`. Copy the current injected `REDIS_*` values into `UPSTASH_*` variables as in [Path 2](#drain-your-queues).

Set the maintenance mode variables so all instances share the "down" state and it survives the cache swap:

```ini theme={null}
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

The store must be `database`, not `redis`. If you keep maintenance state in the cache you are migrating away from, you lose it mid-migration.

Add both Redis connections to `config/database.php`:

```php theme={null}
// config/database.php, inside the 'redis' array...

'upstash' => [
    'host' => env('UPSTASH_REDIS_HOST'),
    'password' => env('UPSTASH_REDIS_PASSWORD'),
    'port' => env('UPSTASH_REDIS_PORT', '6379'),
    'scheme' => env('UPSTASH_REDIS_SCHEME', 'tls'),
    'database' => 0,
    'prefix' => '',
],

'valkey' => [
    'host' => env('VALKEY_REDIS_HOST'),
    'username' => env('VALKEY_REDIS_USERNAME'),
    'password' => env('VALKEY_REDIS_PASSWORD'),
    'port' => env('VALKEY_REDIS_PORT', '6379'),
    'scheme' => 'tls',
    'database' => 0,
    'prefix' => '',
],
```

The empty `prefix` matters. `SCAN` returns raw keys that already carry your application's key prefix, so the copy connections must not apply a prefix of their own. Otherwise, every key would be double-prefixed on write. With an empty prefix, the command copies keys byte-for-byte.

Finally, add the [`cache:migrate` command](#the-migration-command) to your application, commit, and deploy. Nothing has changed for your users yet.

**2. Count the keyspace**

From the **Commands** tab, run `php artisan cache:migrate --dry-run` to count keys by type without copying anything. As a rough planning figure, expect the copy to move a few hundred keys per second. Size your maintenance window to match.

**3. Freeze writes**

Run `php artisan down` from the **Commands** tab. Then stop everything else that writes to Redis. Pause any [managed queues](https://laravel.com/cloud/docs/queues#pausing-and-purging), remove or scale down `queue:work` background processes, and disable the **Scheduler** toggle on your compute cluster. These changes deploy with the environment. `php artisan down` only stops web traffic. Workers and the scheduler keep running until you stop them explicitly.

**4. Copy**

Run `php artisan cache:migrate` from the **Commands** tab. The command replaces each destination key before writing, so it is idempotent and safe to re-run if interrupted.

**5. Swap and verify**

Attach the Valkey cache to the environment and deploy. Then compare key counts by running `php artisan cache:migrate --from=valkey --dry-run` against the source's earlier count. A small difference is normal because keys with short TTLs expire during the window.

**6. Resume**

Run `php artisan up`, re-enable the scheduler and workers, and resume any paused queues. After a burn-in period, remove the migration command, the config blocks, and the `UPSTASH_*` and `VALKEY_*` variables. Then delete the Upstash cache from the Resources page.

### The migration command

This command copies every key from one Redis connection to another with each type's native read and write commands, and it keeps each key's TTL. The command targets phpredis, Laravel's default Redis client. If your application sets `REDIS_CLIENT=predis`, a few calls, such as the `zAdd` argument order, need adapting.

```php theme={null}
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Redis\Connections\Connection;
use Illuminate\Support\Facades\Redis;

class MigrateCache extends Command
{
    protected $signature = 'cache:migrate
                            {--from=upstash : The source Redis connection}
                            {--to=valkey : The destination Redis connection}
                            {--chunk=1000 : Keys per SCAN iteration}
                            {--dry-run : Count keys by type without copying}';

    protected $description = 'Copy every key from one Redis connection to another';

    public function handle(): int
    {
        $source = Redis::connection($this->option('from'));
        $destination = $this->option('dry-run') ? null : Redis::connection($this->option('to'));

        $counts = [];
        $cursor = null;

        do {
            [$cursor, $keys] = $source->scan(
                $cursor, ['match' => '*', 'count' => (int) $this->option('chunk')]
            ) ?: [0, []];

            foreach ($keys as $key) {
                $type = $this->typeOf($source, $key);

                if ($destination && ! $this->copy($source, $destination, $key, $type)) {
                    $this->warn("Skipped [{$key}] of unsupported type [{$type}].");

                    continue;
                }

                $counts[$type] = ($counts[$type] ?? 0) + 1;
            }
        } while ((int) $cursor !== 0);

        $this->table(
            ['Type', $destination ? 'Copied' : 'Counted'],
            collect($counts)->map(fn ($count, $type) => [$type, $count])->values()
        );

        return static::SUCCESS;
    }

    protected function copy(Connection $source, Connection $destination, string $key, string $type): bool
    {
        $ttl = $source->pttl($key);

        if ($ttl === -2) {
            return true; // The key expired mid-scan...
        }

        $destination->del($key);

        $copied = match ($type) {
            'string' => $destination->set($key, $source->get($key)),
            'hash' => $destination->hmset($key, $source->hgetall($key)),
            'list' => $destination->rpush($key, ...$source->lrange($key, 0, -1)),
            'set' => $destination->sadd($key, ...$source->smembers($key)),
            'zset' => $destination->zadd($key, ...collect($source->zrange($key, 0, -1, true))
                ->flatMap(fn ($score, $member) => [$score, $member])->all()),
            default => false,
        };

        if ($copied !== false && $ttl > 0) {
            $destination->pexpire($key, $ttl);
        }

        return $copied !== false;
    }

    protected function typeOf(Connection $connection, string $key): string
    {
        $type = $connection->type($key);

        return match ($type) {
            \Redis::REDIS_STRING => 'string',
            \Redis::REDIS_SET => 'set',
            \Redis::REDIS_LIST => 'list',
            \Redis::REDIS_ZSET => 'zset',
            \Redis::REDIS_HASH => 'hash',
            \Redis::REDIS_STREAM => 'stream',
            default => is_string($type) ? strtolower($type) : 'unknown',
        };
    }
}
```

> [!NOTE]
>
> The command skips Redis streams because it can't copy consumer group state faithfully. It also reads each key's value in a single call, so very large individual keys, such as a hash with millions of fields, may need chunked copying with `HSCAN` instead. Neither limitation affects most Laravel applications.

## Using an AI agent

An AI coding agent can help with this migration when it has this guide, your application's repository, and an authenticated [Laravel Cloud CLI](https://laravel.com/cloud/docs/api/cli). Ask the agent to assess the application first, then approve each user-facing or irreversible step yourself.

```text theme={null}
Read https://laravel.com/cloud/docs/knowledge-base/migrate-upstash-to-valkey and assess this
application's migration from Redis by Upstash to Laravel Valkey. Make no changes yet.

Inspect the Cloud environment's CACHE_STORE, SESSION_DRIVER, and QUEUE_CONNECTION settings; search
the repository for Redis usage, delayed job dispatches, and queue names; and check each queue's
backlog. Recommend a migration path, describe the cutover effects, and show the complete plan.

After I approve the plan, make the code changes on a branch and show me the diff before committing.
Stop and ask before swapping the cache, deploying, enabling maintenance mode, or deleting anything.
Before teardown, verify that the old queue is empty or that the source and destination key counts
match. Do not delete the Upstash cache until I confirm the application is healthy.
```

## Need help?

If you get stuck at any point, or you have an unusual cache workload you are not sure how to migrate, contact support from the **Help** portal in your Laravel Cloud dashboard before you cut over. Talking through the approach in advance is far easier than recovering a failed migration. When you reach out, mention which path you are on and what you use your key-value store for, such as cache, sessions, queues, or direct `Redis` usage. That context helps the team respond faster.
