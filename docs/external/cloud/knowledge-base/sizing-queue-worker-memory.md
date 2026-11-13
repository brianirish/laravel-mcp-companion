Source: https://laravel.com/cloud/docs/knowledge-base/sizing-queue-worker-memory.md

# How much memory do your queue workers need?

Measure what your queued jobs actually use and choose the right memory size for your managed queue workers.

> [!NOTE]
>
> This guide is for Laravel applications.

When you create a Laravel Cloud [managed queue](https://laravel.com/cloud/docs/queues#managed-queues), you choose how much memory each worker receives. Flex workers support between 256 MiB and 2 GiB of memory, while Pro workers support up to 8 GiB. Memory is the only sizing decision a managed queue requires, and you can adjust the size with each deployment. This guide explains how to measure your jobs' memory usage and choose an appropriate size.

Sizing is always a per-queue exercise. Each managed queue processes exactly one Laravel queue name, so you are measuring the jobs that run on that particular queue. Those are the jobs your application dispatches to it with `->onQueue(...)`. If the queue is the environment's [default queue](https://laravel.com/cloud/docs/queues#setting-a-default-queue), they also include every job dispatched without an explicit queue name. Keep that boundary in mind throughout this guide, especially once you have more than one queue.

## Start with your jobs

A worker's memory needs depend on what your job's `handle` method loads into memory while it runs. Job payloads are capped at 1 MiB, so the payload itself is never the problem. The question is what the job loads while it does its work.

Typical Laravel jobs, such as sending mail, firing notifications, processing webhooks, and updating records, use well under 100 MB, and the default **256 MiB** size handles them comfortably. Jobs may require a larger size when they hydrate large sets of Eloquent models, read entire files into memory, generate exports or reports, manipulate images and video, or run machine learning inference.

## Size for the largest job on the queue

Each worker processes one job at a time, and every job dispatched to a queue runs on a worker of that queue's size. The memory size therefore needs to fit the most memory-intensive job that runs on the queue, not the average one.

When a job needs more memory than its worker has, it runs out of memory (often abbreviated "OOM"). The job typically fails with a PHP fatal error reporting that the allowed memory size was exhausted. The worker then restarts, and Laravel Cloud redelivers the job to another worker. Redelivery does not resolve an undersized queue. The job fails on every attempt until it exhausts its retries and appears in [failed jobs](https://laravel.com/cloud/docs/queues#observability). An occasional restart is harmless, but a job class that consistently runs out of memory requires a larger queue size or its own queue.

## Measure locally

For a quick estimate, run your worker in verbose mode while dispatching jobs locally:

```shell theme={null}
php artisan queue:work -v
```

In verbose mode, each completed job's output line includes the worker's current memory usage. The reading reflects the worker process as a whole rather than the individual job, but it gives you an immediate rough estimate.

By default, a worker processes only the default queue. If you are sizing another queue, dispatch your test jobs to that queue and start the worker with the matching option, such as `php artisan queue:work -v --queue=invoices`. Without the `--queue` option, you may measure the wrong jobs.

For a true per-job reading, register a temporary listener in your `AppServiceProvider`'s `boot` method:

```php theme={null}
use Illuminate\Queue\Events\JobAttempted;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Log;

Event::listen(function (JobAttempted $event) {
    Log::info('Job peak memory', [
        'job' => $event->job->resolveName(),
        'peak_mb' => round(memory_get_peak_usage(true) / 1024 / 1024, 1),
    ]);
});
```

The queue worker resets PHP's peak memory counter between jobs, so each log entry reflects the job's peak memory usage. The `JobAttempted` event fires whether the job succeeds or fails. Dispatch a realistic sample of your heaviest jobs with realistic file sizes and production-like data volumes. After the worker processes them, review the peaks in your log.

> [!WARNING]
>
> Dispatch test jobs only into a local environment. If your `QUEUE_CONNECTION`, database, mail driver, or API credentials point at shared or production services, a memory test can drop jobs onto a real queue, send real emails, or hit live APIs. Check your `.env` first and point anything live at a local or sandbox equivalent (for example, `MAIL_MAILER=log`).

Choose the smallest size that provides roughly 30% headroom above your largest peak. This headroom accommodates day-to-day variations in your data and the memory reserved for the worker runtime.

## Let an AI agent measure it for you

An AI coding agent can perform the measurement for you. It can identify the queue you are sizing, verify that your local environment is safe, find and run the relevant jobs locally, and recommend a size or queue split.

Copy this prompt into your coding agent from your application's directory to measure your jobs and get a size recommendation.

Help me choose a memory size for a Laravel Cloud managed queue by measuring what my queued jobs actually use.

1. First, ask me which queue I am sizing. On Laravel Cloud, each managed queue processes exactly one queue name, so we are measuring only the jobs that run on that queue. If it is my environment's default queue, that means every job dispatched without an explicit queue name.

2. Work out which of my job classes run on that queue: dispatches using `->onQueue(...)`, jobs that set their queue in the constructor, and queued listeners, mailables, and notifications (including `viaQueue`), plus jobs that fall through to the default. Flag the ones most likely to use significant memory, such as jobs that load many models, process files, or build exports and reports.

3. Before anything is dispatched, run a safety check on my local setup and report what you find: confirm `APP_ENV` is local; confirm `QUEUE_CONNECTION` uses a driver on this machine (such as `database`, or `redis` pointing at localhost) rather than a remote or production queue; and review my `.env` for live services the sampled jobs would touch, such as a remote database, a real mail driver, or live payment and API keys. Point anything risky at a local or sandbox equivalent (for example `MAIL_MAILER=log`) and tell me what you changed. If my queue connection is `sync`, switch it to `database` for the test. If anything still looks like it could reach production, stop and ask me before continuing.

4. Register a temporary event listener in app/Providers/AppServiceProvider.php that listens for `Illuminate\Queue\Events\JobAttempted` and logs each job's class name and peak memory in MB using `round(memory_get_peak_usage(true) / 1024 / 1024, 1)`. The worker resets the peak between jobs, so each reading is per-job.

5. Once the safety check passes, help me dispatch a representative sample of those jobs locally with realistic data, then process them with `php artisan queue:work --stop-when-empty`, passing `--queue=` with the queue name from step 1 so we process the right jobs.

6. Present a table of peak memory per job class, then recommend the smallest Laravel Cloud managed queue size that leaves at least 30% headroom above the highest peak. The sizes are 256 MiB, 512 MiB, 1 GiB, and 2 GiB on the Flex class, with 4 GiB and 8 GiB available on Pro. If one job class peaks far above the rest, also recommend splitting it onto its own managed queue, with a suggested size for each of the two queues.

7. When we're finished, remove the temporary listener and revert any `.env` changes we made for the test.

## Verify on Cloud

Local measurements provide a useful starting point, while production data confirms whether your queue is sized appropriately. Every environment with managed queues has a **Queues** tab with a **Memory** chart that displays peak worker memory usage over time. If peaks approach the top of the chart, increase the queue size. If peaks remain well below the limit, you may be able to decrease the size.

In a development or staging environment, you may start small, dispatch representative work, and increase the size if jobs fail. In production, start with more memory than you expect to need. Run a full business cycle that includes scheduled work such as nightly imports or reports, and then reduce the size while keeping a comfortable margin below the limit. Workers are billed per second while running, so temporarily allocating additional memory typically costs less than diagnosing out-of-memory failures after launch.

The signals of an undersized queue are a "Managed queue crashed and restarted" notification, fatal errors in your logs reporting exhausted memory, or jobs exhausting their retries without a clear exception.

## Split queues by memory profile

If nine of your job classes peak under 100 MB and one PDF-processing job needs 2 GiB, a single queue forces every job onto 2 GiB workers. Instead, create a smaller queue for most jobs and a larger queue for the resource-intensive job, which you may dispatch using `->onQueue('heavy')`. You size each managed queue independently, so most of your work runs on smaller, less expensive workers. The larger workers are billed only while the resource-intensive job runs.

Before allocating more memory, consider reducing the job's memory usage. Process large datasets with chunked queries or `LazyCollection` instead of loading entire tables. Stream files to [object storage](https://laravel.com/cloud/docs/resources/object-storage) instead of reading them entirely into memory. You can also split one large job into several smaller jobs that run across multiple workers. Each worker's temporary disk scales with its memory (512 MiB of disk per 1 GiB of memory), so a job that stages large files may need a larger size for disk capacity rather than memory. See [Filesystem](https://laravel.com/cloud/docs/queues#filesystem) for details.

For per-job timing and failure analytics across your entire application, consider pairing managed queues with [Laravel Nightwatch](https://nightwatch.laravel.com).
