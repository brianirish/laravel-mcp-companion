Source: https://nightwatch.laravel.com/docs/notifications.md

# Notifications

> Notifications sent via Laravel's notification system

Nightwatch captures notifications sent via Laravel's notification system (email, SMS, Slack, etc.), including recipient details, channel used, and timestamp.

## Notification List

The notification page lists the notification classes that have been observed in your application, with statistics for the total number of notifications sent and the average and p95 processing times.

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of notifications. It
> highlights outliers, bottlenecks and inconsistent behavior that average times
> hide.

## Notification Details

Click on a notification class to view all instances sent during the selected time period, including the channel, timestamp, and duration for each. You may select an instance to view the full trace for that notification within the context of its parent execution.

## Sampling

There are no direct sampling controls for notifications, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

## Filtering

There are a number of different methods to filter notification events.

### Filtering All Notification Events

To completely disable the collection of all notification events, set the `NIGHTWATCH_IGNORE_NOTIFICATIONS` environment variable to `true`:

```bash theme={null}
NIGHTWATCH_IGNORE_NOTIFICATIONS=true
```

### Filtering Specific Notification Events

You can filter out specific notification events using the `Nightwatch::rejectNotifications()` method:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Notification;

Nightwatch::rejectNotifications(function (Notification $notification) {
    return $notification->channel === 'database';
});
```

## Redaction

There are no specific redaction methods for notifications. Notification data is captured as-is from Laravel's notification system.
