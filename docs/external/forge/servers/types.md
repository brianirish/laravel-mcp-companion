# Forge - Servers/Types

*Source: https://forge.laravel.com/docs/servers/types*

---

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

Search...

⌘KAsk AI

- Support
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...

Navigation

Servers

Server Types

[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)

- [Community](https://discord.com/invite/laravel)
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

Servers

# Server Types

Learn about the different types of servers you can provision with Forge.

## [​](#introduction) Introduction

Forge supports provisioning several different types of servers:

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

Web servers contain the web server software you need to deploy a typical Laravel / PHP application, but they do not contain a database or cache. Therefore, these servers are meant to be [networked to](./../resources/network.md) other dedicated database and cache servers. Web servers are provisioned with the following software:

- PHP
- Nginx
- Node.js
- Supervisor

### [​](#database-servers) Database Servers

Database servers are intended to function as dedicated MySQL / Postgres / MariaDB servers for your application. These servers are meant to be accessed by a dedicated application or web server via Forge’s [network management features](./../resources/network.md). Database servers are provisioned with the following software, based on your selections during the server’s creation:

- MySQL, MariaDB, or PostgreSQL

### [​](#cache-servers) Cache Servers

Cache servers are intended to function as dedicated Redis / Memcached servers for your application. These servers are meant to be accessed by a dedicated application or web server via Forge’s [network management features](./../resources/network.md). Cache servers are provisioned with the following software:

- Redis
- Memcached

### [​](#worker-servers) Worker Servers

Worker servers are intended to function as dedicated PHP queue workers for your application. These servers are intended to be networked to your web servers, do not include Nginx, and are not accessible via HTTP. Worker servers are provisioned with the following software:

- PHP
- Supervisor

### [​](#meilisearch-servers) Meilisearch Servers

Meilisearch servers install [Meilisearch](https://meilisearch.com) to provide a blazingly fast search service to your application. They are intended to be connected to another server, and communicate via a [private network](./../resources/network.md#server-network).

A Meilisearch server will only display and manage one [Site](/docs/sites/the-basics). You cannot create or delete other sites on this server. When connecting to the Meilisearch server from a web or application server, you should connect to it via its private IP address.

### [​](#load-balancers) Load Balancers

Load balancers are meant to distribute incoming web traffic across your servers. To do so, load balancers use Nginx as a “reverse proxy” to evenly distribute the incoming traffic. Therefore, load balancers are only provisioned with Nginx.

Once provisioned you may [configure your load balancer](/docs/servers/load-balancing) to meet your needs.

Was this page helpful?

YesNo

[Server Providers](/docs/servers/providers)[Management](/docs/servers/management)

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

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Assistant

Responses are generated using AI and may contain mistakes.