Source: https://laravel.com/cloud/docs/health-checks.md

# Health checks

Configure startup, readiness, and liveness health checks so Laravel Cloud knows when your application has started, can receive traffic, and is still healthy.

## Introduction

Laravel Cloud runs health checks against your application's instances. These checks decide when a new deployment has finished starting, when it may begin receiving traffic, and when Laravel Cloud should restart an instance that has stopped responding.

By default, Laravel Cloud uses built-in checks that work for every application. You may also point these checks at a health endpoint in your application, such as Laravel's `/up` route, so a deployment goes live only once your application can serve requests.

Health checks apply to your environment's App cluster. Worker clusters and queue workers do not receive web traffic, so Laravel Cloud does not run health checks against them.

## Types of health checks

Laravel Cloud supports three types of health checks. Each check is optional and answers a different question:

| Check | Question | When it fails |
| - | - | - |
| **Startup** | Has the application finished starting? | Laravel Cloud restarts the instance. If the check never passes, the deployment fails. |
| **Readiness** | Is the application ready to receive traffic? | Laravel Cloud stops sending traffic to the instance until the check passes again. During a deployment, the new release never receives traffic and the deployment fails. |
| **Liveness** | Is the application still healthy and running? | Laravel Cloud restarts the instance. During a deployment, the new release never receives traffic and the deployment fails. |

