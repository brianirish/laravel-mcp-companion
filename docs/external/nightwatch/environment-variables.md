Source: https://nightwatch.laravel.com/docs/environment-variables.md

# Environment Variables

> A complete reference of all environment variables available in Laravel Nightwatch.

This page provides a comprehensive reference of all environment variables available in Nightwatch. These variables can be set in your application's `.env` file or in the environment where your application runs.

## Core

`NIGHTWATCH_TOKEN`

required

Your environment's API token, used to authenticate the Nightwatch agent. Both the Laravel application and the [Nightwatch agent](https://nightwatch.laravel.com/docs/start-guide.md) must be configured with a valid and matching token.

`NIGHTWATCH_ENABLED`

default:
true

Controls whether Nightwatch is active. Set to `false` to disable monitoring, for example during local development or test suite runs.

`NIGHTWATCH_DEPLOY`

default:
auto-detected

An optional identifier for the current deployment or release version. This is automatically detected when using [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com), and [Laravel Vapor](https://vapor.laravel.com).

`NIGHTWATCH_SERVER`

default:
gethostname()

Sets the server name or instance identifier used when reporting events. Defaults to the system hostname.

## Sampling

Sampling controls the rate at which entry points are collected. For more detail, see the [Filtering](https://nightwatch.laravel.com/docs/filtering.md#sampling) documentation.

`NIGHTWATCH_REQUEST_SAMPLE_RATE`

default:
1.0

The percentage of HTTP requests to sample, from `0.0` (none) to `1.0` (all). When a request is sampled in, Nightwatch captures the full execution context. See [Requests: Sampling](https://nightwatch.laravel.com/docs/requests.md#sampling).

`NIGHTWATCH_COMMAND_SAMPLE_RATE`

default:
1.0

The percentage of Artisan commands to sample, from `0.0` to `1.0`. When a command is sampled in, Nightwatch captures the full execution context. See [Commands: Sampling](https://nightwatch.laravel.com/docs/commands.md#sampling).

`NIGHTWATCH_SCHEDULED_TASK_SAMPLE_RATE`

default:
1.0

The percentage of scheduled tasks to sample, from `0.0` to `1.0`. Takes precedence over `NIGHTWATCH_COMMAND_SAMPLE_RATE` when scheduling Artisan commands. See [Scheduled Tasks: Sampling](https://nightwatch.laravel.com/docs/scheduled-tasks.md#sampling).

`NIGHTWATCH_EXCEPTION_SAMPLE_RATE`

default:
1.0

The percentage of exceptions to sample, from `0.0` to `1.0`. When set to `1.0` (default), Nightwatch captures the full execution context for any execution that encounters an exception, regardless of whether it was otherwise sampled. Set to `0` to only capture exceptions from sampled executions. See [Exceptions: Sampling](https://nightwatch.laravel.com/docs/exceptions.md#sampling).

## Data Capture

`NIGHTWATCH_CAPTURE_EXCEPTION_SOURCE_CODE`

default:
true

Controls whether Nightwatch captures source code snippets for exception stack traces. Set to `false` to disable. See [Exceptions: Source Code Capture](https://nightwatch.laravel.com/docs/exceptions.md#source-code-capture).

`NIGHTWATCH_CAPTURE_REQUEST_PAYLOAD`

default:
false

Enables capture of the request payload for requests that resulted in exceptions. Disabled by default due to the sensitive nature of payload data. See [Requests: Capture Request Payloads](https://nightwatch.laravel.com/docs/requests.md#capture-request-payloads).

## Redaction

`NIGHTWATCH_REDACT_HEADERS`

default:
"Authorization,Cookie,Proxy-Authorization,X-XSRF-TOKEN"

A comma-separated list of request headers to redact. See [Requests: Capture Request Headers](https://nightwatch.laravel.com/docs/requests.md#capture-request-headers).

`NIGHTWATCH_REDACT_PAYLOAD_FIELDS`

default:
"\_token,password,password\_confirmation"

A comma-separated list of request payload fields to redact. See [Requests: Capture Request Payloads](https://nightwatch.laravel.com/docs/requests.md#capture-request-payloads).

## Filtering

Filtering allows you to exclude specific event types from collection. For more detail, see the [Filtering](https://nightwatch.laravel.com/docs/filtering.md#filtering) documentation.

`NIGHTWATCH_IGNORE_QUERIES`

default:
false

Excludes all database queries from collection when set to `true`. See [Queries: Filtering](https://nightwatch.laravel.com/docs/queries.md#filtering).

`NIGHTWATCH_IGNORE_CACHE_EVENTS`

default:
false

Excludes all cache events from collection when set to `true`. See [Cache: Filtering](https://nightwatch.laravel.com/docs/cache.md#filtering).

`NIGHTWATCH_IGNORE_MAIL`

default:
false

Excludes all mail events from collection when set to `true`. See [Mail: Filtering](https://nightwatch.laravel.com/docs/mail.md#filtering).

`NIGHTWATCH_IGNORE_NOTIFICATIONS`

default:
false

Excludes all notification events from collection when set to `true`. See [Notifications: Filtering](https://nightwatch.laravel.com/docs/notifications.md#filtering).

`NIGHTWATCH_IGNORE_OUTGOING_REQUESTS`

default:
false

Excludes all outgoing HTTP requests from collection when set to `true`. See [Outgoing Requests: Filtering](https://nightwatch.laravel.com/docs/outgoing-requests.md#filtering).

`NIGHTWATCH_LOG_LEVEL`

default:
env('LOG\_LEVEL') or "debug"

The minimum log level to send to Nightwatch. Takes precedence over Laravel's `LOG_LEVEL` variable. See [Logs: Filtering](https://nightwatch.laravel.com/docs/logs.md#filtering).

## Ingest

These variables control how the Laravel application sends data to the local Nightwatch agent.

`NIGHTWATCH_INGEST_URI`

default:
"127.0.0.1:2407"

The host and port of the local Nightwatch agent. Must be updated when running multiple agents on the same server or when the agent runs as a separate service (e.g., in Docker). See [Start Guide](https://nightwatch.laravel.com/docs/start-guide.md).

`NIGHTWATCH_INGEST_TIMEOUT`

default:
0.5

Timeout in seconds for each send operation to the agent.

`NIGHTWATCH_INGEST_CONNECTION_TIMEOUT`

default:
0.5

Timeout in seconds for establishing a connection with the agent.

`NIGHTWATCH_INGEST_EVENT_BUFFER`

default:
500

The maximum number of events to buffer before flushing to the agent.

## Agent

These variables are consumed by the standalone Nightwatch agent process, typically set in the agent's environment or `.env` file.

`NIGHTWATCH_TOKEN`

required

The authentication token for the agent. Must match the token configured in your Laravel application.

`NIGHTWATCH_INGEST_URI`

default:
"127.0.0.1:2407"

The address and port the agent listens on for incoming data from the application. In Docker, this defaults to `0.0.0.0:2407` to bind to all interfaces.

`NIGHTWATCH_AGENT_LOG_LEVEL`

default:
"info"

Controls the agent's log verbosity. Accepted values: `critical` (silent), `error` (errors only), `verbose` (debug output).
