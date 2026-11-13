Source: https://laravel.com/cloud/docs/usage.md

# Usage

Learn how usage, limits, and allowances work on Laravel Cloud.

## Introduction

Laravel Cloud's Usage page gives you an organization-level view of your current spend, resource usage, and how costs are distributed across your applications for the selected billing period.

> [!NOTE]
>
> Laravel Cloud refreshes usage data hourly. Use the billing period selector in the header to view the current billing period or switch to a previous period.

## Summary

At the top of the page, Laravel Cloud shows a summary of your organization's spend for the selected billing period.

For the current billing period, the page shows your current spend based on usage accrued so far. When you switch to a previous billing period, the page shows the total spend for that completed period instead.

Depending on your organization and plan, you may also see additional summary cards:

* **Spending limit**: Shows the threshold you configured and how much remains in the current billing period.
* **Bandwidth**: Shows how much of your accrued bandwidth allowance you have used so far.
* **Credits**: Shows available credits that will apply to upcoming invoices.

If you have not configured a spending limit yet, the page includes a shortcut to set one up. For details, see [Spending limits](https://laravel.com/cloud/docs/spending-limits).

### Bandwidth allowances

Your compute earns bandwidth allowances as it runs, and your whole organization shares them. The Usage page shows how much of that accrued allowance you have used during the selected period.

See [Pricing](https://laravel.com/cloud/docs/pricing#how-bandwidth-allowances-work) for details on how Laravel Cloud calculates bandwidth allowances.

## Resources

The Resources section shows current usage and estimated cost by resource type. At the top of the section, you can switch between four resource categories:

* **Databases**
* **Caches**
* **Buckets**
* **WebSockets**

Each category shows a subtotal. When you select a category, the table updates to show the usage and estimated cost for that resource type. Laravel Cloud also shows the total cost for all resources at the bottom of the section.

### Databases

The Databases view helps you understand how each database contributes to your bill. Depending on the database type, Laravel Cloud shows the database identifier, storage usage, compute usage, backups, and the total cost for that database.

### Caches

The Caches view shows each cache's type, storage details, compute usage in hours, and total cost.

### Buckets

The Buckets view shows storage usage alongside Class A and Class B operations, so you can see whether your bucket costs come mainly from storage or from request volume.

### WebSockets

The WebSockets view shows maximum concurrent connections, usage time in hours, and the total cost for each WebSocket cluster.

For pricing details, see [Resources pricing](https://laravel.com/cloud/docs/pricing#resources).

## Applications

If your organization has applications, the Applications section helps you review compute usage and cost by application and environment.

Use the selectors at the top of the section to choose an application and one of its environments. Laravel Cloud also shows the environment identifier here, so you can match the environment with the identifier that appears on invoices.

For the selected environment, Laravel Cloud groups compute usage into cluster types such as:

* **App clusters**
* **Worker clusters**
* **Managed queues**

Within each cluster type, you can review usage, replica activity, CPU usage in hours, and the total cost for each cluster. If a cluster uses multiple replicas, you can inspect the per-replica breakdown from the Replicas tooltip.

At the bottom of the section, Laravel Cloud shows:

* The selected environment's total cost
* The selected application's total cost
* The total cost across all applications in the organization

For details on compute billing, see [Compute pricing](https://laravel.com/cloud/docs/pricing#compute).

## Add-ons

When your organization has additional billable services or infrastructure costs, Laravel Cloud shows them in the Add-ons section.

This section lists each add-on as a separate line item for the selected billing period, followed by a total cost for all add-ons.
