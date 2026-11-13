Source: https://laravel.com/cloud/docs/requests.md

# Requests

Find your busiest pages, investigate errors, and understand response times.


## Introduction

Open the **Requests** tab under **Monitoring** in any environment to see which pages receive traffic, return errors, or respond slowly. Laravel Cloud tracks metrics separately for each environment, including preview environments.

Use this page to investigate individual URL paths. To see how your overall traffic changes over time, including visits, views, referrers, and countries, use the [traffic metrics](https://laravel.com/cloud/docs/metrics/traffic) on the **Overview** tab.

## Choose the traffic to inspect

By default, the page shows the last 24 hours across all of the environment's active domains. When the environment has more than one domain, use the domain selector to narrow the results to one domain. Choose a time range from **Last hour** to **Last 30 days**. Available ranges depend on your plan's [metrics retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention).

By default, the page shows **Allowed requests**, which are requests the edge network did not block, including requests it answered from its cache. Select **All requests** to also include requests the edge network blocked before they reached your application, such as requests stopped by your [firewall](https://laravel.com/cloud/docs/network#web-application-firewall), which typically return `403 Forbidden`.

Each row groups requests by URL path. For example:

* `/orders/123` and `/orders/456` appear separately, even if they match the same route.
* `/search?q=cloud` and `/search?q=laravel` contribute to the same `/search` row. Query strings do not create separate rows.

The page includes every type of response, including HTML pages, JSON API responses, and assets such as images and scripts. Counts represent requests, not visits or unique visitors.

## Find busy or failing pages

Sort by **Total** to find your busiest paths, or by **4XX** or **5XX** to find paths returning errors. Hover over a status count to see the individual response codes and their counts.

| Column | Responses counted |
| - | - |
| **2XX** | Successful responses, such as `200 OK`. |
| **3XX** | Redirects, such as `301 Moved Permanently` or `302 Found`. |
| **4XX** | Client errors, such as `403 Forbidden` or `404 Not Found`. |
| **5XX** | Server errors, such as `500 Internal Server Error` or `502 Bad Gateway`. |
| **Total** | All responses counted across the four status groups. |

These are the status codes that the [Cloud edge network](https://laravel.com/cloud/docs/network#cloud-edge-network) returns to the client. Sorting by a status group selects paths with responses in that group. Each row still shows all of its status counts.

The table shows up to 200 paths based on the selected sort column. Cloud may estimate counts from sampled traffic. To see the sample percentage when available, hover over the information icon beside **Path**.

## Understand response times

The **P95** column helps you spot slow responses that an average can hide. A P95 of 500 ms means approximately 95% of measured requests took 500 ms or less, while 5% took longer.

Hover over a P95 value to see the 95th percentile and average for two timings:

| Timing | What it measures |
| - | - |
| **Origin** | The time the edge network takes to reach and receive a response from your application, including connection time, so it is more than the time spent running your code. |
| **TTFB** | Time to first byte: the time from when the edge network starts processing a request until it starts sending the response. This does not measure how long the browser takes to download or display the page. |

For a deeper look at individual requests, including the queries, jobs, and exceptions they trigger, connect [Laravel Nightwatch](https://laravel.com/cloud/docs/environments#nightwatch-integration).
