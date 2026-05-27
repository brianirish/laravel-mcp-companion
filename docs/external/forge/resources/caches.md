# Forge - Resources/Caches

*Source: https://forge.laravel.com/docs/resources/caches*

---

## On this page
- [Introduction](#introduction)
- [Connecting to Redis and Memcached](#connecting-to-redis-and-memcached)
- [Managing cache services](#managing-cache-services)
  - [Configuring Redis password](#configuring-redis-password)
- [Network connectivity](#network-connectivity)
  - [External connections](#external-connections)
Resources
# Caches
Copy page
Learn how to connect to Redis™ and Memcached on your Laravel Forge server.
Copy page
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://forge.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
## [​](#introduction) Introduction
Laravel Forge automatically installs both [Memcached](https://www.memcached.org/) and [Redis™](https://redis.io/) when provisioning [App Servers](/docs/servers/types#app-servers) or [Cache Servers](/docs/servers/types#cache-servers). Both services are secured by default, remaining inaccessible from external networks and only available for local server connections.
## [​](#connecting-to-redis-and-memcached) Connecting to Redis and Memcached
Both caching services are accessible via localhost using their standard ports:
```
MEMCACHED_HOST=127.0.0.1
MEMCACHED_PORT=11211

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
```
## [​](#managing-cache-services) Managing cache services
Both Redis and Memcached run as system services and can be managed through standard service commands if needed. Laravel Forge handles the initial configuration and setup automatically, ensuring optimal performance for your applications.
### [​](#configuring-redis-password) Configuring Redis password
To configure the Redis password, navigate to the server’s settings page. Then, click “Recipes” in the sidebar. Click the “Set password” button under the Redis section. After entering and confirming your desired password, click the “Add password” button to apply the changes.
## [​](#network-connectivity) Network connectivity
When connecting your applications to Redis or Memcached from another server within your infrastructure, you can utilize [Laravel Forge’s server network feature](/docs/resources/network#server-network) to establish secure internal connections between servers.
### [​](#external-connections) External connections
Laravel Forge servers require SSH key authentication and don’t support password-based access. When connecting to Redis through external clients, ensure you use your **private SSH key** for authentication.
For example, when connecting via [TablePlus](https://tableplus.com/):
Was this page helpful?
YesNo
[Managed Databases](/docs/resources/managed-databases)[Background Processes](/docs/resources/background-processes)
⌘I