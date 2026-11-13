Source: https://laravel.com/cloud/docs/queues.md

# Managed Queues

Process Laravel and Symfony jobs with fully managed queues.

## Introduction

Background jobs allow your application to defer slow or expensive work, such as sending email, generating PDFs, calling external APIs, or processing media, so that it can respond to web requests quickly.

Managed queues are available for Laravel and Symfony applications. To run custom background processes on any supported runtime, see [Workers](https://laravel.com/cloud/docs/workers).

Managed queues isolate background jobs from your web traffic and run them on dedicated workers that scale with the work waiting to be processed. Flex workers scale to zero when idle, so you pay for compute only while jobs run. The Queues dashboard provides metrics, failed-job visibility, and retry controls.

## Managed queues vs. workers

Managed queues are the preferred choice for all new and existing Laravel and Symfony applications. Laravel Cloud provisions and operates the queue infrastructure, so you do not need to manage queue workers or drivers yourself.

Use [Workers](https://laravel.com/cloud/docs/workers) when your application needs a custom long-running process or must continue using a self-managed queue driver, such as Redis or a database queue. Workers are available for every supported runtime, but you configure the command, process count, autoscaling, and operational behavior yourself.

## Managed queues

Each managed queue has its own worker pool, memory allocation, and autoscaling range. Laravel Cloud provisions each queue in its environment's region.


The number of queues available is based on your plan and applies to each environment:

| Plan | Managed queues per environment |
| - | - |
| Starter | 1 |
| Growth | 10 |
| Business | 50 |
| Enterprise | 50 |

Business and Enterprise organizations that need more queues per environment may [contact support](https://laravel.com/cloud/docs/support) to raise this limit.

If you are on the Growth plan and need more queues per environment, [contact support](https://laravel.com/cloud/docs/support) to [request a higher limit](https://laravel.com/cloud/docs/pricing#raising-plan-limits).

> [!TIP]
>
> A single queue is sufficient for most applications. Create separate queues when workloads need different memory allocations or autoscaling ranges.

## Configure managed queues

### Creating a managed queue

Open your environment, click **Add compute** on the canvas toolbar, then **Managed queue**. Provide a queue name, choose its [queue type](#queue-types), memory allocation, and [worker autoscaling range](#worker-autoscaling), then deploy the environment.

Once deployed, Laravel Cloud creates the queue, configures access from your application, and starts its worker pool. Queue names may contain letters, numbers, hyphens, and underscores. Names must be 39 characters or fewer, including the `.fifo` suffix for FIFO queues.

Each managed queue handles one queue name. The first queue you create becomes the environment's default queue. To change the default queue, select **Set as default** from a queue's canvas menu.

### Queue types

Each managed queue is either a standard queue or a FIFO queue. You choose the type when creating the queue and cannot change it afterward.

**Standard queues** provide at-least-once delivery with best-effort ordering and support per-job delays of up to 15 minutes. They are the right choice for most workloads.

**FIFO queues** deliver jobs in dispatch order and deduplicate jobs on arrival. They suit order-sensitive workloads such as payment processing and ledger updates. FIFO queues do not support per-job delays and have a small operations premium.

Laravel Cloud appends `.fifo` to every FIFO queue name. For example, a queue named `orders` becomes `orders.fifo`. A standard `orders` queue and a FIFO `orders.fifo` queue may exist in the same environment.

### Compute classes

Every managed queue runs on either the Flex or Pro compute class:

| | Flex | Pro |
| - | - | - |
| Scaling floor | Scales to zero | Always on, with at least one worker |
| Memory sizes | 256 MiB to 2 GiB | 256 MiB to 8 GiB |
| vCPU | Up to 1 | Up to 4 |
| Job runtime | Up to 90 seconds | No fixed limit |
| Price | Starts at \$0.00000152 per second | Starts at \$0.00000183 per second |

Pro sizes cost 20% more than the equivalent Flex size. Flex is the default and works well for spiky or idle-heavy workloads. Pro is appropriate for steady throughput and for jobs that exceed Flex's runtime or memory limits. Pro is available on the Growth, Business, and Enterprise plans. Enterprise customers on [Private Cloud](https://laravel.com/cloud/docs/private-cloud) can use dedicated Pro sizes up to 16 GiB.

### Memory allocation

Each managed queue worker runs on an instance with configurable memory, and CPU scales proportionally with the selected size. The default, **256 MiB**, is sufficient for typical jobs such as sending email, processing webhooks, updating records, and light data transformation.

| Plan | Flex | Pro |
| - | - | - |
| Starter | 256 MiB to 2 GiB | Not available |
| Growth | 256 MiB to 2 GiB | 256 MiB to 8 GiB |
| Business | 256 MiB to 2 GiB | 256 MiB to 8 GiB |
| Enterprise | 256 MiB to 2 GiB | 256 MiB to 16 GiB |

If a job exceeds its worker's memory allocation, the worker restarts and Laravel Cloud redelivers the job. The failure usually appears as a PHP fatal error reporting that the allowed memory size was exhausted. When workers restart repeatedly, check the **Memory** chart on the Queues dashboard.

See the [queue worker memory sizing guide](https://laravel.com/cloud/docs/knowledge-base/sizing-queue-worker-memory) for guidance on selecting a size.

> [!NOTE]
>
> Managed queue sizes are independent of App and worker cluster sizes. For queues created before Flex and Pro, see [Upgrading from earlier managed queues](#upgrading-from-earlier-managed-queues).

### Worker autoscaling

Each queue scales between a configured minimum and maximum number of workers. The lowest allowed minimum depends on the queue's [compute class](#compute-classes). Choose a maximum that your database, APIs, and other downstream systems can handle in parallel.


| Plan | Maximum workers per queue |
| - | - |
| Starter | 3 |
| Growth | 100 |
| Business | 500 |
| Enterprise | 1,000 |

Business and Enterprise organizations that need more workers per queue may [contact support](https://laravel.com/cloud/docs/support) to raise this limit.

If you are on the Growth plan and need more workers per queue or larger [worker memory sizes](#memory-allocation), [contact support](https://laravel.com/cloud/docs/support) to [request higher limits](https://laravel.com/cloud/docs/pricing#raising-plan-limits).

Laravel Cloud measures queue depth and job duration to add and remove workers. As the queue drains, Laravel Cloud removes workers gradually.

**Scheduled autoscaling.** Managed queues also support scheduled autoscaling, which temporarily changes the minimum and maximum worker count on a one-time or recurring schedule. Scheduled overrides follow the same rules as [scheduled autoscaling](https://laravel.com/cloud/docs/compute#scheduled-autoscaling) for compute clusters.

**Advanced settings.** Organizations with the advanced managed queues entitlement can override visibility and graceful shutdown timeouts from a queue's **Advanced** tab. Flex queues cannot extend the graceful shutdown timeout beyond 90 seconds. Most applications should use Laravel Cloud's defaults.

## Connect your application

> [tab] Laravel
>
> ### Requirements
>
> Managed queues require Laravel 11.55.0, 12.63.0, 13.19.0, or newer and the `aws/aws-sdk-php` package in your `composer.json`:
>
> ```sh theme={null}
> composer update laravel/framework
> composer require aws/aws-sdk-php
> ```
>
> ### Queue connection
>
> When you deploy a managed queue, Laravel Cloud sets `QUEUE_CONNECTION=cloud` for the environment. Jobs dispatched without an explicit connection use the managed queue.
>
> > [!WARNING]
> >
> > Any job dispatched without an explicit connection, including jobs previously processed with the `database`, `redis`, or another driver, routes to a managed queue once one exists in the environment.
>
> To continue using another driver for some jobs, set `QUEUE_CONNECTION` to that driver and dispatch managed-queue jobs explicitly with `->onConnection('cloud')`. Laravel applications that use the default `database` driver are the most likely to be affected.
>
> ### Setting a default queue
>
> The default managed queue receives jobs dispatched without an explicit queue name. For example, `dispatch(new SendEmail)` uses the default queue rather than a queue literally named `default`. You may rename the default queue without changing these dispatch calls.

> [tab] Symfony
>
> ### Requirements
>
> Symfony applications use the [`laravel/laravel-cloud-symfony`](https://github.com/laravel/laravel-cloud-symfony) package, which provides a `cloud` Messenger transport:
>
> ```sh theme={null}
> composer require laravel/laravel-cloud-symfony
> ```
>
> Register its bundle in `config/bundles.php`:
>
> ```php theme={null}
> return [
>     // ...
>     Laravel\Cloud\Symfony\LaravelCloudBundle::class => ['all' => true],
> ];
> ```
>
> > [!NOTE]
> >
> > The package does not ship a Symfony Flex recipe, so register the bundle manually.
>
> ### Routing messages
>
> The package provides a `cloud` Messenger transport with no DSN configuration required. Route messages to it in `config/packages/messenger.yaml`:
>
> ```yaml theme={null}
> framework:
>     messenger:
>         routing:
>             '*': cloud
> ```
>
> If your application uses the conventional `async` transport, Laravel Cloud injects `MESSENGER_TRANSPORT_DSN=laravel-cloud://managed-queue` so it works without changes.
>
> ### Multiple queues, FIFO, and retries
>
> Use `CloudQueueStamp` to dispatch a Symfony message to a named queue. Without a stamp, messages use the environment's default queue:
>
> ```php theme={null}
> use Laravel\Cloud\Symfony\Queue\Messenger\CloudQueueStamp;
> use Symfony\Component\Messenger\MessageBusInterface;
>
> $bus->dispatch(new ProcessReport($report), [new CloudQueueStamp('critical')]);
> ```
>
> Use `CloudFifoStamp` with a `.fifo` queue when you need to set its ordering or deduplication key:
>
> ```php theme={null}
> use Laravel\Cloud\Symfony\Queue\Messenger\CloudFifoStamp;
> use Laravel\Cloud\Symfony\Queue\Messenger\CloudQueueStamp;
>
> $bus->dispatch(new ProcessOrder($order), [
>     new CloudQueueStamp('orders.fifo'),
>     new CloudFifoStamp(
>         messageGroupId: 'customer-'.$order->customerId,
>         messageDeduplicationId: 'order-'.$order->id,
>     ),
> ]);
> ```
>
> On a standard queue, `CloudMessageGroupStamp` enables [SQS fair queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html), so one noisy tenant does not starve the others. Unlike FIFO, the group ID does not impose ordering or deduplication.
>
> ### Delays and retries
>
> A `DelayStamp` on a standard queue maps to an SQS per-message delivery delay, capped at 15 minutes. Requesting a longer delay throws. FIFO queues do not support per-message delays.
>
> Symfony Messenger controls retries for the `cloud` transport:
>
> ```yaml theme={null}
> framework:
>     messenger:
>         transports:
>             cloud:
>                 retry_strategy:
>                     max_retries: 3
>                     delay: 1000
>                     multiplier: 2
>                     max_delay: 0
> ```
>
> If a message exhausts its retries or throws `UnrecoverableExceptionInterface`, Laravel Cloud records it as a failed job in the dashboard.
>
> ### Local development
>
> Override the `cloud` transport in your `dev` environment to process messages inline without SQS:
>
> ```yaml theme={null}
> when@dev:
>     framework:
>         messenger:
>             transports:
>                 cloud: 'sync://'
> ```
>
> See the [`laravel/laravel-cloud-symfony` documentation](https://github.com/laravel/laravel-cloud-symfony) for all stamps and configuration options.

## Operate managed queues

### How jobs are processed

Laravel Cloud long-polls each queue and delivers jobs directly to workers. When workers are running, they usually pick up jobs within milliseconds. When a Flex queue wakes from zero, workers pick up jobs within a second. There is no polling interval to configure.

Laravel Cloud extends a job's visibility timeout in three-minute increments while it runs. If a worker crashes or stops before the job completes, Laravel Cloud retries the job. Design jobs to tolerate at-least-once delivery.

When a worker must stop, Flex workers have 90 seconds and Pro workers have one hour to finish their current job. Run jobs that may exceed 90 seconds on Pro.

### Filesystem

Each managed queue worker has its own ephemeral filesystem. Every 1 GiB of worker memory provides 512 MiB of temporary disk space. Jobs do not share files, and Laravel Cloud resets the filesystem whenever it replaces a worker. Use [Laravel Object Storage](https://laravel.com/cloud/docs/resources/object-storage) for persistent files.

### Observability

The **Queues** dashboard, under an environment's **Monitoring** tab, shows job volume, processing duration, memory usage, active workers, and failed jobs for every managed queue. See [Queue metrics](https://laravel.com/cloud/docs/metrics/queues) for what each metric means. You can inspect, retry, or delete failed jobs from the dashboard or the Laravel Cloud API. Retries and deletions require edit access to the environment.



The environment's [Logs](https://laravel.com/cloud/docs/logs) tab under **Monitoring** includes worker output.

### Pausing and purging

Pause a queue from its canvas menu to stop processing while allowing in-flight jobs to finish. Laravel Cloud stops polling and scales workers to zero, so no worker or polling charges accrue while it is paused. New jobs remain in the queue until you resume it. The `queue:pause` Artisan command is not supported. Pause and purge actions require edit access to the environment.

Purging removes every waiting job and cannot be undone. A purge may take up to 60 seconds and does not affect jobs that workers are already processing.

### Preview environments

Managed queues work in [preview environments](https://laravel.com/cloud/docs/preview-environments). Each preview receives isolated queues and workers, billed like other preview resources.

## Pricing

Managed queues are billed for worker time and queue operations. Flex workers are billed only while running, while Pro workers are billed continuously. For example, a Flex queue that runs three workers for 20 minutes is billed for 3,600 worker-seconds.

Standard queue operations cost **\$1 per 1 million operations** and FIFO operations cost **\$1.10 per 1 million operations**. Dispatching, starting, and deleting a successful job each count as an operation. Long-running jobs record additional visibility-extension operations while they run. Laravel Cloud measures payload-bearing dispatches and starts in 64 KB chunks. A job payload may be up to 1 MiB. Laravel Cloud's polling baseline is approximately \$0.13 per queue each month. See [Managed queues pricing](https://laravel.com/cloud/docs/pricing#managed-queues) for current regional pricing and plan limits.

## Migration and compatibility

### Limitations

See [Queue types](#queue-types) for the delivery, ordering, and delay guarantees of standard and FIFO queues.

Laravel Horizon and the `queue:failed`, `queue:retry`, and `queue:clear` Artisan commands do not support managed queues. Use the Queues dashboard or Laravel Cloud API to manage failed jobs.

### Upgrading from earlier managed queues

The latest managed queue generation automatically manages polling, visibility, and shutdown timeouts. To upgrade an earlier queue, update Laravel to a supported version and commit the updated `composer.lock`. Then select a Flex or Pro size in the queue settings and deploy. Your queue keeps its earlier runtime and settings until you select a new size.

After you upgrade a queue, its previous polling interval setting no longer appears. Its visibility and shutdown timeouts return to the defaults unless your organization has the advanced managed queues entitlement. Failed jobs carry over, but the queue cannot return to its earlier runtime.

Queues that have not been upgraded retain their current settings and pricing until Laravel Cloud retires the earlier generation on **September 30, 2026**. Those queues stop processing after that date. Because the underlying SQS queue retains a message for at most 14 days, jobs that remain unprocessed for longer than 14 days are lost.

### Migrating from queue clusters

Queue clusters are deprecated, and Laravel Cloud will sunset them on **September 30, 2026**. To move a queue cluster to managed queues, create a managed queue with the same queue name and choose an appropriate memory size and worker maximum. Deploy, then use the Queues dashboard to verify that jobs process. Let the old queue drain before deleting its queue cluster. If a queue cluster processes several queue names, create a managed queue for each name.

For complete instructions, including migration to worker clusters, see [Migrate from queue clusters](https://laravel.com/cloud/docs/knowledge-base/migrate-from-queue-clusters).

## Queue workers and scale to zero

Queued jobs do not wake a Laravel environment that has [scaled to zero](https://laravel.com/cloud/docs/compute#scale-to-zero). A self-managed queue worker runs only while the environment is awake. Examples include `php artisan queue:work` running as a background process on your App cluster, or on a Worker cluster that sleeps alongside it. The worker processes jobs until the sleep timeout elapses, and any job still running at that point is interrupted. To run a self-managed worker periodically while your environment otherwise sleeps, configure a [manual wake interval](https://laravel.com/cloud/docs/compute#manual-wake-interval).

Use managed queues for queued jobs on environments that scale to zero. Managed queues run on their own compute and wake on their own when jobs arrive, so jobs keep processing while your environment sleeps. Alternatively, run your queue workers on a [Worker cluster](https://laravel.com/cloud/docs/workers#workers-and-scale-to-zero) that stays awake.
