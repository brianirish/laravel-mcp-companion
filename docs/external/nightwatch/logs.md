Source: https://nightwatch.laravel.com/docs/logs.md

# Logs

> Structured logs from Laravel's logging system

Nightwatch ingests structured logs from Laravel's logging system in real-time, allowing you to search and correlate them alongside requests, jobs, and other event types.

## Log Viewer

The Logs page lists all log entries, including their level, message, contextual data and timestamps. Each entry is automatically linked to its [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts), letting you trace the message back to the exact request, job, command, or scheduled task that generated it and explore all accompanying events.

## Log Context

Nightwatch automatically surfaces any contextual data attached to a log entry, giving you deeper insight into what was happening at the moment the message was written. Clicking a log entry opens the details drawer, where you can explore both the **Log Context** and **Log Extra** sections.

For guidance on supplying context when writing logs, see Laravel’s documentation on [contextual information](https://laravel.com/docs/logging#contextual-information).

> [!NOTE]
>
> Public context added via the `Context` facade is available in the **Extra**
> section of the details drawer.

## Configuring your logging setup

There are several ways to configure Nightwatch as part of your logging setup.

### Option 1: Adding Nightwatch to the Log Stack (Recommended)

If you're using the default `stack` driver, you can simply add Nightwatch to the list of channels in your `.env` file:

```env theme={null}
LOG_CHANNEL=stack
LOG_STACK=single,nightwatch
```

### Option 2: Exclusively send logs to Nightwatch

If you'd prefer to send logs exclusively to Nightwatch, you can set it as your main log channel in your `.env` file:

```env theme={null}
LOG_CHANNEL=nightwatch
```

> [!WARNING]
>
> If you have enabled sampling and require all logs to be captured then you
> should not use Nightwatch as your only log channel. Nightwatch will not
> capture logs from requests, commands, jobs, and scheduled tasks that are not
> captured due to sampling.

### Option 3: Create a Custom Stack

If you're using a custom log channel (e.g. syslog, etc.) and want to use it in combination with Nightwatch, you can create a custom stack in your `.env` file:

```env theme={null}
LOG_CHANNEL=stack
LOG_STACK=syslog,nightwatch
```

For more information on Logging channels and how to combine them, refer to [Laravel's logging documentation](https://laravel.com/docs/logging#introduction).

## Sampling

There are no direct sampling controls for logs, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

## Filtering

### Log Level Filtering

By default, Nightwatch respects Laravel's default logging behavior, but you can customize which logs are sent to Nightwatch using the `NIGHTWATCH_LOG_LEVEL` environment variable.

```bash theme={null}
NIGHTWATCH_LOG_LEVEL=warning
```

This setting ensures that only logs at the specified level or higher (e.g., warning, error, critical) are sent to Nightwatch. Lower-level logs (e.g., info, debug) will be ignored.

The Nightwatch logger is configured to respect [Laravel's standard logging behavior](https://laravel.com/docs/logging). It follows these rules in priority order:

* `NIGHTWATCH_LOG_LEVEL` environment variable
* Laravel's `LOG_LEVEL` environment variable
* If neither variable is set, Nightwatch logs all messages of `debug` level and higher sent to the `nightwatch` log channel

> [accordion] Example
>
> In the following example, Laravel's single channel would log `warning` level and higher, while Nightwatch would log `error` level and higher.
>
> ```bash theme={null}
> LOG_CHANNEL=stack
> LOG_STACK=single,nightwatch
> LOG_LEVEL=warning
> NIGHTWATCH_LOG_LEVEL=error
> ```

> [accordion] Log Levels
>
> | Log level | Description |
> | - | - |
> | `debug` | Detailed debug information |
> | `info` | Interesting events |
> | `notice` | Uncommon events |
> | `warning` | Exceptional occurrences that are not errors |
> | `error` | Runtime errors |
> | `critical` | Critical conditions |
> | `alert` | Action must be taken immediately |
> | `emergency` | Urgent alert |

For more information on log levels, refer to [Laravel's logging documentation](https://laravel.com/docs/logging#log-levels).

## Redaction

There are no specific redaction methods for logs. Log data is captured as-is from Laravel's logging system.
