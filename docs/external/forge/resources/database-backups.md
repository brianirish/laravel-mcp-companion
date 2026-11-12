Source: https://laravel.com/forge/docs/resources/database-backups.md

# Database Backups

> Learn how to configure and manage automated database backups.

## Introduction

Laravel Forge supports automated database backups that can be scheduled directly from your server's dashboard. You can choose to backup one or more databases at a specified frequency and also restore any of your recent backups. The backup script used by Forge is open source and can be [found on GitHub](https://github.com/laravel/forge-database-backups).

> [!WARNING]
>
> Database backups are only available on the Business plan.

## Creating backup configurations

Before creating a backup configuration, you must configure at least one [storage provider](https://forge.laravel.com/docs/storage-providers.md). When creating a backup configuration, you will select which storage provider to use.

You may optionally override the bucket and directory settings for a specific backup configuration. This allows you to use the same storage provider but store backups in different locations.

### Frequency options

Within the Laravel Forge database backup dashboard, you can select the frequency at which your database should be backed up:

* Hourly
* Daily (at a given time)
* Weekly (on a given day and time)
* Custom

When using the API to create a **Daily** or **Weekly** backup, you may provide any valid time (e.g., `13:37`) to your schedule; however, for the sake of simplicity, the Laravel Forge UI allows you to select a time in 30 minute intervals. The time you select should be in your local time as reported by your web browser.

The **Custom** option allows you to provide a custom cron expression. You may wish to use a service such as [crontab.guru](https://crontab.guru) to help you generate this.

### Backup retention

Laravel Forge will automatically prune old backups for you. For example, if you have configured a backup retention rate of "five", only the last five backups will be stored within your storage provider.

### Notifications for failed backups

You may provide an email address to be notified when a backup fails. If you need to notify multiple people, you should create a distribution list such as `team@example.com`.

Laravel Forge will also display failed backups within the "Backups" panel of the Forge server's management dashboard.

## Managing backups

### Editing backups

Existing backup configurations may be edited via the Laravel Forge UI. By default, the configuration details are locked to prevent accidental edits. You may click the "Edit" button to unlock editing.

When changing the databases that should be backed up, Laravel Forge will ask for confirmation that it was an intended change. This is to prevent any future data loss in the event that a database is no longer part of a backup configuration.

### Deleting backup configurations

You can delete a backup configuration by clicking the "Delete" button next to your chosen backup configuration under the "Backup Configurations" section of the server's "Backups" dashboard.

> [!NOTE]
>
> When deleting a backup configuration, your backup archives **will not be removed from cloud storage**. You may remove these manually if you wish.

### Restoring backups

You can restore backups to your database via the "Recent Backups" section. Click the "Restore" button next to your chosen backup. Backups will be restored to the database they were created from. If the backup configuration contains more than one database, you will be asked to select which database to restore.

If you need to restore a backup to another server or database you may download the backup archive from your cloud storage provider and restore it using a database management tool such as [TablePlus](https://tableplus.com).

### Deleting backups

If you need to delete an individual backup, you can do this by clicking the "Delete" button next to the backup.

> [!WARNING]
>
> When deleting a backup, your backup archives **will be removed** from your cloud storage provider. Please take caution when removing backups.

### Backup output

Each backup process will create its own log so that you can inspect the database backup process's output in the event of a failure. You can view the output of a backup by clicking the "Eye" icon next to your backup.

## Team permissions

The ability to manage database backups is split into two permissions.

* `server:create-backups`
* `server:delete-backups`
