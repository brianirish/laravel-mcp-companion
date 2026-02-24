# Vapor - Resources/Caches

*Source: https://docs.vapor.build/resources/caches*

---

[Migrating from Vapor to Cloud? See how Pyle did it (Webinar)](https://lrvl.co/vapor-cloud)
[Laravel Vapor home page](https://vapor.laravel.com)
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)
Search...
Navigation
Resources
Caches
[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)
- [Blog](https://blog.laravel.com)
##### Get Started
- [Introduction](/introduction)
##### Projects
- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)
##### Resources
- [Migrate to Cloud](/resources/migrate-to-cloud)
- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)
##### Integrations
- [Sentry](/integrations/sentry)
##### Other
- [Abuse](/abuse)
On this page
- [Introduction](#introduction)
- [Creating Caches](#creating-caches)
- [Using Caches](#using-caches)
- [Connecting To Caches Locally](#connecting-to-caches-locally)
- [Scaling Caches](#scaling-caches)
- [Metrics](#metrics)
- [DynamoDB Caches](#dynamodb-caches)
- [Deleting Caches](#deleting-caches)
Resources
# Caches
Using caches with Laravel Vapor.
## [​](#introduction) Introduction
Vapor allows you to easily create and manage scalable Redis clusters directly from the Vapor UI or using the Vapor CLI. AWS requires all cache clusters to be private, meaning Vapor will place any application that uses them in a network with a [NAT Gateway](./networks#nat-gateways).
If you are primarily using a cache for Laravel’s task scheduler and atomic locks, you may find that using a [DynamoDB cache](#dynamodb-caches) is a cost-efficient alternative to using Redis clusters. In addition, DynamoDB caches do not require Vapor to attach a NAT Gateway to your application’s network.If no Redis cache is attached to the environment, the DynamoDB cache will automatically be set as the default cache driver.
## [​](#creating-caches) Creating Caches
You may create caches using the Vapor UI or using the `cache` CLI command. When using the CLI command, the command will prompt you for more details about the cache such as its desired performance class:
Copy
Ask AI
```
vapor cache my-application-cache
```
## [​](#using-caches) Using Caches
To attach a cache to an environment, add a `cache` key to the environment’s configuration in your `vapor.yml` file. The value of this key should be the name of the cache. **When the environment is deployed, Vapor will automatically inject the necessary Laravel environment variables for connecting to the cache, allowing your application to start using it immediately:**
vapor.yml
Copy
Ask AI
```
id: 3
name: vapor-app
environments:
    production:
        cache: my-application-cache
        build:
            - 'composer install --no-dev'
        deploy:
            - 'php artisan migrate --force'
```
### [​](#connecting-to-caches-locally) Connecting To Caches Locally
To connect to your cache cluster from your local machine, you can use a Vapor [jumpbox](./networks#jumpboxes) in combination with the `cache:tunnel` CLI command. Jumpboxes are small, SSH-accessible servers placed within your private network.
After creating a jumpbox in your cache’s network, you can use the `cache:tunnel` command:
Copy
Ask AI
```
vapor cache:tunnel my-application-cache
```
This command will make your Redis cache cluster available on `localhost:6378`, allowing you to access it with the Redis management tool of your choice, such as [Medis](http://getmedis.com).
## [​](#scaling-caches) Scaling Caches
You may scale caches via the Vapor UI’s cache detail screen or the `cache:scale` CLI command. When scaling a cache, you will be prompted to specify the number of “nodes” you wish to scale up or down to. When scaling a cache via the CLI, you should specify your desired number of nodes when executing the `cache:scale` command.
Think of each node as a cache server with the performance specs you specified when the cache was created. Cache keys will automatically be sharded across all of your available nodes. Scaling a cache should not typically cause downtime:
Copy
Ask AI
```
vapor cache:scale my-application-cache 5
```
## [​](#metrics) Metrics
A variety of cache performance metrics are available via the Vapor UI’s cache detail screen or using the `cache:metrics` CLI command:
Copy
Ask AI
```
vapor cache:metrics my-application-cache
vapor cache:metrics my-application-cache 5m
vapor cache:metrics my-application-cache 30m
vapor cache:metrics my-application-cache 1h
vapor cache:metrics my-application-cache 8h
vapor cache:metrics my-application-cache 1d
vapor cache:metrics my-application-cache 3d
vapor cache:metrics my-application-cache 7d
vapor cache:metrics my-application-cache 1M
```
## [​](#dynamodb-caches) DynamoDB Caches
When you create a project, Vapor will ensure that an auto-scaling DynamoDB cache table is created in that project’s region. Then, during deployment, Vapor will automatically populate the environment variables required to interact with this cache using Laravel’s built-in `dynamodb` cache driver. All you need to do is start using it within your Laravel application!
If no Redis cache is attached to the environment, the DynamoDB cache will automatically be set as the default cache driver. These caches, while not as performant as Redis clusters, provide a very low-cost alternative for applications with light caching requirements.
Vapor automatically configures Laravel’s task scheduler to use the DynamoDB cache driver to avoid overlapping tasks.
## [​](#deleting-caches) Deleting Caches
Caches may be deleted via the Vapor UI or using the `cache:delete` CLI command:
Copy
Ask AI
```
vapor cache:delete my-application-cache
```
Was this page helpful?
YesNo
[Databases](/resources/databases)[Logs](/resources/logs)
⌘I
[Laravel Vapor home page](https://vapor.laravel.com)
Platform
[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)
Assistant
Responses are generated using AI and may contain mistakes.