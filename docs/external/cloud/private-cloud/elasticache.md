Source: https://laravel.com/cloud/docs/private-cloud/elasticache.md

# ElastiCache

Managed AWS ElastiCache caches (Valkey and Redis OSS).

## Introduction

Laravel Cloud provides fully managed AWS ElastiCache caches (both Valkey and Redis OSS) for your application. ElastiCache supports automatic failover and multi-AZ deployments.

> [!NOTE]
>
> ElastiCache is only available with [Private Cloud](https://laravel.com/cloud/docs/private-cloud). If you do not see ElastiCache as an option when creating a cache, [contact us](https://laravel.com/enterprise) to provision a dedicated cluster in your chosen region.

## Creating ElastiCache caches

To create and attach an ElastiCache cache to an environment:

1. Navigate to **Organization > Resources > Caches**
2. Click **+ New cache**
   * **Cache name**: a unique name for your ElastiCache cache
   * **Type**: choose **AWS ElastiCache Valkey** or **AWS ElastiCache Redis**
   * **Region**: choose a Private Cloud region
   * **Configuration**: choose a preset or customize your ElastiCache configuration

> [!NOTE]
>
> It may take up to 20 minutes for your ElastiCache cache to be fully created. You do not need to stay on the page.

Once the cache is created, you can attach it to any environment in the same region. After you attach a cache to an environment, redeploy the environment for the changes to take effect.

[Contact us](https://laravel.com/enterprise) for information on ElastiCache pricing per region.

## Customizing ElastiCache caches

Laravel Cloud gives you full control over your ElastiCache configuration. When you create or edit an ElastiCache cluster, you may control the following settings.

### Choosing the right node size

Laravel Cloud offers a range of node sizes across the `cache.t4g`, `cache.m7g`, `cache.m8g`, `cache.r7g`, `cache.r8g`, `cache.c7gn`, and `cache.c8gn` instance families. The amount of RAM your node has determines how much data your cache can hold and the number of concurrent connections it can support.

You can update your node size at any point. When multi-AZ is enabled, Laravel Cloud scales up or down online with no downtime.

### Selecting a deployment option

Laravel Cloud supports the following ElastiCache deployment options:

* **Single-AZ cache instance**. One node in a single availability zone. Best for development or non-critical workloads.
* **Single-AZ cache instance, with read replicas**. One primary node plus up to 5 read replicas for read-heavy workloads and high availability.
* **Multi-AZ cache instance**. One primary node and one replica node, placed in separate availability zones. Best for production workloads that require high availability.

> [!NOTE]
>
> Multi-AZ deployments include a replica node and provide automatic failover if the primary node becomes unavailable.

### Picking a maintenance window

AWS may occasionally need to perform maintenance on your ElastiCache cluster, which may cause brief failover events.

To control your scheduled maintenance window, click **Edit settings > Maintenance window** and pick a day and 60-minute time slot. If you don't pick a time slot, AWS performs those updates during the default time slot for your region.

## Connecting to ElastiCache caches

### From your application

When you attach a cache to an environment, Laravel Cloud automatically injects connection environment variables, including `REDIS_HOST` and `REDIS_PASSWORD`. Laravel applications can also use `CACHE_STORE` with the `Cache` facade. You may view these variables under **Environment > Settings > General > Injected variables**.

### From your local machine

ElastiCache caches are not publicly accessible by default. You can reach them only from within your Private Cloud network.

## Detaching and deleting your cache

If your project no longer needs a cache, you can detach it from your application canvas.

> [!WARNING]
>
> **Detaching a cache does not delete it.** Because many applications can share a cache, you can only detach a cache from your application, not delete it.
>
> Laravel Cloud bills caches for their availability, whether or not an application uses them. To permanently delete a cache, visit your [organization's Resources page](https://laravel.com/to/org/resources/caches).

You may delete an ElastiCache cluster from your [organization's Resources page](https://laravel.com/to/org/resources/caches). Navigate to the **Caches** tab and click the **...** icon for the cluster you would like to delete. Then, click **Delete cache**.

## Cache backups

Laravel Cloud ElastiCache caches support automated daily backups.

### Backup configuration

To configure backups for your ElastiCache cluster:

1. Navigate to **Organization > Resources > Caches**.
2. Click the **...** menu for your ElastiCache cluster and select **Edit settings**.
3. Find the **Backups** field.
4. Select a backup type:
   * **Daily backups**: enable automatic daily backups
   * **None**: disable automatic backups
5. If you enable daily backups, configure **Backup retention**.
6. Click **Update** to save your settings.

### Backup retention period

If you select daily backups, you can configure a retention period of 1 to 35 days. Laravel Cloud takes automatic backups once per day during your cluster's snapshot window.

[Contact us](https://laravel.com/enterprise) for information on ElastiCache backup storage costs.

## Monitoring ElastiCache performance

To view metrics such as throughput, cache storage, and cache hit and miss ratios for your ElastiCache cluster, navigate to **Organization > Resources > Caches**, click your cluster, and review the **Metrics** section. Use the time range selector to adjust the period shown.
