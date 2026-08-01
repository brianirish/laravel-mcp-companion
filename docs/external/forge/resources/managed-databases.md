# Forge - Resources/Managed-Databases

*Source: https://forge.laravel.com/docs/resources/managed-databases*

---

## On this page
- [Introduction](#introduction)
  - [Supported engines](#supported-engines)
- [Creating a database cluster](#creating-a-database-cluster)
- [Cluster overview](#cluster-overview)
  - [Connection credentials](#connection-credentials)
- [Managing databases](#managing-databases)
- [Managing users](#managing-users)
- [Read replicas](#read-replicas)
- [Backups and restoration](#backups-and-restoration)
  - [Configuring backup time](#configuring-backup-time)
  - [Point-in-time recovery](#point-in-time-recovery)
  - [Restoring from a backup](#restoring-from-a-backup)
- [Monitoring](#monitoring)
- [Settings](#settings)
  - [Configuration](#configuration)
  - [Upgrade window](#upgrade-window)
  - [Public access](#public-access)
  - [Deleting a cluster](#deleting-a-cluster)
- [Pricing](#pricing)
Resources
# Managed Databases
Copy pageCopy page
Learn how to create and manage fully managed database clusters with Laravel Forge.
Copy pageCopy page
## [​](#introduction) Introduction
Laravel Forge managed databases let you provision fully managed MySQL and PostgreSQL database clusters without worrying about server administration, patches, or infrastructure. Each cluster includes high availability options, automated daily backups, point-in-time recovery, and real-time monitoring, all managed directly from the Forge dashboard.
Managed databases are offered through our infrastructure partnership with DigitalOcean and billed hourly through Forge, so there is no need to manage a separate provider account.
### [​](#supported-engines) Supported engines
- MySQL 8.4
- PostgreSQL (17, 18)
## [​](#creating-a-database-cluster) Creating a database cluster
To create a new managed database cluster, navigate to your organization’s “Resources” page and click “Create database cluster.” You will be prompted to configure the following options:
- **Cluster name**: A unique name for your cluster. This cannot be changed after creation.
- **Engine**: The database engine and version to use.
- **Region**: The datacenter region where your cluster will be provisioned.
- **Private network**: Choose “Laravel managed” for automatic networking, or select an existing VPC in the chosen region.
- **Compute size**: The CPU and memory allocation for your cluster. Sizes are grouped into categories such as Standard, General Purpose, and Storage Optimized.
- **Storage**: The disk storage for your cluster. The available range depends on the selected compute size and can be adjusted in increments of 10 GB.
- **High availability**: When enabled, a standby node is automatically maintained and will replace the primary node in case of failure. Enabling high availability doubles the monthly cost.
The estimated monthly cost is displayed at the bottom of the creation modal and updates dynamically as you adjust options.
After creating a cluster, it may take a few minutes for the cluster to finish initializing. The cluster’s overview page will display a loading state until the cluster is ready.
## [​](#cluster-overview) Cluster overview
Once your cluster is ready, the overview page displays the cluster’s connection credentials, databases, users, and read replicas.
### [​](#connection-credentials) Connection credentials
The credentials panel provides the connection details needed to connect to your database cluster. Credentials are organized into tabs:
- **Primary**: The main read/write endpoint for your cluster.
- **Standby**: The standby endpoint, available when high availability is enabled.
- **Replicas**: Individual connection details for each read replica.
Each tab displays the host, port, default username, and password. Connection URLs are also provided for quick setup with database clients such as [TablePlus](https://tableplus.com).
By default, managed database clusters only accept connections from resources within the same VPC. This means you must connect from a [Laravel VPS](/docs/servers/laravel-vps) server within the same Forge organization to use private connectivity. Servers provisioned through other providers (e.g., DigitalOcean, Hetzner, or AWS) do not share the same private network and cannot connect privately, even if they are in the same region. To allow connections from servers outside the VPC, you must enable [public access](#public-access) in the cluster’s settings.
## [​](#managing-databases) Managing databases
You can create multiple database schemas within a single cluster. To create a new database, navigate to the cluster’s overview page, click “Add database” in the “Databases” section, and provide a database name.
To delete a database, click the action menu next to the database and select “Delete”.
## [​](#managing-users) Managing users
Database users control who can connect to your cluster. To create a new user, click “Add user” in the “Users” section of the cluster’s overview page, enter a username, and select which databases you would like to give the user access to.
A secure password is automatically generated for each user.
To delete a user, click the action menu next to the user and select “Delete”.
## [​](#read-replicas) Read replicas
Read replicas allow you to distribute read query load across multiple nodes, improving performance for read-heavy applications. Each replica has its own connection endpoint displayed in the credentials panel.
To create a read replica, click “Add replica” in the “Replicas” section of the cluster’s overview page and provide a name. The replica is then initialized, and its status updates in real time.
To delete a replica, click the action menu next to the replica and select “Delete”.
## [​](#backups-and-restoration) Backups and restoration
Managed database clusters include automated daily backups at no additional cost.
### [​](#configuring-backup-time) Configuring backup time
By default, backups are taken daily at 5:30 AM UTC. You can change the backup time by navigating to the cluster’s “Backups” page and clicking the current backup time to open the configuration modal. The time is configured in UTC.
### [​](#point-in-time-recovery) Point-in-time recovery
You can restore your database to any point in time within the last 7 days. This is useful for recovering from accidental data loss or corruption. To perform a point-in-time restore, navigate to the “Backups” page and click “Restore” in the “Restore from point in time” section. You will need to select a date and time, then provide a name for the new cluster.
### [​](#restoring-from-a-backup) Restoring from a backup
You can also restore from a specific daily backup listed on the “Backups” page. Click the action menu next to the backup and select “Restore”. You will need to provide a name for the new cluster.
Both restoration methods create a new database cluster with the restored data. Your existing cluster remains unchanged.
## [​](#monitoring) Monitoring
The “Observe” page provides real-time monitoring charts for your database cluster:
- **CPU usage**: Percentage of CPU utilization over time.
- **Memory usage**: Percentage of memory utilization over time.
- **Disk usage**: Percentage of disk utilization over time.
You can view metrics for the last 1 day, 7 days, or 30 days using the timeframe selector.
## [​](#settings) Settings
The cluster’s “Settings” page allows you to manage the following:
### [​](#configuration) Configuration
You can update the compute size, storage allocation, and high availability status of your cluster by clicking “Update configuration”. The cluster will enter a “Resizing” state during the update and will be temporarily unavailable.
Downscaling compute is currently not supported. You may only increase the compute size of your cluster.
### [​](#upgrade-window) Upgrade window
Required upgrades, such as database engine patches, are applied automatically during the configured maintenance window. You can set the preferred day of the week and hour (UTC) for these upgrades.
### [​](#public-access) Public access
By default, managed database clusters only accept connections from resources within the same private network. Only [Laravel VPS](/docs/servers/laravel-vps) servers within the same Forge organization share this private network. Servers from other providers cannot connect privately, even if they are located in the same region. Enabling public access allows connections from any IP address. A confirmation prompt is displayed when enabling this setting.
### [​](#deleting-a-cluster) Deleting a cluster
You can permanently delete a database cluster from the “Danger” section of the settings page. This action is irreversible. All data, databases, users, and replicas within the cluster will be permanently destroyed.
## [​](#pricing) Pricing
Usage for managed database clusters is billed hourly, similar to [Laravel VPS servers](/docs/servers/laravel-vps#pricing). The total monthly cost is determined by:
- **Compute size**: Each size tier has a base monthly cost.
- **Additional storage**: Storage beyond the base allocation included with your compute size is charged per 10 GB block.
- **High availability**: When enabled, the monthly cost is doubled to account for the standby node.
The following table outlines the base monthly pricing for each compute size, per Forge subscription plan. These prices do not include additional storage or high availability costs.
You can view your current usage and billing history on the organization’s “Usage” page.
Was this page helpful?
YesNo
[Database Backups](/docs/resources/database-backups)[Managed Cache](/docs/resources/managed-cache)
⌘I