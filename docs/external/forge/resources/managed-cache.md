# Forge - Resources/Managed-Cache

*Source: https://forge.laravel.com/docs/resources/managed-cache*

---

## On this page
- [Introduction](#introduction)
- [Creating a cache cluster](#creating-a-cache-cluster)
- [Cluster overview](#cluster-overview)
  - [Connection credentials](#connection-credentials)
- [Monitoring](#monitoring)
- [Settings](#settings)
  - [Configuration](#configuration)
  - [Upgrade window](#upgrade-window)
  - [Public access](#public-access)
  - [Deleting a cluster](#deleting-a-cluster)
- [Pricing](#pricing)
Resources
# Managed Cache
Copy pageCopy page
Learn how to create and manage fully managed cache clusters with Laravel Forge.
Copy pageCopy page
## [​](#introduction) Introduction
Laravel Forge managed cache clusters let you provision fully managed Valkey clusters without worrying about server administration, patches, or infrastructure. Each cluster includes high availability options and real-time monitoring, all managed directly from the Forge dashboard.
Managed cache clusters are offered through our infrastructure partnership with DigitalOcean and billed hourly through Forge, so there is no need to manage a separate provider account.
## [​](#creating-a-cache-cluster) Creating a cache cluster
To create a new managed cache cluster, navigate to your organization’s “Resources” section, select the “Cache” page, and click “Create cache cluster.” You will be prompted to configure the following options:
- **Cluster name**: A unique name for your cluster. This cannot be changed after creation.
- **Region**: The datacenter region where your cluster will be provisioned.
- **Private network**: Choose “Laravel managed” for automatic networking, or select an existing VPC in the chosen region.
- **Compute size**: The CPU and memory allocation for your cluster. Sizes are grouped into categories such as Standard and Memory Optimized.
- **High availability**: When enabled, a standby node is automatically maintained and will replace the primary node in case of failure. Enabling high availability doubles the monthly cost.
The estimated monthly cost is displayed at the bottom of the creation modal and updates dynamically as you adjust options.
After creating a cluster, it may take a few minutes for initialization to finish. The cluster’s overview page will display a loading state until the cluster is ready.
## [​](#cluster-overview) Cluster overview
Once your cluster is ready, the overview page displays the cluster’s connection credentials.
### [​](#connection-credentials) Connection credentials
The credentials panel provides the connection details needed to connect to your cache cluster. Credentials are organized into tabs:
- **Primary**: The main read/write endpoint for your cluster.
- **Standby**: The standby endpoint, available when high availability is enabled.
Each tab displays the host, port, default username, and password. Connection URLs are also provided for quick setup with clients such as [TablePlus](https://tableplus.com).
By default, managed cache clusters only accept connections from resources within the same VPC. This means you must connect from a [Laravel VPS](/docs/servers/laravel-vps) server within the same Forge organization to use private connectivity. Servers provisioned through other providers (e.g., DigitalOcean, Hetzner, or AWS) do not share the same private network and cannot connect privately, even if they are in the same region. To allow connections from servers outside the VPC, you must enable [public access](#public-access) in the cluster’s settings.
## [​](#monitoring) Monitoring
The “Observe” page provides real-time monitoring charts for your cache cluster:
- **CPU usage**: Percentage of CPU utilization over time.
- **Memory usage**: Percentage of memory utilization over time.
- **Disk usage**: Percentage of disk utilization over time.
You can view metrics for the last 1 day, 7 days, or 30 days using the timeframe selector.
## [​](#settings) Settings
The cluster’s “Settings” page allows you to manage the following:
### [​](#configuration) Configuration
You can update the compute size and high availability status of your cluster by clicking “Update configuration”. The cluster will enter a “Resizing” state during the update and will be temporarily unavailable.
Downscaling compute is currently not supported. You may only increase the compute size of your cluster.
### [​](#upgrade-window) Upgrade window
Required upgrades, such as Valkey patches, are applied automatically during the configured maintenance window. You can set the preferred day of the week and hour (UTC) for these upgrades.
### [​](#public-access) Public access
By default, managed cache clusters only accept connections from resources within the same private network. Only [Laravel VPS](/docs/servers/laravel-vps) servers within the same Forge organization share this private network. Servers from other providers cannot connect privately, even if they are located in the same region. Enabling public access allows connections from any IP address. A confirmation prompt is displayed when enabling this setting.
### [​](#deleting-a-cluster) Deleting a cluster
You can permanently delete a cache cluster from the “Danger” section of the settings page. This action is irreversible. All data within the cluster will be permanently destroyed.
## [​](#pricing) Pricing
Usage for managed cache clusters is billed hourly, similar to [Laravel VPS servers](/docs/servers/laravel-vps#pricing). The total monthly cost is determined by:
- **Compute size**: Each size tier has a base monthly cost.
- **High availability**: When enabled, the monthly cost is doubled to account for the standby node.
The following table outlines the base monthly pricing for each compute size, per Forge subscription plan. These prices do not include high availability costs.
You can view your current usage and billing history on the organization’s “Usage” page.
Was this page helpful?
YesNo
[Managed Databases](/docs/resources/managed-databases)[Object Storage](/docs/resources/object-storage)
⌘I