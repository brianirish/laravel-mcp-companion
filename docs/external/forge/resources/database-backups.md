# Forge - Resources/Database-Backups

*Source: https://forge.laravel.com/docs/resources/database-backups*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Resources

Database Backups

[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)

- [Community](https://discord.gg/laravel)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)

##### Get Started

- [Introduction](/docs/introduction)
- [Laravel Forge CLI](/docs/cli)
- [Laravel Forge SDK](/docs/sdk)

##### Basics

- [Organizations](/docs/organizations)
- [Teams](/docs/teams)
- [Server Providers](/docs/server-providers)
- [Storage Providers](/docs/storage-providers)
- [Source Control](/docs/source-control)
- [SSH Keys](/docs/ssh)
- [Recipes](/docs/recipes)
- [API](/docs/api)

##### Servers

- [Managing Servers](/docs/servers/the-basics)
- [Server Types](/docs/servers/types)
- [Laravel VPS](/docs/servers/laravel-vps)
- [PHP](/docs/servers/php)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Security](/docs/servers/security)
- [Monitoring](/docs/servers/monitoring)
- [Real-Time Metrics](/docs/servers/real-time-metrics)

##### Sites

- [Managing Sites](/docs/sites/the-basics)
- [Domains](/docs/sites/domains)
- [Deployments](/docs/sites/deployments)
- [Environment Variables](/docs/sites/environment-variables)
- [Commands](/docs/sites/commands)
- [Queues](/docs/sites/queues)
- [Network](/docs/sites/network)
- [Isolation](/docs/sites/user-isolation)
- [Laravel](/docs/sites/laravel)
- [Logs](/docs/sites/logs)

##### Resources

- [Databases](/docs/resources/databases)
- [Database Backups](/docs/resources/database-backups)
- [Caches](/docs/resources/caches)
- [Background Processes](/docs/resources/background-processes)
- [Scheduler](/docs/resources/scheduler)
- [Network](/docs/resources/network)
- [Packages](/docs/resources/packages)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)
- [OpenClaw](/docs/integrations/openclaw)

##### Other

- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)

On this page

- [Introduction](#introduction)
- [Creating backup configurations](#creating-backup-configurations)
- [Frequency options](#frequency-options)
- [Backup retention](#backup-retention)
- [Notifications for failed backups](#notifications-for-failed-backups)
- [Managing backups](#managing-backups)
- [Editing backups](#editing-backups)
- [Deleting backup configurations](#deleting-backup-configurations)
- [Restoring backups](#restoring-backups)
- [Deleting backups](#deleting-backups)
- [Backup output](#backup-output)
- [Team permissions](#team-permissions)

Resources

# Database Backups

Copy page

Learn how to configure and manage automated database backups.

Copy page

## [​](#introduction) Introduction

Laravel Forge supports automated database backups that can be scheduled directly from your server’s dashboard. You can choose to backup one or more databases at a specified frequency and also restore any of your recent backups. The backup script used by Forge is open source and can be [found on GitHub](https://github.com/laravel/forge-database-backups).

Database backups are only available on the Business plan.

## [​](#creating-backup-configurations) Creating backup configurations

Before creating a backup configuration, you must configure at least one [storage provider](/docs/storage-providers). When creating a backup configuration, you will select which storage provider to use.
You may optionally override the bucket and directory settings for a specific backup configuration. This allows you to use the same storage provider but store backups in different locations.

### [​](#frequency-options) Frequency options

Within the Laravel Forge database backup dashboard, you can select the frequency at which your database should be backed up:

- Hourly
- Daily (at a given time)
- Weekly (on a given day and time)
- Custom

When using the API to create a **Daily** or **Weekly** backup, you may provide any valid time (e.g., `13:37`) to your schedule; however, for the sake of simplicity, the Laravel Forge UI allows you to select a time in 30 minute intervals. The time you select should be in your local time as reported by your web browser.
The **Custom** option allows you to provide a custom cron expression. You may wish to use a service such as [crontab.guru](https://crontab.guru) to help you generate this.

### [​](#backup-retention) Backup retention

Laravel Forge will automatically prune old backups for you. For example, if you have configured a backup retention rate of “five”, only the last five backups will be stored within your storage provider.

### [​](#notifications-for-failed-backups) Notifications for failed backups

You may provide an email address to be notified when a backup fails. If you need to notify multiple people, you should create a distribution list such as `[email protected]`.
Laravel Forge will also display failed backups within the “Backups” panel of the Forge server’s management dashboard.

## [​](#managing-backups) Managing backups

### [​](#editing-backups) Editing backups

Existing backup configurations may be edited via the Laravel Forge UI. By default, the configuration details are locked to prevent accidental edits. You may click the “Edit” button to unlock editing.
When changing the databases that should be backed up, Laravel Forge will ask for confirmation that it was an intended change. This is to prevent any future data loss in the event that a database is no longer part of a backup configuration.

### [​](#deleting-backup-configurations) Deleting backup configurations

You can delete a backup configuration by clicking the “Delete” button next to your chosen backup configuration under the “Backup Configurations” section of the server’s “Backups” dashboard.

When deleting a backup configuration, your backup archives **will not be removed from cloud storage**. You may remove these manually if you wish.

### [​](#restoring-backups) Restoring backups

You can restore backups to your database via the “Recent Backups” section. Click the “Restore” button next to your chosen backup. Backups will be restored to the database they were created from. If the backup configuration contains more than one database, you will be asked to select which database to restore.
If you need to restore a backup to another server or database you may download the backup archive from your cloud storage provider and restore it using a database management tool such as [TablePlus](https://tableplus.com).

### [​](#deleting-backups) Deleting backups

If you need to delete an individual backup, you can do this by clicking the “Delete” button next to the backup.

When deleting a backup, your backup archives **will be removed** from your cloud storage provider. Please take caution when removing backups.

### [​](#backup-output) Backup output

Each backup process will create its own log so that you can inspect the database backup process’s output in the event of a failure. You can view the output of a backup by clicking the “Eye” icon next to your backup.

## [​](#team-permissions) Team permissions

The ability to manage database backups is split into two permissions.

- `server:create-backups`
- `server:delete-backups`

Was this page helpful?

YesNo

[Databases](/docs/resources/databases)[Caches](/docs/resources/caches)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)