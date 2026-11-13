Source: https://laravel.com/cloud/docs/metrics/overview.md

# Metrics

Learn where Laravel Cloud shows metrics for your applications and resources, and what they tell you.

## Introduction

Laravel Cloud collects metrics for your environments and the resources they use, so you can see how your application handles traffic, how much compute it needs, and whether a database or cache is running out of storage. You do not need to install anything to collect them.

Metrics appear in two places:

* **Environment monitoring:** open an environment and select **Monitoring** to see traffic, requests, compute, and queue metrics for that environment. The **Metrics** tab also shows the databases, caches, WebSocket applications, and buckets attached to the environment.
* **Resource pages:** navigate to **Organization > Resources**, choose a resource type, and click a resource to see its **Metrics** section. A resource page shows metrics for the whole resource, even when several environments share it.

## Where to find each metric

| Page | What it shows | Where to find it |
| - | - | - |
| [Traffic](https://laravel.com/cloud/docs/metrics/traffic) | Requests, visits, page views, and top pages, referrers, and countries | **Monitoring > Overview** in an environment |
| [Requests](https://laravel.com/cloud/docs/requests) | Request counts, status codes, and response times for each URL path | **Monitoring > Requests** in an environment |
| [Compute](https://laravel.com/cloud/docs/metrics/compute) | CPU, memory, replicas, and web workers for App and worker clusters | **Monitoring > Metrics** in an environment |
| [Queues](https://laravel.com/cloud/docs/metrics/queues) | Job volume, duration, memory, workers, and failed jobs for managed queues | **Monitoring > Queues** in an environment |
| [Databases](https://laravel.com/cloud/docs/metrics/databases) | CPU, memory, storage, and compute usage for database clusters | The database cluster's page, or **Monitoring > Metrics** |
| [Caches](https://laravel.com/cloud/docs/metrics/caches) | Throughput, hits and misses, storage, and bandwidth | The cache's page, or **Monitoring > Metrics** |
| [WebSockets](https://laravel.com/cloud/docs/metrics/websockets) | Message rate and open connections | The WebSocket cluster's page, or **Monitoring > Metrics** |
| [Object storage](https://laravel.com/cloud/docs/metrics/object-storage) | Operations, errors, egress, and bucket size | The bucket's page, or **Monitoring > Metrics** |

## Time ranges and retention

Every metrics page has a time range selector. Environment monitoring pages offer **Last hour**, **Last 6 hours**, **Last day**, **Last 7 days**, and **Last 30 days**. Resource pages offer the same ranges, except **Last hour**. The managed queues dashboard also offers **Last 5 minutes** and a custom range.

How far back you can look depends on your plan's log and metrics retention period. Ranges beyond your plan's retention appear disabled in the selector:

| Plan | Retention | Longest range |
| - | - | - |
| Starter | 1 day | **Last day** |
| Growth | 7 days | **Last 7 days** |
| Business | 30 days | **Last 30 days** |
| Enterprise | Custom | **Last 30 days** |

See the [plans feature table](https://laravel.com/cloud/docs/pricing#plans) for the full list of plan features.

Each range ends about one minute before the current time, so the most recent minute of data does not appear yet. Longer ranges show fewer, wider data points. For example, a chart covering the last hour may plot a point every minute, while a chart covering the last 30 days may plot one point every few hours. Laravel Cloud keeps the highest and lowest values when it thins out a chart, so short spikes stay visible.

## Canvas hovercards

The infrastructure canvas gives you a quick look at recent metrics without leaving the environment overview. Hover over the compute size on an App cluster, worker cluster, or managed queue card, or over a database or cache card, to see a small chart of the last 6 hours along with its most recent value. If you can view your organization's usage, the hovercard also shows the resource's **Current spend**.

## Permissions

Viewing metrics requires permission to view an environment's metrics. The Admin, Manager, Developer, and Viewer [team roles](https://laravel.com/cloud/docs/rbac#team-roles) all include it. Some details, such as the failed job payloads on the managed queues dashboard or **Current spend** on canvas hovercards, require additional permissions.

## Going deeper with Nightwatch

Laravel Cloud's metrics tell you how your infrastructure is behaving. To understand why, such as which queries, jobs, or exceptions make a request slow, connect [Laravel Nightwatch](https://laravel.com/cloud/docs/environments#nightwatch-integration) to your environment. Nightwatch traces individual requests, jobs, and commands through your application code.
