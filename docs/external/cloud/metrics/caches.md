Source: https://laravel.com/cloud/docs/metrics/caches.md

# Cache metrics

Understand the throughput, hit and miss, storage, and bandwidth metrics for your caches.

## Introduction

Laravel Cloud shows metrics for each cache in two places:

* **The cache's page:** navigate to **Organization > Resources > Caches**, click your cache, and review the **Metrics** section.
* **The environment's Metrics tab:** open **Monitoring > Metrics** in any environment to see the cache attached to it alongside the environment's compute.

Metrics cover the whole cache, even when several environments share it. Use the time range selector to choose a period, depending on your plan's [retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention).

## Throughput

The **Throughput** chart shows how many operations your application sends to the cache each second:

* **Reads:** commands that read data, such as `GET`.
* **Writes:** commands that write data, such as `SET`.
* **Commands:** all commands the cache processes, including reads and writes.

A sudden rise in throughput usually follows a change in your application, such as a new feature that caches more data or a loop that reads the cache many times per request.

## Hit and miss

The **Hit/Miss** chart shows how many read requests per second found the key they asked for:

* **Hit:** the key existed, so your application used the cached value.
* **Miss:** the key did not exist, so your application had to compute the value or fetch it from its source, such as your database.

The headline values show the average rate of each across the selected range. To estimate your hit rate, divide hits by the sum of hits and misses. A falling hit rate often means keys are expiring too quickly, or the cache is full and evicting keys to make room for new ones.

## Storage

The **Storage** chart shows how much data the cache holds. The headline **Current** value is the most recent measurement, and the chart's vertical axis extends to your cache size's limit. For [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey), storage is the memory the cache uses.

When storage reaches the limit, the cache may evict keys or reject writes that need more memory, depending on its [eviction policy](https://laravel.com/cloud/docs/resources/caches/valkey#picking-an-eviction-policy). For example, Laravel Valkey's `noeviction` policy rejects these writes rather than removing keys. If storage stays close to the limit, resize the cache to a larger size, or let Laravel Valkey [upsize it automatically](https://laravel.com/cloud/docs/resources/caches/valkey#automatic-upsizing).

## Bandwidth

[Redis by Upstash](https://laravel.com/cloud/docs/resources/caches/redis) caches also show a **Bandwidth** chart, which shows the data transferred to and from the cache. The headline **Total** value is the data transferred during the current calendar month, regardless of the selected time range. Compare it to your cache size's [monthly data transfer allowance](https://laravel.com/cloud/docs/resources/caches/redis#bandwidth-limits-and-auto-upgrades).

Laravel Valkey has no data transfer allowance, so its metrics do not include bandwidth.

## Canvas hovercard

To check a cache at a glance, hover over its card in the infrastructure canvas. The hovercard shows a **Storage** sparkline for the last 6 hours, with the most recent storage used out of the cache size's limit. If you can view your organization's usage, the hovercard also shows the cache's **Current spend**.
