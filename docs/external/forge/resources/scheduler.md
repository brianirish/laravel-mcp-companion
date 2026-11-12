Source: https://laravel.com/forge/docs/resources/scheduler.md

# Scheduler

> Learn how to configure and manage scheduled jobs on your Laravel Forge server.

## Scheduled jobs

Laravel Forge enables you to configure scheduled jobs that run commands at specified intervals on either a server or site level. You can choose from predefined frequencies or create custom Cron schedules tailored to your specific needs.

> [!TIP]
>
> If your scheduled job fails to run, verify that the command path is correct and accessible.

### Laravel application scheduling

For Laravel applications using the built-in [scheduler feature](https://laravel.com/docs/scheduling), you can use the [Laravel integration](https://forge.laravel.com/docs/sites/laravel.md#laravel-scheduler) to quickly configure the scheduled job.

### Default scheduled jobs

Laravel Forge automatically configures essential maintenance jobs during server provisioning:

* **Update Composer:** Runs `composer self-update` nightly to keep Composer current
* **Remove unused packages:** Performs Ubuntu package cleanup weekly to maintain system efficiency

These default jobs help ensure your server remains updated and optimized without manual intervention.

## Managing scheduled jobs

### Creating scheduled jobs

To create a scheduled job, navigate to "Server / Processes / Scheduler" or "Site / Processes / Scheduler" depending on your requirements. Then, click the "Add scheduled job" button. Configure the command, user, and frequency settings, then click the "Create scheduled job" button to activate it.

Server-level jobs are ideal for system maintenance tasks, while site-level jobs are perfect for application-specific commands like Laravel's scheduler or custom deployment scripts.

### Editing scheduled jobs

To edit a scheduled job, navigate to the appropriate "Processes / Scheduler" section. Then, click on the dropdown next to the job you want to modify. Click the "Edit" dropdown item and update the job configuration as needed.

### Running scheduled jobs manually

You can manually execute a scheduled job by clicking on the dropdown next to the job and selecting "Run". This is useful for testing jobs or running them outside their normal schedule.

Jobs executed via the "Run" dropdown option have a 60 second maximum execution length timeout. Regular scheduled jobs executed via cron do not have this timeout limitation.

### Deleting scheduled jobs

To delete a scheduled job, navigate to the "Processes / Scheduler" section. Then, click on the dropdown next to the job you want to remove. Click the "Delete" dropdown item and confirm that you want to delete the scheduled job.

## Heartbeats

Heartbeats provide proactive monitoring for your scheduled jobs, ensuring they execute successfully and on time. This feature helps you identify failed or stuck jobs before they impact your application.

### Configuring heartbeat monitoring

When creating or editing a scheduled job, enable monitoring by toggling the "Monitor with heartbeats" option. Once enabled, specify the notification threshold by setting the "Notify me after" value in minutes.

Laravel Forge generates a unique endpoint URL that your scheduled job must ping upon successful completion. If Forge doesn't receive a heartbeat ping within the specified timeframe, you'll be notified that the job is missing or has failed to execute.

### Using heartbeat endpoints

Your scheduled job should include a request to the provided heartbeat endpoint as its final step. This confirms successful execution and resets the monitoring timer. You can implement the ping using curl, HTTP libraries, or Laravel's HTTP client depending on your job's requirements.

This monitoring system is particularly valuable for critical maintenance tasks, data processing jobs, and backup operations where timely execution is essential for your application's health.

Applications running Laravel can use the `pingBefore` and `thenPing` methods to automatically send heartbeats when using the Laravel scheduler. [Read the Laravel documentation](https://laravel.com/docs/scheduling#pinging-urls).
