Source: https://laravel.com/cloud/docs/scheduled-tasks.md

# Scheduled tasks

Run recurring commands with Cloud Scheduler or your framework's task scheduler on Laravel Cloud.

## Introduction

Laravel Cloud runs scheduled tasks without requiring you to manage cron infrastructure. Laravel applications use the framework's task scheduler. For non-Laravel applications, [Cloud Scheduler](#other-stacks) runs commands on a schedule you define in the dashboard.

> [tab] Laravel
>
> The Laravel framework includes a built-in "cron" system for [task scheduling](https://laravel.com/docs/scheduling) that runs tasks every minute, hour, day, or at another custom frequency. You can enable the scheduler from the Laravel Cloud dashboard.
>
> ## Enabling the task scheduler
>
> The most direct way to start running scheduled tasks is to enable the task scheduler on your environment's App cluster. On the App cluster, scheduled tasks run on the same compute instances that handle your application's incoming HTTP traffic.
>
> To get started, click your environment's App cluster in the infrastructure canvas dashboard. Then, enable the "Scheduler" toggle. Finally, save and redeploy the changes to your App cluster.
>
> 
>
> After your deployment completes, Laravel Cloud runs the `schedule:run` Artisan command every minute on your App cluster, and your Laravel application processes its scheduled tasks.
>
> > [!NOTE]
> >
> > If you would like to run scheduled tasks on infrastructure that is separate from the compute that handles your incoming web traffic, you may also enable the task scheduler on a [worker cluster](https://laravel.com/cloud/docs/workers#worker-clusters).
>
> ## Scheduled tasks and multiple replicas
>
> If you have scaled your environment's compute to use multiple replicas, make sure you are using Laravel's `onOneServer` method when scheduling your tasks. Otherwise, your tasks will run on every replica, which may lead to unexpected behavior in your application. If you intend for a scheduled task to run on all replicas, you may omit the `onOneServer` method when scheduling the task.
>
> For more information on Laravel task scheduling, consult the [Laravel task scheduler documentation](https://laravel.com/docs/scheduling#running-tasks-on-one-server).
>
> ## Scheduled tasks and scale to zero
>
> When an environment can [scale to zero](https://laravel.com/cloud/docs/compute#scale-to-zero), it automatically wakes to run your scheduled tasks, so they continue to run on schedule even while the environment is sleeping.
>
> To determine when to wake your application, Laravel Cloud relies on the cron schedules reported by the `php artisan schedule:list` command. Each time you deploy, Laravel Cloud runs this command and stores its output. Laravel Cloud then uses the stored schedule to calculate when each of your tasks is next due, and wakes your environment at that time. Because Laravel Cloud captures this output only at deploy time, changes to your task schedule do not take effect until your next deployment.
>
> When the environment wakes to run a scheduled task, it stays awake for the duration of the sleep timeout. To avoid keeping your environment awake continuously, do not schedule tasks at intervals shorter than your sleep timeout. For example, a task that runs every 5 minutes on an environment with a 5-minute sleep timeout will never allow the environment to sleep.
>
> Laravel Cloud points the scheduler's cache driver at your environment's cache store. The task scheduler queries this store only when a task uses Laravel's `withoutOverlapping` or `onOneServer` methods, or when it runs sub-minute tasks. A typical schedule does not query the store on every run. However, if you frequently run tasks that rely on these methods, the resulting cache lookups may keep an attached database or cache awake, so it cannot scale to zero.

> [tab] Symfony
>
> Symfony's [Scheduler component](https://symfony.com/doc/current/scheduler.html) works with Laravel Cloud's scheduler toggle, so you can run recurring messages on a defined frequency.
>
> ## Enabling the task scheduler
>
> To enable the scheduler, click your environment's App cluster in the infrastructure canvas dashboard. Enable the **Scheduler** toggle, then save and redeploy your environment.
>
> 
>
> > [!NOTE]
> >
> > If you would like to run scheduled tasks on infrastructure that is separate from the compute that handles your incoming web traffic, you may also enable the task scheduler on a [worker cluster](https://laravel.com/cloud/docs/workers#worker-clusters).
>
> ## Cron expressions
>
> If your schedule uses `RecurringMessage::cron(...)`, explicitly require `dragonmantank/cron-expression` in your `composer.json`. The `symfony/scheduler` package lists it only as a `require-dev` dependency, so Composer does not install it for production builds:
>
> ```sh theme={null}
> composer require dragonmantank/cron-expression
> ```
>
> Schedules using only `RecurringMessage::every('1 hour')` and similar period-based triggers do not require this package.
>
> ## Scheduled tasks and scale to zero
>
> Symfony environments can still [scale to zero](https://laravel.com/cloud/docs/compute#scale-to-zero), but scheduled tasks will not run while the environment is sleeping. To keep scheduled tasks running on time, run the scheduler on a dedicated [worker cluster](https://laravel.com/cloud/docs/workers#worker-clusters) that does not scale to zero.

> [tab] Other stacks
>
> Cloud Scheduler runs recurring commands for non-Laravel applications. Define each command and its schedule in Cloud, and Cloud runs it on the selected compute cluster. You don't need to install cron or run a scheduling process inside your application.
>
> ## Configure scheduled commands
>
> To add a scheduled command:
>
> 1. Open your environment's App cluster or a [worker cluster](https://laravel.com/cloud/docs/workers#worker-clusters) on the infrastructure canvas.
> 2. In **Scheduled commands**, click **New command**.
> 3. Enter the command and choose a schedule.
> 4. Click **Create**, then save the cluster settings and deploy the environment.
>
> For example, if your repository contains an executable cleanup script at `scripts/cleanup.sh`, use:
>
> ```sh theme={null}
> ./scripts/cleanup.sh
> ```
>
> Commands can read your environment's variables, including your database credentials. You may chain commands with shell operators such as `&&`:
>
> ```sh theme={null}
> python manage.py clearsessions && python manage.py cleanup_uploads
> ```
>
> To change a command or its schedule, edit it in **Scheduled commands** and save the cluster settings. The change takes effect after your next deployment.
>
> ## Schedules
>
> Cloud Scheduler has the following presets:
>
> | Preset | When it runs |
> | - | - |
> | **Every hour** | At a fixed minute past each hour |
> | **Every day** | At a fixed time between 12:00 AM and 12:15 AM UTC |
> | **Every week** | On Sunday, at a fixed time shortly after midnight UTC |
> | **Every month** | On the 1st of the month, at a fixed time shortly after midnight UTC |
>
> When you create a command with a preset, Cloud picks a random offset from the top of the hour or from midnight. The command uses the same offset for every run. To see the exact time, save the command and hover over its next run time.
>
> To run a command at an exact time, select **Custom** and enter a cron expression or an alias such as `@hourly`, `@daily`, `@weekly`, `@monthly`, or `@yearly`. For example, `30 2 * * 1-5` runs at 2:30 AM UTC every weekday. As you type, Cloud describes the expression in plain language. Cloud rejects invalid expressions. All schedules use UTC.
>
> ## Scheduled commands and multiple replicas
>
> Each scheduled command runs on one instance of its cluster, no matter how many replicas the cluster has.
>
> ## Timeouts and interruptions
>
> Each run of a scheduled command may take up to 30 minutes. Cloud stops any run that is still going after 30 minutes.
>
> Cloud cannot guarantee that every run will finish, even within the 30-minute limit. Deployments, scaling, and platform maintenance replace the instances that run your commands. When an instance stops, Cloud sends a `SIGTERM` signal to its processes and waits for your environment's graceful shutdown timeout (30 seconds by default). Then Cloud stops any process that is still running.
>
> For this reason, write scheduled commands so they can safely run again after an interruption. If a task takes longer than a few minutes, consider breaking it into smaller pieces of work and processing them in a [background worker](https://laravel.com/cloud/docs/workers).
>
> ## Scheduled commands and scale to zero
>
> Cloud Scheduler wakes a sleeping App cluster to run its scheduled commands, so you can keep [scale to zero](https://laravel.com/cloud/docs/compute#scale-to-zero) enabled. You don't need to run a separate cron process in your application or configure a manual wake interval for these commands.
>
> If your command enqueues work instead of completing it directly, configure a worker to process that queue. A [worker cluster that stays awake](https://laravel.com/cloud/docs/workers#workers-and-scale-to-zero) can process queued work independently of the App cluster.
>
> ## View command output
>
> Cloud sends the output of each run to your environment's [Logs](https://laravel.com/cloud/docs/logs) dashboard. To view a command's runs, open its **...** menu and select **View logs**. On the Logs page, you may filter to a single scheduled command or to every scheduled command on an instance.
>
> Each log entry includes the command's output, its exit code, and when it started and finished. Cloud highlights runs that exit with a non-zero code.
>
> ## Failed command alerts
>
> When a scheduled command exits with a non-zero code, Cloud notifies you by email or Slack, based on your [notification settings](https://laravel.com/cloud/docs/notifications). Each alert links directly to that command's logs.
>
> Cloud sends at most one failure alert per scheduled command every 24 hours. For example, a command that runs every minute and fails every time produces one alert in 24 hours, not one per run. A successful run resets the limit, so Cloud alerts you right away the next time the command fails.
