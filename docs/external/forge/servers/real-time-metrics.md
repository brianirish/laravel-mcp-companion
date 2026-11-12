Source: https://laravel.com/forge/docs/servers/real-time-metrics.md

# Real-Time Metrics

> Learn how to view real-time server metrics in Laravel Forge.

## Introduction

Laravel Forge provides real-time metrics for servers provisioned through supported providers. These interactive charts allow you to monitor your server's performance and resource utilization over various time periods, helping you identify trends and respond to issues quickly.

> [!WARNING]
>
> Real-time metrics are only available for Laravel VPS, Hetzner, and DigitalOcean server providers.

## Available metrics

The following real-time metrics are available for your servers:

* **CPU** - displays the percentage of CPU resources being utilized by your server over time.
* **Memory** - displays the percentage of RAM being used by your server.
* **Disk Usage** - displays the percentage of storage space being consumed on your server's primary drive.
* **Inbound Bandwidth** - displays the network traffic coming into your server, measured in Mbps.
* **Outbound Bandwidth** - displays the network traffic leaving your server, measured in Mbps.

## Viewing metrics

To view real-time metrics for your server, navigate to the server's "Observe" tab, and then click "Metrics". The metrics dashboard will display interactive charts for each available metric.

### Time scopes

You can adjust the time range displayed in the charts to view metrics over different periods:

* **1 hour** - view metrics for the last hour, ideal for monitoring immediate performance changes.
* **6 hours** - review metrics over the last six hours to identify short-term trends.
* **24 hours** - analyze a full day of metrics to understand daily usage patterns.
* **7 days** - examine a week's worth of data to spot longer-term trends or recurring issues.
* **1 month** - review a month of metrics for capacity planning and historical analysis.

These time scopes allow you to quickly identify performance issues, correlate events across different metrics, and make informed decisions about server scaling and optimization.
