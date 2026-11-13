Source: https://nightwatch.laravel.com/docs/filtering.md

# Filtering

> Learn how the Nightwatch package observes and processes data

Nightwatch observes your Laravel application as it runs, capturing events and data that occur during execution. The package follows a predefined flow that determines what data is collected and how it’s processed, ensuring a consistent and predictable experience.

1. **Observation**: The agent monitors your Laravel application, observing requests, commands, scheduled tasks, and all the events they trigger, e.g. queries, jobs, exceptions, etc.

2. **[Sampling](#sampling)**: For entry points (requests, commands, and scheduled tasks), sampling determines whether the entire trace should be collected based on configured sample rates. If a request is sampled, all related events within that request lifecycle are captured.

3. **[Filtering](#filtering)**: Once a trace has been selected for collection, filters can be applied with scalpel-like precision to exclude specific events based on criteria. Filters allow you to make granular decisions about individual events, determining whether they should be collected or excluded.

4. **[Redaction](#redaction)**: After data has passed through sampling and filtering gates, redaction methods allow you to manipulate the data being collected. This enables you to obfuscate sensitive information, modify user details, or add contextual information to records.

5. **[Rate limiting](#rate-limiting)**: Finally, before a batch of events is transmitted, Nightwatch dispatches an event that allows you to enforce hard limits on the total number of events ingested.

## Sampling

Sampling controls the rate at which entry points are collected. Entry points are the initial events that trigger a trace. These are **requests**, **commands**, and **scheduled tasks**. When an entry point is sampled in, the entire trace (including all related events like queries, jobs, and exceptions) is captured. If an entry point is sampled out, all related events are not captured.

**By default**, Nightwatch has a sample rate of 100% for all entry points, resulting in unrestricted data collection and complete visibility out of the box.

### Recommended

We recommend everyone to apply some level of **Sampling** to reduce the volume of data collected. For new applications, we recommend starting with the global sample rate of `0.1` or lower on **requests** to build an understanding of your application's profile and adjusting the rate based on your observations.

```bash theme={null}
NIGHTWATCH_EXCEPTION_SAMPLE_RATE=1.0
NIGHTWATCH_COMMAND_SAMPLE_RATE=1.0
NIGHTWATCH_REQUEST_SAMPLE_RATE=0.1 # Recommended
```

In addition to global sample rates, there are a number of advanced sampling methods, including route-based sampling, package route sampling and dynamic sampling.

Please see the following guides for more detail for each specific event type:

| Event Type | Description |
| - | - |
| [Requests](https://nightwatch.laravel.com/docs/requests.md#sampling) | Configure sampling rates for Requests with advanced sampling methods |
| [Commands](https://nightwatch.laravel.com/docs/commands.md#sampling) | Configure sampling for Artisan commands executed in your application |
| [Exceptions](https://nightwatch.laravel.com/docs/exceptions.md#sampling) | Configure sampling for exceptions observed in your application |

## Filtering

Filtering allows you to exclude specific events from collection with precision. Once a trace has been selected for collection through sampling, filters can be applied to individual events based on criteria, allowing you to make granular decisions about what should be collected or excluded.

Please see the following guides for how to apply filtering to the following event types:

| Event Type | Description |
| - | - |
| [Queries](https://nightwatch.laravel.com/docs/queries.md#filtering) | Filter database queries based on SQL patterns or other criteria |
| [Cache](https://nightwatch.laravel.com/docs/cache.md#filtering) | Exclude cache events by key patterns or specific cache operations |
| [Mail](https://nightwatch.laravel.com/docs/mail.md#filtering) | Filter mail events based on subject, recipient, or other attributes |
| [Notifications](https://nightwatch.laravel.com/docs/notifications.md#filtering) | Exclude notification events by channel, type, or other criteria |
| [Outgoing Requests](https://nightwatch.laravel.com/docs/outgoing-requests.md#filtering) | Filter outgoing HTTP requests based on URL patterns or other attributes |
| [Jobs](https://nightwatch.laravel.com/docs/jobs.md#filtering) | Exclude specific jobs from collection based on job class or other criteria |

### Inline filtering

In addition to the callback-based filtering above, you may also filter events inline. The `Nightwatch::ignore` method accepts a callback which will filter out any events occurring within the callback:

```php theme={null}
use App\Jobs\SyncUsers;
use App\Models\User;
use Laravel\Nightwatch\Facades\Nightwatch;

/*
 * Nightwatch will not capture the query, the queued job, or the job's attempts.
 */
$users = Nightwatch::ignore(function () {
    $users = User::get();

    SyncUsers::dispatch($users);

    return $users;
});
```

If you are unable to use the callback API and need more fine-grained control, you may use the `Nightwatch::pause` and `Nightwatch::resume` methods instead.

```php theme={null}
use App\Jobs\SyncUsers;
use App\Models\User;
use Laravel\Nightwatch\Facades\Nightwatch;

/*
 * Nightwatch will not capture the query, the queued job, or the job's attempts.
 */

Nightwatch::pause();

$users = User::get();

SyncUsers::dispatch($users);

Nightwatch::resume();
```

## Redaction

Redaction allows you to manipulate collected data before it's sent to Nightwatch. After data has passed through sampling and filtering, redaction methods enable you to obfuscate sensitive information, modify user details, or add contextual information to records.

Please see the following guides for how to apply redaction to the following event types:

| Event Type | Description |
| - | - |
| [Requests](https://nightwatch.laravel.com/docs/requests.md#redaction) | Redact URLs, IP addresses, headers, and payload data from requests |
| [Queries](https://nightwatch.laravel.com/docs/queries.md#redaction) | Modify SQL statements to remove or obfuscate sensitive data |
| [Cache](https://nightwatch.laravel.com/docs/cache.md#redaction) | Redact cache key names that may contain sensitive information |
| [Commands](https://nightwatch.laravel.com/docs/commands.md#redaction) | Modify command arguments to remove sensitive data |
| [Mail](https://nightwatch.laravel.com/docs/mail.md#redaction) | Redact mail subjects or other mail-related data |
| [Outgoing Requests](https://nightwatch.laravel.com/docs/outgoing-requests.md#redaction) | Modify outgoing request URLs or other request data |
| [Exceptions](https://nightwatch.laravel.com/docs/exceptions.md#redaction) | Redact sensitive information from exception messages |

## Rate limiting

In addition to sampling and filtering, you may also cap the number of events ingested by Nightwatch. This can be useful to ensure a noisy application does not consume all of your quota.

Before ingesting, Nightwatch dispatches the `Laravel\Nightwatch\Events\IngestingEvents` event. When a listener returns `false`, the ingest will be canceled. Combining this event with Laravel's rate limiter allows you to cap ingestion at the application or environment level, or even across several applications that share a cache.

The following example listener, which is typically registered in a service provider's `boot` method, limits the application to 1,000 events per day:

```php theme={null}
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\RateLimiter;
use Laravel\Nightwatch\Events\IngestingEvents;

Event::listen(function (IngestingEvents $event) {
    $ingestedEvents = RateLimiter::increment(
        key: 'nightwatch-events',
        decaySeconds: 60 * 60 * 24,
        amount: $event->eventCount(),
    );

    if ($ingestedEvents >= 1_000) {
        return false;
    }
});
```

> [!NOTE]
>
> Events occurring while the listener executes, such as the cache operations performed by the rate limiter, will not be collected by Nightwatch.
