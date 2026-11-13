Source: https://nightwatch.laravel.com/docs/scheduled-tasks.md

# Scheduled Tasks

> Tasks registered in Laravel's scheduler

Tasks are automatically captured when registered in Laravel's scheduler in `routes/console.php` or defined using `Schedule::command()` and `Schedule::call()`.

Scheduled tasks are one of the primary execution contexts in Nightwatch, alongside requests and commands. Each task execution becomes the starting point of a new trace, where all subsequent events such as database queries and exceptions are captured and linked together to provide a complete picture of your application’s behavior.

## Task List

View all scheduled tasks for an application from the **Scheduled Tasks** panel. Each task is displayed with its name, schedule, next run and execution times, including the average and p95 execution time.

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of scheduled tasks.
> It highlights outliers, bottlenecks and inconsistent behavior that average
> times hide.

## Task Details

Click on any task in the list to view its full details page, which shows the task's performance over time. You can also see every individual execution of a task within its parent context. Clicking on an execution opens the full trace, showing the job within the context of its parent lifecycle.

## Sampling

### Global Sampling

You can configure global sampling for scheduled tasks using the `NIGHTWATCH_SCHEDULED_TASK_SAMPLE_RATE` environment variable. When a scheduled task is sampled in, Nightwatch captures the full execution context, including related database queries, queued jobs, and exceptions. This environment variable takes precedence over `NIGHTWATCH_COMMAND_SAMPLE_RATE` when you schedule Artisan commands.

```bash theme={null}
NIGHTWATCH_SCHEDULED_TASK_SAMPLE_RATE=1.0 # Sample 100% of tasks
```

### Sampling Specific Tasks

The `Sample` class allows you to apply sampling rates to individual scheduled tasks.

```php routes/console.php theme={null}
use Illuminate\Support\Facades\Schedule;
use Laravel\Nightwatch\Console\Sample;

// Sample a task 50% of executions
Schedule::command('app:daily-report')->daily()->tap(Sample::rate(0.5));

// Always sample a task
Schedule::command('app:upload-post')->daily()->tap(Sample::always());

// Never sample a task
Schedule::command('app:process-comments')->everyHour()->tap(Sample::never());
```

## Filtering

There are no specific filtering methods for scheduled tasks.

## Redaction

There are no specific redaction methods for scheduled tasks. However, you may still apply [redaction](https://nightwatch.laravel.com/docs/filtering.md#redaction) to any of the child events that occur as a result of the scheduled task being executed. For example, you may want to redact the contents of a scheduled task's output.
