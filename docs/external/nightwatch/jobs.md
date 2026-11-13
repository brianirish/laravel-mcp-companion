Source: https://nightwatch.laravel.com/docs/jobs.md

# Jobs

> Queued jobs executed by your Laravel application

Jobs are automatically captured whenever a queued job is dispatched and executed by Laravel's queue system, including jobs dispatched via `dispatch()`, `Job::dispatch()`, or pushed directly to queues.

## Job List

View all jobs for an application from the **Jobs** panel. Each job is displayed with counts of queued, processed, released and failed executions and execution times, including the average and p95 execution time.

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of jobs. It
> highlights outliers, bottlenecks and inconsistent behavior that average times
> hide.

## Job Details

Click any job in the list to open its details page, where you can view its performance over time. The page also shows every individual execution of that job and its parent context. Selecting an execution opens the full trace, allowing you to see the job within its parent lifecycle.

## Sampling

There are no direct sampling controls for job events, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

### Sampling Specific Jobs

While not recommended, you can apply a dynamic sample rate for a specific job by calling `Nightwatch::sample()` at the start of your job:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;

class MyJob
{
    public function handle()
    {
        Nightwatch::sample(rate: 0.5); // Sample 50%

        // ...
    }
}
```

> [!NOTE]
>
> Nightwatch currently doesn't offer or recommend setting a sample rate for a
> specific job. However, you could achieve this by adding the sampling call to
> the start of your job as shown above.

### Decoupling Job Sampling

You can de-couple the sampling of jobs from the sample rates of their parent execution contexts:

```php AppServiceProvider.php theme={null}
use Illuminate\Support\Facades\Queue;
use Laravel\Nightwatch\Facades\Nightwatch;

public function boot(): void
{
    Queue::before(fn () => Nightwatch::sample(rate: 0.5));
}
```

> [!NOTE]
>
> This may lead to the request, command or scheduled task that triggered a
> captured job not being captured, or a job triggered by a captured request,
> command, or scheduled task not being captured, which could lead to a less
> complete view of how your application is performing.

## Filtering

You can filter out specific jobs using the `Nightwatch::rejectQueuedJobs()` method:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\QueuedJob;

Nightwatch::rejectQueuedJobs(function (QueuedJob $job) {
    return $job->name === 'App\Jobs\LowPriorityJob';
});
```

## Redaction

There are no specific redaction methods for jobs. Job data is captured as-is from Laravel's queue system.

## Reporting Manually Failed Jobs

If you want to report a manually failed job, you need to manually report an exception.

```php theme={null}
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    report($e);

    $this->fail($e);
}
```
