Source: https://laravel.com/cloud/docs/spending-limits.md

# Spending limits

Set a monthly spending limit to monitor or cap your Laravel Cloud bill, with optional alerts and compute shutdown.

A spending limit is a monthly threshold that helps you track and control how much your Laravel Cloud organization spends during a billing period. You can use a spending limit only to stay informed through alerts, or pair it with compute shutdown to enforce a hard cap. Combined with the per-second pricing of [scale to zero](https://laravel.com/cloud/docs/compute#scale-to-zero), spending limits help you set a clear monthly budget before the month begins.

Spending limits are available on the Starter, Growth, and Business plans.

## Setting a spending limit

To set a spending limit, go to **Organization > Settings > Billing > Spending limit**, and enter a monthly amount. The limit must be at least \$5, and there is no maximum value.


When you set a limit, you can choose how Laravel Cloud responds as your spend approaches and reaches the amount.

### Alerts only

By default, a spending limit acts as a notification threshold. Laravel Cloud sends alerts as your spend approaches and reaches the limit, at 50%, 80%, 90%, and 100% of the amount. Your resources keep running normally even after your spend exceeds the limit, so this option never interrupts your applications.

Laravel Cloud emails alerts to the organization's admins and billing contact. You may also enable Slack notifications in a channel of your choice from **Organization > Settings > Notifications**.

### Alerts with compute shutdown

For a hard cap, enable the **Stop all compute** option in addition to alerts. With this option enabled, Laravel Cloud still sends the approaching-limit alerts. When your organization reaches the limit, Laravel Cloud stops new resource provisioning and pauses your running app, database, and cache compute.

Laravel Cloud lets in-flight operations finish, so a small overage is possible.


> [!NOTE]
>
> Object storage and database storage remain active even when compute is stopped, so your data is preserved and you can resume quickly. Because storage stays active, your final bill may slightly exceed your spending limit.

Spending stays paused until you raise the limit or the next billing period begins. At that point, provisioning and compute resume automatically.

## Resuming compute

If Laravel Cloud has shut off your compute, you don't need to wait for the next billing period to bring your applications back online. Go to **Organization > Settings > Billing > Spending limit** and edit the limit to raise it above your current spend, or remove it entirely. As soon as you update the limit, new resource provisioning and your app, database, and cache compute resume automatically.
