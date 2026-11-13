Source: https://nightwatch.laravel.com/docs/outgoing-requests.md

# Outgoing Requests

>  HTTP requests made from your Laravel application to external services

Nightwatch captures outgoing HTTP requests made via Laravel's `Http` facade or the underlying Guzzle client. This is particularly useful for monitoring the performance of your external dependencies and identifying bottlenecks.

## Outgoing Request List

The outgoing request list view aggregates all outgoing requests by their host domain. Each domain includes high-level aggregate statistics over the selected time period including:

* **Successful requests** (1xx, 2xx, 3xx status codes)
* **Client errors** (4xx status codes)
* **Server errors** (5xx status codes)
* **Total requests** for the time period
* **Average request duration**
* **P95 request duration**

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of outgoing requests.
> It highlights outliers, bottlenecks and inconsistent behavior that average
> times hide.

## Outgoing Request Details

Clicking on any host domain in the list view will display a list of all outgoing requests for that domain over the selected time period, including the status code and duration for each request.

## Configuration

### Monitoring Guzzle Requests

Nightwatch automatically captures outgoing HTTP requests made via Laravel's Http client. However, if you would like to capture requests made with Guzzle directly, you will need to attach Nightwatch's Guzzle middleware to your stack.

```php theme={null}
use GuzzleHttp\Client;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\Handler\CurlHandler;
use Laravel\Nightwatch\Facades\Nightwatch;

// Set up the handler stack...
$stack = new HandlerStack;
$stack->setHandler(new CurlHandler);

// Push Nightwatch's middleware...
$stack->push(Nightwatch::guzzleMiddleware());

// Create the client with the stack...
$client = new Client(['handler' => $stack]);
```

Requests made by `$client` will now be monitored by Nightwatch.

## Sampling

There are no direct sampling controls for outgoing requests, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

## Filtering

There are a number of different methods to filter outgoing requests.

### Filtering All Outgoing Requests

To completely disable the collection of all outgoing HTTP requests, set the `NIGHTWATCH_IGNORE_OUTGOING_REQUESTS` environment variable to `true`:

```bash theme={null}
NIGHTWATCH_IGNORE_OUTGOING_REQUESTS=true
```

### Filtering Specific Outgoing Requests

You can filter out specific outgoing requests using the `Nightwatch::rejectOutgoingRequests()` method:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\OutgoingRequest;

Nightwatch::rejectOutgoingRequests(function (OutgoingRequest $request) {
    return str_contains($request->url, 'analytics.example.com');
});
```

## Redaction

You can manually redact sensitive information from outgoing request URLs using the `redactOutgoingRequests` callback:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\OutgoingRequest;

Nightwatch::redactOutgoingRequests(function (OutgoingRequest $outgoingRequest) {
    $outgoingRequest->url = str_replace('secret', '***', $outgoingRequest->url);
});
```
