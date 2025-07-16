# Envoyer - Projects/Heartbeats

*Source: https://docs.envoyer.io/projects/heartbeats*

---

- [Envoyer home page](https://envoyer.io)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#96f3f8e0f9eff3e4d6faf7e4f7e0f3fab8f5f9fb)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://envoyer.io)
- [Dashboard](https://envoyer.io)

Search...NavigationProjectsHeartbeats- [Documentation](/introduction)
- [Community](https://discord.com/invite/laravel)
##### Get Started

- [Introduction](/introduction)
- [Quick Start](/quick-start)

##### Accounts

- [Source Control](/accounts/source-control)
- [Your Account](/accounts/your-account)

##### Projects

- [Management](/projects/management)
- [Servers](/projects/servers)
- [Deployment Hooks](/projects/deployment-hooks)
- [Heartbeats](/projects/heartbeats)
- [Notifications](/projects/notifications)
- [Collaborators](/projects/collaborators)

Projects# Heartbeats

Learn how to monitor your application’s cron jobs.

## [​](#overview)Overview

Heartbeats provide a monitoring mechanism for your Cron jobs or any other scheduled task performed by your application. You may select from a variety of schedule frequencies when creating the heartbeat. So, for example, if your scheduled job runs daily, you should select the 1 Day monitoring option.

After creating a heartbeat, a unique URL will be assigned to the heartbeat. When this URL is called via a HTTP `GET` request, the “Last Check-In” time of your heartbeat will be updated.

If Envoyer does not receive a check-in from your job within the specified monitoring frequency, a notification will be sent to your configured notification channels.

## [​](#heartbeat-urls)Heartbeat URLs

### [​](#calling-manually)Calling Manually

If you are manually modifying your server’s `/etc/crontab` file to define scheduled tasks, you can simply append a curl request to your Cron command. For example:

/etc/crontabCopyAsk AI```
* * * * * user php command && curl http://beats.envoyer.io/heartbeat-id

```

### [​](#calling-with-laravel)Calling With Laravel

If you’re using Laravel’s task scheduler, you may use the `thenPing` method on your scheduled job.

app/Console/Kernel.phpCopyAsk AI```
$schedule->command('foo')->thenPing('http://beats.envoyer.io/heartbeat-id');

```
Was this page helpful?

YesNo[Deployment Hooks](/projects/deployment-hooks)[Notifications](/projects/notifications)On this page
- [Overview](#overview)
- [Heartbeat URLs](#heartbeat-urls)
- [Calling Manually](#calling-manually)
- [Calling With Laravel](#calling-with-laravel)

[Envoyer home page](https://envoyer.io)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://envoyer.io/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://envoyer.io/terms)[Privacy Policy](https://envoyer.io/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.