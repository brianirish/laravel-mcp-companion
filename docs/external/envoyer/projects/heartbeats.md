# Envoyer - Projects/Heartbeats

*Source: https://docs.envoyer.io/projects/heartbeats*

---

[Envoyer home page![light logo](https://mintcdn.com/envoyer/t2bz6kuyoDJvJvYR/logo/light.svg?fit=max&auto=format&n=t2bz6kuyoDJvJvYR&q=85&s=f90c47f92772d2c636d509fe836b1feb)![dark logo](https://mintcdn.com/envoyer/t2bz6kuyoDJvJvYR/logo/dark.svg?fit=max&auto=format&n=t2bz6kuyoDJvJvYR&q=85&s=53c14c20c18b8e4cd5659d574dc07c45)](https://envoyer.io)

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://envoyer.io)
- [Dashboard](https://envoyer.io)

Search...

Navigation

Projects

Heartbeats

- [Documentation](/introduction)
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

On this page

- [Overview](#overview)
- [Heartbeat URLs](#heartbeat-urls)
- [Calling Manually](#calling-manually)
- [Calling With Laravel](#calling-with-laravel)

Projects

# Heartbeats

Learn how to monitor your application’s cron jobs.

## [​](#overview) Overview

Heartbeats provide a monitoring mechanism for your Cron jobs or any other scheduled task performed by your application. You may select from a variety of schedule frequencies when creating the heartbeat. So, for example, if your scheduled job runs daily, you should select the 1 Day monitoring option.
After creating a heartbeat, a unique URL will be assigned to the heartbeat. When this URL is called via a HTTP `GET` request, the “Last Check-In” time of your heartbeat will be updated.
If Envoyer does not receive a check-in from your job within the specified monitoring frequency, a notification will be sent to your configured notification channels.

## [​](#heartbeat-urls) Heartbeat URLs

### [​](#calling-manually) Calling Manually

If you are manually modifying your server’s `/etc/crontab` file to define scheduled tasks, you can simply append a curl request to your Cron command. For example:

/etc/crontab

Copy

Ask AI

```
* * * * * user php command && curl http://beats.envoyer.io/heartbeat-id
```

### [​](#calling-with-laravel) Calling With Laravel

If you’re using Laravel’s task scheduler, you may use the `thenPing` method on your scheduled job.

app/Console/Kernel.php

Copy

Ask AI

```
$schedule->command('foo')->thenPing('http://beats.envoyer.io/heartbeat-id');
```

Was this page helpful?

YesNo

[Deployment Hooks](/projects/deployment-hooks)[Notifications](/projects/notifications)

⌘I

[Envoyer home page![light logo](https://mintcdn.com/envoyer/t2bz6kuyoDJvJvYR/logo/light.svg?fit=max&auto=format&n=t2bz6kuyoDJvJvYR&q=85&s=f90c47f92772d2c636d509fe836b1feb)![dark logo](https://mintcdn.com/envoyer/t2bz6kuyoDJvJvYR/logo/dark.svg?fit=max&auto=format&n=t2bz6kuyoDJvJvYR&q=85&s=53c14c20c18b8e4cd5659d574dc07c45)](https://envoyer.io)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Platform

[Dashboard](https://envoyer.io/)[Status](https://status.laravel.com/)

Legal and Compliance

[Term of Service](https://envoyer.io/terms)[Privacy Policy](https://envoyer.io/privacy)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)