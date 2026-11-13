Source: https://nightwatch.laravel.com/docs/requests.md

# Requests

> HTTP requests handled by your Laravel application

HTTP requests are one of the primary execution contexts in Nightwatch, alongside commands and scheduled tasks. Each request becomes the starting point of a new trace, where all subsequent events such as database queries, queued jobs, and exceptions are captured and linked together to provide a complete picture of your application’s behavior.

## Route List

View all requests for an application from the **Requests** panel. Each route is displayed with its method and path (e.g., `GET /users`) and shows high-level aggregate statistics over the selected time period:

* **Successful requests** (2xx status codes)
* **Client errors** (4xx status codes)
* **Server errors** (5xx status codes)
* **Total requests** for the time period
* **Average request duration**
* **P95 request duration**

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of requests. It
> highlights outliers, bottlenecks and inconsistent behavior that average times
> hide.

## Individual Route

Click on a route to see all requests for that route over the selected time period, including the status code and duration for each request.

## Individual Request

Click on any request to view the full details page, which shows a timeline breakdown of the request's lifecycle and all events that occurred within it. Every event in the timeline can be expanded and navigated to for more details.

Standard details include the route name, request method, full URL, request headers, response code, IP address, and user information (if authenticated). Exceptions and request payloads are also displayed if they were captured. See the [Redaction](#redaction) section below to configure what is captured.

## Configuration

### Add Context

Nightwatch integrates with [**Laravel Context**](https://laravel.com/docs/context), enabling you to attach metadata to your requests, jobs, and commands.
This is a particularly powerful feature for understanding the behaviors your users experience.
For example, you can capture which feature flags were active during a request or include tenant context to help diagnose tenant-specific issues.

> [accordion] Examples
>
> ### Track feature flags
>
> Track which feature flags were active during a request:
>
> ```php theme={null}
> use Illuminate\Support\Facades\Context;
> use Laravel\Pennant\Feature;
>
> Context::add('feature_flags', [
>     'new_dashboard' => Feature::active('new_dashboard'),
>     'enhanced_search' => Feature::active('enhanced_search'),
>     'beta_checkout' => Feature::active('beta_checkout'),
> ]);
> ```
>
> ### Debug multi-tenant issues
>
> Add tenant context to help debug tenant-specific issues:
>
> ```php theme={null}
> use Illuminate\Support\Facades\Context;
>
> Context::add('tenant', [
>     'id' => $tenant->id,
>     'name' => $tenant->name,
>     'plan' => $tenant->subscription_plan,
>     'region' => $tenant->region,
> ]);
> ```

### Capture Request Headers

Request headers are captured by default with common sensitive values like cookies and authorization tokens automatically redacted.
You can customize and extend the list of redacted headers via the `NIGHTWATCH_REDACT_HEADERS` environment variable.

```bash theme={null}
NIGHTWATCH_REDACT_HEADERS=Authorization,Cookie,Proxy-Authorization,X-XSRF-TOKEN
```

### Capture Request Payloads

Nightwatch can automatically capture the request payload for a request that resulted in an exception. This is exceptionally useful for gaining a deeper understanding of what triggered an exception. Due to the possible sensitive nature of payload data, this setting is disabled by default. However, you can enable it via the `NIGHTWATCH_CAPTURE_REQUEST_PAYLOAD` environment variable.

```bash theme={null}
NIGHTWATCH_CAPTURE_REQUEST_PAYLOAD=true
```

A number of common sensitive fields are automatically redacted, including: `_token`, `password`, `password_confirmation`. You can customize the list of redacted fields via the `NIGHTWATCH_REDACT_PAYLOAD_FIELDS` environment variable.

```bash theme={null}
NIGHTWATCH_REDACT_PAYLOAD_FIELDS=password,password_confirmation
```

## Sampling

### Global Sampling

You can configure global sampling for HTTP requests using the `NIGHTWATCH_REQUEST_SAMPLE_RATE` environment variable. When a request is sampled in, Nightwatch captures the full execution context, including related database queries, queued jobs, exceptions, and outbound HTTP calls.

```bash theme={null}
NIGHTWATCH_REQUEST_SAMPLE_RATE=0.1 # Sample 10% of requests
```

### Route-Based Sampling

The Nightwatch `Sample` middleware provides individual route or route group sample rates within your Laravel application.

```php routes/web.php theme={null}
use Illuminate\Support\Facades\Route;
use Laravel\Nightwatch\Http\Middleware\Sample;

// Applied to a single route
Route::get('/users', [UserController::class, 'index'])
    ->middleware(Sample::rate(0.5));

// Applied to a route group
Route::middleware(Sample::rate(0.5))->group(function () {
    // ...
});

// Always sample a route
Route::get('/users', [UserController::class, 'index'])
    ->middleware(Sample::always());

// Never sample a route
Route::get('/users', [UserController::class, 'index'])
    ->middleware(Sample::never());
```

### Unmatched Routes Sampling

You can set sample rates for bot traffic by using the `Sample` middleware with Laravel's [fallback route](https://laravel.com/docs/12.x/routing#fallback-routes). We don't recommend ignoring all unmatched routes. Instead, you should implement a reduced sample rate for bot traffic to help identify and block unwanted requests.

```php routes/web.php theme={null}
// Applied to unmatched 404 routes
Route::fallback(fn () => abort(404))
    ->middleware(Sample::rate(0.5));
```

### Package Route Sampling

Many packages provide options to modify the middleware applied to their routes through configuration. For example, [Laravel Nova](https://nova.laravel.com/) lets you add middleware to its internal routes in your `config/nova.php` configuration file.

```php config/nova.php theme={null}
'middleware' => [
    \Laravel\Nightwatch\Http\Middleware\Sample::rate(0.5),
    'web',
    \Laravel\Nova\Http\Middleware\HandleInertiaRequests::class,
    'nova:serving',
],
```

### Dynamic Sampling

You can use dynamic sampling based on request attributes, such as user roles or other conditions:

```php app/Http/Middleware/SampleAdminRequests.php theme={null}
use Closure;
use Illuminate\Http\Request;
use Laravel\Nightwatch\Facades\Nightwatch;
use Symfony\Component\HttpFoundation\Response;

class SampleAdminRequests
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $user = $request->user()) {
            return $next($request);
        }

        if ($user->isAdmin()) {
            Nightwatch::sample();

            return $next($request);
        }

        return $next($request);
    }
}
```

```php routes/web.php theme={null}
use App\Http\Middleware\SampleAdminRequests;

Route::middleware(SampleAdminRequests::class)->group(function () {
    // ...
});
```

## Filtering

There are no specific filtering methods for requests. To conditionally exclude requests from collection, you can use the sampling mechanisms described above.

## Redaction

You can manually redact sensitive information from requests, including request URLs and IP addresses using the `Nightwatch::redactRequests()` function:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Request;

Nightwatch::redactRequests(function (Request $request) {
    $request->url = str_replace('secret', '***', $request->url);
    $request->ip = str_replace('secret', '***', $request->ip);
});
```
