# Forge - Servers/Load-Balancing

*Source: https://forge.laravel.com/docs/servers/load-balancing*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#05636a77626045696477647360692b666a68)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersLoad Balancing[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)
##### Get Started

- [Introduction](/docs/introduction)
- [Forge CLI](/docs/cli)
- [Forge SDK](/docs/sdk)

##### Accounts

- [Your Account](/docs/accounts/your-account)
- [Circles](/docs/accounts/circles)
- [Source Control](/docs/accounts/source-control)
- [SSH Keys](/docs/accounts/ssh)
- [API](/docs/accounts/api)
- [Tags](/docs/accounts/tags)
- [Troubleshooting](/docs/accounts/cookbook)

##### Servers

- [Server Providers](/docs/servers/providers)
- [Server Types](/docs/servers/types)
- [Management](/docs/servers/management)
- [Root Access / Security](/docs/servers/provisioning-process)
- [SSH Keys / Git Access](/docs/servers/ssh)
- [PHP](/docs/servers/php)
- [Packages](/docs/servers/packages)
- [Recipes](/docs/servers/recipes)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Database Backups](/docs/servers/backups)
- [Monitoring](/docs/servers/monitoring)
- [Cookbook](/docs/servers/cookbook)

##### Sites

- [The Basics](/docs/sites/the-basics)
- [Applications](/docs/sites/applications)
- [Deployments](/docs/sites/deployments)
- [Commands](/docs/sites/commands)
- [Packages](/docs/sites/packages)
- [Queues](/docs/sites/queues)
- [Security Rules](/docs/sites/security-rules)
- [Redirects](/docs/sites/redirects)
- [SSL](/docs/sites/ssl)
- [User Isolation](/docs/sites/user-isolation)
- [Cookbook](/docs/sites/cookbook)

##### Resources

- [Daemons](/docs/resources/daemons)
- [Databases](/docs/resources/databases)
- [Caches](/docs/resources/caches)
- [Network](/docs/resources/network)
- [Scheduler](/docs/resources/scheduler)
- [Integrations](/docs/resources/integrations)
- [Cookbook](/docs/resources/cookbook)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Abuse](/docs/abuse)

Servers# Load Balancing

Learn how to use load balancers to distribute traffic across multiple servers.

## [​](#overview)Overview

Load balancers are used to distribute web traffic amongst two or more servers and are often used for websites which receive high volumes of traffic.

The key differences between a Forge application server and a load balancer are:

- A database server will not be installed

- PHP is not installed

- Node.js is not installed

## [​](#creating-load-balancers)Creating Load Balancers

When provisioning a new server, select the **Load Balancer** type. Once provisioning has completed, you can now create a load balanced site. The site name / domain should match the name of the corresponding site on the servers that will be receiving the traffic.

Once you have added the site to your server, Forge will ask you to select the servers you wish to balance traffic across. The list of servers will include all of the servers in the same private network as the load balancer.

### [​](#load-balancer-methods)Load Balancer Methods

Forge allows you to select one of three load balancer methods:

- Round Robin - The default method, where requests are distributed evenly across all servers.

- Least Connections - Requests are sent to the server with the least connections.

- IP Hash - The server to which a request is sent is determined by the client IP address. This means that requests from the same address are always handled by the same server unless it is unavailable.

You may switch the load balancer method at any time.

You can learn more about how Nginx load balancers work by [consulting the Nginx documentation](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#method).

### [​](#server-weights)Server Weights

Each server balanced by the load balancer can be configured with different weights, indicating that some servers should serve more traffic than others. For example, if you have two servers in your load balancer, one with a weight of 5 and the other with 1, then the first server would be sent five out of every six requests made to the load balancer.

### [​](#backup-servers)Backup Servers

Individual servers can be marked as a **backup**. Backup servers will receive no traffic unless all other servers managed by the load balancer are not responding.

### [​](#pausing-traffic)Pausing Traffic

You may pause traffic to a specific server being managed by the balancer. While paused, the selected server will no longer serve incoming traffic. You may unpause the server at any time.

## [​](#ssl)SSL

Typically, SSL certificates are installed on the individual application servers. However, when using load balancing, the certificate should be configured on the load balancer itself. You should consult the [SSL documentation](/docs/sites/ssl#ssl) for more information on managing SSL certificates for your servers, including load balancers.

When using SSL on a load balancer, you will likely need to configure the “trusted proxies” for your application. For Laravel applications, consult the [trusted proxies documentation](https://laravel.com/docs/requests#configuring-trusted-proxies).

Was this page helpful?

YesNo[Recipes](/docs/servers/recipes)[Nginx Templates](/docs/servers/nginx-templates)On this page
- [Overview](#overview)
- [Creating Load Balancers](#creating-load-balancers)
- [Load Balancer Methods](#load-balancer-methods)
- [Server Weights](#server-weights)
- [Backup Servers](#backup-servers)
- [Pausing Traffic](#pausing-traffic)
- [SSL](#ssl)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.