Readiness and liveness checks begin once the startup check passes. During a deployment, Laravel Cloud sends traffic to your new release and shuts down the previous release only after the new release passes its startup and readiness checks. If you configured a liveness check, Laravel Cloud also waits one full liveness window, as described in [how health checks affect deployments](#how-health-checks-affect-deployments). A startup check pointed at your application's health endpoint keeps users from seeing 502 or 503 responses while a new release boots.

### Default health checks

When you leave a health check empty, Laravel Cloud uses its built-in check. Each instance runs Laravel Cloud's web server on port `8080`. The default checks confirm that your instance is up and that this web server responds. They do not request a route in your application.

| Check | Default behavior | Delay | Interval | Timeout | Tries |
| - | - | - | - | - | - |
| Startup | PHP applications: Laravel Cloud's web server responds. All other runtimes: a TCP connection to your application on the `PORT` environment variable succeeds. | 0s | 1s | 5s | 15 |
| Readiness | Laravel Cloud's web server responds. | 0s | 30s | 5s | 3 |
| Liveness | A TCP connection to Laravel Cloud's web server succeeds. | 0s | 10s | 5s | 4 |

If you do not configure any health checks, Laravel Cloud uses these defaults.

## Configuring health checks

To configure your health checks, navigate to your environment's **Settings > Deployments** page and click **Configure** next to **Health checks**. Each check accepts an endpoint. To adjust a check's port and timing, click **Edit** within the check's advanced settings:

| Setting | Description | Allowed values |
| - | - | - |
| **Endpoint** | The path Laravel Cloud requests, such as `/up`. A response with a `2xx` or `3xx` status code passes. | Must start with a single `/`, may not contain spaces, and may be at most 255 characters. |
| **Port** | The port the check connects to. | 1 to 65535. Defaults to `8080`. |
| **Timeout** | How long a single check may take before it counts as a failure. | 1 to 120 seconds |
| **Delay** | How long to wait before the first check runs. | 0 to 600 seconds |
| **Interval** | How long to wait between checks. | 1 to 300 seconds |
| **Tries** | How many checks in a row must fail before Laravel Cloud acts on the failure. | 1 to 1000 |

Any setting you leave untouched keeps its [default value](#default-health-checks). Health check changes take effect on your environment's next deployment.

A startup check's `delay + interval × tries` may be at most 600 seconds. If your application needs a long time to boot, raise the startup check's tries or interval rather than its delay. A delay makes every deployment wait for its full length, while extra tries let the check pass as soon as your application is ready.

### How health checks affect deployments

Each check you configure changes how long a deployment may take:

* **Startup:** The deployment waits until the check passes, for up to its `delay + interval × tries`.
* **Readiness:** If the readiness check keeps failing after your application has started, the deployment fails after three minutes. If the check's `delay + interval × tries` is longer than three minutes, the deployment fails after that time instead. If your application needs more time to become ready after it starts listening, configure a startup check that covers its boot time.
* **Liveness:** Once your new release is ready, the deployment waits for up to `delay + interval × tries + timeout` before sending it traffic. As a result, a liveness check that can never pass fails the deployment and does not restart your live application. A liveness check with the default timing adds up to 45 seconds to each deployment.

When a deployment fails because of a health check, your previous release keeps serving traffic.

### Choosing a port

When you set only an endpoint, Laravel Cloud requests it through its web server on port `8080`. For PHP applications, this web server serves your application directly. For all other runtimes, it forwards the request to your application on the `PORT` environment variable, the same way it forwards user traffic. We recommend this setup for most applications.

If you specify a different port, Laravel Cloud connects to your application on that port directly. This is useful if your application serves its health endpoint on a separate management port. Laravel Cloud's network uses IPv6, so your application must listen on all IPv6 interfaces for this port. Bind to `::` rather than `0.0.0.0`, `127.0.0.1`, or `localhost`:

```js Node.js theme={null}
app.listen(9090, '::');
```

```shell Uvicorn theme={null}
uvicorn main:app --host :: --port 9090
```

```shell Puma theme={null}
bundle exec puma -b 'tcp://[::]:9090'
```

If you set a port without an endpoint using the [Laravel Cloud API](#api), the check becomes a TCP check that passes as soon as a connection to that port succeeds.

## Framework detection

When you create a new environment, Laravel Cloud looks for your framework's health route in your repository. If it finds the route in your code, it pre-fills the startup and readiness endpoints with it. It leaves the liveness endpoint empty, so liveness uses the default check. Laravel Cloud does not pre-fill a route it can't find, since checking a route that doesn't exist would fail every deployment.

| Framework | Detected endpoint | Detected when |
| - | - | - |
| Laravel 11+ | `/up`, or your custom path | Your `bootstrap/app.php` file passes a `health` path to `withRouting`. |
| Rails 7.1+ | `/up`, or your custom path | Your `config/routes.rb` file routes a path to `rails/health#show` at the top level of the routes block. |

Framework detection runs only for new environments. Existing environments keep the default checks until you configure them.

## Liveness checks and external services

A liveness check should confirm only that your application's process is running and able to answer requests. **Avoid liveness checks that depend on your database, cache, or any other external service.**

Suppose your liveness endpoint checks your database and that database becomes slow or briefly unavailable. Every instance fails its liveness check at the same time, and Laravel Cloud restarts all of them. Restarting your application does not fix the database, so your instances can become stuck in a restart loop and turn a brief slowdown into an outage.

Laravel's `/up` route and Rails' `/up` route are good liveness endpoints because they confirm only that the application booted. If you want an instance to stop receiving traffic while a dependency is unavailable, check that dependency in your readiness endpoint instead. A failing readiness check stops traffic to the instance without restarting it.

## Health checks and scale to zero

Health checks do not keep a sleeping environment awake. When your environment [scales to zero](https://laravel.com/cloud/docs/compute#scale-to-zero), Laravel Cloud answers its health checks on your application's behalf. It does not restart sleeping instances, and they wake on the next request as usual.

## Troubleshooting health check failures

When a health check fails during a deployment, the deployment page names the check that failed, the request Laravel Cloud made, and what went wrong. For example:

> Your readiness health check (GET /up on port 8080) returned HTTP 500, so no traffic was sent to the new release and the deployment was stopped.

The deployment logs include the same explanation, followed by your application's output. The most common causes are:

| Failure | Meaning | What to do |
| - | - | - |
| **Returned HTTP 404** | Your application doesn't serve the endpoint. | Make sure your application serves the path, or change the health check's endpoint. |
| **Returned HTTP 502, 503, or 504** | Your application wasn't accepting requests yet, or crashed while answering. | Check the deployment logs for errors. If your application needs longer to start, raise the startup check's tries or interval. |
| **Returned another status code** | Your endpoint answered with an error. | Only `2xx` and `3xx` responses pass. Check the deployment logs for why the request failed. |
| **Couldn't connect** | Nothing was listening on the check's port. | Make sure your application listens on that port and binds to `::`, as described in [choosing a port](#choosing-a-port). |
| **Got no answer** | The endpoint took longer than the check's timeout to respond. | Make the endpoint respond faster, or raise the check's timeout. |

If a liveness check keeps failing during a deployment, Laravel Cloud restarts the new release's instances and fails the deployment. Your previous release keeps serving traffic. If your liveness endpoint checks a database or another service, review the [guidance on liveness checks](#liveness-checks-and-external-services).

## API

You may also manage health checks using the `probes` attribute when [updating an instance](https://laravel.com/cloud/docs/api/instances/update-instance) through the Laravel Cloud API. Each check accepts the `path`, `port`, `delay`, `interval`, `timeout`, and `tries` keys, all of which are optional:

```json theme={null}
{
    "probes": {
        "startup": {"path": "/up", "tries": 60},
        "readiness": {"path": "/up"},
        "liveness": {"port": 8080}
    }
}
```

The `probes` attribute replaces all of the instance's existing health checks. Set it to `null` to remove them, or leave it out of the request to keep the current checks. As with the dashboard, changes take effect on the environment's next deployment.
