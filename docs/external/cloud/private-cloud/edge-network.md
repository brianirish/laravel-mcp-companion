Source: https://laravel.com/cloud/docs/private-cloud/edge-network.md

# Dedicated edge network

An isolated edge zone with custom rules, cache rules, and traffic visibility.

## Introduction

A dedicated edge network gives your organization its own isolated edge zone with full control over caching, custom rules, and traffic visibility. The dedicated edge network appears as the **Private network** card on your environment's canvas.

A dedicated edge network includes everything in the [shared Cloud edge network](https://laravel.com/cloud/docs/network), plus:

* **Rule builder**: Create cache rules and custom rules with execution ordering inside each rule type.
* **Custom rules**: Match requests on conditions like path, IP, country, or headers, and apply a challenge, block, or IP access action.
* **Cache rules**: Override default caching with per-path control over cache eligibility, edge TTL, browser TTL, stale-while-revalidate, and ETag handling.
* **Traffic visibility**: Review the top IP addresses and paths hitting your edge over the last 24 hours, 7 days, or 30 days.
* **Rule event counts**: See how many requests matched each custom rule and rate limit rule in the last 24 hours.

> [!NOTE]
>
> Dedicated edge networks are available as an add-on to the [Business plan](https://laravel.com/cloud/docs/pricing) for an additional fee. [Private Cloud](https://laravel.com/cloud/docs/private-cloud) includes one dedicated edge network. [Contact Sales](https://laravel.com/enterprise) to request one.

## Custom rules

Custom rules let you define request-matching conditions and apply an action to anything that matches. Use them to block known-bad traffic, allow specific clients, challenge suspicious requests, or restrict access by IP.

Each custom rule has:

* **Conditions**: Request properties to match against, including path, hostname, IP, country, user agent, headers, and query parameters.
* **Action**: What happens to a matching request. Available actions are challenge, block, and IP access (allow or block specific addresses or ranges).
* **Name**: A human-readable label for the rule.

Rules execute in order within the custom rules section, and the first matching rule wins. You can reorder rules by dragging them.

To create a custom rule, click the **Private network** card on your environment's canvas, then add a new rule under **Custom rules**.

## Cache rules

Cache rules give you per-path control over how the edge caches content. They override the default extension-based caching behavior described in the [Cloud edge network](https://laravel.com/cloud/docs/network) documentation.

Each cache rule applies to requests matching its conditions and lets you configure:

* **Cache eligibility**: Whether matching responses are eligible for caching at all.
* **Edge TTL**: How long the response stays in the edge cache.
* **Browser TTL**: The cache lifetime served to the client browser.
* **Serve stale while revalidating**: Serve a stale response while the edge fetches a fresh copy in the background.
* **Respect strong ETags**: Honor strong ETag validators on origin responses.

Cache rules execute in order within the cache rules section, independent of custom rules. You can reorder them by dragging.

> [!NOTE]
>
> Cache rules do not display per-rule hit counts. Use the traffic cards on the network overview to understand cache performance instead.

## Traffic visibility

The network overview displays cards with the top IP addresses and top paths hitting your dedicated edge network. Use the time filter to switch between the last 24 hours (the default), 7 days, or 30 days.

Click a row in the traffic cards to open a new custom rule pre-filled with that IP or path as a condition. You can then block or challenge that traffic.

## Rule event counts

Custom rules and rate limit rules display an inline event count next to each rule. The count shows how many requests matched in the last 24 hours. Cache rules do not display this count.

## Nameserver monitoring

A dedicated edge network works only while your domain's NS records point to the nameservers that Laravel Cloud assigned to it. If someone removes or changes those records at your domain registrar, every application on the edge network stops receiving traffic.

Cloud checks the nameservers of each dedicated edge network every hour. If the nameservers no longer point to Cloud, Cloud marks the edge network as inactive and notifies your organization by email and Slack. The alert lists the nameservers to restore. After you restore them at your registrar, the edge network becomes active again. DNS changes can take up to 48 hours to propagate.

Cloud also runs [domain health](https://laravel.com/cloud/docs/domains#domain-health) checks on the custom domains that use the edge network.
