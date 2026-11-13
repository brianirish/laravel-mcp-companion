Source: https://laravel.com/cloud/docs/private-cloud/data-transfer.md

# Data transfer

How data transfer is billed on Private Cloud and how to minimize transfer spend.

## Introduction

On Private Cloud, Laravel Cloud bills data transfer based on where traffic originates, where it is going, and which networking components handle it along the way. Understanding each category can help you design systems that minimize unnecessary transfer spend and reduce latency for your end users.

> [accordion] Data Transfer Out (DTO)
>
> Data Transfer Out refers to traffic leaving your compute to the public internet. This is most commonly HTTP responses served to end users, outbound API calls to external services, or downloads for assets served by your compute. This cost often scales directly with your application's traffic.
>
> * Review your caching strategy. Use Cloud's [cache control](https://laravel.com/cloud/docs/network#cache-control) and [cache rules](https://laravel.com/cloud/docs/private-cloud/edge-network#cache-rules) to reduce traffic that hits your origin compute.
> * Connecting to external services like databases, caches, or other resources that do not use internal connections may disproportionately contribute to bandwidth allocation. When possible, configure [private networking](https://laravel.com/cloud/docs/private-cloud/private-networking) to route connections internally instead of over the public internet.
> * Applications within the same Private Cloud that communicate with each other over their public URLs generate Data Transfer Out and NAT Gateway traffic in both directions. Enable [internal networking](https://laravel.com/cloud/docs/private-cloud/internal-networking) to keep this traffic on the private cluster network instead.
> * Applications that make heavy use of assets such as images and videos should use [object storage](https://laravel.com/cloud/docs/resources/object-storage) to reduce data transfer from your application compute.

> [accordion] Data Transfer In (DTI)
>
> Data Transfer In refers to traffic entering your applications from the public internet. There is no charge for inbound internet traffic, including user traffic, webhooks, or other forms of ingress.
>
> * Although Data Transfer In is free, inbound requests often produce responses from your application, which Cloud bills as **Data Transfer Out**. Consider configuring your [web application firewall](https://laravel.com/cloud/docs/network#web-application-firewall) to reduce unnecessary or malicious inbound request volume.

> [accordion] NAT Gateway
>
> A **NAT (Network Address Translation) Gateway** is a network component that lets compute in a private subnet make outbound connections to the internet. IPv4 traffic from private subnets needs a NAT Gateway to reach the public internet. NAT Gateway traffic is typically equal to or less than your **Data Transfer Out** traffic, and Cloud bills it in addition to **Data Transfer Out**. IPv6 connections don't need a NAT Gateway.
>
> * Cloud bills NAT Gateway traffic in **both directions**, not only outbound requests. For example, if your application makes a `GET` request to download a 1 GiB file, you pay for the small outbound request and for the 1 GiB response that returns through the gateway.
> * Connecting to external services like databases, caches, or other resources that do not use internal connections may disproportionately contribute to bandwidth allocation. When possible, configure [private networking](https://laravel.com/cloud/docs/private-cloud/private-networking) to route connections internally instead of over the public internet.
> * Use IPv6 endpoints where available. IPv6 traffic routes without a NAT Gateway, so it avoids these costs.

> [accordion] Regional Data Transfer
>
> Cloud bills traffic between resources in different Availability Zones (AZs) within the same region in both directions. On Private Cloud, Cloud distributes compute clusters across multiple AZs to enable automatic failover. Cloud also places workloads and balances traffic across the cluster automatically, so inter-AZ transfer is part of the managed high-availability design. Some cross-AZ transfer is healthy and expected in a resilient architecture.

> [accordion] VPC Peering
>
> Cloud bills traffic that flows privately across a VPC peering connection between your Private Cloud and your own AWS account in the same region at a rate well below typical Data Transfer Out. If your Private Cloud connects to services in your own AWS account over VPC Peering, the cost for that traffic is minimal compared to other transfer types.
>
> * When possible, use VPC peering private connections in the same AWS region to avoid cross-region peering rates, which can be significantly higher.
> * If you use VPC peering to connect to high-traffic external resources in your AWS account, such as databases or caches, consider migrating them to Laravel Cloud managed resources. Private Cloud customers can provision RDS and ElastiCache directly inside their Private Cloud VPC, which removes the need for peering altogether. Contact your account team for help with resource migrations.

> [accordion] Cloudflare Edge Traffic
>
> Cloudflare Edge Traffic refers to traffic that Cloudflare's global edge network handles in front of your origin. It has two dimensions. Data transfer is the volume of HTTP(S) responses the edge serves to clients. Requests is the number of HTTP(S) requests the edge handles. A single page load can trigger multiple requests, depending on how your application requests assets.
>
> * Maximize your cache hit ratio with Cloud's [cache control](https://laravel.com/cloud/docs/network#cache-control) and [cache rules](https://laravel.com/cloud/docs/private-cloud/edge-network#cache-rules).
> * Pages that make separate requests for linked assets, such as fonts, images, and JavaScript bundles, add to the request volume that Cloudflare counts.
