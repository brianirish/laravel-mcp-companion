Source: https://laravel.com/cloud/docs/metrics/compute.md

# Compute metrics

Understand the CPU, memory, replica, and web worker metrics for your App and worker clusters.

## Introduction

Open the **Metrics** tab under **Monitoring** in any environment to see how your [compute clusters](https://laravel.com/cloud/docs/compute) use the resources you give them. The tab shows a card for your App cluster, a card for each [worker cluster](https://laravel.com/cloud/docs/workers#worker-clusters), and cards for the [managed queues](https://laravel.com/cloud/docs/metrics/queues), [databases](https://laravel.com/cloud/docs/metrics/databases), [caches](https://laravel.com/cloud/docs/metrics/caches), [WebSocket applications](https://laravel.com/cloud/docs/metrics/websockets), and [buckets](https://laravel.com/cloud/docs/metrics/object-storage) attached to the environment.

Each compute card's header shows the cluster's region, compute size, and replica range. Use the time range selector to choose a period from **Last hour** to **Last 30 days**, depending on your plan's [retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention). The tab refreshes every minute for ranges up to a day.

Compute metrics start after your environment's first deployment. If you add a worker cluster, its metrics appear after you deploy the environment.

## Resources

The **Resources** chart plots CPU and memory together, each as a percentage of what your compute size allows:

* **CPU:** the CPU your cluster uses as a percentage of its CPU allocation, averaged across all of the cluster's replicas. If your cluster runs three replicas at 90%, 30%, and 30%, the chart shows 50%.
* **MEM:** the memory used by the cluster's busiest replica, as a percentage of the memory allocated to each replica. If your cluster runs three replicas using 80%, 40%, and 40% of their memory, the chart shows 80%. Hover over the chart to see the memory in use, such as `50.0% (512 MiB)`.

The CPU line shows how busy the cluster is overall. An average would hide a single replica running out of memory, so the memory line follows the busiest replica instead.

Sustained high CPU usage means your application needs more processing power, either from more replicas or a larger [compute size](https://laravel.com/cloud/docs/compute#compute-classes). Memory that climbs steadily without dropping between deployments often points to a memory leak, especially with [Laravel Octane](https://laravel.com/cloud/docs/compute#laravel-octane), which keeps your application in memory between requests. Memory can briefly exceed 100% before the replica restarts.

## Replicas

The **Replicas** chart shows how many replicas of the cluster were running over time. Each step in the line is a moment when [autoscaling](https://laravel.com/cloud/docs/compute#autoscaling) added or removed a replica, or when a deployment changed the cluster. The headline **Peak** value is the highest number of replicas that ran during the selected range. The chart's vertical axis extends to the cluster's maximum replica count, which shows how much room the cluster has left to scale.

If your cluster regularly reaches its maximum replicas, it may not have enough capacity for traffic peaks. Raise the maximum in your autoscaling settings or choose a larger compute size.

## Web workers

For PHP applications, the App cluster card also shows a **Web workers** chart. A web worker is a PHP process that serves one request at a time. The chart adds together the workers on every replica in the App cluster:

| Line | Meaning |
| - | - |
| **Active** | Workers currently serving a request. |
| **Idle** | Workers that are running and waiting for a request. |
| **Limit** | The maximum number of workers the cluster can run, based on its compute size and replica count. |
| **Total** | Shown instead of **Limit** when the cluster runs [Laravel Octane](https://laravel.com/cloud/docs/compute#laravel-octane). The number of FrankenPHP workers the cluster started. |

The headline values show the latest **Active** count and the latest **Limit** or **Total**. When **Active** stays close to **Limit**, new requests have to wait for a free worker, which increases response times. Laravel Cloud's [HTTP traffic autoscaling](https://laravel.com/cloud/docs/compute#http-traffic-autoscaling) adds replicas as active requests approach capacity, so clusters below their maximum replica count usually recover without any changes. Faster responses also free workers sooner, so [Laravel Nightwatch](https://laravel.com/cloud/docs/environments#nightwatch-integration) can help you find the slow requests that keep workers busy.

Worker cluster cards show **Resources** and **Replicas** only.

## Canvas hovercard

To check a cluster at a glance, hover over the compute size on its card in the infrastructure canvas. The hovercard shows **CPU** and **MEM** sparklines for the last 6 hours with their most recent values. These use the same calculations as the **Resources** chart. If you can view your organization's usage, the hovercard also shows the cluster's **Current spend**.
