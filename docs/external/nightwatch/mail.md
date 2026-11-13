Source: https://nightwatch.laravel.com/docs/mail.md

# Mail

> Outbound emails sent via Laravel's mail system

Nightwatch captures outbound emails sent via Laravel's mail system, including subject, recipient, and delivery status. This makes it easier to trace email issues without needing to check your mail provider dashboard.

## Mail List

The mail page lists the email classes that have been observed in your application, with statistics for the total number of emails sent and the average and p95 for processing time.

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of emails. It
> highlights outliers, bottlenecks and inconsistent behavior that average times
> hide.

## Mail Details

Click on a mail class to view all emails sent for that mailable during the selected time period, including the subject, mail driver, attachment count, and a recipient breakdown (To, CC, and BCC). You may select an instance to view the full trace for that email within the context of its parent execution.

## Sampling

There are no direct sampling controls for mail events, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

## Filtering

There are a number of different methods to filter mail events.

### Filtering All Mail Events

To completely disable the collection of all mail events, set the `NIGHTWATCH_IGNORE_MAIL` environment variable to `true`:

```bash theme={null}
NIGHTWATCH_IGNORE_MAIL=true
```

### Filtering Specific Mail Events

You can filter out specific mail events using the `Nightwatch::rejectMail()` method:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Mail;

Nightwatch::rejectMail(function (Mail $mail) {
    return str_contains($mail->subject, 'Newsletter');
});
```

## Redaction

You can manually redact sensitive information from mail subjects using the `redactMail` callback:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Mail;

Nightwatch::redactMail(function (Mail $mail) {
    $mail->subject = str_replace('secret', '***', $mail->subject);
});
```
