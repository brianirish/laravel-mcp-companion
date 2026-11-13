Source: https://laravel.com/cloud/docs/metrics/traffic.md

# Traffic metrics

Understand the requests, visits, and views your environment receives, and where its traffic comes from.

## Introduction

Open the **Overview** tab under **Monitoring** in any environment to see how much traffic the environment receives and where it comes from. Laravel Cloud measures this traffic at the [Cloud edge network](https://laravel.com/cloud/docs/network#cloud-edge-network), before requests reach your application, so the numbers include requests your application never sees, such as cached responses and requests the edge network blocks.

The page covers the environment's Laravel Cloud domain and its verified custom domains. When the environment has more than one domain, use the domain selector to view **All domains** or a single domain. Use the time range selector to choose a period from **Last hour** to **Last 30 days**, depending on your plan's [retention period](https://laravel.com/cloud/docs/metrics/overview#time-ranges-and-retention).

To find which URL paths return errors or respond slowly, use [Requests](https://laravel.com/cloud/docs/requests) instead.

> [!NOTE]
>
> For busy applications, the edge network measures a sample of requests and estimates the totals from it. When a chart or list uses sampled data, an information icon appears beside its title. Hover over the icon to see the percentage of traffic in the sample. Estimated counts are accurate for spotting trends and comparing pages, but they may differ slightly from the exact number of requests your application received.

## Requests

The **Requests** chart shows every HTTP response the edge network served for the environment during the selected range, stacked by status code class. The classes match the [status columns on the Requests page](https://laravel.com/cloud/docs/requests#find-busy-or-failing-pages), plus **1XX** for informational responses, which are rare in most applications.

The headline value is the total number of requests in the range, and the legend shows the total for each class. This chart counts every request, including requests from bots, crawlers, uptime monitors, and API clients, and requests for images, scripts, and stylesheets.

A rising share of **5XX** responses usually means your application is failing or overloaded. See [502 errors](https://laravel.com/cloud/docs/knowledge-base/502-error) for common causes. A rising share of **4XX** responses can point to broken links, bots probing for common paths, or requests your [firewall](https://laravel.com/cloud/docs/network#web-application-firewall) blocks.

## Visits and views

The **Visits** and **Views** charts estimate how many people use your application:

* **Visits:** a visit is one browsing session from a visitor. A visit begins when someone loads an HTML page from your environment without arriving from another page on the same site, such as from a search engine, a link elsewhere, or by typing the address.
* **Views:** the edge network counts a view for each request a visitor makes. Because a single page load also requests images, scripts, stylesheets, and API endpoints, **Views** is usually much higher than the number of pages your visitors open.

Both charts exclude traffic generated internally by the edge network. Neither chart counts unique visitors, so someone who returns tomorrow counts as a new visit.

The **Recent visitors** card shows the number of visits in the last 5 minutes. It ignores the time range selector and refreshes every minute.

## Top lists

The bottom of the page lists the 10 most common values in each category for the selected range:

| List | What it shows |
| - | - |
| **Top requests** | The URL paths that receive the most requests, of any type. For status codes and response times for each path, use [Requests](https://laravel.com/cloud/docs/requests). |
| **Top pages** | The HTML pages that visitors load most often with a `200` response. Use it to find your most popular pages. |
| **Top referrers** | The sites that link visitors to your application, such as search engines or social networks. |
| **Top countries** | The countries your visits and views come from. |

The bar behind each row shows its share of the 10 rows listed, not its share of all traffic.

## Requests on the dashboard

Your organization's dashboard shows a **Requests (10h)** column for each recent environment. The column shows the total number of requests over the last 10 hours, the percentage of those requests that returned a **5XX** error, and a small bar chart with one bar for every 30 minutes. The error percentage turns red when it exceeds 3%. Hover over a bar to see its time window and the request count for each status class.
