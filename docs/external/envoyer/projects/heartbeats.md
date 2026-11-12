Source: https://docs.envoyer.io/projects/heartbeats.md

# Heartbeats

> Learn how to monitor your application's cron jobs.

## Overview

Heartbeats provide a monitoring mechanism for your Cron jobs or any other scheduled task performed by your application. You may select from a variety of schedule frequencies when creating the heartbeat. So, for example, if your scheduled job runs daily, you should select the 1 Day monitoring option.

After creating a heartbeat, a unique URL will be assigned to the heartbeat. When this URL is called via a HTTP `GET` request, the "Last Check-In" time of your heartbeat will be updated.

If Envoyer does not receive a check-in from your job within the specified monitoring frequency, a notification will be sent to your configured notification channels.

## Heartbeat URLs

### Calling Manually

If you are manually modifying your server's `/etc/crontab` file to define scheduled tasks, you can simply append a curl request to your Cron command. For example:

```text /etc/crontab theme={null}
* * * * * user php command && curl http://beats.envoyer.io/heartbeat-id
```

### Calling With Laravel

If you're using Laravel's task scheduler, you may use the `thenPing` method on your scheduled job.

```php app/Console/Kernel.php theme={null}
$schedule->command('foo')->thenPing('http://beats.envoyer.io/heartbeat-id');
```
