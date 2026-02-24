# Forge - Servers/Types

*Source: https://forge.laravel.com/docs/servers/types*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Server Types
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
- [Server Types](#server-types)
- [App Servers](#app-servers)
- [Web Servers](#web-servers)
- [Database Servers](#database-servers)
- [Cache Servers](#cache-servers)
- [Worker Servers](#worker-servers)
- [Meilisearch Servers](#meilisearch-servers)
- [Load Balancers](#load-balancers)
- [OpenClaw Servers](#openclaw-servers)
Servers
# Server Types
Copy page
Learn about the different types of servers you can provision with Laravel Forge.
Copy page
## [​](#introduction) Introduction
Laravel Forge supports provisioning several different types of servers:
- Application Servers
- Web Servers
- Worker Servers
- Load Balancers
- Database Servers
- Cache Servers
Below, we will discuss each of these server types in more detail.
## [​](#server-types) Server Types
For reference, here is a breakdown of what is offered by each server type:
| Type | Nginx | PHP | MySQL / Postgres / MariaDB | Redis, Memcached | Node.js | Meilisearch |
| --- | --- | --- | --- | --- | --- | --- |
| App Server | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| Web Server | ✅ | ✅ |  |  | ✅ |  |
| Database Server |  |  | ✅ |  |  |  |
| Cache Server |  |  |  | ✅ |  |  |
| Worker Server |  | ✅ |  |  |  |  |
| MeiliSearch Server |  |  |  |  |  | ✅ |
| Load Balancer | ✅ |  |  |  |  |  |
### [​](#app-servers) App Servers
Application servers are designed to include everything you need to deploy a typical Laravel / PHP application within a single server. Therefore, they are provisioned with the following software:
- PHP
- Nginx
- MySQL / Postgres / MariaDB (if selected)
- Redis
- Memcached
- Node.js
- Supervisor
Application servers are the most typical type of server provisioned on Laravel Forge. If you’re unsure which server type you need, most likely you should provision an application server. As you need to scale your application, you may look at provisioning dedicated servers for services such as your database or caching, but starting with an App server is recommended.
### [​](#web-servers) Web Servers
Web servers contain the web server software you need to deploy a typical Laravel / PHP application, but they do not contain a database or cache. Therefore, these servers are meant to be [networked to](./../resources/network) other dedicated database and cache servers. Web servers are provisioned with the following software:
- PHP
- Nginx
- Node.js
- Supervisor
### [​](#database-servers) Database Servers
Database servers are intended to function as dedicated MySQL / Postgres / MariaDB servers for your application. These servers are meant to be accessed by a dedicated application or web server via Laravel Forge’s [network management features](./../resources/network). Database servers are provisioned with the following software, based on your selections during the server’s creation:
- MySQL, MariaDB, or PostgreSQL
Laravel VPS does not support installing MariaDB.
### [​](#cache-servers) Cache Servers
Cache servers are intended to function as dedicated Redis / Memcached servers for your application. These servers are meant to be accessed by a dedicated application or web server via Laravel Forge’s [network management features](./../resources/network). Cache servers are provisioned with the following software:
- Redis
- Memcached
### [​](#worker-servers) Worker Servers
Worker servers are intended to function as dedicated PHP queue workers for your application. These servers are intended to be networked to your web servers, do not include Nginx, and are not accessible via HTTP. Worker servers are provisioned with the following software:
- PHP
- Supervisor
### [​](#meilisearch-servers) Meilisearch Servers
Meilisearch servers install [Meilisearch](https://meilisearch.com) to provide a blazingly fast search service to your application. They are intended to be connected to another server, and communicate via a [private network](./../resources/network#server-network).
A Meilisearch server will only display and manage one [Site](/docs/sites/the-basics). You cannot create or delete other sites on this server. When connecting to the Meilisearch server from a web or application server, you should connect to it via its private IP address.
### [​](#load-balancers) Load Balancers
Load balancers are meant to distribute incoming web traffic across your servers. To do so, load balancers use Nginx as a “reverse proxy” to evenly distribute the incoming traffic. Therefore, load balancers are only provisioned with Nginx.
Once provisioned you may [configure your load balancer](/docs/servers/load-balancing) to meet your needs.
### [​](#openclaw-servers) OpenClaw Servers
OpenClaw servers provide a minimal environment for running [OpenClaw](https://openclaw.ai) AI agents. These servers only install Homebrew and OpenClaw, and after provisioning, you are dropped straight into the shell to begin configuration.
OpenClaw servers are only available on [Laravel VPS](/docs/servers/laravel-vps).
For more information on configuring and managing OpenClaw servers, see the [OpenClaw integration](/docs/integrations/openclaw) documentation.
Was this page helpful?
YesNo
[Managing Servers](/docs/servers/the-basics)[Laravel VPS](/docs/servers/laravel-vps)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.