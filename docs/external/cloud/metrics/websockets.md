Source: https://laravel.com/cloud/docs/metrics/websockets.md

# WebSocket metrics

Understand the message rate and connection metrics for your Laravel Reverb WebSocket clusters.

## Introduction

Laravel Cloud shows metrics for each [Laravel Reverb](https://laravel.com/cloud/docs/resources/websockets) WebSocket cluster in two places:

* **The cluster's page:** navigate to **Organization > Resources > WebSockets**, click your cluster, and review the **Metrics** section. You can also select **... > View metrics** on the cluster card. Use the application selector to view **All applications** on the cluster or a single WebSocket application.
* **The environment's Metrics tab:** open **Monitoring > Metrics** in any environment to see the WebSocket application attached to that environment. This card covers only that application, even when the cluster serves other applications. A **Shared** badge appears when the cluster's applications serve more than one environment.

Use the time range selector to choose a period, depending on your plan's [retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention).

## Message rate

The **Message rate** chart shows how many messages per second pass through Reverb, such as the events your application broadcasts to channels. The headline **Avg** value is the average rate across the selected range.

Spikes in the message rate usually follow events in your application, such as a broadcast sent to a busy channel, which Reverb delivers to every subscribed connection.

## Connections

The **Connections** chart shows the number of WebSocket connections open at each point in time. Each browser tab or client connected to your application counts as one connection. The headline **Current** value is the most recent count.

The chart's vertical axis extends to the cluster's maximum concurrent connections, so you can see how much capacity remains.

Each WebSocket application has its own connection limit, which is the share of the cluster's connections you [allocated to it](https://laravel.com/cloud/docs/resources/websockets#editing-resizing-and-splitting-clusters). Once an application reaches its limit, Reverb rejects new connections to that application, even if the cluster has capacity left. When you view a single application, the axis still extends to the whole cluster's maximum, so compare the line to the application's limit rather than to the top of the chart. Laravel Cloud also sends a [notification](https://laravel.com/cloud/docs/notifications) when an application reaches 90% of its limit.

If an application regularly approaches its limit, allocate more of the cluster's connections to it, or resize the cluster to support more concurrent connections.
