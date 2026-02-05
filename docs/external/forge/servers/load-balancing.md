# Forge - Servers/Load-Balancing

*Source: https://forge.laravel.com/docs/servers/load-balancing*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Load Balancing
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
- [Creating load balanced sites](#creating-load-balanced-sites)
- [Load balancer methods](#load-balancer-methods)
- [Server configurations](#server-configurations)
- [Server weights](#server-weights)
- [Backup servers](#backup-servers)
- [Pausing traffic](#pausing-traffic)
- [SSL](#ssl)
Servers
# Load Balancing
Copy page
Learn how to horizontally scale your application using load balancers.
Copy page
## [​](#introduction) Introduction
Load balancers are used to distribute web traffic amongst two or more servers and are often used for websites which receive high volumes of traffic.
## [​](#creating-load-balanced-sites) Creating load balanced sites
Load balanced sites can only be created on [load balancer servers](/docs/servers/types#load-balancers).
To create a new load balanced site, navigate to the server’s dashboard, and click New site. Next, provide the name of the site, the balancing method and add the servers you want to balance the traffic to.
The selected servers must have a site with a matching domain, otherwise traffic will not be routed correctly. Forge domains (`on-forge.com`) are not available for load balancers.
## [​](#load-balancer-methods) Load balancer methods
Laravel Forge allows you to select one of three load balancer methods:
1. **Round-robin** - the default method, where requests are distributed evenly across all servers.
2. **Least connections** - requests are sent to the server with the least connections.
3. **IP hash** - the server to which a request is sent is determined by the client IP address. This means that requests from the same address are always handled by the same server unless it is unavailable.
You may switch load balancers method at any time.
You can learn more about how Nginx load balancers work by [consulting the Nginx documentation](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#method).
## [​](#server-configurations) Server configurations
### [​](#server-weights) Server weights
Each server balanced by the load balancer can be configured with different weights, indicating that some servers should serve more traffic than others. For example, if you have two servers in your load balancer, one with a weight of 5 and the other with 1, then the first server would be sent five out of every six requests made to the load balancer.
### [​](#backup-servers) Backup servers
Individual servers can be marked as a **backup**. Backup servers will receive no traffic unless all other servers managed by the load balancer are not responding.
### [​](#pausing-traffic) Pausing traffic
You may pause traffic to a specific server being managed by the balancer. While paused, the selected server will no longer serve incoming traffic. You may unpause the server at any time.
## [​](#ssl) SSL
Typically, SSL certificates are installed on the individual application servers. However, when using load balancing, the certificate should be configured on the load balancer itself. You should consult the [SSL documentation](/docs/sites/domains#certificates) for more information on managing SSL certificates for your servers, including load balancers.
When using SSL on a load balancer, you will likely need to configure the “trusted proxies” for your application. For Laravel applications, consult the [trusted proxies documentation](https://laravel.com/docs/requests#configuring-trusted-proxies).
Was this page helpful?
YesNo
[PHP](/docs/servers/php)[Nginx Templates](/docs/servers/nginx-templates)
⌘I