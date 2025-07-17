# Forge - Resources/Caches

*Source: https://forge.laravel.com/docs/resources/caches*

---

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

Search...

⌘KAsk AI

- Support
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...

Navigation

Resources

Caches

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

Resources

# Caches

Learn how to connect to Redis and Memcache on your Forge server.

## [​](#overview) Overview

When provisioning an [App Server](/docs/servers/types#app-servers) or a [Cache Server](/docs/servers/types#cache-servers), Forge will automatically install [Memcache](https://www.memcached.org/) and [Redis](https://redis.io/). By default, neither of these services are exposed to the public and may only be accessed from within your server.

## [​](#connecting-to-redis) Connecting To Redis

Redis and Memcache are both available via `127.0.0.1` and their default ports.

Copy

Ask AI

```
MEMCACHED_HOST=127.0.0.1
MEMCACHED_PORT=11211

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

```

## [​](#external-connections) External Connections

All Forge servers require SSH key authentication and are not able to be accessed using passwords. Therefore, when selecting the SSH key to use during authentication, ensure that you select your private SSH key. For example, when connecting to Redis using the [TablePlus](https://tableplus.com/) database client:

![Connecting to Redis with TablePlus](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/images/redis-gui.png)

Was this page helpful?

YesNo

[Databases](/docs/resources/databases)[Network](/docs/resources/network)

On this page

- [Overview](#overview)
- [Connecting To Redis](#connecting-to-redis)
- [External Connections](#external-connections)

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Assistant

Responses are generated using AI and may contain mistakes.