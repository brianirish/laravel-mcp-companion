Source: https://nightwatch.laravel.com/docs/exceptions.md

# Exceptions

> Exceptions that occur in your Laravel application

Nightwatch automatically captures all exceptions in your Laravel application. It shows the exception type, message, stack trace, request context, and related events to help you debug without switching tools.

## Exception List

The exception page lists all the unique exceptions that have been observed in your application, showing the total count and users affected.

> [!NOTE]
>
> Uniqueness of exceptions is determined by the combination of their class,
> code, and the file and line number where they were thrown or reported. This
> means that if an exception is thrown in the same file and line number, but
> with a different message, it will be considered as a different exception.

## Exception Details

When you click an exception in the list, Nightwatch opens the exception details view. This page gives you everything you need to understand the scope and impact of the error at a glance.

Nightwatch shows when the exception was first and most recently seen, along with the total number of occurrences and users affected across the last 30 days, 7 days, and 24 hours.

Where [Source Code Capture](#source-code-capture) is enabled you will see the stack trace includes inlined source code, highlighting the exact line where the exception was triggered.

The details page also provides a list of individual occurrences of the exception related to their parent context (such as a request, job, or command). Selecting any occurrence opens the full trace view, allowing you to follow the path that led to the exception and debug in detail.

## Auto-generating issues

Nightwatch automatically creates a new issue for each unhandled exception that is reported, and will associate any new occurrences of the same exception with the existing issue, so that you can track the issue and resolve it systematically.

## Configuration

### Source Code Capture

Nightwatch will automatically augment the stack trace with the relevant source code where possible. You can disable this behavior by setting the `NIGHTWATCH_CAPTURE_EXCEPTION_SOURCE_CODE` environment variable to `false`.

```bash theme={null}
NIGHTWATCH_CAPTURE_EXCEPTION_SOURCE_CODE=false
```

## Sampling

### Default Behavior

By default, Nightwatch captures all exceptions from all requests and commands to ensure that you have the full context of any exception that occurs in your application.

For example, if you set the request sample rate to 10% and the exception sample rate to 100% (default), Nightwatch will capture any request that throws an exception, regardless of whether the request would have been sampled otherwise.

### Exception Sampling Rate

To ignore exceptions on non-sampled requests, set `NIGHTWATCH_EXCEPTION_SAMPLE_RATE=0`. This setting ensures that exceptions are captured only from sampled requests.

```bash theme={null}
NIGHTWATCH_EXCEPTION_SAMPLE_RATE=0
```

### Exception Throttling

Laravel provides additional ways to throttle exception reporting for high traffic applications or when you need to protect against sudden spikes.

[https://laravel.com/docs/errors#throttling-reported-exceptions](https://laravel.com/docs/errors#throttling-reported-exceptions)

## Filtering

There are no specific filtering methods for exceptions. Exceptions are captured based on the sampling configuration described above.

## Redaction

You can manually redact sensitive information from exception messages using the `redactExceptions` callback:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Exception;

Nightwatch::redactExceptions(function (Exception $exception) {
    $exception->message = str_replace('secret', '***', $exception->message);
});
```

## Manually Reporting Exceptions

Nightwatch automatically listens to all exceptions reported within your Laravel application:

```php theme={null}
report($e); // Nightwatch will capture this exception...
```

If you're not seeing an exception in your Nightwatch dashboard, you can explicitly report it using the facade:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;

Nightwatch::report($e);
```

> 📘 This is only needed in rare cases where exceptions are not captured automatically.

## Unrecoverable Exceptions

If Nightwatch experiences an unrecoverable exception when recording events from your application, it can become unable to notify you of the issue. You may register a handler for these scenarios with the `Nightwatch::handleUnrecoverableExceptionsUsing` method. You should put this in your `AppServiceProvider::register` method:

```php AppServiceProvider.php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Illuminate\Support\Facades\Log;

Nightwatch::handleUnrecoverableExceptionsUsing(function ($e) {
    // Ensure the error is written to a channel other than the `nightwatch` channel.
    Log::channel('single')->error(
        'Nightwatch experienced an unrecoverable exception',
        ['exception' => $e]
    );
});
```

> [!WARNING]
>
> This may generate a large number of logs in cases where Nightwatch is not
> configured correctly and fails on every request to your application.
