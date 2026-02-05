# Forge - Servers/Laravel-Vps

*Source: https://forge.laravel.com/docs/servers/laravel-vps*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Laravel VPS
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)
##### Get Started
- [Introduction](/docs/introduction)
- [Laravel Forge CLI](/docs/cli)
- [Laravel Forge SDK](/docs/sdk)
##### Basics
- [Organizations](/docs/organizations)
- [Teams](/docs/teams)
- [Server Providers](/docs/server-providers)
- [Storage Providers](/docs/storage-providers)
- [Source Control](/docs/source-control)
- [SSH Keys](/docs/ssh)
- [Recipes](/docs/recipes)
- [API](/docs/api)
##### Servers
- [Managing Servers](/docs/servers/the-basics)
- [Server Types](/docs/servers/types)
- [Laravel VPS](/docs/servers/laravel-vps)
- [PHP](/docs/servers/php)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Security](/docs/servers/security)
- [Monitoring](/docs/servers/monitoring)
- [Real-Time Metrics](/docs/servers/real-time-metrics)
##### Sites
- [Managing Sites](/docs/sites/the-basics)
- [Domains](/docs/sites/domains)
- [Deployments](/docs/sites/deployments)
- [Environment Variables](/docs/sites/environment-variables)
- [Commands](/docs/sites/commands)
- [Queues](/docs/sites/queues)
- [Network](/docs/sites/network)
- [Isolation](/docs/sites/user-isolation)
- [Laravel](/docs/sites/laravel)
- [Logs](/docs/sites/logs)
##### Resources
- [Databases](/docs/resources/databases)
- [Database Backups](/docs/resources/database-backups)
- [Caches](/docs/resources/caches)
- [Background Processes](/docs/resources/background-processes)
- [Scheduler](/docs/resources/scheduler)
- [Network](/docs/resources/network)
- [Packages](/docs/resources/packages)
##### Integrations
- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)
- [OpenClaw](/docs/integrations/openclaw)
##### Other
- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)
On this page
- [Introduction](#introduction)
- [Benefits of Laravel VPS](#benefits-of-laravel-vps)
- [Forge Terminal](#forge-terminal)
- [Private networking](#private-networking)
- [Mail ports](#mail-ports)
- [Sudo password reset](#sudo-password-reset)
- [Pricing](#pricing)
Servers
# Laravel VPS
Copy page
Learn about Laravel VPS and instant provisioning.
Copy page
## [​](#introduction) Introduction
Laravel VPS cuts server provisioning from minutes to seconds. One click gets you a fully configured server optimized for modern applications. All Laravel VPS servers are Ubuntu powered servers that you receive full access to, and are offered through our infrastructure partnership with DigitalOcean.
But Laravel VPS offers more than just speed. It’s one of the most affordable cloud provider options in Forge, making it easier to experiment with new projects or scale existing ones. You’ll also get simplified billing through Forge instead of managing separate charges from multiple providers.
## [​](#benefits-of-laravel-vps) Benefits of Laravel VPS
Using Laravel VPS servers offers several benefits:
- No need to link Forge to external server providers like AWS.
- Provision servers in seconds. External server providers can take over 10 minutes.
- Utilize Laravel VPS integrated terminal, and instantly gain SSH access to your Laravel VPS servers directly from Forge.
- Consolidate billing on Laravel Forge, instead of managing billing via an external server provider and Forge.
- You are only billed for the number of hours your Laravel VPS is provisioned.
## [​](#forge-terminal) Forge Terminal
When using Laravel VPS, you can gain SSH access to the server with a fully-functional terminal directly from Forge. To get started, navigate to any of your servers or sites and click the context menu for the server or site, usually on the right side of the page and represented by three dots. Then, click “Launch terminal”.
Alternatively, you may launch the terminal from any server or site page using the `` Control+` `` keyboard shortcut.
## [​](#private-networking) Private networking
All Laravel VPS servers should use their internal hostnames for private networking. Using private hostnames instead of IP addresses provides a more reliable way to connect servers within your infrastructure, as the hostname remains consistent even if the underlying IP address changes.
You can find your server’s private hostname on the server’s “Overview” page in the sidebar, under the “Networking” section. Use this hostname when configuring connections between Laravel VPS servers, such as connecting to a dedicated database server or cache server.
## [​](#mail-ports) Mail ports
Mail ports (25, 465, 587) are blocked by default on Laravel VPS servers to prevent abuse. If you need to send email from your server, use an HTTP / API based service like [Resend](https://resend.com), or contact [Laravel Forge support](/docs/support) to request these ports be unblocked.
## [​](#sudo-password-reset) Sudo password reset
To reset the `forge` sudo password for your Laravel VPS server, navigate to your server’s dashboard and click “Settings”. Within the “Danger Zone” section, click the “Reset password” button in the “Reset sudo password” section.
## [​](#pricing) Pricing
Usage is charged in increments of 1 hour blocks. For example, running a server for 5 minutes will be billed as 1 hour of usage.
Free bandwidth is included when using Laravel VPS servers. This is subject to fair usage, and abuse will be blocked. For more information, see our [trust center](https://trust.laravel.com/?product=forge).
Was this page helpful?
YesNo
[Server Types](/docs/servers/types)[PHP](/docs/servers/php)
⌘I