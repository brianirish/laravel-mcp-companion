Source: https://laravel.com/cloud/docs/metrics/databases.md

# Database metrics

Understand the CPU, memory, storage, and compute metrics for your database clusters.

## Introduction

Laravel Cloud shows metrics for each database cluster in two places:

* **The database cluster's page:** navigate to **Organization > Resources > Databases**, click the database cluster, and review the **Metrics** section.
* **The environment's Metrics tab:** open **Monitoring > Metrics** in any environment to see the database cluster attached to it alongside the environment's compute.

Metrics cover the whole database cluster, including every database and schema on it. The charts you see depend on the type of database cluster. Use the time range selector to choose a period, depending on your plan's [retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention).

## Laravel MySQL

[Laravel MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) database clusters show the following charts:

| Chart | What it shows |
| - | - |
| **Resources** | CPU and memory usage, each as a percentage of what the cluster size allows. Hover over the chart to see the memory in use. |
| **Storage** | The disk space the cluster uses. The headline **Current** value is the most recent measurement, and the chart's vertical axis extends to the cluster's provisioned storage. |

Storage includes your data, indexes, and MySQL's [binary logs](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#binary-logs-and-storage-usage), so it can grow even when your tables do not. When a cluster runs low on storage, Laravel Cloud can [upsize it automatically](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#automatic-upsizing).

Sustained high CPU usage usually means the cluster is too small for your workload or that some queries are slow. High memory usage alone does not show that MySQL needs more memory, since it uses memory to cache data. Check query performance and signs of memory pressure before increasing the cluster size, because changing the compute size [restarts the cluster](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#editing-and-resizing-database-clusters) with under a minute of downtime. [Laravel Nightwatch](https://laravel.com/cloud/docs/environments#nightwatch-integration) can show you your slowest queries. See [Database sizing and performance](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#database-sizing-and-performance) to choose a cluster size.

## Serverless Postgres

[Serverless Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) database clusters scale their compute automatically, so they measure compute in compute units instead of CPU and memory percentages:

| Chart | What it shows |
| - | - |
| **Compute** | The compute unit hours the cluster used. One compute unit hour is one compute unit running for one hour, so a cluster running at 0.5 compute units for two hours uses one compute unit hour. The headline **Total** value is the sum for the selected range. Shown on the environment's **Metrics** tab. |
| **Storage** | The current size of your data. Laravel Cloud shows the latest size across the selected range rather than its history. |

A cluster that [scales to zero](https://laravel.com/cloud/docs/resources/databases/postgres#scale-to-zero) uses no compute while it sleeps, which shows as low or zero values in the **Compute** chart. The **Compute** total measures how long the cluster's compute ran and at what size, not its CPU utilization. A cluster that runs continuously at a small size can have a high total without needing more compute. To see whether the cluster reaches its limit, compare individual points to your maximum compute units. For ranges up to **Last 7 days**, each point covers one hour, so a point equal to your maximum means the cluster ran at its maximum for that whole hour.

If queries are slow while the cluster runs at its maximum, look for slow or unindexed queries first. If the cluster still needs more compute, [raise the maximum](https://laravel.com/cloud/docs/resources/databases/postgres#editing-and-resizing-database-clusters). Changing the compute unit range restarts the cluster's compute and briefly drops existing connections.

## AWS RDS

[AWS RDS](https://laravel.com/cloud/docs/private-cloud/rds) database clusters show the following charts:

| Chart | What it shows |
| - | - |
| **Resources** | CPU and memory usage, each as a percentage of what the instance size allows. |
| **Storage** | The disk space the cluster uses, with the chart's vertical axis extending to its provisioned storage. |
| **Connections** | The number of open connections to the database. The headline **Peak** value is the highest number of connections during the selected range. |
| **Operations** | The data written to the primary instance. The headline **Written** value is the total for the selected range. Shown on the database cluster's page for the primary instance only. |

When an RDS cluster has read replicas, use the instance selector on the database cluster's page to switch between the **Primary** instance and each replica.

If **Connections** approaches your database's connection limit, new connections may fail. Reduce the number of replicas or workers that connect at once, or use a larger instance size.

## Canvas hovercard

To check a database cluster at a glance, hover over its card in the infrastructure canvas. The hovercard shows sparklines for the last 6 hours with their most recent values:

* **Laravel MySQL and AWS RDS:** **CPU**, **MEM**, and **Storage** used out of the provisioned storage.
* **Serverless Postgres:** **CU**, the compute unit hours used in the most recent hour, and **Storage**.

If you can view your organization's usage, the hovercard also shows the database cluster's **Current spend**.
