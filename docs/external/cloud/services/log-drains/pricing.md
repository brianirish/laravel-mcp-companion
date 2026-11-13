Source: https://laravel.com/cloud/docs/services/log-drains/pricing.md

# Log Drains Pricing

Learn how Laravel Cloud bills log drains and how to view your usage.

## Introduction

Laravel Cloud bills log drains on two metrics:

* **Log Drain Compute**: the time each drain is configured and running.
* **Log Drain Volume**: the volume of data the drain processes.

## Log Drain Compute

### How charges are calculated

You are charged only for the time each drain is running, measured by the second. Laravel Cloud sums the compute time across all of your drains for the period.

For example, if your billing period runs from January 1 to January 31 and you configure a drain on January 10 at 4:30 PM that runs for the remainder of the period, you are billed from 4:30 PM on January 10 through the end of the month:

| Window | Drain running | Time billed |
| - | - | - |
| Jan 1, 00:00:00 – Jan 10, 4:30 PM | No | 0 |
| Jan 10, 4:30 PM – Jan 31, 23:59:59 | Yes | 511.5 hours |

### Pricing

\$0.0685 per hour, metered per second, or approximately \$50 per month.

## Log Drain Volume

### How charges are calculated

You're charged for the uncompressed log data your drains process before sending it to their destinations. Laravel Cloud meters volume in bytes with no rounding, so you pay for exactly the data processed.

### Pricing

\$0.25 per GB, metered per byte.

## Data Transfer Out

Data sent by your drains to their destinations qualifies for free data transfer under your [bandwidth allowance](https://laravel.com/cloud/docs/pricing#bandwidth). If you have exceeded your bandwidth allowance, additional data transfer costs \$0.10 per GB.

## Billing example

Consider a single drain that runs for an entire monthly billing period of approximately 730 hours. It processes 10 GB of uncompressed log data and transfers 2.2 GB out to the drain destination. For illustration, this example assumes you have exceeded the bandwidth allowance. The following table shows only the charges related to the drain:

| Line item | Units | Cost |
| - | - | - |
| Log Drain Compute | 730 hours | \$50.00 |
| Log Drain Volume | 10 GB | \$2.50 |
| Data Transfer Out | 2.2 GB | \$0.22 |
| **Total** | | **\$52.72** |

## View usage

Your organization's [Usage](https://laravel.com/cloud/docs/usage) page shows log drain usage across all projects by default. Filter to a single project or environment, or change the billing period, to see per-drain compute and volume processed.
