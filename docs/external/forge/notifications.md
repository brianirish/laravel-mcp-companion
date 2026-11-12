Source: https://laravel.com/forge/docs/notifications.md

# Notifications

> Control which Laravel Forge notifications you receive, and on which channel.

## Introduction

Laravel Forge sends notifications for server and site events, including completed server provisioning, failed deployments, and monitor alerts.

* **Personal notification preferences.** These apply to your own account and control which notifications Laravel Forge sends you, and whether they arrive by email, in the notification center, or both.
* **Resource notification channels.** These are configured for individual sites, monitors, and backup configurations and are sent to their configured recipients.

This page covers personal notification preferences. To configure resource notifications, see [deployment notifications](https://forge.laravel.com/docs/sites/deployments.md#deployment-notifications), [backup notifications](https://forge.laravel.com/docs/resources/database-backups.md#notifications-for-failed-backups), and [server monitoring](https://forge.laravel.com/docs/servers/monitoring.md).

## Notification channels

Laravel Forge delivers personal notifications on two channels:

| Channel | Delivery |
| - | - |
| Email | Sent to the email address on your Laravel Forge account. |
| In-app | Shown in the notification center within the Laravel Forge dashboard. |

You can enable or disable email and in-app notifications independently. When a channel is disabled, its individual notification preferences are hidden.

> [!NOTE]
>
> Preferences are per user. Changing yours does not affect what your organization's other members receive.

## Managing your preferences

To manage your notification preferences, click your avatar in the top right corner of the dashboard, click "Account", then click "Notifications" in the sidebar. Use the "Enable email notifications" and "Enable in-app notifications" switches to control each channel as a whole, then check or uncheck individual notifications in the "Email" and "In-app" columns. Once done, click "Save".

A checkbox is disabled when the notification cannot be delivered on that channel. Hovering over it explains why.

## Available notifications

The tables below list every notification covered by personal preferences, along with its **default state** on each channel.

### Server notifications

| Notification | What it covers | Email | In-app |
| - | - | - | - |
| Server provisioned | A new server has finished provisioning and is ready. | On | On |
| Server provisioning failed | Something went wrong while provisioning a server. | Off | On |
| Server deletion failed | A server could not be deleted from your provider. | Off | On |
| Server marked as stale | A server has not been used for a while and may be worth reviewing. | Unavailable | On |
| Server monitor alert | A resource monitor crossed its alert threshold, or recovered afterward. | On | On |
| Heartbeat check-in missed | A heartbeat monitor missed its expected check-in. | On | On |
| Backup failed | A scheduled database backup failed to complete. | On | On |
| Recipe execution report | A summary report after a recipe finishes running on a server. | On | On |

### Site notifications

| Notification | What it covers | Email | In-app |
| - | - | - | - |
| Deployment succeeded | A deployment finished successfully. | Unavailable | On |
| Deployment failed | A deployment failed to complete. | On | On |
| SSL certificate renewal failed | A certificate could not be renewed. Includes the error log for diagnosis. | On | On |
| Site health check failed | A site failed its health check and may need attention. | Off | On |

## Muting servers

Mute a server to stop personal notifications for it and its sites without changing your preferences for other servers.

To mute a server, open the notifications page, click the "Muted servers" dropdown, and check each server you want to silence. Servers are grouped by organization, and the search field filters the list. Click "Save" to apply your changes.

> [!WARNING]
>
> Muting does not affect notifications configured in a site's own settings. If your email address appears on a site's failure notification recipient list, you will continue to receive those emails for a muted server, because that list delivers to raw addresses rather than to Laravel Forge accounts. Remove your address from the site's recipients to stop them.

Archived servers and servers you can no longer access are removed from the muted servers list the next time you save the page. If you restore the server or regain access, mute it again if needed.
