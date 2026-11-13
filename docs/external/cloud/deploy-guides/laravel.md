Source: https://laravel.com/cloud/docs/deploy-guides/laravel.md

# Laravel deploy guide

Configure your Laravel application for production on Laravel Cloud.

The [Laravel quickstart](https://laravel.com/cloud/docs/quickstart#laravel) walks you through your first deployment to Laravel Cloud. Cloud already handles most of what a Laravel application needs in production. This guide focuses on the handful of decisions that are still yours to make, such as how you build your application, how you process jobs, and where your data lives. Each section links to the full documentation if you would like to dig deeper.

## Build your application

Your environment's [build commands](https://laravel.com/cloud/docs/environments#build-commands) run each time you deploy. Typically, they install your production dependencies, compile your frontend assets, and cache your application's configuration:

```sh theme={null}
composer install --no-dev
npm ci --audit false
npm run build
php artisan optimize
```

You should run `php artisan optimize` as part of your build rather than in your deploy commands, so the cached files are baked into your deployment. If you are using Inertia SSR with one of Laravel's [starter kits](https://laravel.com/docs/starter-kits), use `npm run build:ssr` in place of `npm run build`.

If your application installs private Composer packages, configure your credentials before you run `composer install`. The [build commands](https://laravel.com/cloud/docs/environments#build-commands) documentation shows how. And, if you prefer Yarn, pnpm, or Bun over npm, take a look at [Using Yarn, PNPM, or Bun](https://laravel.com/cloud/docs/knowledge-base/using-yarn-bun-pnpm).

## Attach a database

Nearly every Laravel application needs a database. To add one, click **Add database** on your environment's infrastructure canvas, then create or attach a [Laravel MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) or [Laravel Serverless Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) database. The database must be in the same region as your environment.

Once you attach the database, Cloud injects `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE`, and the rest of your connection details into your environment, so Laravel connects to it without any additional configuration. Redeploy your environment so the new variables take effect.

Because Cloud resets your environment's filesystem on every deployment, SQLite is [not supported](https://laravel.com/cloud/docs/knowledge-base/sqlite) in production. If you have been using SQLite locally, Cloud's MySQL and Postgres databases are a great fit.

### Using your database as a cache

Most Laravel applications don't need a dedicated cache. For light to medium workloads, Laravel's `database` cache and session drivers work great. They also keep your infrastructure simple, since there's one less resource to manage and pay for. To use them, point both drivers at your database in your environment variables:

```ini theme={null}
CACHE_STORE=database
SESSION_DRIVER=database
```

If your application grows to the point where it needs a dedicated cache, you may attach a [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) cache by clicking **Cache** on your environment's canvas. Cloud injects the connection details and set `CACHE_STORE` for you, so Laravel starts using the cache right away.

## Run migrations

Database migrations belong in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Cloud runs these commands just before your new deployment goes live, so your database schema is ready by the time the new code starts serving requests:

```sh theme={null}
php artisan migrate --force
```

Deploy commands must finish within 15 minutes. Cloud doesn't keep any changes they make to the filesystem, so deploy commands are best suited to tasks like migrations that write to external resources.

You do not need to run `queue:restart` or `horizon:terminate` yourself, since Cloud restarts your queue workers and manages Horizon for you after every deployment. You should also avoid running `optimize:clear` and `storage:link` during deployment. The [unnecessary build and deploy commands](https://laravel.com/cloud/docs/environments#unnecessary-build-and-deploy-commands) documentation explains why.

## Environment variables

Cloud writes your environment variables to a `.env` file before your application starts, so Laravel reads them exactly the way it does on your local machine. You can manage these values from your environment's [settings](https://laravel.com/cloud/docs/environments#environment-variables).

In addition to the variables Cloud injects for your attached resources, you may define any variables your application needs. If you define a variable that Cloud also injects, your value takes precedence. Remember to redeploy after changing your environment variables so your application picks up the new values.

## Store files in object storage

Your environment's [filesystem](https://laravel.com/cloud/docs/environments#filesystem) is ephemeral. Cloud resets it each time you deploy. In addition, each replica of your application has its own disk, so a file written while handling one request may not be visible to the next.

For user uploads and any other files your application needs to keep, attach a [bucket](https://laravel.com/cloud/docs/resources/object-storage) to your environment. Cloud injects `FILESYSTEM_DISK` along with the bucket's S3-compatible credentials, so you can work with your files through Laravel's `Storage` facade just like you would locally. Before you do, add the `league/flysystem-aws-s3-v3` package to your application's dependencies:

```sh theme={null}
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

## Process queued jobs

[Managed queues](https://laravel.com/cloud/docs/queues) are the easiest way to process your application's queued jobs on Cloud. Cloud provisions the queue for you and automatically scales its workers based on how many jobs are waiting, so you do not need to manage any queue infrastructure yourself. Managed queues require a recent version of Laravel and the `aws/aws-sdk-php` package. You can find the exact requirements in the [managed queue documentation](https://laravel.com/cloud/docs/queues#connect-your-application).

When you deploy a managed queue, Cloud sets `QUEUE_CONNECTION=cloud` for your environment. From then on, any job dispatched without an explicit connection is sent to your managed queue, including jobs that the `database` or `redis` driver previously processed.

If you would rather keep using your own queue driver, you may run `queue:work` processes on your App cluster or on a dedicated [worker cluster](https://laravel.com/cloud/docs/workers#laravel-queue-workers) instead.

## Schedule tasks

To run your application's [scheduled tasks](https://laravel.com/cloud/docs/scheduled-tasks), enable the **Scheduler** toggle on your App cluster or on a worker cluster. Cloud then invokes `schedule:run` every minute, just like a traditional cron entry.

If your App cluster runs multiple replicas, you should use Laravel's `onOneServer` method for any task that should run only once. Otherwise, the task runs on every replica.
And, if your environment [scales to zero](https://laravel.com/cloud/docs/compute#scale-to-zero), don't worry: Cloud automatically wakes your environment so your scheduled tasks keep running on time.
